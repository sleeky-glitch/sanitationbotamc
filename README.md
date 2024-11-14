# Sanitation Bot AMC

A Retrieval-Augmented Generation (RAG) chatbot for the Ahmedabad Municipal Corporation's sanitation services, built using Streamlit, LangChain, and Mixtral-8x7B.

## Overview

This project implements an AI-powered chatbot that answers questions about sanitation policies for the Ahmedabad Municipal Corporation (AMC). The bot uses RAG architecture to provide accurate, context-aware responses based on official documentation.

## Features

- Interactive chat interface using Streamlit
- RAG implementation using LangChain
- Document processing with PyMuPDF
- Vector storage using Pinecone
- Mixtral-8x7B language model integration
- Automatic bullet-point formatting for long responses

## Technical Stack

- **Frontend**: Streamlit
- **Language Model**: Mixtral-8x7B-Instruct-v0.1
- **Vector Database**: Pinecone
- **Embeddings**: HuggingFace Embeddings
- **Document Processing**: PyMuPDF
- **Framework**: LangChain

## Setup

1. Clone the repository:
```bash
git clone https://github.com/sleeky-glitch/sanitationbotamc.git
cd sanitationbotamc
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following:
```env
HUGGINGFACE_API_KEY=your_huggingface_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

4. Add your sanitation policy document:
Place your `sanitation.pdf` in the root directory.

5. Run the application:
```bash
streamlit run streamlit.py
```

## Project Structure

- `main.py`: Core chatbot implementation with RAG architecture
- `streamlit.py`: Streamlit interface implementation
- `requirements.txt`: Project dependencies
- `sanitation.pdf`: Source document (not included in repo)

## Features

- Real-time chat interface
- Context-aware responses based on official documentation
- Automatic formatting of long responses into bullet points
- Persistent chat history during session
- Responsive UI with loading indicators

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Ahmedabad Municipal Corporation
- Mistral AI for the language model
- Pinecone for vector database services
- HuggingFace for model hosting