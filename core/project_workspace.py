"""
AI Creator OS - Project Workspace & Cross-Module Pipeline Bus
Maintains end-to-end multi-module project assets and metadata across pipelines.
"""
import os
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List


class ProjectWorkspace:
    """Manages an end-to-end multi-media project folder structure on Google Drive."""

    SUBFOLDERS = [
        "input",
        "research",
        "script",
        "images",
        "audio",
        "video",
        "subtitles",
        "thumbnail",
        "metadata",
        "exports",
    ]

    def __init__(self, project_id: str, root_dir: str = "/content/drive/MyDrive/AI_Creator_OS"):
        self.project_id = project_id
        self.root_dir = Path(root_dir)
        self.project_path = self.root_dir / f"projects/{project_id}"
        self.metadata_file = self.project_path / "project.json"
        self._initialize_project()

    def _initialize_project(self) -> None:
        self.project_path.mkdir(parents=True, exist_ok=True)
        for sub in self.SUBFOLDERS:
            (self.project_path / sub).mkdir(parents=True, exist_ok=True)

        if not self.metadata_file.exists():
            initial_data = {
                "project_id": self.project_id,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "created",
                "title": "",
                "description": "",
                "pipeline_stages": {
                    "research": {"completed": False, "files": []},
                    "script": {"completed": False, "files": []},
                    "voiceover": {"completed": False, "files": []},
                    "images": {"completed": False, "files": []},
                    "video": {"completed": False, "files": []},
                    "subtitles": {"completed": False, "files": []},
                    "thumbnail": {"completed": False, "files": []},
                    "final_export": {"completed": False, "files": []},
                },
                "tags": [],
                "target_duration_seconds": 60,
            }
            self.save_metadata(initial_data)

    def load_metadata(self) -> Dict[str, Any]:
        try:
            with open(self.metadata_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}

    def save_metadata(self, data: Dict[str, Any]) -> None:
        try:
            with open(self.metadata_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving project metadata: {e}")

    def update_stage(self, stage_name: str, file_path: str, extra: Optional[Dict[str, Any]] = None) -> None:
        meta = self.load_metadata()
        if "pipeline_stages" in meta and stage_name in meta["pipeline_stages"]:
            meta["pipeline_stages"][stage_name]["completed"] = True
            if file_path not in meta["pipeline_stages"][stage_name]["files"]:
                meta["pipeline_stages"][stage_name]["files"].append(file_path)
            if extra:
                meta["pipeline_stages"][stage_name].update(extra)
            self.save_metadata(meta)

    def get_stage_folder(self, stage_name: str) -> Path:
        p = self.project_path / stage_name
        p.mkdir(parents=True, exist_ok=True)
        return p


class CrossModuleBus:
    """Orchestrates asset handoffs between Writer, Voice, Media, Video, and YouTube engines."""

    @staticmethod
    def transfer_script_to_voice(workspace: ProjectWorkspace, script_text: str, title: str) -> str:
        """Stores script and prepares input for voice generation."""
        script_dir = workspace.get_stage_folder("script")
        script_file = script_dir / "full_script.txt"
        with open(script_file, "w", encoding="utf-8") as f:
            f.write(script_text)

        workspace.update_stage("script", str(script_file), {"title": title, "word_count": len(script_text.split())})
        print(f"✨ Script saved and passed to Voice Engine pipeline: {script_file}")
        return str(script_file)

    @staticmethod
    def transfer_audio_to_video(workspace: ProjectWorkspace, audio_file: str) -> None:
        """Registers generated audio for video timeline compilation."""
        workspace.update_stage("voiceover", audio_file)
        print(f"✨ Voice track registered to Project timeline: {audio_file}")


if __name__ == "__main__":
    pw = ProjectWorkspace("DEMO_PROJECT_001", "/tmp/AI_Creator_OS_test")
    print("Project Workspace initialized:", pw.project_path)
