import asyncio
import os
import sys

# Ensure backend folder is in python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.planner import planner_agent
from app.agents.ui_planner import ui_planner_agent
from app.agents.code_generator import code_generator_agent
from app.agents.exporter import export_agent
from app.services.ollama import ollama_service

async def test_backend_pipeline():
    print("==========================================")
    print("Testing OpenForge AI Stage 1 Backend...")
    print("==========================================")

    # 1. Test Ollama Health & Models
    health = await ollama_service.check_health()
    models = await ollama_service.get_available_models()
    print(f"-> Ollama Online: {health}")
    print(f"-> Available Models: {models}")

    # 2. Agent 1: Planner
    print("\n[Step 1] Running Agent 1 (Planner)...")
    plan = await planner_agent.execute(
        prompt="Create a SaaS landing page for an AI startup",
        theme="Modern Dark",
        model="qwen3.6"
    )
    print(f"-> Project Name: {plan['project_name']}")
    print(f"-> Components: {plan['components']}")

    # 3. Agent 2: UI Planner
    print("\n[Step 2] Running Agent 2 (UI Planner)...")
    ui_plan = await ui_planner_agent.execute(plan, "Create a SaaS landing page for an AI startup", "qwen3.6")
    print(f"-> UI Component Specs Count: {len(ui_plan.get('component_specs', []))}")

    # 4. Agent 3: Code Generator
    print("\n[Step 3] Running Agent 3 (Code Generator)...")
    config_files = code_generator_agent.generate_config_files(plan['project_name'], plan['description'])
    
    project_files = dict(config_files)
    comp_files_list = []

    for comp in plan['components']:
        print(f"   -> Generating src/components/{comp}.tsx...")
        comp_code = await code_generator_agent.generate_component(
            component_name=comp,
            project_name=plan['project_name'],
            prompt="Create a SaaS landing page for an AI startup",
            theme_name="Modern Dark",
            spec={"purpose": f"Standard {comp} section"},
            model="qwen3.6"
        )
        file_path = f"src/components/{comp}.tsx"
        project_files[file_path] = comp_code
        comp_files_list.append(file_path)

    project_files["src/App.tsx"] = code_generator_agent.generate_app_tsx(plan['project_name'], comp_files_list)
    print(f"-> Total files generated: {len(project_files)}")

    # 5. Agent 4: Exporter
    print("\n[Step 4] Running Agent 4 (Exporter)...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    test_id = "stage1-test-proj"
    res = export_agent.export_project(test_id, project_files, base_dir)

    print(f"-> Project Dir: {res['project_dir']}")
    print(f"-> Zip Filepath: {res['zip_filepath']}")

    # Verify Zip File Exists & Non-Empty
    if os.path.exists(res['zip_filepath']) and os.path.getsize(res['zip_filepath']) > 0:
        print("\nSUCCESS: Stage 1 Pipeline Passed! Website ZIP successfully created!")
        return True
    else:
        print("\nFAILED: Zip file missing or empty!")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_backend_pipeline())
    if not success:
        sys.exit(1)
