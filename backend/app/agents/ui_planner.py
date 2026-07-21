import json
import logging
import re
from typing import Dict, Any
from app.services.ollama import ollama_service

logger = logging.getLogger("openforge.agent.ui_planner")

class UIPlannerAgent:
    async def execute(self, plan: Dict[str, Any], prompt: str, model: str = "qwen3.6") -> Dict[str, Any]:
        """Agent 2: UI Planner - Refines UI design tokens, layout hierarchy, and component specs."""
        system_prompt = (
            "You are a Principal UI/UX Architect specializing in modern Tailwind CSS design systems. "
            "Return strictly a valid JSON object defining design specs for each component."
        )

        user_msg = f"""Project Plan: {json.dumps(plan)}
User Request: "{prompt}"

Return valid JSON matching this structure:
{{
  "design_system": {{
    "theme": "{plan.get('theme', 'Modern Dark')}",
    "typography": "Plus Jakarta Sans",
    "spacing": "comfortable",
    "border_radius": "rounded-2xl"
  }},
  "component_specs": [
    {{
      "name": "Navbar",
      "purpose": "Global top navigation with logo, nav links, and CTA",
      "lucide_icons": ["Sparkles", "Menu", "X", "ArrowRight"]
    }},
    {{
      "name": "Hero",
      "purpose": "Main value proposition header with headline, subtitle, buttons, and visual element",
      "lucide_icons": ["ArrowRight", "CheckCircle2", "Zap", "Shield", "Star"]
    }},
    {{
      "name": "Features",
      "purpose": "3x2 grid displaying key features with icons and descriptions",
      "lucide_icons": ["Cpu", "Rocket", "ShieldCheck", "Layers", "Globe", "Sparkles"]
    }},
    {{
      "name": "Pricing",
      "purpose": "3 tier pricing cards with highlight badge on Pro plan",
      "lucide_icons": ["Check"]
    }},
    {{
      "name": "Footer",
      "purpose": "Footer with brand summary, links columns, social icons and copyright",
      "lucide_icons": ["Sparkles", "Github", "Twitter", "Linkedin"]
    }}
  ]
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
                    if "component_specs" in parsed:
                        logger.info("Successfully received UI plan from Ollama LLM.")
                        return parsed
            except Exception as e:
                logger.warning(f"Failed to parse UI plan JSON: {e}")

        # Fallback UI Design Specs
        return {
            "design_system": {
                "theme": plan.get("theme", "Modern Dark"),
                "typography": "Plus Jakarta Sans",
                "spacing": "comfortable",
                "border_radius": "rounded-2xl"
            },
            "component_specs": [
                {"name": c, "purpose": f"Standard {c} section for {plan.get('project_name')}", "lucide_icons": []}
                for c in plan.get("components", ["Navbar", "Hero", "Features", "Pricing", "Footer"])
            ]
        }

ui_planner_agent = UIPlannerAgent()
