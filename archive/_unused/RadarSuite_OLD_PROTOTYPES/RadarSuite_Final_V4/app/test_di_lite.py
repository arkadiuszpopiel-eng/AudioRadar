#!/usr/bin/env python3
"""
Lightweight DI Container Test - Point 11 Validation
Tests ServiceContainer class logic without requiring all dependencies
"""

import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.di import ServiceContainer

def test_service_container():
    """Test ServiceContainer class functionality"""

    print("=" * 60)
    print("Point 11 - ServiceContainer Logic Test")
    print("=" * 60)

    container = ServiceContainer()

    # Test 1: Register and retrieve instance
    print("\n[Test 1] Register and retrieve instance...")
    test_instance = {"name": "test_service", "value": 42}
    container.register_instance('test_instance', test_instance)
    retrieved = container.get('test_instance')
    assert retrieved == test_instance, "Instance retrieval failed"
    print("  ✓ Instance registration and retrieval works")

    # Test 2: Register and retrieve singleton (lazy)
    print("\n[Test 2] Register and retrieve singleton (lazy)...")
    instantiation_count = [0]

    def test_factory(c):
        instantiation_count[0] += 1
        return {"factory": "result", "count": instantiation_count[0]}

    container.register_singleton('test_singleton', test_factory)
    assert 'test_singleton' not in container._instances, "Should not instantiate until get()"

    # First get - should instantiate
    result1 = container.get('test_singleton')
    assert instantiation_count[0] == 1, "Factory should be called once"

    # Second get - should return cached instance
    result2 = container.get('test_singleton')
    assert instantiation_count[0] == 1, "Factory should not be called again"
    assert result1 is result2, "Should return same instance"
    print("  ✓ Singleton registration and lazy instantiation works")

    # Test 3: Check has() method
    print("\n[Test 3] Check has() method...")
    assert container.has('test_instance'), "Should find registered instance"
    assert container.has('test_singleton'), "Should find registered singleton"
    assert not container.has('nonexistent'), "Should not find unregistered service"
    print("  ✓ has() method works correctly")

    # Test 4: Test reset()
    print("\n[Test 4] Test reset() method...")
    container.reset()
    assert len(container._instances) == 0, "Instances should be cleared"
    # Factories should still be registered
    assert container.has('test_singleton'), "Factories should persist after reset"
    print("  ✓ reset() clears instances while preserving registrations")

    # Test 5: Test get_registered_services()
    print("\n[Test 5] Test get_registered_services()...")
    container = ServiceContainer()
    container.register_instance('svc1', "test1")
    container.register_singleton('svc2', lambda c: "test2")
    container.register_singleton('svc3', lambda c: "test3")

    services = container.get_registered_services()
    assert len(services) == 3, f"Expected 3 services, got {len(services)}"
    assert 'svc1' in services, "Should list instance"
    assert 'svc2' in services, "Should list singleton"
    assert 'svc3' in services, "Should list singleton"
    print(f"  ✓ get_registered_services() returns all {len(services)} services")

    # Test 6: Test error handling
    print("\n[Test 6] Test error handling...")
    try:
        container.get('nonexistent_service')
        assert False, "Should raise KeyError"
    except KeyError as e:
        assert 'not registered' in str(e), "Error message should be descriptive"
        print("  ✓ Raises KeyError for unregistered services")

    # Test 7: Test dependency resolution
    print("\n[Test 7] Test dependency resolution (factory receives container)...")
    def service_a_factory(c):
        return {"name": "ServiceA"}

    def service_b_factory(c):
        # ServiceB depends on ServiceA
        service_a = c.get('service_a')
        return {"name": "ServiceB", "dependency": service_a}

    container.register_singleton('service_a', service_a_factory)
    container.register_singleton('service_b', service_b_factory)

    service_b = container.get('service_b')
    assert service_b['dependency']['name'] == 'ServiceA', "Dependency resolution failed"
    print("  ✓ Dependency resolution works (factories receive container)")

    print("\n" + "=" * 60)
    print("✓ All ServiceContainer tests passed!")
    print("✓ Point 11 - DI Container Logic: VALIDATED")
    print("=" * 60)

    return True

if __name__ == '__main__':
    try:
        success = test_service_container()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
