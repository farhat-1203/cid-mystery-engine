"""
Demo script to test individual modules without running the full game
"""

from src.modules.forensics import ForensicAnalyzer, EvidenceGraph
from src.modules.interrogation import InterrogationEngine, SuspectProfile, Evidence

def test_forensics():
    """Test the forensic analysis module"""
    print("=== Forensic Analysis Demo ===")
    
    analyzer = ForensicAnalyzer()
    
    # Test evidence graph
    evidence_graph = EvidenceGraph()
    
    # Add some evidence
    evidence_graph.add_evidence("fp1", "forensic", "Fingerprint on door handle", "Office entrance")
    evidence_graph.add_evidence("blood1", "forensic", "Blood sample on floor", "Office floor")
    evidence_graph.add_evidence("witness1", "testimony", "Saw suspect at 9 PM", "Street corner")
    evidence_graph.add_evidence("cctv1", "digital", "Security footage", "Building lobby")
    
    # Connect evidence
    evidence_graph.connect_evidence("fp1", "witness1", "time_correlation")
    evidence_graph.connect_evidence("blood1", "cctv1", "location_match")
    evidence_graph.connect_evidence("fp1", "blood1", "forensic_match")
    
    print(f"Deduction Score: {evidence_graph.deduction_score:.1f}/100")
    print(f"Evidence Connections: {len(evidence_graph.connections)}")
    
    # Show deduction paths
    paths = evidence_graph.get_deduction_paths()
    print(f"Logical Paths Found: {len(paths)}")
    for i, path in enumerate(paths):
        print(f"  Path {i+1}: {' -> '.join(path)}")

def test_interrogation():
    """Test the interrogation module"""
    print("\n=== Interrogation Demo ===")
    
    # Create a suspect
    suspect = SuspectProfile(
        name="Rajesh Kumar",
        age=35,
        occupation="Office Manager", 
        background="Recently passed over for promotion, financial troubles",
        personality_traits=["nervous", "defensive", "ambitious"],
        guilty=True,
        alibi="I was at home watching TV all evening",
        secrets=["Had a heated argument with the victim", "Desperately needed money"],
        stress_triggers=["promotion", "money", "argument", "victim"]
    )
    
    # Create evidence
    evidence = [
        Evidence("fingerprint", "Fingerprints found on victim's desk", 0.8),
        Evidence("witness", "Witness saw suspect near office at 9 PM", 0.6),
        Evidence("financial", "Bank records show suspect's debt", 0.9)
    ]
    
    # Start interrogation
    engine = InterrogationEngine(api_type="fallback")  # Use fallback responses
    opening = engine.start_interrogation(suspect, evidence)
    
    print(f"Suspect: {suspect.name}")
    print(f"Opening Statement: {opening}")
    print(f"Initial Stress Level: {engine.stress_meter:.1f}")
    
    # Simulate some questions
    questions = [
        ("Where were you last night at 9 PM?", "ACP"),
        ("We have a witness who saw you at the office!", "DAYA"),
        ("Your fingerprints were found on the victim's desk.", "ABHIJEET")
    ]
    
    for question, team_member in questions:
        print(f"\n{team_member}: {question}")
        
        result = engine.ask_question(question, team_member)
        
        print(f"Suspect: {result['response']}")
        print(f"Stress Change: +{result['stress_change']:.1f}")
        print(f"New Stress Level: {result['new_stress_level']:.1f}")
        
        if result['behavioral_notes']:
            for note in result['behavioral_notes']:
                print(f"[Observation: {note}]")
        
        if result['breakthrough']:
            print("[BREAKTHROUGH MOMENT!]")
    
    # Present evidence
    print(f"\nPresenting evidence: {evidence[0].description}")
    result = engine.ask_question("Explain these fingerprints!", "ACP", "fingerprint")
    print(f"Suspect: {result['response']}")
    print(f"Final Stress Level: {result['new_stress_level']:.1f}")
    
    # Get summary
    summary = engine.get_interrogation_summary()
    print(f"\n=== Interrogation Summary ===")
    print(f"Total Questions: {summary['total_questions']}")
    print(f"Evidence Presented: {summary['evidence_presented']}")
    print(f"Final Stress: {summary['final_stress_level']:.1f}")
    print(f"Confession Likelihood: {summary['confession_likelihood']:.1f}%")

def main():
    """Run all demos"""
    print("CID: The Silicon Casefiles - Module Demo")
    print("=" * 50)
    
    test_forensics()
    test_interrogation()
    
    print("\n" + "=" * 50)
    print("Demo completed! Run 'python main.py' to start the full game.")

if __name__ == "__main__":
    main()