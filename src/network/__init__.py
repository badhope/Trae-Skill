"""Network Module - Distributed communication and service mesh"""

from network.communication import (
    MessageType,
    ServiceStatus,
    Message,
    ServiceEndpoint,
    IMessageBroker,
    InMemoryBroker,
    LoadBalancer,
    CircuitBreaker,
    ServiceRegistry,
    NetworkMonitor,
    NetworkModule,
)

__all__ = [
    "MessageType",
    "ServiceStatus",
    "Message",
    "ServiceEndpoint",
    "IMessageBroker",
    "InMemoryBroker",
    "LoadBalancer",
    "CircuitBreaker",
    "ServiceRegistry",
    "NetworkMonitor",
    "NetworkModule",
]

__version__ = "1.1.0"
