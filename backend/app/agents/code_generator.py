import logging
import re
from typing import Dict, Any, List
from app.services.ollama import ollama_service
from app.services import templates

logger = logging.getLogger("openforge.agent.code_generator")

class CodeGeneratorAgent:
    async def generate_component(
        self,
        component_name: str,
        project_name: str,
        prompt: str,
        theme_name: str,
        spec: Dict[str, Any],
        model: str = "qwen3.6"
    ) -> str:
        """Generates TSX React code for a single component."""
        c_lower = component_name.lower()

        # Route dedicated multi-page components directly for guaranteed working interactive state
        if c_lower in ["todoworkspace", "todoapp", "todolist", "taskmanager"]:
            logger.info("Using template generator for TodoWorkspace")
            return templates.generate_todo_workspace(project_name, theme_name)
        elif c_lower == "categoryview":
            return templates.generate_category_view(project_name, theme_name)
        elif c_lower == "analyticsview":
            return templates.generate_analytics_view(project_name, theme_name)
        elif c_lower == "settingsview":
            return templates.generate_settings_view(project_name, theme_name)
        elif c_lower == "navbar":
            return templates.generate_navbar_component(project_name, theme_name)
        elif c_lower == "hero":
            return templates.generate_hero_component(project_name, prompt, theme_name)
        elif c_lower == "features":
            return templates.generate_features_component(theme_name)
        elif c_lower == "pricing":
            return templates.generate_pricing_component(theme_name)
        elif c_lower == "footer":
            return templates.generate_footer_component(project_name, theme_name)

        # Prompt LLM for custom components
        system_prompt = (
            "You are a Master React & Tailwind CSS Developer. "
            "Generate ONLY valid TypeScript React TSX code for the component. "
            "Use Lucide React icons. Export the component as named export `export const ComponentName: React.FC = () => ...`."
            "Do NOT include conversational intro text or explanations. Output clean TSX code inside ```tsx codeblocks."
        )

        user_msg = f"""Create component `{component_name}` for React + Vite project "{project_name}".
User Description: "{prompt}"
Theme: "{theme_name}"
Purpose: "{spec.get('purpose', '')}"

Requirements:
1. Must use Tailwind CSS for styling matching the theme.
2. Must import Lucide icons from 'lucide-react'.
3. Must be clean, responsive, and visually modern.
4. Export as `export const {component_name}: React.FC = () => {{ ... }}`.
"""

        raw_code = await ollama_service.generate(
            model=model,
            prompt=user_msg,
            system_prompt=system_prompt,
            temperature=0.4
        )

        if raw_code:
            cleaned = self._clean_code(raw_code)
            if "export const" in cleaned or "export function" in cleaned or "return" in cleaned:
                logger.info(f"Generated clean LLM code for {component_name}")
                return cleaned

        # Fallback Generic Component
        t = templates.get_theme(theme_name)
        return f"""import React from 'react';
import {{ Sparkles }} from 'lucide-react';

export const {component_name}: React.FC = () => {{
  return (
    <section className="py-20 {t['bg']} {t['text']}">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="inline-flex p-3 rounded-2xl {t['card_bg']} mb-4">
          <Sparkles className="w-6 h-6 text-indigo-400" />
        </div>
        <h2 className="text-3xl font-extrabold mb-4">{component_name}</h2>
        <p className="{t['muted_text']} max-w-xl mx-auto">
          Production ready component for {component_name} in {project_name}.
        </p>
      </div>
    </section>
  );
}};
"""

    def generate_app_tsx(self, project_name: str, components: List[str]) -> str:
        return templates.generate_app_tsx(project_name, components)

    def generate_config_files(self, project_name: str, description: str) -> Dict[str, str]:
        return {
            "package.json": templates.generate_package_json(project_name),
            "tailwind.config.js": templates.generate_tailwind_config(),
            "postcss.config.js": templates.generate_postcss_config(),
            "vite.config.ts": templates.generate_vite_config(),
            "index.html": templates.generate_index_html(project_name),
            "README.md": templates.generate_readme(project_name, description),
            "public/vite.svg": templates.generate_vite_svg(),
            "src/index.css": templates.generate_index_css(),
            "src/main.tsx": templates.generate_main_tsx(),
        }

    def _clean_code(self, raw_code: str) -> str:
        if not raw_code:
            return ""

        match = re.search(r"```(?:tsx|jsx|typescript|javascript)?\s*\n(.*?)\n```", raw_code, re.DOTALL)
        if match:
            code = match.group(1).strip()
        else:
            code = raw_code.strip()

        first_code_line = re.search(r"((?:import|export|const|function|interface|type)\s+.*)", code, re.DOTALL)
        if first_code_line:
            code = first_code_line.group(1).strip()

        code = re.sub(r"```$", "", code).strip()

        return code

code_generator_agent = CodeGeneratorAgent()
