#!/usr/bin/env python3
"""
Debug TAP Protocol batch processing issue
"""

import sys
from pathlib import Path

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from core.tap_protocol.tap_integration import TapProtocolIntegrator

def debug_tap_protocol():
    print("🔍 Debugging TAP Protocol batch processing...")
    
    # Create integrator
    tap_integrator = TapProtocolIntegrator()
    
    # Test single hypertoken creation first
    print("\n1. Testing single hypertoken creation...")
    test_governor = {
        "name": "ABRIOND",
        "aethyr": "POP",
        "traditions": ["enochian_magic", "hermetic_qabalah"],
        "primary_traits": [{"name": "Celestial Protector", "influence": 0.8}]
    }
    
    try:
        hypertoken = tap_integrator.create_governor_hypertoken(test_governor)
        print(f"✅ Single hypertoken created successfully")
        print(f"   Token ID: {hypertoken['token_id']}")
        print(f"   Metadata type: {type(hypertoken['metadata'])}")
        print(f"   Metadata keys: {list(hypertoken['metadata'].keys()) if isinstance(hypertoken['metadata'], dict) else 'Not a dict'}")
        
        # Test cross-token interaction tracking manually
        print("\n2. Testing cross-token interaction tracking...")
        interactions = {}
        tap_integrator._track_cross_token_interactions(hypertoken, interactions)
        print(f"✅ Cross-token interactions tracked: {list(interactions.keys())}")
        
    except Exception as e:
        print(f"❌ Single hypertoken creation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test batch creation
    print("\n3. Testing batch creation...")
    test_governors = [
        {
            "name": "ABRIOND",
            "aethyr": "POP",
            "traditions": ["enochian_magic", "hermetic_qabalah"],
            "primary_traits": [{"name": "Celestial Protector", "influence": 0.8}]
        },
        {
            "name": "OCCODON", 
            "aethyr": "ZOM",
            "traditions": ["enochian_magic", "tarot_system"],
            "primary_traits": [{"name": "Mystic Scholar", "influence": 0.9}]
        }
    ]
    
    try:
        batch_result = tap_integrator.create_batch_hypertokens(test_governors)
        print(f"✅ Batch creation successful")
        print(f"   Tokens created: {len(batch_result['tokens_created'])}")
        print(f"   Cross interactions: {list(batch_result['cross_interactions'].keys())}")
        
        # Test evolution opportunities
        print("\n4. Testing evolution opportunities...")
        hypertoken = batch_result["tokens_created"][0]
        print(f"   Hypertoken metadata type: {type(hypertoken['metadata'])}")
        
        opportunities = tap_integrator.get_cross_token_evolution_opportunities(hypertoken)
        print(f"✅ Evolution opportunities: {len(opportunities)}")
        
    except Exception as e:
        print(f"❌ Batch creation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_tap_protocol()
