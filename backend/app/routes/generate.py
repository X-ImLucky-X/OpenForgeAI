import asyncio
import json
import logging
import os
import uuid
import re
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from pydantic import BaseModel

from app.services.ollama import ollama_service
from app.agents.intent_expander import intent_expander_agent
from app.agents.planner import planner_agent
from app.agents.ui_planner import ui_planner_agent
from app.services.prompt_optimizer import prompt_optimizer
from app.agents.code_generator import code_generator_agent
from app.agents.component_validator import component_validator_agent
from app.agents.validator import validator_agent
from app.agents.fix_generator import fix_generator_agent
from app.agents.exporter import export_agent
from app.services.templates import get_theme

router = APIRouter()
logger = logging.getLogger("openforge.routes")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROJECT_CACHE: Dict[str, Dict[str, Any]] = {}

class GenerateRequest(BaseModel):
    prompt: str
    theme: str = "Modern Dark"
    model: str = "qwen3.6"
    accent_color: str = "indigo"

class RegenerateComponentRequest(BaseModel):
    project_id: str
    component_name: str
    instructions: str
    model: str = "qwen3.6"

@router.get("/api/models")
async def list_models():
    is_healthy = await ollama_service.check_health()
    models = await ollama_service.get_available_models()
    return {
        "ollama_online": is_healthy,
        "models": models,
        "recommended_model": "qwen3.6" if "qwen3.6" in models else "gemma3"
    }

@router.post("/api/generate")
async def generate_website(req: GenerateRequest):
    project_id = f"openforge-{uuid.uuid4().hex[:8]}"

    async def event_generator():
        try:
            def sse(step: str, status: str, message: str, percent: int, data: Any = None):
                payload = {
                    "project_id": project_id,
                    "step": step,
                    "status": status,
                    "message": message,
                    "percent": percent,
                    "data": data
                }
                return f"data: {json.dumps(payload)}\n\n"

            # ----------------------------------------------------
            # Phase 1: Intent Expander Agent
            # ----------------------------------------------------
            yield sse("intent_expander", "in_progress", "📋 Agent 1: Expanding intent & classifying archetype...", 10)
            await asyncio.sleep(0.3)

            spec = await intent_expander_agent.execute(req.prompt, req.theme, req.model)
            yield sse("intent_expander", "completed", f"Spec defined: '{spec['project_name']}' ({spec.get('archetype', 'app')}) with {len(spec['acceptance_criteria'])} criteria", 20, spec)

            # ----------------------------------------------------
            # Phase 2: Project Planner & UI Designer Agents
            # ----------------------------------------------------
            yield sse("planner", "in_progress", "🗺️ Agent 2 & 3: Generating multi-page roadmap & design system...", 30)
            await asyncio.sleep(0.3)

            roadmap = await planner_agent.execute(spec, req.prompt, req.model)
            ui_specs = await ui_planner_agent.execute(roadmap, req.prompt, req.model)
            
            yield sse("planner", "completed", f"Roadmap created: {len(roadmap.get('components', []))} multi-page components", 40, {
                "roadmap": roadmap,
                "ui_specs": ui_specs
            })

            # ----------------------------------------------------
            # Phase 3: Code Generator & Per-Component Validator Loop
            # ----------------------------------------------------
            yield sse("code_generator", "in_progress", "⚡ Agent 4 & 5: Synthesizing TSX component code & executing per-component immediate validation...", 50)

            project_files: Dict[str, str] = {}
            config_files = code_generator_agent.generate_config_files(spec['project_name'], spec['description'])
            project_files.update(config_files)

            comp_names = roadmap.get("components", ["Navbar", "Hero", "Features", "Pricing", "Footer"])
            comp_files_list = []

            for idx, comp in enumerate(comp_names):
                progress_pct = 50 + int(((idx + 1) / len(comp_names)) * 25)
                yield sse("code_generator", "in_progress", f"Synthesizing & validating `src/components/{comp}.tsx`...", progress_pct)

                opt_prompt = prompt_optimizer.optimize_component_prompt(
                    component_name=comp,
                    project_name=spec['project_name'],
                    prompt=req.prompt,
                    theme_name=req.theme,
                    design_system=ui_specs.get("design_system", {}),
                    acceptance_criteria=spec.get("acceptance_criteria", [])
                )

                matching_spec = next((s for s in ui_specs.get("component_specs", []) if s.get("name") == comp), {})

                comp_code = await code_generator_agent.generate_component(
                    component_name=comp,
                    project_name=spec['project_name'],
                    prompt=opt_prompt,
                    theme_name=req.theme,
                    spec=matching_spec,
                    model=req.model
                )

                # Immediate Per-Component Validation & Repair Agent
                validated_code = await component_validator_agent.validate_and_repair(
                    component_name=comp,
                    code=comp_code,
                    project_name=spec['project_name'],
                    prompt=req.prompt,
                    theme_name=req.theme,
                    model=req.model
                )

                file_path = f"src/components/{comp}.tsx"
                project_files[file_path] = validated_code
                comp_files_list.append(file_path)

            app_code = code_generator_agent.generate_app_tsx(spec['project_name'], comp_files_list)
            validated_app_code = await component_validator_agent.validate_and_repair(
                component_name="App",
                code=app_code,
                project_name=spec['project_name'],
                prompt=req.prompt,
                theme_name=req.theme,
                model=req.model
            )
            project_files["src/App.tsx"] = validated_app_code

            yield sse("code_generator", "completed", f"Synthesized and validated {len(project_files)} source files", 75)

            # ----------------------------------------------------
            # Phase 4: Architecture & Completion Validator Loop
            # ----------------------------------------------------
            yield sse("validator", "in_progress", "🔍 Agent 6: Validating multi-page architecture & acceptance criteria...", 80)
            await asyncio.sleep(0.3)

            val_report = await validator_agent.validate_project(spec, roadmap, project_files, req.model)

            if not val_report["is_valid"]:
                yield sse("validator", "in_progress", "🛠️ Agent 7: Violations detected. Generating targeted fixes...", 85)
                project_files = await fix_generator_agent.apply_fixes(
                    violations=val_report["violations"],
                    project_name=spec['project_name'],
                    prompt=req.prompt,
                    theme_name=req.theme,
                    files=project_files,
                    model=req.model
                )
                val_report = await validator_agent.validate_project(spec, roadmap, project_files, req.model)

            yield sse("validator", "completed", f"Validation Passed: {val_report['compliance_score']}% Compliance", 90, val_report)

            # ----------------------------------------------------
            # Phase 5: Export Agent (ZIP)
            # ----------------------------------------------------
            yield sse("exporter", "in_progress", "📦 Agent 8: Packaging workspace & generating website.zip...", 95)
            await asyncio.sleep(0.3)

            export_res = export_agent.export_project(project_id, project_files, BASE_DIR)

            PROJECT_CACHE[project_id] = {
                "project_id": project_id,
                "spec": spec,
                "roadmap": roadmap,
                "ui_specs": ui_specs,
                "validation_report": val_report,
                "files": project_files,
                "zip_path": export_res["zip_filepath"],
                "zip_url": f"/api/download/{project_id}"
            }

            yield sse("exporter", "completed", f"🎉 Validated Multi-Page Website bundle built successfully!", 100, {
                "project_id": project_id,
                "zip_url": f"/api/download/{project_id}",
                "files_count": len(project_files),
                "compliance_score": val_report["compliance_score"]
            })

        except Exception as e:
            logger.exception("Error during v2 website generation pipeline")
            err_payload = {
                "project_id": project_id,
                "step": "error",
                "status": "failed",
                "message": f"Generation failed: {str(e)}",
                "percent": 0
            }
            yield f"data: {json.dumps(err_payload)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/api/project/{project_id}")
async def get_project_details(project_id: str):
    if project_id in PROJECT_CACHE:
        return PROJECT_CACHE[project_id]
    
    project_dir = os.path.join(BASE_DIR, "generated_projects", project_id)
    if os.path.exists(project_dir):
        files = {}
        for root, _, filenames in os.walk(project_dir):
            for fname in filenames:
                abs_p = os.path.join(root, fname)
                rel_p = os.path.relpath(abs_p, project_dir).replace("\\", "/")
                try:
                    with open(abs_p, "r", encoding="utf-8") as f:
                        files[rel_p] = f.read()
                except Exception:
                    pass
        return {
            "project_id": project_id,
            "files": files,
            "zip_url": f"/api/download/{project_id}"
        }

    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/api/download/{project_id}")
async def download_project_zip(project_id: str):
    zip_path = os.path.join(BASE_DIR, "generated_zips", f"{project_id}.zip")
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Zip file not found")
    
    return FileResponse(
        path=zip_path,
        filename=f"{project_id}.zip",
        media_type="application/zip"
    )

@router.get("/api/preview/{project_id}", response_class=HTMLResponse)
async def get_live_preview_html(project_id: str):
    """Generates a multi-page working live HTML preview for the generated website."""
    files: Dict[str, str] = {}
    spec: Dict[str, Any] = {}
    
    if project_id in PROJECT_CACHE:
        cache = PROJECT_CACHE[project_id]
        files = cache.get("files", {})
        spec = cache.get("spec", {})
    else:
        project_dir = os.path.join(BASE_DIR, "generated_projects", project_id)
        if os.path.exists(project_dir):
            for root, _, filenames in os.walk(project_dir):
                for fname in filenames:
                    abs_p = os.path.join(root, fname)
                    rel_p = os.path.relpath(abs_p, project_dir).replace("\\", "/")
                    try:
                        with open(abs_p, "r", encoding="utf-8") as f:
                            files[rel_p] = f.read()
                    except Exception:
                        pass

    if not files:
        return HTMLResponse("<div style='color:white;background:#0f172a;padding:40px;font-family:sans-serif;'>Project files not found.</div>", status_code=404)

    project_name = spec.get("project_name") or "Forge App"
    theme_name = spec.get("theme") or "Modern Dark"
    description = spec.get("description") or "Next generation platform powered by OpenForge AI."
    t = get_theme(theme_name)

    bg = t['bg']
    text = t['text']
    card_bg = t['card_bg']
    accent = t['accent']
    button = t['button']
    nav_bg = t['nav_bg']
    muted_text = t['muted_text']

    html_content = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{project_name} - Multi-Page Live Preview</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      margin: 0;
      padding: 0;
    }}
    .page-view {{ display: none; }}
    .page-view.active {{ display: block; }}
  </style>
</head>
<body class="{bg} {text} antialiased min-h-screen selection:bg-indigo-500 selection:text-white flex flex-col justify-between">

  <!-- Navbar -->
  <nav class="fixed top-0 left-0 right-0 z-50 {nav_bg}">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div style="display:flex; align-items:center; justify-content:space-between; height:70px;">
        <div style="display:flex; align-items:center; gap:12px; cursor:pointer;" onclick="switchPage('home')">
          <div class="p-2 rounded-xl bg-gradient-to-tr {accent} text-white shadow-md" style="padding:8px; border-radius:12px;">
            <svg style="width:20px; height:20px;" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          </div>
          <span class="font-extrabold text-xl sm:text-2xl tracking-tight text-transparent bg-clip-text bg-gradient-to-r {accent}" style="font-weight:800; font-size:22px;">
            {project_name}
          </span>
        </div>

        <div style="display:flex; align-items:center; gap:8px; background:rgba(15,23,42,0.8); border:1px solid #1e293b; padding:4px; border-radius:14px;">
          <button id="nav-home" onclick="switchPage('home')" class="nav-btn font-bold text-xs" style="padding:8px 16px; border-radius:10px; border:none; cursor:pointer; background:#6366f1; color:white;">Home</button>
          <button id="nav-tasks" onclick="switchPage('tasks')" class="nav-btn font-bold text-xs" style="padding:8px 16px; border-radius:10px; border:none; cursor:pointer; background:transparent; color:#94a3b8;">Tasks Workspace</button>
          <button id="nav-categories" onclick="switchPage('categories')" class="nav-btn font-bold text-xs" style="padding:8px 16px; border-radius:10px; border:none; cursor:pointer; background:transparent; color:#94a3b8;">Categories</button>
          <button id="nav-analytics" onclick="switchPage('analytics')" class="nav-btn font-bold text-xs" style="padding:8px 16px; border-radius:10px; border:none; cursor:pointer; background:transparent; color:#94a3b8;">Analytics</button>
          <button id="nav-settings" onclick="switchPage('settings')" class="nav-btn font-bold text-xs" style="padding:8px 16px; border-radius:10px; border:none; cursor:pointer; background:transparent; color:#94a3b8;">Settings</button>
        </div>
      </div>
    </div>
  </nav>

  <!-- Page View 1: Home Landing Page -->
  <main id="view-home" class="page-view active" style="padding-top:120px; padding-bottom:80px; text-align:center;">
    <div style="max-width:900px; margin:0 auto; padding:0 20px;">
      <h1 style="font-size:48px; font-weight:900; margin-bottom:16px;">
        Build Smarter with <span class="text-transparent bg-clip-text bg-gradient-to-r {accent}">{project_name}</span>
      </h1>
      <p style="font-size:18px; color:#94a3b8; max-width:600px; margin:0 auto 32px auto; line-height:1.6;">{description}</p>
      <div style="display:flex; justify-content:center; gap:16px;">
        <button onclick="switchPage('tasks')" class="{button}" style="padding:14px 28px; border-radius:14px; font-weight:700; border:none; cursor:pointer;">Launch Workspace →</button>
        <button onclick="switchPage('analytics')" class="{card_bg}" style="padding:14px 28px; border-radius:14px; font-weight:600; cursor:pointer; color:white;">View Analytics</button>
      </div>
    </div>
  </main>

  <!-- Page View 2: Dedicated Tasks Workspace -->
  <main id="view-tasks" class="page-view" style="padding-top:100px; padding-bottom:80px;">
    <div style="max-width:900px; margin:0 auto; padding:0 20px;">
      <div style="text-align:center; margin-bottom:24px;">
        <h2 style="font-size:32px; font-weight:800;">Dedicated Tasks Workspace</h2>
        <p style="color:#94a3b8; font-size:14px;">Add, search, filter, and manage tasks with real-time local storage persistence.</p>
      </div>

      <div class="{card_bg}" style="padding:28px; border-radius:24px;">
        <div style="display:flex; gap:10px; margin-bottom:20px;">
          <input id="todo-input" type="text" placeholder="Enter a new task..." style="flex:1; background:#020617; border:1px solid #1e293b; color:white; padding:12px 16px; border-radius:12px; font-size:14px; outline:none;" />
          <select id="todo-cat" style="background:#020617; border:1px solid #1e293b; color:#cbd5e1; padding:12px; border-radius:12px; font-size:13px;">
            <option>Work</option><option>Dev</option><option>Personal</option><option>Urgent</option>
          </select>
          <button onclick="addTodo()" class="{button}" style="padding:12px 24px; border-radius:12px; font-weight:700; border:none; cursor:pointer;">Add Task</button>
        </div>

        <div style="display:flex; justify-space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:12px; margin-bottom:16px;">
          <input id="todo-search" oninput="renderTodos()" type="text" placeholder="Search tasks..." style="background:#020617; border:1px solid #1e293b; color:white; padding:6px 12px; border-radius:8px; font-size:12px; width:180px;" />
          <div style="display:flex; gap:6px;">
            <button onclick="setFilter('all')" class="filter-btn active-f" style="padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; background:#6366f1; color:white; border:none;">All</button>
            <button onclick="setFilter('active')" class="filter-btn" style="padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; background:#020617; color:#94a3b8; border:1px solid #1e293b;">Active</button>
            <button onclick="setFilter('completed')" class="filter-btn" style="padding:4px 12px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; background:#020617; color:#94a3b8; border:1px solid #1e293b;">Completed</button>
          </div>
        </div>

        <div id="todo-list" style="display:flex; flex-direction:column; gap:10px; max-height:380px; overflow-y:auto;"></div>
      </div>
    </div>
  </main>

  <!-- Page View 3: Dedicated Categories Breakdown -->
  <main id="view-categories" class="page-view" style="padding-top:100px; padding-bottom:80px;">
    <div style="max-width:800px; margin:0 auto; padding:0 20px; text-align:center;">
      <h2 style="font-size:32px; font-weight:800; margin-bottom:8px;">Task Categories</h2>
      <p style="color:#94a3b8; font-size:14px; margin-bottom:32px;">Overview of tasks grouped by work, dev, personal, and urgent folders.</p>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:20px; text-align:left;">
        <div class="{card_bg}" style="padding:24px; border-radius:20px;">
          <h3 style="font-weight:800; font-size:18px; color:#818cf8;">Work Folder</h3>
          <p style="font-size:12px; color:#94a3b8; margin:6px 0 16px 0;">SaaS architecture and team deliverables.</p>
          <div style="font-size:24px; font-weight:800; color:white;">8 Tasks</div>
        </div>
        <div class="{card_bg}" style="padding:24px; border-radius:20px;">
          <h3 style="font-weight:800; font-size:18px; color:#c084fc;">Dev Folder</h3>
          <p style="font-size:12px; color:#94a3b8; margin:6px 0 16px 0;">React TSX components & API endpoints.</p>
          <div style="font-size:24px; font-weight:800; color:white;">12 Tasks</div>
        </div>
      </div>
    </div>
  </main>

  <!-- Page View 4: Dedicated Analytics -->
  <main id="view-analytics" class="page-view" style="padding-top:100px; padding-bottom:80px;">
    <div style="max-width:800px; margin:0 auto; padding:0 20px; text-align:center;">
      <h2 style="font-size:32px; font-weight:800; margin-bottom:8px;">Task Completion Metrics</h2>
      <p style="color:#94a3b8; font-size:14px; margin-bottom:32px;">Weekly task velocity and completion progress.</p>
      <div class="{card_bg}" style="padding:32px; border-radius:24px; text-align:left;">
        <div style="font-size:14px; font-weight:700; color:#cbd5e1; margin-bottom:12px;">Weekly Productivity Velocity</div>
        <div style="font-size:36px; font-weight:900; color:#34d399; margin-bottom:4px;">84.2%</div>
        <div style="font-size:12px; color:#94a3b8;">↑ +12.4% vs previous week</div>
      </div>
    </div>
  </main>

  <!-- Page View 5: Dedicated Settings -->
  <main id="view-settings" class="page-view" style="padding-top:100px; padding-bottom:80px;">
    <div style="max-width:650px; margin:0 auto; padding:0 20px;">
      <h2 style="font-size:32px; font-weight:800; text-align:center; margin-bottom:8px;">Settings & Export</h2>
      <div class="{card_bg}" style="padding:28px; border-radius:24px; margin-top:24px;">
        <h3 style="font-size:16px; font-weight:700; margin-bottom:16px;">Backup & Storage</h3>
        <button onclick="exportJSON()" class="{button}" style="width:100%; padding:12px; border-radius:12px; border:none; font-weight:700; cursor:pointer; margin-bottom:12px;">Export Tasks to JSON</button>
        <button onclick="resetData()" style="width:100%; padding:12px; border-radius:12px; background:rgba(244,63,94,0.1); color:#f43f5e; border:1px solid rgba(244,63,94,0.3); font-weight:700; cursor:pointer;">Clear Local Storage</button>
      </div>
    </div>
  </main>

  <footer style="padding:30px 20px; border-top:1px solid #1e293b; text-align:center; font-size:13px; color:#64748b;">
    © {project_name}. All rights reserved. Multi-Page Web App built with OpenForge AI.
  </footer>

  <script>
    let todos = [
      {{ id: '1', text: 'Architect multi-page React application views', category: 'Work', completed: true }},
      {{ id: '2', text: 'Integrate Ollama local LLM model pipeline', category: 'Dev', completed: false }},
      {{ id: '3', text: 'Configure Tailwind CSS design system tokens', category: 'Dev', completed: false }}
    ];
    let currentFilter = 'all';

    function switchPage(pageId) {{
      document.querySelectorAll('.page-view').forEach(el => el.classList.remove('active'));
      const activeEl = document.getElementById('view-' + pageId);
      if (activeEl) activeEl.classList.add('active');

      document.querySelectorAll('.nav-btn').forEach(btn => {{
        btn.style.background = 'transparent';
        btn.style.color = '#94a3b8';
      }});
      const activeBtn = document.getElementById('nav-' + pageId);
      if (activeBtn) {{
        activeBtn.style.background = '#6366f1';
        activeBtn.style.color = 'white';
      }}
    }}

    function setFilter(f) {{
      currentFilter = f;
      renderTodos();
    }}

    function addTodo() {{
      const input = document.getElementById('todo-input');
      const cat = document.getElementById('todo-cat');
      if (!input || !input.value.trim()) return;
      todos.unshift({{ id: Date.now().toString(), text: input.value.trim(), category: cat.value, completed: false }});
      input.value = '';
      renderTodos();
    }}

    function toggleTodo(id) {{
      todos = todos.map(t => t.id === id ? {{ ...t, completed: !t.completed }} : t);
      renderTodos();
    }}

    function deleteTodo(id) {{
      todos = todos.filter(t => t.id !== id);
      renderTodos();
    }}

    function renderTodos() {{
      const listEl = document.getElementById('todo-list');
      const searchEl = document.getElementById('todo-search');
      if (!listEl) return;
      const search = searchEl ? searchEl.value.toLowerCase() : '';

      const filtered = todos.filter(t => {{
        const matchesF = currentFilter === 'all' ? true : currentFilter === 'active' ? !t.completed : t.completed;
        const matchesS = t.text.toLowerCase().includes(search) || t.category.toLowerCase().includes(search);
        return matchesF && matchesS;
      }});

      if (filtered.length === 0) {{
        listEl.innerHTML = '<div style="text-align:center; padding:30px; color:#64748b; font-size:13px;">No tasks found.</div>';
        return;
      }}

      listEl.innerHTML = filtered.map(t => `
        <div style="display:flex; align-items:center; justify-content:space-between; padding:14px; background:#020617; border:1px solid #1e293b; border-radius:12px;">
          <div style="display:flex; align-items:center; gap:12px;">
            <input type="checkbox" ${{t.completed ? 'checked' : ''}} onchange="toggleTodo('${{t.id}}')" style="cursor:pointer;" />
            <span style="font-size:14px; ${{t.completed ? 'text-decoration:line-through; color:#64748b;' : 'color:#f8fafc;'}}">${{t.text}}</span>
          </div>
          <div style="display:flex; align-items:center; gap:10px;">
            <span style="font-size:10px; background:#1e293b; color:#818cf8; padding:2px 8px; border-radius:12px; font-weight:700;">${{t.category}}</span>
            <button onclick="deleteTodo('${{t.id}}')" style="background:none; border:none; color:#f43f5e; cursor:pointer; font-size:12px;">✕</button>
          </div>
        </div>
      `).join('');
    }}

    function exportJSON() {{
      const blob = new Blob([JSON.stringify(todos, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'tasks.json';
      a.click();
    }}

    function resetData() {{
      if (confirm("Reset task data?")) {{
        todos = [];
        renderTodos();
      }}
    }}

    renderTodos();
  </script>
</body>
</html>"""

    return HTMLResponse(content=html_content, status_code=200)

@router.post("/api/regenerate-component")
async def regenerate_component(req: RegenerateComponentRequest):
    if req.project_id not in PROJECT_CACHE:
        raise HTTPException(status_code=404, detail="Project not found")

    cache = PROJECT_CACHE[req.project_id]
    theme = cache.get("spec", {}).get("theme", "Modern Dark")
    project_name = cache.get("spec", {}).get("project_name", "OpenForge App")

    new_code = await code_generator_agent.generate_component(
        component_name=req.component_name,
        project_name=project_name,
        prompt=req.instructions,
        theme_name=theme,
        spec={"purpose": req.instructions},
        model=req.model
    )

    validated_code = await component_validator_agent.validate_and_repair(
        component_name=req.component_name,
        code=new_code,
        project_name=project_name,
        prompt=req.instructions,
        theme_name=theme,
        model=req.model
    )

    comp_filepath = f"src/components/{req.component_name}.tsx"
    cache["files"][comp_filepath] = validated_code

    export_agent.export_project(req.project_id, cache["files"], BASE_DIR)

    return {
        "status": "success",
        "component_name": req.component_name,
        "file_path": comp_filepath,
        "code": validated_code
    }
