import json
import logging
import re
from typing import Dict, Any
from app.services.ollama import ollama_service

logger = logging.getLogger("openforge.agent.intent_expander")

class IntentExpanderAgent:
    def classify_archetype(self, prompt: str) -> str:
        p = prompt.lower()
        if any(k in p for k in ["todo", "task", "checklist", "reminder", "kanban"]):
            return "todo_app"
        if any(k in p for k in ["portfolio", "photographer", "gallery", "personal site", "resume"]):
            return "portfolio"
        if any(k in p for k in ["store", "shop", "ecommerce", "cart", "product"]):
            return "ecommerce"
        if any(k in p for k in ["dashboard", "analytics", "metrics", "saas", "platform"]):
            return "saas_dashboard"
        return "landing_page"

    async def execute(self, prompt: str, theme: str = "Modern Dark", model: str = "qwen3.6") -> Dict[str, Any]:
        """Agent 1: Intent Expander - Writes complete requirement specification and explicit Acceptance Criteria."""
        archetype = self.classify_archetype(prompt)

        system_prompt = (
            "You are a Senior Systems Architect & Product Manager. "
            "Given a user prompt, produce a comprehensive JSON Specification matching the schema strictly. "
            "Do NOT include markdown formatting. Return valid JSON only."
        )

        user_msg = f"""User Request: "{prompt}"
Preferred Theme: "{theme}"
Detected Archetype: "{archetype}"

Produce valid JSON with this exact structure:
{{
  "project_name": "Short Title",
  "archetype": "{archetype}",
  "target": "Web Application",
  "theme": "{theme}",
  "description": "Comprehensive specification for the requested application.",
  "pages": ["Home", "App", "Features", "Pricing", "Contact"],
  "features": [
    "Feature 1",
    "Feature 2",
    "Feature 3",
    "Responsive Layout",
    "Dark Mode Support"
  ],
  "ui_style": "Modern Minimalist Glassmorphism",
  "tech_stack": {{
    "framework": "React 18 + Vite + TypeScript",
    "styling": "Tailwind CSS",
    "icons": "Lucide React"
  }},
  "acceptance_criteria": [
    {{"id": "ac-1", "feature": "Navigation", "criterion": "Navbar with brand logo and active view switching tabs"}},
    {{"id": "ac-2", "feature": "Core App Logic", "criterion": "Fully working interactive app components with state management and local storage"}},
    {{"id": "ac-3", "feature": "Feature Showcase", "criterion": "Responsive feature cards with Lucide icons"}},
    {{"id": "ac-4", "feature": "Pricing & Plans", "criterion": "Tiered pricing cards with highlight badge"}},
    {{"id": "ac-5", "feature": "Footer", "criterion": "Footer containing brand links and copyright info"}}
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
                    if "acceptance_criteria" in parsed and "project_name" in parsed:
                        parsed["archetype"] = archetype
                        logger.info(f"Successfully generated Intent Specification for archetype '{archetype}' via LLM.")
                        return parsed
            except Exception as e:
                logger.warning(f"Failed to parse LLM Intent Spec JSON: {e}")

        # Fallback Specification Generator
        logger.info(f"Generating fallback Intent Specification for archetype '{archetype}'.")
        title = self._infer_title(prompt, archetype)
        
        pages_map = {
          "todo_app": ["Tasks", "Completed", "Categories", "Settings"],
          "portfolio": ["Home", "Gallery", "About", "Contact"],
          "ecommerce": ["Store", "Categories", "Cart", "Checkout"],
          "saas_dashboard": ["Home", "Dashboard", "Pricing", "Contact"],
          "landing_page": ["Home", "Features", "Pricing", "Contact"]
        }

        return {
            "project_name": title,
            "archetype": archetype,
            "target": "Web Application",
            "theme": theme,
            "description": f"Production functional web application for '{prompt}'",
            "pages": pages_map.get(archetype, ["Home", "App", "Features", "Pricing", "Contact"]),
            "features": ["Working Interactive State", "Multi-Page Tab Routing", "Local Storage Persistence", "Responsive Design"],
            "ui_style": "Modern Minimalist",
            "tech_stack": {
                "framework": "React 18 + Vite + TypeScript",
                "styling": "Tailwind CSS",
                "icons": "Lucide React"
            },
            "acceptance_criteria": [
                {"id": "ac-1", "feature": "Navbar", "criterion": "Header with brand logo, nav tabs, and CTA button"},
                {"id": "ac-2", "feature": "Interactive Component", "criterion": f"Working interactive {archetype} section with state persistence"},
                {"id": "ac-3", "feature": "Features", "criterion": "Grid layout highlighting key capabilities with Lucide icons"},
                {"id": "ac-4", "feature": "Pricing", "criterion": "Multiple pricing tiers with clear feature bullet points"},
                {"id": "ac-5", "feature": "Footer", "criterion": "Footer containing copyright and product links"}
            ]
        }

    def _infer_title(self, prompt: str, archetype: str) -> str:
        if archetype == "todo_app":
            return "TaskFlow Pro"
        elif archetype == "portfolio":
            return "Apex Studio"
        elif archetype == "ecommerce":
            return "Nexus Store"
        elif archetype == "saas_dashboard":
            return "Forge SaaS"
        
        words = prompt.split()
        if len(words) <= 4:
            return " ".join([w.capitalize() for w in words])
        return "Forge Studio"

intent_expander_agent = IntentExpanderAgent()
