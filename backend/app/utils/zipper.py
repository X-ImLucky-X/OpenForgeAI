import os
import zipfile
import logging

logger = logging.getLogger("openforge.utils.zipper")

def create_project_zip(source_dir: str, output_zip_path: str) -> str:
    """Compresses a project folder into a ZIP archive."""
    os.makedirs(os.path.dirname(output_zip_path), exist_ok=True)

    with zipfile.ZipFile(output_zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, filenames in os.walk(source_dir):
            for filename in filenames:
                abs_path = os.path.join(root, filename)
                rel_path = os.path.relpath(abs_path, source_dir)
                zipf.write(abs_path, arcname=rel_path)

    logger.info(f"Created ZIP file at {output_zip_path}")
    return output_zip_path
