"""CLI for Capability Negotiation Broker."""
import argparse
from .core import CapabilityBroker, ClientManifest, ServerManifest

def main():
    parser = argparse.ArgumentParser(description="MCP Capability Negotiation Broker CLI")
    parser.add_argument("--demo", action="store_true", help="Run capability negotiation demo")
    args = parser.parse_args()

    client = ClientManifest("agent-cli", ["2.1", "2.0", "1.0"], {"streaming", "speculation", "compression"})
    server = ServerManifest("mcp-server", ["2.1", "2.0"], {"streaming", "speculation", "encryption"}, {"streaming"})

    desc = CapabilityBroker.negotiate(client, server)
    print(f"Negotiation Status: {desc.status} | Version: {desc.version} | Active Features: {list(desc.active_features)}")

if __name__ == "__main__":
    main()
