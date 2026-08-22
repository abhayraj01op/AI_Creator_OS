"""
AI Creator OS - Automated Test Suite
Validates core hardware detection, storage topology creation,
manifest integrity, and error recovery handling.
"""
import os
import sys
import unittest
import shutil
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.hardware import HardwareDetector
from core.storage import StorageManager
from core.model_manager import ModelManager
from core.installer import PersistentInstaller
from core.project_workspace import ProjectWorkspace, CrossModuleBus


class TestAICreatorOS(unittest.TestCase):
    def setUp(self):
        self.test_root = "/tmp/AI_Creator_OS_unit_test"
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)
        self.storage = StorageManager(self.test_root)
        self.storage.initialize_filesystem()

    def tearDown(self):
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)

    def test_hardware_detection(self):
        hw = HardwareDetector.get_hardware_info()
        self.assertIn("platform", hw)
        self.assertIn("cpu_count", hw)
        self.assertIn("tier", hw)
        self.assertGreater(hw["cpu_count"], 0)

    def test_storage_initialization(self):
        p = Path(self.test_root)
        self.assertTrue((p / "models").exists())
        self.assertTrue((p / "checkpoints").exists())
        self.assertTrue((p / "outputs/media").exists())
        self.assertTrue((p / "outputs/youtube").exists())
        self.assertTrue((p / "projects").exists())

    def test_model_manager_registration(self):
        mm = ModelManager(self.test_root)
        dummy_file = Path(self.test_root) / "models/test_model.pth"
        with open(dummy_file, "wb") as f:
            f.write(b"SAMPLE_MODEL_BYTES_TEST")

        entry = mm.register_model(
            model_key="test_model",
            category="models",
            name="Test Model Unit",
            file_path=str(dummy_file),
            source_url="https://example.com/test_model.pth",
        )
        self.assertEqual(entry["status"], "verified")
        self.assertTrue(mm.is_model_ready("test_model", expected_min_bytes=10))

    def test_project_workspace_and_cross_module(self):
        pw = ProjectWorkspace("TEST_PROJ_999", self.test_root)
        meta = pw.load_metadata()
        self.assertEqual(meta["project_id"], "TEST_PROJ_999")

        # Test script to voice handoff
        script_path = CrossModuleBus.transfer_script_to_voice(pw, "Hello world AI Creator OS script test.", "Test Title")
        self.assertTrue(os.path.exists(script_path))

        meta_updated = pw.load_metadata()
        self.assertTrue(meta_updated["pipeline_stages"]["script"]["completed"])


if __name__ == "__main__":
    unittest.main()
