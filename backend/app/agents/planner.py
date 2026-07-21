import json
import logging
import re
from typing import Dict, Any, List
from app.services.ollama import ollama_service

logger = logging.getLogger("openforge.agent.planner")

ARCHETYPE_COMPONENTS = {
    "todo_app": ["Navbar", "Hero", "TodoWorkspace", "CategoryView", "AnalyticsView", "SettingsView", "Footer"],
    "portfolio": ["Navbar", "Hero", "Gallery", "About", "ContactForm", "Footer"],
    "ecommerce": ["Navbar", "HeroBanner", "ProductGrid", "CheckoutModal", "Footer"],
    "saas_dashboard": ["Navbar", "Hero", "DashboardView", "Pricing", "ContactForm", "Footer"],
    "landing_page": ["Navbar", "Hero", "Features", "Pricing", "Footer"]
}

class PlannerAgent:
    async def execute(self, spec: Dict[str, Any], prompt: str, model: str = "qwen3.6") -> Dict[str, Any]:
        """Agent 2: Project Planner - Generates phased development roadmap and archetype component graph."""
        archetype = spec.get("archetype", "landing_page")
        default_comps = ARCHETYPE_COMPONENTS.get(archetype, ARCHETYPE_COMPONENTS["landing_page"])

        system_prompt = (
            "You are a Lead Software Architect & Technical Program Manager. "
            "Given a project specification, return strictly a valid JSON document defining phases and dependencies."
        )

        user_msg = f"""Specification: {json.dumps(spec)}
User Request: "{prompt}"
Archetype: "{archetype}"

Return valid JSON matching this schema:
{{
  "project_name": "{spec.get('project_name', 'OpenForge Project')}",
  "archetype": "{archetype}",
  "theme": "{spec.get('theme', 'Modern Dark')}",
  "description": "{spec.get('description', '')}",
  "pages": {json.dumps(spec.get('pages', ['Home', 'Tasks', 'Categories', 'Analytics', 'Settings']))},
  "components": {json.dumps(default_comps)},
  "phases": [
    {{"phase": 1, "name": "Project Setup", "files": ["package.json", "vite.config.ts", "index.html"]}},
    {{"phase": 2, "name": "Navigation & Core Layout", "files": ["src/components/Navbar.tsx"]}},
    {{"phase": 3, "name": "Dedicated Multi-Page Views", "files": ["src/components/TodoWorkspace.tsx", "src/components/CategoryView.tsx", "src/components/AnalyticsView.tsx"]}},
    {{"phase": 4, "name": "Settings & Conversion", "files": ["src/components/SettingsView.tsx", "src/components/Footer.tsx"]}},
    {{"phase": 5, "name": "Isolated App View Router", "files": ["src/App.tsx"]}}
  ],
  "dependencies": {{
    "Navbar": [],
    "Hero": ["Navbar"],
    "TodoWorkspace": ["Navbar"],
    "CategoryView": ["TodoWorkspace"],
    "AnalyticsView": ["CategoryView"],
    "SettingsView": ["AnalyticsView"],
    "Footer": ["SettingsView"]
  }}
}}
"""

        raw_response = await ollama_service.generate(
            model=model,
            prompt=user_msg,
            system_prompt=system_prompt,
            temperature=0.3
        )

        if raw_response:
            try:
                cleaned = re.sub(r"```(?:json)?", "", raw_response).strip()
                match = re.search(r"\{.*\}", cleaned, re.DOTALL)
                if match:
                    parsed = json.loads(match.group(0))
                    if "components" in parsed and "phases" in parsed:
                        logger.info(f"Successfully generated Roadmap for archetype '{archetype}' from LLM.")
                        return parsed
            except Exception as e:
                logger.warning(f"Failed to parse LLM roadmap JSON: {e}")

        # Fallback Roadmap Generator
        return {
            "project_name": spec.get("project_name", "OpenForge App"),
            "archetype": archetype,
            "theme": spec.get("theme", "Modern Dark"),
            "description": spec.get("description", f"Roadmap for {prompt}"),
            "pages": spec.get("pages", ["Home", "Tasks", "Categories", "Analytics", "Settings"]),
            "components": default_comps,
            "phases": [
                {"phase": 1, "name": "Project Setup", "files": ["package.json", "vite.config.ts", "index.html"]},
                {"phase": 2, "name": "Navigation & Header", "files": ["src/components/Navbar.tsx", f"src/components/{default_comps[1]}.tsx"]},
                {"phase": 3, "name": "Dedicated Multi-Page Views", "files": [f"src/components/{c}.tsx" for c in default_comps[2:5]]},
                {"phase": 4, "name": "Footer & App Router", "files": ["src/components/Footer.tsx", "src/App.tsx"]}
            ],
            "dependencies": {
                "Navbar": [],
                default_comps[1]: ["Navbar"],
                default_comps[2]: [default_comps[1]],
                default_comps[3]: [default_comps[2]],
                "Footer": [default_comps[-1]]
            }
        }

planner_agent = PlannerAgent()
