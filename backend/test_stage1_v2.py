import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.intent_expander import intent_expander_agent
from app.agents.planner import planner_agent
from app.agents.ui_planner import ui_planner_agent
from app.services.prompt_optimizer import prompt_optimizer

async def test_stage1_v2():
    print("==========================================")
    print("Testing OpenForge AI v2 - Stage 1 Agents...")
    print("==========================================")

    # 1. Intent Expander
    print("[1] Running Intent Expander Agent...")
    spec = await intent_expander_agent.execute(
        prompt="Build a SaaS landing page for an AI startup",
        theme="Modern Dark",
        model="qwen3.6"
    )
    print(f" -> Project Name: {spec['project_name']}")
    print(f" -> Acceptance Criteria Count: {len(spec.get('acceptance_criteria', []))}")

    # 2. Roadmap Planner
    print("\n[2] Running Roadmap Planner Agent...")
    roadmap = await planner_agent.execute(spec, "Build a SaaS landing page for an AI startup", "qwen3.6")
    print(f" -> Components Roadmap: {roadmap['components']}")
    print(f" -> Development Phases: {len(roadmap.get('phases', []))}")

    # 3. UI/UX Designer
    print("\n[3] Running UI Designer Agent...")
    ui_specs = await ui_planner_agent.execute(roadmap, "Build a SaaS landing page for an AI startup", "qwen3.6")
    print(f" -> Design Tokens: {ui_specs.get('design_system', {})}")

    # 4. Prompt Optimizer Service
    print("\n[4] Running Prompt Optimizer Service...")
    opt_prompt = prompt_optimizer.optimize_component_prompt(
        component_name="Hero",
        project_name=spec['project_name'],
        prompt="Build a SaaS landing page for an AI startup",
        theme_name="Modern Dark",
        design_system=ui_specs.get('design_system', {}),
        acceptance_criteria=spec.get('acceptance_criteria', [])
    )
    print(" -> Optimized Prompt Length:", len(opt_prompt))

    if len(spec.get('acceptance_criteria', [])) > 0 and len(roadmap.get('components', [])) > 0:
        print("\nSUCCESS: Stage 1 v2 Passed!")
        return True
    else:
        print("\nFAILED: Missing spec criteria or components!")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_stage1_v2())
    if not success:
        sys.exit(1)
