"""Core Capability Negotiation Broker."""
from typing import Dict, List, Set, Optional

class ClientManifest:
    def __init__(self, client_id: str, supported_versions: List[str], features: Set[str]):
        self.client_id = client_id
        self.supported_versions = supported_versions
        self.features = features

class ServerManifest:
    def __init__(self, server_id: str, supported_versions: List[str], available_features: Set[str], required_features: Set[str]):
        self.server_id = server_id
        self.supported_versions = supported_versions
        self.available_features = available_features
        self.required_features = required_features

class SessionDescriptor:
    def __init__(self, version: str, active_features: Set[str], status: str):
        self.version = version
        self.active_features = active_features
        self.status = status

class CapabilityBroker:
    @staticmethod
    def negotiate(client: ClientManifest, server: ServerManifest) -> SessionDescriptor:
        # 1. Negotiate highest common version
        common_versions = [v for v in client.supported_versions if v in server.supported_versions]
        if not common_versions:
            # Fallback to base v1.0
            return SessionDescriptor("1.0", set(), "fallback_downgrade")

        chosen_version = common_versions[0]  # assumes sorted descending

        # 2. Check required features
        if not server.required_features.issubset(client.features):
            return SessionDescriptor(chosen_version, set(), "rejected_missing_required_features")

        # 3. Intersect optional features
        active_features = client.features.intersection(server.available_features)
        return SessionDescriptor(chosen_version, active_features, "negotiated_ok")
