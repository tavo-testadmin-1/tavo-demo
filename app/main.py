import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agents.compliance_agent import ComplianceAgent

app = FastAPI(title="Healthcare Compliance RAG System")

class DocumentRequest(BaseModel):
    document_text: str
    compliance_area: str = "general"  # e.g., "HIPAA", "FDA", "general"
    
class ComplianceResponse(BaseModel):
    document_text: str
    compliance_issues: list
    suggestions: list
    references: list

@app.get("/")
async def root():
    return {"status": "Healthcare Compliance RAG System is running"}

@app.post("/compliance_checks", response_model=ComplianceResponse)
async def check_compliance(request: DocumentRequest):
    try:
        agent = ComplianceAgent()
        result = agent.run(
            document=request.document_text,
            compliance_area=request.compliance_area
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000))) 
