import logging
import re
from typing import Dict, Any
from app.services.ollama import ollama_service
from app.services import templates

logger = logging.getLogger("openforge.agent.component_validator")

class ComponentValidatorAgent:
    """Agent that validates and repairs EVERY component immediately after generation/update."""

    async def validate_and_repair(
        self,
        component_name: str,
        code: str,
        project_name: str,
        prompt: str,
        theme_name: str,
        model: str = "qwen3.6"
    ) -> str:
        if not code:
            logger.warning(f"Component '{component_name}' code is empty. Triggering repair...")
            return self._fallback_repair(component_name, project_name, theme_name)

        violations = []

        # Check 1: Must have valid export
        if f"export const {component_name}" not in code and f"export function {component_name}" not in code:
            violations.append(f"Missing expected export `export const {component_name}`")

        # Check 2: Conversational preamble residue
        if re.search(r"^(Here|Sure|Certainly|Below|This)\s+is", code, re.IGNORECASE | re.MULTILINE):
            violations.append("Contains conversational intro text outside codeblocks")

        # Check 3: Interactive App Component Check
        c_lower = component_name.lower()
        if any(kw in c_lower for kw in ["todo", "task", "workspace", "form", "dashboard"]):
            if "useState" not in code:
                violations.append("Interactive component missing `useState` state management")
            if "onClick" not in code and "onSubmit" not in code:
                violations.append("Interactive component missing click/submit event handlers")

        if not violations:
            logger.info(f"Component `{component_name}` passed immediate validation checks (0 violations).")
            return self._clean_code(code)

        logger.warning(f"Component `{component_name}` has {len(violations)} violation(s): {violations}. Repairing...")

        # Repair prompt via LLM or template fallback
        system_prompt = (
            "You are a Senior React & TypeScript Quality Assurance Engineer. "
            "Fix all syntax and structural violations in the component code. "
            "Output ONLY clean TSX code inside ```tsx codeblocks."
        )

        user_msg = f"""Repair Component: `{component_name}`
Project: "{project_name}"
Violations Found: {json.dumps(violations)}

Original Code:
```tsx
{code}
```

Requirements:
1. Fix all syntax errors and missing exports.
2. Ensure named export `export const {component_name}: React.FC = () => ...`.
3. Must use Lucide icons and Tailwind CSS.
4. Ensure interactive state (`useState`, `onClick`, `onChange`) is cleanly implemented.
"""

        try:
            repaired = await ollama_service.generate(
                model=model,
                prompt=user_msg,
                system_prompt=system_prompt,
                temperature=0.2
            )

            if repaired:
                cleaned = self._clean_code(repaired)
                if f"export const {component_name}" in cleaned or f"export function {component_name}" in cleaned:
                    logger.info(f"Component `{component_name}` successfully repaired via LLM.")
                    return cleaned
        except Exception as e:
            logger.error(f"LLM Component repair failed for `{component_name}`: {e}")

        return self._fallback_repair(component_name, project_name, theme_name)

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

    def _fallback_repair(self, component_name: str, project_name: str, theme_name: str) -> str:
        c_lower = component_name.lower()
        if "todo" in c_lower or "workspace" in c_lower or "task" in c_lower:
            return templates.generate_todo_component(project_name, theme_name)
        elif c_lower == "navbar":
            return templates.generate_navbar_component(project_name, theme_name)
        elif c_lower == "hero":
            return templates.generate_hero_component(project_name, "", theme_name)
        elif c_lower == "features":
            return templates.generate_features_component(theme_name)
        elif c_lower == "pricing":
            return templates.generate_pricing_component(theme_name)
        elif c_lower == "footer":
            return templates.generate_footer_component(project_name, theme_name)
        else:
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

import json
component_validator_agent = ComponentValidatorAgent()
