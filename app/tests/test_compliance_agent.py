import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the app directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.agents.compliance_agent import ComplianceAgent, AgentState
from langchain_core.documents import Document

class TestComplianceAgent(unittest.TestCase):
    @patch("app.services.vector_store.get_vector_store")
    @patch("langchain_openai.ChatOpenAI")
    def test_compliance_agent_flow(self, mock_chat_openai, mock_get_vector_store):
        # Mock vector store
        mock_vector_store = MagicMock()
        mock_vector_store.similarity_search.return_value = [
            Document(
                page_content="HIPAA requires patient authorization for disclosure of PHI.",
                metadata={"source": "hipaa.txt"}
            ),
            Document(
                page_content="Medical records must be complete, accurate, and timely.",
                metadata={"source": "general_healthcare_compliance.txt"}
            )
        ]
        mock_get_vector_store.return_value = mock_vector_store
        
        # Mock LLM responses
        mock_llm = MagicMock()
        mock_response1 = MagicMock()
        mock_response1.content = "Missing patient authorization for PHI disclosure\nIncomplete documentation"
        
        mock_response2 = MagicMock()
        mock_response2.content = """suggestions:
        - Obtain written patient authorization before disclosing PHI
        - Ensure all medical records are complete with required fields
        
        references:
        - HIPAA Privacy Rule 45 CFR 164.508
        - Healthcare Documentation Standards AHIMA 2.1"""
        
        mock_llm.invoke.side_effect = [mock_response1, mock_response2]
        mock_chat_openai.return_value = mock_llm
        
        # Create and run agent
        agent = ComplianceAgent()
        result = agent.run(
            document="Patient data was shared with the research team. Some fields in the record were left blank.",
            compliance_area="HIPAA"
        )
        
        # Assertions
        self.assertIn("Missing patient authorization", result["compliance_issues"][0])
        self.assertIn("Incomplete documentation", result["compliance_issues"][1])
        self.assertIn("Obtain written patient authorization", result["suggestions"][0])
        self.assertIn("HIPAA Privacy Rule", result["references"][0])

if __name__ == "__main__":
    unittest.main() 