import os
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader  
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Pinecone
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from pinecone import Pinecone as PineconeClient, ServerlessSpec  
from dotenv import load_dotenv
from huggingface_hub import login

# Load environment variables
load_dotenv()

# Set up API keys
os.environ['HUGGINGFACE_API_KEY'] = st.secrets["HUGGINGFACE_API_KEY"]
os.environ['PINECONE_API_KEY'] = st.secrets["PINECONE_API_KEY"]

class Chatbot:
    def __init__(self):
        # Load PDF data
        loader = PyMuPDFLoader('sanitation.pdf') 
        documents = loader.load()
        
        # Split documents into smaller chunks
        text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=4)
        self.docs = text_splitter.split_documents(documents)

        
        self.embeddings = HuggingFaceEmbeddings()

        # Define the index name
        self.index_name = "amcsanitation"

        # Initialize Pinecone client
        self.pc = PineconeClient(api_key=os.getenv('PINECONE_API_KEY')) 
        # Create Pinecone index if it doesn't exist
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=768,  
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws', 
                    region='us-east-1'  
                )
            )

        # Set up Hugging Face model
        repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.llm = HuggingFaceEndpoint(
            repo_id=repo_id, 
            temperature=0.8, 
            top_k=50, 
            huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY')
        )

        # Define prompt template
        template = """
        You are a chatbot for the Ahmedabad Government. The Human will ask questions about Sanitation Policies. 
        Use the following piece of context to answer the question. 
        If you don't know the answer, just say you don't know. 

        Context: {context}
        Question: {question}
        Answer: 
        """
        self.prompt = PromptTemplate(
            template=template, 
            input_variables=["context", "question"]
        )

        # Initialize Pinecone index with documents
        self.docsearch = Pinecone.from_documents(self.docs, self.embeddings, index_name=self.index_name)

        # Define the retrieval-augmented generation (RAG) chain
        self.rag_chain = (
            {"context": self.docsearch.as_retriever(), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, question):
        return self.rag_chain.invoke(question)
