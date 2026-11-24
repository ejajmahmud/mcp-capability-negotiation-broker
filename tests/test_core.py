"""Tests for CapabilityBroker."""
import unittest
from mcp_capability_negotiation_broker.core import CapabilityBroker, ClientManifest, ServerManifest

class TestCapabilityBroker(unittest.TestCase):
    def test_successful_negotiation(self):
        c = ClientManifest("c1", ["2.0", "1.0"], {"stream", "compress"})
        s = ServerManifest("s1", ["2.0"], {"stream", "compress", "audit"}, {"stream"})
        desc = CapabilityBroker.negotiate(c, s)
        self.assertEqual(desc.status, "negotiated_ok")
        self.assertEqual(desc.version, "2.0")
        self.assertIn("stream", desc.active_features)

    def test_missing_required_feature(self):
        c = ClientManifest("c2", ["2.0"], {"compress"})
        s = ServerManifest("s2", ["2.0"], {"stream"}, {"stream"})
        desc = CapabilityBroker.negotiate(c, s)
        self.assertEqual(desc.status, "rejected_missing_required_features")
