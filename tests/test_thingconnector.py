import importlib
import sys
import types
import unittest
from unittest.mock import patch


def _install_fake_paho_modules():
    fake_client_module = types.ModuleType("paho.mqtt.client")

    class _FakeClient:
        def __init__(self, *args, **kwargs):
            pass

    fake_client_module.Client = _FakeClient

    fake_mqtt_module = types.ModuleType("paho.mqtt")
    fake_mqtt_module.client = fake_client_module

    fake_paho_module = types.ModuleType("paho")
    fake_paho_module.mqtt = fake_mqtt_module

    sys.modules.setdefault("paho", fake_paho_module)
    sys.modules.setdefault("paho.mqtt", fake_mqtt_module)
    sys.modules.setdefault("paho.mqtt.client", fake_client_module)


_install_fake_paho_modules()
thingconnector = importlib.import_module("iotknit.thingconnector")


class ThingConnectorClientInitTests(unittest.TestCase):
    def test_uses_plain_client_for_legacy_paho(self):
        calls = []

        def client(*args, **kwargs):
            calls.append((args, kwargs))
            return object()

        fake_mqtt = types.SimpleNamespace(Client=client)
        with patch.object(thingconnector, "mqtt", fake_mqtt):
            thingconnector._create_mqtt_client()

        self.assertEqual(calls, [((), {})])

    def test_uses_keyword_callback_api_version_when_supported(self):
        calls = []

        def client(*args, **kwargs):
            calls.append((args, kwargs))
            return object()

        fake_mqtt = types.SimpleNamespace(
            Client=client,
            CallbackAPIVersion=types.SimpleNamespace(VERSION1="v1"),
        )
        with patch.object(thingconnector, "mqtt", fake_mqtt):
            thingconnector._create_mqtt_client()

        self.assertEqual(calls, [((), {"callback_api_version": "v1"})])

    def test_falls_back_to_positional_callback_api_version(self):
        calls = []

        def client(*args, **kwargs):
            if kwargs:
                raise TypeError("unexpected keyword")
            calls.append((args, kwargs))
            return object()

        fake_mqtt = types.SimpleNamespace(
            Client=client,
            CallbackAPIVersion=types.SimpleNamespace(VERSION1="v1"),
        )
        with patch.object(thingconnector, "mqtt", fake_mqtt):
            thingconnector._create_mqtt_client()

        self.assertEqual(calls, [(("v1",), {})])


if __name__ == "__main__":
    unittest.main()
