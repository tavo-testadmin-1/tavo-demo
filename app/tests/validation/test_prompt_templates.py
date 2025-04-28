import unittest
from app.agents.compliance_agent import analyze, summarize
from app.config.settings import settings

class TestPromptTemplates(unittest.TestCase):
    def test_analyze_prompt_format(self):
        """Test that the analyze prompt correctly formats variables."""
        state = {
            "document": "Test document",
            "compliance_area": "HIPAA",
            "retrieved_documents": []
        }
        
        # This will raise an error if the prompt template has formatting issues
        try:
            analyze(state)
            self.fail("Expected exception due to empty retrieved_documents")
        except Exception as e:
            # We expect an error due to empty docs, but not a KeyError or formatting error
            self.assertNotIsInstance(e, KeyError)
            
    def test_summarize_prompt_format(self):
        """Test that the summarize prompt correctly formats variables."""
        state = {
            "document": "Test document",
            "compliance_area": "HIPAA",
            "compliance_issues": ["Issue 1"],
            "retrieved_documents": []
        }
        
        # This will raise an error if the prompt template has formatting issues
        try:
            summarize(state)
            self.fail("Expected exception due to empty retrieved_documents")
        except Exception as e:
            # We expect an error due to empty docs, but not a KeyError or formatting error
            self.assertNotIsInstance(e, KeyError)

if __name__ == "__main__":
    unittest.main() 