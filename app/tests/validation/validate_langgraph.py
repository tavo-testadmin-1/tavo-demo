from app.agents.compliance_agent import ComplianceAgent

def validate_langgraph_structure():
    """Validate the Langgraph structure has all expected nodes."""
    # Instantiate agent to validate graph compilation
    agent = ComplianceAgent()
    
    # Validate graph has expected nodes
    expected_nodes = ["retrieve", "analyze", "summarize"]
    actual_nodes = list(agent.workflow._graph.nodes.keys())
    
    # Check if all expected nodes are present
    missing_nodes = [node for node in expected_nodes if node not in actual_nodes]
    if missing_nodes:
        raise ValueError(f"Missing expected nodes: {missing_nodes}")
    
    print("Langgraph structure validation passed!")
    return True

if __name__ == "__main__":
    validate_langgraph_structure() 