import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("gpu_build", Path(__file__).with_name("build.py"))
gpu_build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gpu_build)


class RuntimeProfileTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        source = Path(__file__).resolve().parents[2]
        for name in ("ubuntu/minimal", "ubuntu/python", "ubuntu/gpu"):
            shutil.copytree(source / name, self.root / name)
        self.env = patch.dict(os.environ, {"GITHUB_BASE_REF": "", "GITHUB_REF_NAME": ""}, clear=True)
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_current_profile_and_build_order(self):
        profile, cuda_image = gpu_build.check_profile(self.root)
        commands = gpu_build.build_commands(self.root, profile, cuda_image)
        contexts = [command[-1] for command in commands if command[:2] == ["docker", "build"]]
        self.assertEqual(contexts, [str(self.root / path) for path in (
            "ubuntu/gpu", "ubuntu/minimal", "ubuntu/python", "ubuntu/gpu/pytorch", "ubuntu/gpu/tensorflow",
        )])
        self.assertEqual(len(commands), 9)

    def test_copied_profile_is_rejected_on_another_release(self):
        os.environ["GITHUB_BASE_REF"] = "release-99.1-LTS"
        with self.assertRaisesRegex(ValueError, "runtime_tag must be"):
            gpu_build.check_profile(self.root)

    def test_python_package_drift_is_rejected(self):
        path = self.root / "ubuntu/python/requirements.txt"
        profile = json.loads((self.root / "ubuntu/gpu/runtime.json").read_text())
        before = "pyarrow==" + profile["python_packages"]["pyarrow"]
        path.write_text(path.read_text().replace(before, "pyarrow==8.0.0"))
        with self.assertRaisesRegex(ValueError, "pyarrow pin differs"):
            gpu_build.check_profile(self.root)

    def test_python_interpreter_drift_is_rejected(self):
        path = self.root / "ubuntu/python/Dockerfile"
        profile = json.loads((self.root / "ubuntu/gpu/runtime.json").read_text())
        before = 'ARG python_version="' + profile["python_version"] + '"'
        path.write_text(path.read_text().replace(before, 'ARG python_version="3.99"'))
        with self.assertRaisesRegex(ValueError, "Python version differs"):
            gpu_build.check_profile(self.root)

    def test_framework_constraint_drift_is_rejected(self):
        path = self.root / "ubuntu/gpu/framework-constraints.txt"
        path.write_text(path.read_text() + "unplanned-package==1.0\n")
        with self.assertRaisesRegex(ValueError, "framework constraints differ"):
            gpu_build.check_profile(self.root)


if __name__ == "__main__":
    unittest.main()
