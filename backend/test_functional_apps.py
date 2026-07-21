import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.agents.intent_expander import intent_expander_agent
from app.agents.planner import planner_agent
from app.agents.code_generator import code_generator_agent
from app.agents.exporter import export_agent

async def test_todo_functional_app():
    print("==========================================")
    print("Testing Functional Todo App Generation...")
    print("==========================================")

    # 1. Intent Expander
    print("[1] Intent Expander Archetype Detection...")
    spec = await intent_expander_agent.execute("Build a Todo App with dark mode and search", "Modern Dark", "qwen3.6")
    print(f" -> Archetype: {spec.get('archetype')}")
    print(f" -> Pages: {spec.get('pages')}")

    # 2. Roadmap Planner
    print("\n[2] Roadmap Planner Components...")
    roadmap = await planner_agent.execute(spec, "Build a Todo App", "qwen3.6")
    print(f" -> Components: {roadmap['components']}")

    # 3. Code Generation
    print("\n[3] Synthesizing Component Files...")
    config_files = code_generator_agent.generate_config_files(spec['project_name'], spec['description'])
    project_files = dict(config_files)
    comp_files_list = []

    for comp in roadmap['components']:
        print(f"   -> Generating src/components/{comp}.tsx...")
        comp_code = await code_generator_agent.generate_component(
            component_name=comp,
            project_name=spec['project_name'],
            prompt="Build a Todo App with dark mode and search",
            theme_name="Modern Dark",
            spec={"purpose": f"Working {comp} component"},
            model="qwen3.6"
        )
        file_path = f"src/components/{comp}.tsx"
        project_files[file_path] = comp_code
        comp_files_list.append(file_path)

    project_files["src/App.tsx"] = code_generator_agent.generate_app_tsx(spec['project_name'], comp_files_list)

    # Verify TodoApp.tsx contains working state
    todo_code = project_files.get("src/components/TodoApp.tsx", "")
    has_state = "useState" in todo_code and ("handleAddTodo" in todo_code or "toggleComplete" in todo_code or "todos" in todo_code)
    has_localstorage = "localStorage" in todo_code

    print(f"\n[Verification] TodoApp Has Interactive State: {has_state}")
    print(f"[Verification] TodoApp Has LocalStorage Persistence: {has_localstorage}")

    # 4. Exporter
    base_dir = os.path.dirname(os.path.abspath(__file__))
    res = export_agent.export_project("functional-todo-test", project_files, base_dir)
    print(f" -> Exported Zip: {res['zip_filepath']}")

    if has_state and os.path.exists(res['zip_filepath']):
        print("\nSUCCESS: Functional Todo App Generation Test Passed!")
        return True
    else:
        print("\nFAILED: Missing interactive state in TodoApp!")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_todo_functional_app())
    if not success:
        sys.exit(1)
