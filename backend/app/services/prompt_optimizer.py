from typing import Dict, Any

class PromptOptimizerService:
    def optimize_component_prompt(
        self,
        component_name: str,
        project_name: str,
        prompt: str,
        theme_name: str,
        design_system: Dict[str, Any],
        acceptance_criteria: list
    ) -> str:
        """Enriches component generation prompt with design tokens and acceptance criteria."""
        matching_criteria = [
            ac for ac in acceptance_criteria 
            if component_name.lower() in ac.get("feature", "").lower() or component_name.lower() in ac.get("criterion", "").lower()
        ]

        criteria_str = "\n".join([f"- {ac.get('criterion')}" for ac in matching_criteria]) if matching_criteria else "- Must be visually modern, responsive, and follow Tailwind styling."

        return f"""Task: Generate component `{component_name}` for React + Vite + TypeScript application "{project_name}".

User Request Context: "{prompt}"

Design System Directives:
- Theme: {theme_name}
- Typography: {design_system.get('typography', 'Plus Jakarta Sans')}
- Spacing & Radius: {design_system.get('border_radius', 'rounded-2xl')}
- Color Tokens: Primary Accent ({theme_name})

Acceptance Criteria to Satisfy:
{criteria_str}

Technical Constraints:
1. Export as `export const {component_name}: React.FC = () => {{ ... }}`.
2. Use Lucide React icons (`import {{ ... }} from 'lucide-react'`).
3. Fully responsive layout using Tailwind CSS.
4. Output clean TypeScript code without markdown codeblocks.
"""

prompt_optimizer = PromptOptimizerService()
