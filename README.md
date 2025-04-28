# Healthcare Compliance RAG System

A minimal agentic RAG system for healthcare compliance document review built with Langgraph.

## Overview

This system helps healthcare professionals verify that their documents meet regulatory requirements by retrieving relevant compliance information, analyzing the content for potential issues, and providing recommendations to ensure compliance.

### Use Case

Healthcare compliance officers and medical professionals need to ensure their documentation follows strict regulatory requirements. This system:

1. Retrieves relevant compliance information based on the document content and specified compliance area
2. Analyzes the document for potential compliance issues
3. Provides concrete suggestions for improving compliance
4. References relevant regulations or guidelines

## Architecture

The system implements a Langgraph-based agent workflow with the following components:

- **Retrieval Node**: Finds relevant compliance information from a vector database
- **Analysis Node**: Analyzes the document against retrieved compliance information
- **Summarization Node**: Generates specific suggestions and regulatory references

## Setup

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

Start the API server:

```bash
cd app
python main.py
```

The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /`: Health check
- `POST /compliance_check`: Check document compliance
  - Request body:
    ```json
    {
      "document_text": "Your healthcare document text here",
      "compliance_area": "HIPAA"
    }
    ```
  - Response:
    ```json
    {
      "document_text": "Your healthcare document text here",
      "compliance_issues": ["Issue 1", "Issue 2"],
      "suggestions": ["Suggestion 1", "Suggestion 2"],
      "references": ["Reference 1", "Reference 2"]
    }
    ```

## Testing

Run the tests:

```bash
pytest app/tests
```

## License

MIT
