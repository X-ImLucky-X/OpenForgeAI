import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.intent_expander import intent_expander_agent
from app.agents.planner import planner_agent
from app.agents.ui_planner import ui_planner_agent
from app.agents.code_generator import code_generator_agent
from app.agents.validator import validator_agent
from app.agents.fix_generator import fix_generator_agent
from app.agents.exporter import export_agent

async def test_full_v2_pipeline():
    print("==========================================")
    print("Testing OpenForge AI v2 Full Pipeline...")
    print("==========================================")

    # 1. Intent Expander
    print("[1] Running Intent Expander Agent...")
    spec = await intent_expander_agent.execute("Create a Todo App with dark mode and search", "Modern Dark", "qwen3.6")
    print(f" -> Title: {spec['project_name']}")
    print(f" -> Criteria: {len(spec.get('acceptance_criteria', []))}")

    # 2. Roadmap & UI Designer
    print("\n[2] Running Planner & UI Designer...")
    roadmap = await planner_agent.execute(spec, "Create a Todo App with dark mode and search", "qwen3.6")
    ui_specs = await ui_planner_agent.execute(roadmap, "Create a Todo App with dark mode and search", "qwen3.6")
    print(f" -> Components: {roadmap['components']}")

    # 3. Code Generation
    print("\n[3] Synthesizing Project Files...")
    config_files = code_generator_agent.generate_config_files(spec['project_name'], spec['description'])
    project_files = dict(config_files)
    comp_files_list = []

    for comp in roadmap['components']:
        print(f"   -> Generating src/components/{comp}.tsx...")
        comp_code = await code_generator_agent.generate_component(
            component_name=comp,
            project_name=spec['project_name'],
            prompt="Create a Todo App with dark mode and search",
            theme_name="Modern Dark",
            spec={"purpose": f"Standard {comp} section"},
            model="qwen3.6"
        )
        file_path = f"src/components/{comp}.tsx"
        project_files[file_path] = comp_code
        comp_files_list.append(file_path)

    project_files["src/App.tsx"] = code_generator_agent.generate_app_tsx(spec['project_name'], comp_files_list)

    # 4. Architecture Validator
    print("\n[4] Running Architecture Validator...")
    val_report = await validator_agent.validate_project(spec, roadmap, project_files, "qwen3.6")
    print(f" -> Compliance Score: {val_report['compliance_score']}%")
    print(f" -> Violations: {len(val_report['violations'])}")

    # 5. Fix Generator (if needed)
    if not val_report["is_valid"]:
        print("\n[4.1] Applying Targeted Fixes...")
        project_files = await fix_generator_agent.apply_fixes(
            violations=val_report["violations"],
            project_name=spec['project_name'],
            prompt="Create a Todo App",
            theme_name="Modern Dark",
            files=project_files,
            model="qwen3.6"
        )

    # 6. Exporter
    print("\n[5] Running Exporter Agent...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    res = export_agent.export_project("v2-pipeline-test", project_files, base_dir)

    print(f" -> Zip Filepath: {res['zip_filepath']}")

    if os.path.exists(res['zip_filepath']) and val_report['compliance_score'] >= 80:
        print("\nSUCCESS: Stage 2 v2 Pipeline Passed!")
        return True
    else:
        print("\nFAILED: Zip missing or low compliance!")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_full_v2_pipeline())
    if not success:
        sys.exit(1)
