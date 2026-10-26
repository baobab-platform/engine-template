"""Test DEV-14 adapter template never claims real runtime acceptance."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


TEMPLATE = Path(__file__).resolve().parents[1] / ".baobab/development_adapter.py.example"


class AdapterTemplateTests(unittest.TestCase):
    def test_all_owner_phases_refuse_until_implemented(self):
        for phase in ("readiness", "migrate", "seed", "exercise", "cleanup"):
            with self.subTest(phase=phase):
                result = subprocess.run([sys.executable, "-B", str(TEMPLATE), phase],
                                        text=True, capture_output=True, timeout=10)
                self.assertEqual(result.returncode, 2)
                receipt = json.loads(result.stdout)
                self.assertEqual(receipt["reason"], "OWNER_ADAPTER_NOT_IMPLEMENTED")
                self.assertEqual(receipt["result"], "BLOCKED")
                self.assertFalse(receipt["real_native_effect"])
                self.assertFalse(receipt["protected_acceptance"])
                self.assertFalse(receipt["production_authorized"])

    def test_unknown_phase_refuses(self):
        result = subprocess.run([sys.executable, "-B", str(TEMPLATE), "approve"],
                                text=True, capture_output=True, timeout=10)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
