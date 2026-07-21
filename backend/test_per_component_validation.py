import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.intent_expander import intent_expander_agent
from app.agents.planner import planner_agent
from app.agents.code_generator import code_generator_agent
from app.agents.component_validator import component_validator_agent
from app.agents.exporter import export_agent

async def test_per_component_validation_and_multi_page():
    print("=========================================================")
    print("Testing Per-Component Validation & Multi-Page Generator...")
    print("=========================================================")

    # 1. Intent Expander
    print("[1] Intent Expander Archetype & Sub-Pages Detection...")
    prompt = "Build a working Todo App with dark mode, task categories, search, and local storage, it should be a multi page working website"
    spec = await intent_expander_agent.execute(prompt, "Modern Dark", "qwen3.6")
    print(f" -> Archetype: {spec.get('archetype')}")
    print(f" -> Sub-Pages: {spec.get('pages')}")

    # 2. Roadmap Planner
    print("\n[2] Roadmap Planner Multi-Page Components...")
    roadmap = await planner_agent.execute(spec, prompt, "qwen3.6")
    print(f" -> Components: {roadmap['components']}")

    # 3. Component Generation & Per-Component Immediate Validation Loop
    print("\n[3] Synthesizing Component Files with Immediate Per-Component Validation...")
    config_files = code_generator_agent.generate_config_files(spec['project_name'], spec['description'])
    project_files = dict(config_files)
    comp_files_list = []

    for comp in roadmap['components']:
        print(f"   -> Generating `src/components/{comp}.tsx`...")
        comp_code = await code_generator_agent.generate_component(
            component_name=comp,
            project_name=spec['project_name'],
            prompt=prompt,
            theme_name="Modern Dark",
            spec={"purpose": f"Dedicated multi-page {comp} view"},
            model="qwen3.6"
        )

        print(f"   -> Executing Immediate Per-Component Validator on `{comp}`...")
        validated_code = await component_validator_agent.validate_and_repair(
            component_name=comp,
            code=comp_code,
            project_name=spec['project_name'],
            prompt=prompt,
            theme_name="Modern Dark",
            model="qwen3.6"
        )
        file_path = f"src/components/{comp}.tsx"
        project_files[file_path] = validated_code
        comp_files_list.append(file_path)

    app_code = code_generator_agent.generate_app_tsx(spec['project_name'], comp_files_list)
    project_files["src/App.tsx"] = await component_validator_agent.validate_and_repair(
        component_name="App",
        code=app_code,
        project_name=spec['project_name'],
        prompt=prompt,
        theme_name="Modern Dark",
        model="qwen3.6"
    )

    # Verification Checks
    has_workspace = "src/components/TodoWorkspace.tsx" in project_files
    has_categories = "src/components/CategoryView.tsx" in project_files
    has_analytics = "src/components/AnalyticsView.tsx" in project_files
    has_settings = "src/components/SettingsView.tsx" in project_files
    has_routing = "activeTab ===" in project_files["src/App.tsx"]

    print(f"\n[Verification] Dedicated TodoWorkspace Component: {has_workspace}")
    print(f"[Verification] Dedicated CategoryView Component: {has_categories}")
    print(f"[Verification] Dedicated AnalyticsView Component: {has_analytics}")
    print(f"[Verification] Dedicated SettingsView Component: {has_settings}")
    print(f"[Verification] App.tsx Isolated Multi-Page Router: {has_routing}")

    # 4. Exporter
    base_dir = os.path.dirname(os.path.abspath(__file__))
    res = export_agent.export_project("per-comp-val-test", project_files, base_dir)
    print(f" -> Exported Zip: {res['zip_filepath']}")

    if has_workspace and has_categories and has_analytics and has_settings and has_routing:
        print("\nSUCCESS: Per-Component Immediate Validation & Dedicated Multi-Page Architecture Test Passed!")
        return True
    else:
        print("\nFAILED: Missing dedicated multi-page view components!")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_per_component_validation_and_multi_page())
    if not success:
        sys.exit(1)
