"""
AI Creator OS - Persistent Dependency & Environment Installer
Maintains installation markers on Google Drive so running a notebook a 2nd time
takes <3 seconds instead of 10 minutes of redundant pip installations.
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional


class PersistentInstaller:
    """Installs dependencies and marks modules as installed on Drive."""

    def __init__(self, root_dir: str = "/content/drive/MyDrive/AI_Creator_OS"):
        self.root_dir = Path(root_dir)
        self.state_file = self.root_dir / "config/installation_state.json"
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"modules": {}, "installed_packages": []}

    def _save_state(self) -> None:
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, "w") as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning saving install state: {e}")

    def is_module_installed(self, module_name: str, version: str = "1.0.0") -> bool:
        mod_info = self.state.get("modules", {}).get(module_name)
        if mod_info and mod_info.get("installed") and mod_info.get("version") == version:
            return True
        return False

    def install_requirements(
        self,
        module_name: str,
        requirements_file: Optional[str] = None,
        package_list: Optional[List[str]] = None,
        force_reinstall: bool = False,
        version: str = "1.0.0",
    ) -> bool:
        """Installs dependencies only when needed, then updates persistent marker."""
        if not force_reinstall and self.is_module_installed(module_name, version):
            print(f"⚡ [CACHE HIT] Dependencies for '{module_name}' (v{version}) are already installed.")
            return True

        print(f"📦 Installing dependencies for module: {module_name}...")
        cmd = [sys.executable, "-m", "pip", "install", "--quiet", "--no-warn-script-location"]

        packages_to_install = []
        if requirements_file and os.path.exists(requirements_file):
            cmd.extend(["-r", requirements_file])
            print(f"  -> Using requirements file: {requirements_file}")
        elif package_list:
            packages_to_install = package_list
            cmd.extend(package_list)
            print(f"  -> Packages: {', '.join(package_list)}")
        else:
            print("  -> No explicit packages required.")

        try:
            res = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ Dependencies successfully installed for '{module_name}'.")

            # Update state
            if "modules" not in self.state:
                self.state["modules"] = {}
            self.state["modules"][module_name] = {
                "installed": True,
                "version": version,
                "packages": packages_to_install,
            }
            self._save_state()
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error during installation: {e.stderr}")
            return False


if __name__ == "__main__":
    pi = PersistentInstaller()
    print("Persistent installer ready.")
