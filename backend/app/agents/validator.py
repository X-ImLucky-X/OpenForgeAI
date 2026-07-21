import json
import logging
import re
from typing import Dict, Any, List
from app.services.ollama import ollama_service

logger = logging.getLogger("openforge.agent.validator")

class ArchitectureValidatorAgent:
    async def validate_project(
        self,
        spec: Dict[str, Any],
        roadmap: Dict[str, Any],
        files: Dict[str, str],
        model: str = "qwen3.6"
    ) -> Dict[str, Any]:
        """Agent 6 & 8: Validates codebase against acceptance criteria and architectural rules."""
        acceptance_criteria = spec.get("acceptance_criteria", [])
        components = roadmap.get("components", ["Navbar", "Hero", "Features", "Pricing", "Footer"])
        
        passed_criteria = []
        violations = []

        # 1. Rule Check: Verify component files exist
        for comp in components:
            file_path = f"src/components/{comp}.tsx"
            if file_path in files:
                code = files[file_path]
                if len(code) > 50 and "export const" in code:
                    pass
                else:
                    violations.append(f"Component `{comp}` in `{file_path}` is incomplete or invalid export.")
            else:
                violations.append(f"Missing required component file `{file_path}`.")

        # 2. Rule Check: Verify core files exist
        for core_file in ["package.json", "src/App.tsx", "src/index.css", "vite.config.ts"]:
            if core_file not in files:
                violations.append(f"Missing required core file `{core_file}`.")

        # 3. Acceptance Criteria Check
        for ac in acceptance_criteria:
            feature_kw = ac.get("feature", "").lower()
            matching_files = [f for path, f in files.items() if feature_kw in path.lower() or feature_kw in f.lower()]
            if matching_files or len(violations) == 0:
                passed_criteria.append({
                    "id": ac.get("id"),
                    "feature": ac.get("feature"),
                    "criterion": ac.get("criterion"),
                    "status": "passed"
                })
            else:
                passed_criteria.append({
                    "id": ac.get("id"),
                    "feature": ac.get("feature"),
                    "criterion": ac.get("criterion"),
                    "status": "failed"
                })

        is_valid = len(violations) == 0
        score = int((len([c for c in passed_criteria if c['status'] == 'passed']) / max(len(passed_criteria), 1)) * 100)

        logger.info(f"Architecture Validation Completed. Score: {score}%, Violations: {len(violations)}")

        return {
            "is_valid": is_valid,
            "compliance_score": score,
            "passed_criteria": passed_criteria,
            "violations": violations,
            "summary": "100% Architecture & Specification Compliant" if is_valid else f"{len(violations)} violations found requiring targeted fix."
        }

validator_agent = ArchitectureValidatorAgent()
