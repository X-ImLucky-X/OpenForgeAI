import logging
from typing import Dict, Any, List
from app.agents.code_generator import code_generator_agent

logger = logging.getLogger("openforge.agent.fix_generator")

class FixGeneratorAgent:
    async def apply_fixes(
        self,
        violations: List[str],
        project_name: str,
        prompt: str,
        theme_name: str,
        files: Dict[str, str],
        model: str = "qwen3.6"
    ) -> Dict[str, str]:
        """Agent 7: Fix Generator - Produces targeted patches for affected files only."""
        patched_files = dict(files)

        for violation in violations:
            logger.info(f"Targeted fix patch for: {violation}")

            # Check if missing component violation
            for comp in ["Navbar", "Hero", "Features", "Pricing", "Footer"]:
                if comp in violation:
                    comp_code = await code_generator_agent.generate_component(
                        component_name=comp,
                        project_name=project_name,
                        prompt=prompt,
                        theme_name=theme_name,
                        spec={"purpose": f"Targeted patch for {comp}"},
                        model=model
                    )
                    patched_files[f"src/components/{comp}.tsx"] = comp_code

        return patched_files

fix_generator_agent = FixGeneratorAgent()
