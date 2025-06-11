from typing import List, Dict, Any, TypedDict, Annotated, Literal
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field

from app.services.vector_store import get_vector_store

# Define state types
class AgentState(TypedDict):
    document: str
    compliance_area: str
    messages: list
    retrieved_documents: list
    compliance_issues: list
    suggestions: list
    references: list
    next: Literal["retrieve", "analyze", "summarize", "end"]

# Define tools and nodes
def retrieve(state: AgentState) -> AgentState:
    """Retrieve relevant compliance information."""
    document = state["document"]
    compliance_area = state["compliance_area"]
    
    # Get the vector store
    vector_store = get_vector_store()
    
    # Query vector store
    retrieved_docs = vector_store.similarity_search(
        f"Healthcare compliance regulations for {compliance_area} related to: {document[:200]}...",
        k=3
    )
    
    # Add retrieved documents to state
    return {
        **state,
        "retrieved_documents": retrieved_docs,
        "next": "analyze"
    }

def analyze(state: AgentState) -> AgentState:
    """Analyze document for compliance issues."""
    document = state["document"]
    compliance_area = state["compliance_area"]
    retrieved_docs = state["retrieved_documents"]
    
    # Format retrieved documents
    context = "\n".join([f"Source {i+1}: {doc.page_content}" for i, doc in enumerate(retrieved_docs)])
    
    # Create LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a healthcare compliance expert that have a lot of knowledge. 
         Analyze the document for compliance issues related to the specified compliance area.
         Focus only on identifying potential regulatory violations or issues.
         Use the provided reference context to inform your analysis."""),
        ("user", """
         Compliance Area: {compliance_area}
         
         Reference Context:
         {context}
         
         Document to Analyze:
         {document}
         
         Identify all potential compliance issues in the document:
         """)
    ])
    
    # Get compliance issues
    response = llm.invoke(
        prompt.format(
            compliance_area=compliance_area,
            context=context,
            document=document
        )
    )
    
    # Parse compliance issues
    compliance_issues = [issue.strip() for issue in response.content.split('\n') if issue.strip()]
    
    return {
        **state,
        "compliance_issues": compliance_issues,
        "next": "summarize"
    }

def summarize(state: AgentState) -> AgentState:
    """Generate suggestions and references."""
    document = state["document"]
    compliance_area = state["compliance_area"]
    compliance_issues = state["compliance_issues"]
    retrieved_docs = state["retrieved_documents"]
    
    # Format compliance issues
    issues_text = "\n".join([f"- {issue}" for issue in compliance_issues])
    
    # Format retrieved documents
    context = "\n".join([f"Source {i+1}: {doc.page_content}" for i, doc in enumerate(retrieved_docs)])
    
    # Create LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a healthcare compliance expert. 
         Based on the identified compliance issues, provide concrete suggestions for improvement.
         Also provide specific references to regulations or guidelines that are relevant."""),
        ("user", """
         Compliance Area: {compliance_area}
         
         Reference Context:
         {context}
         
         Identified Compliance Issues:
         {issues_text}
         
         1. Provide concrete suggestions to address each compliance issue.
         2. Provide specific references to relevant regulations or guidelines.
         
         Format your response as a JSON with two arrays: 'suggestions' and 'references'.
         """)
    ])
    
    # Get suggestions and references
    response = llm.invoke(
        prompt.format(
            compliance_area=compliance_area,
            context=context,
            issues_text=issues_text
        )
    )
    
    # For simplicity, we'll manually parse the response
    # In production, use a more robust parsing method
    
    suggestions = []
    references = []
    
    content = response.content
    if "suggestions" in content.lower():
        suggestions_text = content.split("suggestions")[1].split("references")[0]
        suggestions = [s.strip().replace("- ", "", 1) for s in suggestions_text.split("\n") if s.strip()]
    
    if "references" in content.lower():
        references_text = content.split("references")[1]
        references = [r.strip().replace("- ", "", 1) for r in references_text.split("\n") if r.strip()]
    
    return {
        **state,
        "suggestions": suggestions,
        "references": references,
        "next": "end"
    }

# Define the agent
class ComplianceAgent:
    def __init__(self):
        # Define the workflow graph
        self.workflow = StateGraph(AgentState)
        
        # Add nodes
        self.workflow.add_node("retrieve", retrieve)
        self.workflow.add_node("analyze", analyze)
        self.workflow.add_node("summarize", summarize)
        
        # Add edges
        self.workflow.add_edge("retrieve", "analyze")
        self.workflow.add_edge("analyze", "summarize")
        self.workflow.add_edge("summarize", END)
        
        # Set entry point
        self.workflow.set_entry_point("retrieve")
        
        # Compile the workflow
        self.agent = self.workflow.compile()
    
    def run(self, document: str, compliance_area: str = "general") -> Dict:
        """Run the compliance agent on the document."""
        # Initialize state
        initial_state = {
            "document": document,
            "compliance_area": compliance_area,
            "messages": [],
            "retrieved_documents": [],
            "compliance_issues": [],
            "suggestions": [],
            "references": [],
            "next": "retrieve"
        }
        
        # Run the agent
        result = self.agent.invoke(initial_state)
        
        # Return the results
        return {
            "document_text": document,
            "compliance_issues": result["compliance_issues"],
            "suggestions": result["suggestions"],
            "references": result["references"]
        } 
