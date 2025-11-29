"""
RadarSuite v3.5.0 - Point 12: Dependency Injection Tests
Tests for core/di.py
"""

from tests.compat import pytest
from core.di import ServiceContainer, configure_services


class TestServiceContainer:
    """Test suite for ServiceContainer class"""

    def test_register_and_retrieve_instance(self, di_container):
        """Test instance registration and retrieval"""
        test_instance = {"name": "test_service", "value": 42}
        di_container.register_instance('test_instance', test_instance)

        retrieved = di_container.get('test_instance')
        assert retrieved == test_instance
        assert retrieved is test_instance  # Same object reference

    def test_register_and_retrieve_singleton(self, di_container):
        """Test singleton registration with lazy instantiation"""
        instantiation_count = [0]

        def test_factory(c):
            instantiation_count[0] += 1
            return {"factory": "result", "count": instantiation_count[0]}

        di_container.register_singleton('test_singleton', test_factory)

        # Should not instantiate until get()
        assert 'test_singleton' not in di_container._instances

        # First get - should instantiate
        result1 = di_container.get('test_singleton')
        assert instantiation_count[0] == 1

        # Second get - should return cached instance
        result2 = di_container.get('test_singleton')
        assert instantiation_count[0] == 1  # Still only called once
        assert result1 is result2  # Same instance

    def test_has_method(self, di_container):
        """Test has() method for checking service registration"""
        di_container.register_instance('instance', "test")
        di_container.register_singleton('singleton', lambda c: "test")

        assert di_container.has('instance')
        assert di_container.has('singleton')
        assert not di_container.has('nonexistent')

    def test_reset_clears_instances(self, di_container):
        """Test reset() clears instances but preserves registrations"""
        di_container.register_singleton('test', lambda c: {"value": 42})

        # Get the service to instantiate it
        di_container.get('test')
        assert len(di_container._instances) > 0

        # Reset
        di_container.reset()
        assert len(di_container._instances) == 0

        # Factories should still be registered
        assert di_container.has('test')

    def test_get_registered_services(self, di_container):
        """Test get_registered_services() returns all services"""
        di_container.register_instance('svc1', "test1")
        di_container.register_singleton('svc2', lambda c: "test2")
        di_container.register_singleton('svc3', lambda c: "test3")

        services = di_container.get_registered_services()
        assert len(services) == 3
        assert 'svc1' in services
        assert 'svc2' in services
        assert 'svc3' in services

    def test_get_unregistered_service_raises_error(self, di_container):
        """Test that getting unregistered service raises KeyError"""
        with pytest.raises(KeyError) as exc_info:
            di_container.get('nonexistent_service')

        assert 'not registered' in str(exc_info.value)

    def test_dependency_resolution(self, di_container):
        """Test that factories receive container for dependency resolution"""
        def service_a_factory(c):
            return {"name": "ServiceA"}

        def service_b_factory(c):
            # ServiceB depends on ServiceA
            service_a = c.get('service_a')
            return {"name": "ServiceB", "dependency": service_a}

        di_container.register_singleton('service_a', service_a_factory)
        di_container.register_singleton('service_b', service_b_factory)

        service_b = di_container.get('service_b')
        assert service_b['dependency']['name'] == 'ServiceA'

    def test_circular_dependency_detection(self, di_container):
        """Test behavior with circular dependencies"""
        def service_a_factory(c):
            return {"name": "A", "dep": c.get('service_b')}

        def service_b_factory(c):
            return {"name": "B", "dep": c.get('service_a')}

        di_container.register_singleton('service_a', service_a_factory)
        di_container.register_singleton('service_b', service_b_factory)

        # This should cause recursion error
        with pytest.raises(RecursionError):
            di_container.get('service_a')

    def test_multiple_containers_isolated(self):
        """Test that multiple containers are isolated from each other"""
        container1 = ServiceContainer()
        container2 = ServiceContainer()

        container1.register_instance('service', "container1")
        container2.register_instance('service', "container2")

        assert container1.get('service') == "container1"
        assert container2.get('service') == "container2"


class TestConfigureServices:
    """Test suite for configure_services() function"""

    def test_configure_services_basic(self, sample_config):
        """Test that configure_services creates a container"""
        container = configure_services(sample_config)
        assert isinstance(container, ServiceContainer)

    def test_config_manager_registered(self, sample_config):
        """Test that config_manager is registered"""
        container = configure_services(sample_config)
        assert container.has('config_manager')

    def test_registered_services_count(self, sample_config):
        """Test expected number of services are registered"""
        container = configure_services(sample_config)
        services = container.get_registered_services()

        # Should have at least: config_manager, gpu, soundblaster,
        # audio_cache, audio_engine, sound_classifier, audio_recorder,
        # voice_detector, detection_worker, footstep_detector,
        # target_tracker, threat_system, performance_monitor,
        # game_detector, launcher_detector, audio_scanner
        assert len(services) >= 16

    def test_services_lazy_instantiation(self, sample_config):
        """Test that services are not instantiated until needed"""
        container = configure_services(sample_config)

        # Only config_manager should be instantiated (registered as instance)
        # All others should be lazy singletons
        assert 'config_manager' in container._instances
        assert 'gpu' not in container._instances
        assert 'audio_engine' not in container._instances

    @pytest.mark.integration
    def test_service_resolution_without_dependencies(self, sample_config):
        """Test resolving services that don't need heavy dependencies"""
        # This would require numpy/PyQt5, so mark as integration test
        # For unit tests, we just verify the container is configured
        container = configure_services(sample_config)

        # Verify structure without actually instantiating
        assert container.has('config_manager')
        assert container.has('gpu')
        assert container.has('soundblaster')
