import time
from app.agents.compliance_agent import ComplianceAgent

def run_performance_benchmark():
    """Run performance benchmarks on the compliance agent."""
    # Test documents
    documents = [
        "Patient data was shared with the research team without explicit consent.",
        "Medical records were updated but some fields were left blank."
    ]
    
    # Initialize agent
    agent = ComplianceAgent()
    
    # Run benchmarks
    results = []
    for doc in documents:
        start_time = time.time()
        result = agent.run(document=doc, compliance_area="HIPAA")
        duration = time.time() - start_time
        
        # Check result validity
        assert "compliance_issues" in result
        assert "suggestions" in result
        assert "references" in result
        
        results.append({
            "document_length": len(doc),
            "issues_found": len(result["compliance_issues"]),
            "suggestions": len(result["suggestions"]),
            "references": len(result["references"]),
            "duration_seconds": duration
        })
    
    print("Benchmark Results:")
    for i, res in enumerate(results):
        print(f"Document {i+1}:")
        print(f"  Duration: {res['duration_seconds']:.2f} seconds")
        print(f"  Issues found: {res['issues_found']}")
        print(f"  Suggestions: {res['suggestions']}")
        print(f"  References: {res['references']}")
    
    return results

if __name__ == "__main__":
    run_performance_benchmark() 