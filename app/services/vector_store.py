import os
from typing import List, Dict
import json
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Singleton vector store
_vector_store = None

def load_documents() -> List[Document]:
    """Load compliance documents from the data directory."""
    data_dir = Path("app/data/compliance_docs")
    documents = []
    
    # Create the data directory if it doesn't exist
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
        
        # Create some sample compliance documents
        sample_docs = {
            "hipaa.txt": """
            HIPAA Privacy Rule: The HIPAA Privacy Rule establishes national standards to protect individuals' medical records and other personal health information. 
            Key requirements include:
            - Patient rights to access their health information
            - Notice of privacy practices must be provided to patients
            - Limitations on use of health information without patient authorization
            - Organization must implement safeguards to protect health information
            - Business associate agreements must be established with vendors
            
            HIPAA Security Rule: The HIPAA Security Rule establishes national standards to protect electronic personal health information.
            Key requirements include:
            - Administrative safeguards (security management, workforce training)
            - Physical safeguards (facility access controls, workstation security)
            - Technical safeguards (access controls, transmission security)
            - Organizational requirements (business associate contracts)
            """,
            
            "fda_regulations.txt": """
            FDA Medical Device Regulations: Medical devices are subject to FDA regulations that ensure safety and effectiveness.
            Key requirements include:
            - Medical device classification (Class I, II, III)
            - Premarket notification (510(k)) or approval (PMA)
            - Quality System Regulation (QSR) compliance
            - Medical Device Reporting (MDR) for adverse events
            - Labeling requirements
            
            FDA Clinical Trial Requirements: Clinical trials must follow FDA regulations for human subject protection.
            Key requirements include:
            - Institutional Review Board (IRB) approval
            - Informed consent procedures
            - Protocol adherence
            - Adverse event reporting
            - Data integrity and recordkeeping
            """,
            
            "general_healthcare_compliance.txt": """
            General Healthcare Compliance Requirements:
            
            Anti-Kickback Statute (AKS): Prohibits knowingly and willfully offering, paying, soliciting, or receiving remuneration to induce referrals of items or services covered by Medicare, Medicaid, or other federal healthcare programs.
            
            Stark Law (Physician Self-Referral Law): Prohibits physicians from referring Medicare patients to entities with which they (or an immediate family member) have a financial relationship.
            
            False Claims Act (FCA): Imposes liability on persons or companies who submit false claims to the government or cause others to submit false claims.
            
            HITECH Act: Expands HIPAA requirements related to the privacy and security of protected health information (PHI).
            
            Documentation Requirements:
            - All medical records must be complete, accurate, and timely
            - Authentication of medical records through signatures
            - Maintaining records for required retention periods
            - Proper correction of errors in documentation
            """
        }
        
        for filename, content in sample_docs.items():
            with open(data_dir / filename, "w") as f:
                f.write(content)
    
    # Load all documents in the data directory
    for file_path in data_dir.glob("*.txt"):
        with open(file_path, "r") as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": file_path.name}))
    
    return documents

def create_vector_store() -> FAISS:
    """Create a vector store from compliance documents."""
    # Load documents
    documents = load_documents()
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Create vector store
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(splits, embeddings)
    
    return vector_store

def get_vector_store() -> FAISS:
    """Get the vector store singleton."""
    global _vector_store
    
    if _vector_store is None:
        _vector_store = create_vector_store()
    
    return _vector_store 