import os
import logging
from typing import Dict
from app.utils.zipper import create_project_zip

logger = logging.getLogger("openforge.agent.exporter")

class ExportAgent:
    def export_project(self, project_id: str, files: Dict[str, str], base_dir: str) -> Dict[str, str]:
        """Agent 4: Saves project files to disk and creates downloadable website.zip."""
        project_dir = os.path.join(base_dir, "generated_projects", project_id)
        zips_dir = os.path.join(base_dir, "generated_zips")
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(zips_dir, exist_ok=True)

        zip_filepath = os.path.join(zips_dir, f"{project_id}.zip")

        # Write each file to project directory
        for filepath, content in files.items():
            full_path = os.path.join(project_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        # Create zip archive using zipper utility
        create_project_zip(project_dir, zip_filepath)

        logger.info(f"Project exported successfully to {project_dir} and ZIP created at {zip_filepath}")

        return {
            "project_dir": project_dir,
            "zip_filepath": zip_filepath,
            "zip_filename": f"{project_id}.zip"
        }

export_agent = ExportAgent()
