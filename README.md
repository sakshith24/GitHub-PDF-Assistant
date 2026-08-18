# GitHub & PDF Assistant

An AI-powered RAG assistant that allows users to ask questions about
PDF documents and GitHub repositories using natural language.

The application retrieves relevant content from the selected source,
provides it as context to an LLM, and generates an answer grounded in
the retrieved information.

## Demo

The assistant supports querying:

- PDF documents
- GitHub repositories
- Both sources together

## Features

- Upload and process PDF documents
- Clone and process public GitHub repositories
- Extract relevant source files from repositories
- Chunk documents for retrieval
- Generate embeddings for document chunks
- Store embeddings in ChromaDB
- Semantic similarity search
- Filter retrieval by source:
  - PDF
  - GitHub
  - All
- Generate answers using an LLM
- Display retrieved sources
- Ground answers using retrieved context
- Prevent the model from guessing when relevant information is not found

## How It Works

The application follows a Retrieval-Augmented Generation (RAG) pipeline.

### 1. Data Ingestion

PDF files and GitHub repositories are loaded into the application.

### 2. Document Processing

Documents are extracted and split into smaller chunks.

For GitHub repositories, relevant source files are processed along
with their metadata such as file path and file type.

### 3. Embeddings

Each document chunk is converted into a vector embedding using a
sentence-transformer model.

### 4. Vector Storage

The embeddings and metadata are stored in ChromaDB.

### 5. Retrieval

When the user asks a question, the query is converted into an
embedding and compared against stored document embeddings.

The most relevant chunks are retrieved based on semantic similarity.

### 6. Generation

The retrieved chunks are provided to the LLM as context.

The LLM generates an answer using the retrieved context rather than
relying only on its internal knowledge.

### 7. Sources

The application displays the documents/files used to generate the
answer.

## Architecture

```text
                    User Query
                        |
                        v
                Streamlit Interface
                        |
                        v
                  Query Embedding
                        |
                        v
                    ChromaDB
                        |
             +----------+----------+
             |                     |
             v                     v
          PDF Data            GitHub Data
             |                     |
             +----------+----------+
                        |
                        v
                 Relevant Chunks
                        |
                        v
                  Context Builder
                        |
                        v
                       LLM
                        |
                        v
                     Answer
                        |
                        v
                    Sources

# 6. Tech Stack

Keep this clean:

```markdown
## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| LLM | Gemini |
| RAG | LangChain |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| PDF Processing | PyMuPDF |
| GitHub Processing | GitPython / GitHub repository cloning |
| Environment | uv |

# 8. Installation

This is essential.

Since you're using `uv`, document that instead of only giving pip commands.

```markdown
## Installation

### 1. Clone the repository

git clone https://github.com/sakshith24/GitHub-PDF-Assistant.git

cd GitHub-PDF-Assistant

### 2. Create the environment

uv sync

### 3. Activate the environment

Windows:

.venv\Scripts\activate

### 4. Configure environment variables

Create a `.env` file:

GEMINI_API_KEY=your_api_key_here

### 5. Run the application

streamlit run main.py


## Future Improvements

- Improve hybrid retrieval
- Add reranking
- Improve chunking strategies
- Add conversational memory
- Add query rewriting
- Add multi-query retrieval
- Add retrieval evaluation
- Add LLM evaluation
- Add authentication
- Add FastAPI backend
- Add React/Next.js frontend
- Add Docker deployment
- Add MCP integration
- Add agentic workflows
