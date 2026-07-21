"""
OpenForge AI - Core React Component & Multi-Page View Templates
Generates production-grade, state-managed React + Vite + Tailwind CSS + Lucide React code.
"""

import json
from typing import Dict, Any, List

THEMES = {
    "Modern Dark": {
        "bg": "bg-slate-950",
        "text": "text-slate-100",
        "card_bg": "bg-slate-900/80 border border-slate-800",
        "accent": "from-indigo-500 to-purple-600",
        "button": "bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white shadow-lg shadow-indigo-500/25",
        "nav_bg": "bg-slate-950/80 backdrop-blur-md border-b border-slate-800",
        "muted_text": "text-slate-400"
    },
    "Minimal Light": {
        "bg": "bg-gray-50",
        "text": "text-gray-900",
        "card_bg": "bg-white border border-gray-200 shadow-sm",
        "accent": "from-blue-600 to-indigo-600",
        "button": "bg-black hover:bg-gray-800 text-white shadow-md",
        "nav_bg": "bg-white/80 backdrop-blur-md border-b border-gray-200",
        "muted_text": "text-gray-600"
    },
    "Cyberpunk Neon": {
        "bg": "bg-zinc-950",
        "text": "text-zinc-100",
        "card_bg": "bg-zinc-900/90 border border-cyan-500/30 shadow-lg shadow-cyan-500/10",
        "accent": "from-cyan-400 to-fuchsia-500",
        "button": "bg-gradient-to-r from-cyan-500 to-fuchsia-500 hover:from-cyan-400 hover:to-fuchsia-400 text-black font-bold shadow-lg shadow-cyan-500/30",
        "nav_bg": "bg-zinc-950/90 backdrop-blur-md border-b border-cyan-500/30",
        "muted_text": "text-zinc-400"
    },
    "Glassmorphism": {
        "bg": "bg-gradient-to-br from-slate-900 via-purple-950 to-indigo-950",
        "text": "text-white",
        "card_bg": "bg-white/10 backdrop-blur-lg border border-white/20 shadow-2xl",
        "accent": "from-purple-400 to-pink-400",
        "button": "bg-white/20 hover:bg-white/30 backdrop-blur-md border border-white/30 text-white font-medium shadow-lg",
        "nav_bg": "bg-white/5 backdrop-blur-xl border-b border-white/10",
        "muted_text": "text-purple-200"
    },
    "Sunset Vibrant": {
        "bg": "bg-slate-950",
        "text": "text-slate-50",
        "card_bg": "bg-slate-900/90 border border-amber-500/20",
        "accent": "from-amber-500 via-rose-500 to-purple-600",
        "button": "bg-gradient-to-r from-amber-500 to-rose-600 hover:from-amber-600 hover:to-rose-700 text-white shadow-lg shadow-rose-500/25",
        "nav_bg": "bg-slate-950/80 backdrop-blur-md border-b border-slate-800",
        "muted_text": "text-slate-400"
    }
}

def get_theme(theme_name: str) -> Dict[str, str]:
    return THEMES.get(theme_name, THEMES["Modern Dark"])

def generate_vite_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--logos" width="31.88" height="32" viewBox="0 0 256 257"><path fill="#41D1FF" d="M255.153 37.938L134.897 252.976c-2.483 4.44-8.862 4.466-11.382.048L.875 37.958c-2.746-4.814 1.371-10.646 6.827-9.67l120.385 21.517a6.537 6.537 0 0 0 2.322-.004l117.867-21.483c5.438-.991 9.574 4.796 6.877 9.62z"></path><path fill="#BD34FE" d="M185.432.128L128.708 101.47a5.534 5.534 0 0 1-9.646.046L63.504.184c-3.15-5.632-11.517-4.321-12.825 2.012L.875 37.958c-2.746-4.814 1.371-10.646 6.827-9.67l120.385 21.517a6.537 6.537 0 0 0 2.322-.004l117.867-21.483c5.438-.991 9.574 4.796 6.877 9.62L198.24 2.181C196.945-4.148 188.583-5.497 185.432.128z"></path></svg>"""

def generate_package_json(project_name: str) -> str:
    slug = project_name.lower().replace(" ", "-")
    return f"""{{
  "name": "{slug}",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.344.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.1"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.66",
    "@types/react-dom": "^18.2.22",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.18",
    "postcss": "^8.4.35",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.2.2",
    "vite": "^5.1.6"
  }}
}}"""

def generate_tailwind_config() -> str:
    return """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          500: '#06b6d4',
          600: '#0284c7',
          700: '#0369a1',
        }
      }
    },
  },
  plugins: [],
}"""

def generate_vite_config() -> str:
    return """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})"""

def generate_postcss_config() -> str:
    return """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}"""

def generate_index_html(title: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  </head>
  <body class="font-['Plus_Jakarta_Sans',sans-serif] antialiased">
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>"""

def generate_index_css() -> str:
    return """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-slate-950 text-slate-100 min-h-screen selection:bg-indigo-500 selection:text-white;
  }
}
"""

def generate_readme(project_name: str, description: str) -> str:
    return f"""# {project_name}

{description}

Generated with ❤️ by **OpenForge AI** (Local AI SaaS Website Builder).

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the local development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## 🛠️ Stack
- **Framework**: React 18 + Vite + TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
"""

def generate_navbar_component(project_name: str, theme_name: str, pages: List[str] = None) -> str:
    t = get_theme(theme_name)
    pages_list = pages or ["Home", "Tasks", "Categories", "Analytics", "Settings"]

    code = """import React, { useState } from 'react';
import { Sparkles, Menu, X, ArrowRight } from 'lucide-react';

interface NavbarProps {
  activeTab?: string;
  onSelectTab?: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab = "Home", onSelectTab }) => {
  const [isOpen, setIsOpen] = useState(false);

  const tabs = __PAGES_JSON__;

  const handleTabClick = (tName: string) => {
    if (onSelectTab) onSelectTab(tName);
    setIsOpen(false);
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 __NAV_BG__">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => handleTabClick("Home")}>
            <div className="p-2 rounded-xl bg-gradient-to-tr __ACCENT__ text-white shadow-md">
              <Sparkles className="w-5 h-5" />
            </div>
            <span className="font-extrabold text-xl sm:text-2xl tracking-tight text-transparent bg-clip-text bg-gradient-to-r __ACCENT__">
              __PROJECT_NAME__
            </span>
          </div>

          <div className="hidden md:flex items-center gap-2 bg-slate-900/90 border border-slate-800 rounded-2xl p-1.5 shadow-inner">
            {tabs.map((tab) => (
              <button
                key={tab}
                onClick={() => handleTabClick(tab)}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  activeTab === tab
                    ? 'bg-gradient-to-r __ACCENT__ text-white shadow-md scale-105'
                    : '__MUTED_TEXT__ hover:__TEXT__ hover:bg-slate-800/60'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="hidden md:flex items-center gap-4">
            <button 
              onClick={() => handleTabClick("Tasks")}
              className="px-5 py-2.5 text-xs rounded-xl font-extrabold __BUTTON__ flex items-center gap-2 transition-all shadow-lg"
            >
              Launch Workspace <ArrowRight className="w-4 h-4" />
            </button>
          </div>

          <div className="md:hidden">
            <button onClick={() => setIsOpen(!isOpen)} className="p-2 rounded-lg __MUTED_TEXT__ hover:__TEXT__">
              {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden px-4 pt-2 pb-6 space-y-2 __CARD_BG__ border-b">
          {tabs.map((tab) => (
            <button
              key={tab}
              onClick={() => handleTabClick(tab)}
              className={`block w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold ${
                activeTab === tab ? 'bg-gradient-to-r __ACCENT__ text-white' : '__MUTED_TEXT__'
              }`}
            >
              {tab}
            </button>
          ))}
          <div className="pt-4 border-t border-slate-800">
            <button 
              onClick={() => handleTabClick("Tasks")}
              className="w-full py-3 text-center text-xs rounded-xl font-bold __BUTTON__"
            >
              Launch Workspace
            </button>
          </div>
        </div>
      )}
    </nav>
  );
};
"""
    return (code
        .replace("__PROJECT_NAME__", project_name)
        .replace("__PAGES_JSON__", json.dumps(pages_list))
        .replace("__NAV_BG__", t['nav_bg'])
        .replace("__ACCENT__", t['accent'])
        .replace("__BUTTON__", t['button'])
        .replace("__TEXT__", t['text'])
        .replace("__CARD_BG__", t['card_bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_todo_workspace(project_name: str, theme_name: str) -> str:
    """Dedicated 'Tasks' Workspace View Component."""
    t = get_theme(theme_name)
    code = """import React, { useState, useEffect } from 'react';
import { Plus, Trash2, CheckCircle2, Circle, Search, Filter, Sparkles, Folder, Layers, CheckSquare } from 'lucide-react';

interface Todo {
  id: string;
  text: string;
  category: string;
  completed: boolean;
  createdAt: string;
}

export const TodoWorkspace: React.FC = () => {
  const [todos, setTodos] = useState<Todo[]>(() => {
    try {
      const saved = localStorage.getItem('openforge_todos');
      return saved ? JSON.parse(saved) : [
        { id: '1', text: 'Architect multi-page React application views', category: 'Work', completed: true, createdAt: 'Today' },
        { id: '2', text: 'Integrate Ollama local LLM model pipeline', category: 'Dev', completed: false, createdAt: 'Today' },
        { id: '3', text: 'Configure Tailwind CSS design system tokens', category: 'Dev', completed: false, createdAt: 'Yesterday' }
      ];
    } catch {
      return [];
    }
  });

  const [newText, setNewText] = useState('');
  const [newCategory, setNewCategory] = useState('Work');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [selectedCat, setSelectedCat] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    localStorage.setItem('openforge_todos', JSON.stringify(todos));
  }, [todos]);

  const handleAddTodo = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newText.trim()) return;

    const newTodo: Todo = {
      id: Date.now().toString(),
      text: newText.trim(),
      category: newCategory,
      completed: false,
      createdAt: 'Just now'
    };

    setTodos([newTodo, ...todos]);
    setNewText('');
  };

  const toggleComplete = (id: string) => {
    setTodos(todos.map(t => t.id === id ? { ...t, completed: !t.completed } : t));
  };

  const deleteTodo = (id: string) => {
    setTodos(todos.filter(t => t.id !== id));
  };

  const filteredTodos = todos.filter(t => {
    const matchesFilter = filter === 'all' ? true : filter === 'active' ? !t.completed : t.completed;
    const matchesCat = selectedCat === 'All' ? true : t.category === selectedCat;
    const matchesSearch = t.text.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesCat && matchesSearch;
  });

  const categories = ['All', 'Work', 'Dev', 'Personal', 'Urgent'];

  return (
    <div className="pt-24 pb-16 min-h-screen __BG__">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-start justify-between gap-6 mb-8">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full __CARD_BG__ text-xs font-bold text-indigo-400 mb-3">
              <CheckSquare className="w-3.5 h-3.5" />
              <span>Dedicated Tasks Workspace</span>
            </div>
            <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight __TEXT__">
              Task Management Workspace
            </h1>
            <p className="text-sm __MUTED_TEXT__ mt-1">
              Full-featured task workspace with real-time browser storage persistence.
            </p>
          </div>

          {/* Stat Pills */}
          <div className="flex items-center gap-3">
            <div className="px-4 py-2.5 rounded-2xl __CARD_BG__ text-center min-w-[100px]">
              <div className="text-xs text-slate-500 font-bold uppercase">Total</div>
              <div className="text-xl font-extrabold text-white">{todos.length}</div>
            </div>
            <div className="px-4 py-2.5 rounded-2xl __CARD_BG__ text-center min-w-[100px]">
              <div className="text-xs text-slate-500 font-bold uppercase">Active</div>
              <div className="text-xl font-extrabold text-indigo-400">{todos.filter(t => !t.completed).length}</div>
            </div>
            <div className="px-4 py-2.5 rounded-2xl __CARD_BG__ text-center min-w-[100px]">
              <div className="text-xs text-slate-500 font-bold uppercase">Done</div>
              <div className="text-xl font-extrabold text-emerald-400">{todos.filter(t => t.completed).length}</div>
            </div>
          </div>
        </div>

        {/* Main Grid Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Filters */}
          <div className="space-y-6">
            <div className="__CARD_BG__ rounded-3xl p-6 space-y-4">
              <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <Folder className="w-4 h-4 text-indigo-400" />
                Categories
              </h3>
              <div className="space-y-1">
                {categories.map((cat) => {
                  const count = cat === 'All' ? todos.length : todos.filter(t => t.category === cat).length;
                  return (
                    <button
                      key={cat}
                      onClick={() => setSelectedCat(cat)}
                      className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                        selectedCat === cat
                          ? 'bg-gradient-to-r __ACCENT__ text-white shadow-md'
                          : '__MUTED_TEXT__ hover:bg-slate-800/60 hover:text-white'
                      }`}
                    >
                      <span>{cat}</span>
                      <span className="px-2 py-0.5 rounded-full bg-slate-950/60 text-[10px] font-bold">
                        {count}
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Workspace Task List Area */}
          <div className="lg:col-span-3 space-y-6">
            {/* Task Input Card */}
            <form onSubmit={handleAddTodo} className="__CARD_BG__ rounded-3xl p-4 sm:p-6 flex flex-col sm:flex-row gap-3">
              <input
                type="text"
                value={newText}
                onChange={(e) => setNewText(e.target.value)}
                placeholder="Add a new task to your workspace..."
                className="flex-1 bg-slate-950 border border-slate-800 rounded-2xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
              <select
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
                className="bg-slate-950 border border-slate-800 rounded-2xl px-4 py-3 text-xs text-slate-300 font-bold focus:outline-none"
              >
                <option value="Work">Work</option>
                <option value="Dev">Dev</option>
                <option value="Personal">Personal</option>
                <option value="Urgent">Urgent</option>
              </select>
              <button
                type="submit"
                disabled={!newText.trim()}
                className="px-6 py-3 rounded-2xl __BUTTON__ font-extrabold text-sm flex items-center justify-center gap-2 disabled:opacity-50 transition-all shrink-0"
              >
                <Plus className="w-4 h-4" />
                <span>Add Task</span>
              </button>
            </form>

            {/* Filter & Search Bar */}
            <div className="__CARD_BG__ rounded-3xl p-4 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="relative w-full sm:w-72">
                <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Filter workspace tasks..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex items-center gap-1.5 bg-slate-950 border border-slate-800 rounded-xl p-1">
                {(['all', 'active', 'completed'] as const).map((f) => (
                  <button
                    key={f}
                    onClick={() => setFilter(f)}
                    className={`px-4 py-1.5 rounded-lg text-xs font-bold capitalize transition-colors ${
                      filter === f ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-white'
                    }`}
                  >
                    {f}
                  </button>
                ))}
              </div>
            </div>

            {/* Task Item Cards */}
            <div className="space-y-3">
              {filteredTodos.length === 0 ? (
                <div className="__CARD_BG__ rounded-3xl p-12 text-center text-slate-500 text-xs italic">
                  No tasks matching your current view or filter. Add a task above!
                </div>
              ) : (
                filteredTodos.map((todo) => (
                  <div
                    key={todo.id}
                    className={`__CARD_BG__ rounded-2xl p-4 flex items-center justify-between gap-4 transition-all hover:border-slate-700 ${
                      todo.completed ? 'opacity-50' : ''
                    }`}
                  >
                    <div className="flex items-center gap-3.5 flex-1 min-w-0">
                      <button onClick={() => toggleComplete(todo.id)} className="text-indigo-400 shrink-0">
                        {todo.completed ? <CheckCircle2 className="w-5 h-5 text-emerald-400" /> : <Circle className="w-5 h-5 text-slate-500" />}
                      </button>
                      <span className={`text-sm ${todo.completed ? 'line-through text-slate-500' : 'text-white font-medium'}`}>
                        {todo.text}
                      </span>
                    </div>

                    <div className="flex items-center gap-3 shrink-0">
                      <span className="px-3 py-1 rounded-full bg-slate-950 border border-slate-800 text-[10px] font-bold text-indigo-300">
                        {todo.category}
                      </span>
                      <button onClick={() => deleteTodo(todo.id)} className="text-slate-500 hover:text-rose-400 transition-colors p-1">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
"""
    return (code
        .replace("__BG__", t['bg'])
        .replace("__BUTTON__", t['button'])
        .replace("__TEXT__", t['text'])
        .replace("__ACCENT__", t['accent'])
        .replace("__CARD_BG__", t['card_bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_category_view(project_name: str, theme_name: str) -> str:
    """Dedicated 'Categories' Page Component."""
    t = get_theme(theme_name)
    code = """import React from 'react';
import { Folder, Layers, CheckCircle2, AlertCircle, Sparkles } from 'lucide-react';

export const CategoryView: React.FC = () => {
  const categoryStats = [
    { name: "Work", count: 8, completed: 5, color: "from-blue-500 to-indigo-600", desc: "Core SaaS architecture and team assignments" },
    { name: "Dev", count: 12, completed: 9, color: "from-purple-500 to-pink-600", desc: "React components, API routes, and state storage" },
    { name: "Personal", count: 4, completed: 2, color: "from-emerald-500 to-teal-600", desc: "Personal goals and learning schedule" },
    { name: "Urgent", count: 3, completed: 1, color: "from-rose-500 to-amber-600", desc: "High priority bug fixes and release blockers" }
  ];

  return (
    <div className="pt-24 pb-16 min-h-screen __BG__">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-10 text-center max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full __CARD_BG__ text-xs font-bold text-indigo-400 mb-3">
            <Folder className="w-3.5 h-3.5" />
            <span>Category Breakdown View</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight __TEXT__">
            Task Categories & Folders
          </h1>
          <p className="text-sm __MUTED_TEXT__ mt-1">
            Organize your tasks into structured projects and monitor completion rates by category.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {categoryStats.map((c, idx) => {
            const pct = Math.round((c.completed / c.count) * 100);
            return (
              <div key={idx} className="__CARD_BG__ rounded-3xl p-8 space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-2xl bg-gradient-to-tr ${c.color} flex items-center justify-center text-white font-bold shadow-md`}>
                      <Folder className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold __TEXT__">{c.name}</h3>
                      <p className="text-xs __MUTED_TEXT__">{c.desc}</p>
                    </div>
                  </div>
                  <span className="text-2xl font-extrabold __TEXT__">{pct}%</span>
                </div>

                {/* Progress bar */}
                <div className="w-full h-3 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                  <div 
                    className={`h-full bg-gradient-to-r ${c.color} transition-all duration-500`}
                    style={{ width: `${pct}%` }}
                  />
                </div>

                <div className="flex items-center justify-between text-xs __MUTED_TEXT__ font-medium pt-2 border-t border-slate-800/80">
                  <span className="flex items-center gap-1.5 text-emerald-400">
                    <CheckCircle2 className="w-4 h-4" /> {c.completed} Completed
                  </span>
                  <span>{c.count - c.completed} Pending Tasks</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
"""
    return (code
        .replace("__BG__", t['bg'])
        .replace("__TEXT__", t['text'])
        .replace("__CARD_BG__", t['card_bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_analytics_view(project_name: str, theme_name: str) -> str:
    """Dedicated 'Analytics' Page Component."""
    t = get_theme(theme_name)
    code = """import React from 'react';
import { BarChart2, TrendingUp, CheckCircle2, Clock, Zap } from 'lucide-react';

export const AnalyticsView: React.FC = () => {
  return (
    <div className="pt-24 pb-16 min-h-screen __BG__">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-10 text-center max-w-2xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full __CARD_BG__ text-xs font-bold text-indigo-400 mb-3">
            <BarChart2 className="w-3.5 h-3.5" />
            <span>Productivity Metrics</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight __TEXT__">
            Task Analytics & Productivity
          </h1>
          <p className="text-sm __MUTED_TEXT__ mt-1">
            Track weekly task completion rates, velocity, and focus hours.
          </p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-10">
          <div className="__CARD_BG__ rounded-3xl p-6">
            <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase mb-2">
              <span>Weekly Completion</span>
              <TrendingUp className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-3xl font-extrabold __TEXT__">84.2%</div>
            <div className="text-xs text-emerald-400 mt-2 font-semibold">↑ +12.4% vs last week</div>
          </div>

          <div className="__CARD_BG__ rounded-3xl p-6">
            <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase mb-2">
              <span>Avg Task Velocity</span>
              <Clock className="w-4 h-4 text-indigo-400" />
            </div>
            <div className="text-3xl font-extrabold __TEXT__">2.4 hrs</div>
            <div className="text-xs text-indigo-400 mt-2 font-semibold">⚡ Fast resolution time</div>
          </div>

          <div className="__CARD_BG__ rounded-3xl p-6">
            <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase mb-2">
              <span>Completed Tasks</span>
              <CheckCircle2 className="w-4 h-4 text-purple-400" />
            </div>
            <div className="text-3xl font-extrabold __TEXT__">142</div>
            <div className="text-xs text-purple-400 mt-2 font-semibold">This month total</div>
          </div>

          <div className="__CARD_BG__ rounded-3xl p-6">
            <div className="flex items-center justify-between text-slate-400 text-xs font-bold uppercase mb-2">
              <span>Streak Record</span>
              <Zap className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-3xl font-extrabold __TEXT__">14 Days</div>
            <div className="text-xs text-amber-400 mt-2 font-semibold">🔥 Active productivity streak</div>
          </div>
        </div>

        {/* Productivity Activity Table */}
        <div className="__CARD_BG__ rounded-3xl p-8">
          <h3 className="text-lg font-bold __TEXT__ mb-6">Recent Task Activity Log</h3>
          <div className="space-y-4">
            {[
              { task: "Integrated Ollama local LLM model API", category: "Dev", time: "10 mins ago", status: "Completed" },
              { task: "Designed dedicated multi-page component router", category: "Architecture", time: "1 hr ago", status: "Completed" },
              { task: "Configured Tailwind CSS glassmorphism themes", category: "UI/UX", time: "3 hrs ago", status: "Completed" },
              { task: "Set up browser local storage task persistence", category: "Dev", time: "Yesterday", status: "Completed" }
            ].map((log, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 rounded-2xl bg-slate-950/60 border border-slate-800 text-xs">
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span className="font-semibold text-white">{log.task}</span>
                </div>
                <div className="flex items-center gap-4 text-slate-400">
                  <span className="px-2.5 py-0.5 rounded-full bg-slate-900 border border-slate-800 text-[10px] font-bold text-indigo-300">{log.category}</span>
                  <span>{log.time}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
"""
    return (code
        .replace("__BG__", t['bg'])
        .replace("__TEXT__", t['text'])
        .replace("__CARD_BG__", t['card_bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_settings_view(project_name: str, theme_name: str) -> str:
    """Dedicated 'Settings' Page Component."""
    t = get_theme(theme_name)
    code = """import React, { useState } from 'react';
import { Settings, Download, Trash2, Moon, Shield, RefreshCw } from 'lucide-react';

export const SettingsView: React.FC = () => {
  const [theme, setTheme] = useState("Dark");
  const [autoSave, setAutoSave] = useState(true);

  const handleExportJSON = () => {
    try {
      const data = localStorage.getItem('openforge_todos') || '[]';
      const blob = new Blob([data], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'tasks_export.json';
      a.click();
    } catch {
      alert("No data available to export.");
    }
  };

  const handleClearData = () => {
    if (confirm("Are you sure you want to clear all tasks from browser storage?")) {
      localStorage.removeItem('openforge_todos');
      alert("Local task data cleared!");
    }
  };

  return (
    <div className="pt-24 pb-16 min-h-screen __BG__">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="text-center max-w-xl mx-auto">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full __CARD_BG__ text-xs font-bold text-indigo-400 mb-3">
            <Settings className="w-3.5 h-3.5" />
            <span>App Preferences</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight __TEXT__">
            Settings & Data Export
          </h1>
          <p className="text-sm __MUTED_TEXT__ mt-1">
            Configure application theme, automatic storage, and export your task data.
          </p>
        </div>

        <div className="__CARD_BG__ rounded-3xl p-8 space-y-6">
          <h3 className="text-base font-bold __TEXT__ border-b border-slate-800 pb-3">Preferences</h3>
          
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm font-semibold __TEXT__">Theme Mode</div>
              <div className="text-xs __MUTED_TEXT__">Switch between dark mode and system theme</div>
            </div>
            <select 
              value={theme}
              onChange={(e) => setTheme(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-xs text-white outline-none"
            >
              <option value="Dark">Modern Dark</option>
              <option value="Light">Minimal Light</option>
            </select>
          </div>

          <div className="flex items-center justify-between border-t border-slate-800/80 pt-4">
            <div>
              <div className="text-sm font-semibold __TEXT__">Auto Storage Sync</div>
              <div className="text-xs __MUTED_TEXT__">Automatically sync tasks to browser localStorage</div>
            </div>
            <input 
              type="checkbox"
              checked={autoSave}
              onChange={(e) => setAutoSave(e.target.checked)}
              className="w-4 h-4 accent-indigo-500 cursor-pointer"
            />
          </div>
        </div>

        <div className="__CARD_BG__ rounded-3xl p-8 space-y-6">
          <h3 className="text-base font-bold __TEXT__ border-b border-slate-800 pb-3">Data & Backups</h3>

          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <div className="text-sm font-semibold __TEXT__">Export Task Data (JSON)</div>
              <div className="text-xs __MUTED_TEXT__">Download a local backup file of all your tasks</div>
            </div>
            <button 
              onClick={handleExportJSON}
              className="px-5 py-2.5 rounded-xl __BUTTON__ text-xs font-bold flex items-center gap-2 shrink-0"
            >
              <Download className="w-4 h-4" /> Export Tasks JSON
            </button>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-t border-slate-800/80 pt-4">
            <div>
              <div className="text-sm font-semibold text-rose-400">Clear Storage Data</div>
              <div className="text-xs __MUTED_TEXT__">Delete all task items stored in this browser</div>
            </div>
            <button 
              onClick={handleClearData}
              className="px-5 py-2.5 rounded-xl bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 text-xs font-bold flex items-center gap-2 shrink-0 transition-colors"
            >
              <Trash2 className="w-4 h-4" /> Reset Storage
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
"""
    return (code
        .replace("__BG__", t['bg'])
        .replace("__BUTTON__", t['button'])
        .replace("__TEXT__", t['text'])
        .replace("__CARD_BG__", t['card_bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_hero_component(project_name: str, prompt_summary: str, theme_name: str) -> str:
    t = get_theme(theme_name)
    clean_summary = prompt_summary or "Transform your ideas into production-ready software in minutes."
    slug = project_name.lower().replace(' ', '')

    code = """import React from 'react';
import { ArrowRight, CheckCircle2, Zap, Shield, Star } from 'lucide-react';

export const Hero: React.FC = () => {
  return (
    <section className="relative pt-32 pb-20 sm:pt-40 sm:pb-32 overflow-hidden __BG__">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full __CARD_BG__ mb-8">
          <span className="flex h-2 w-2 rounded-full bg-indigo-500 animate-pulse"></span>
          <span className="text-xs sm:text-sm font-semibold __MUTED_TEXT__">
            Next Generation Web Application • Multi-Page
          </span>
        </div>

        <h1 className="text-4xl sm:text-6xl md:text-7xl font-extrabold tracking-tight __TEXT__ leading-tight max-w-4xl mx-auto">
          Build Smarter with <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r __ACCENT__">
            __PROJECT_NAME__
          </span>
        </h1>

        <p className="mt-6 text-lg sm:text-xl __MUTED_TEXT__ max-w-2xl mx-auto leading-relaxed">
          __CLEAN_SUMMARY__
        </p>

        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto">
          <button className="w-full sm:w-auto px-8 py-4 text-base rounded-xl font-bold __BUTTON__ flex items-center justify-center gap-3 transition-transform hover:scale-105">
            Launch Tasks Workspace <ArrowRight className="w-5 h-5" />
          </button>
          <button className="w-full sm:w-auto px-8 py-4 text-base rounded-xl font-semibold __CARD_BG__ __TEXT__ hover:opacity-80 transition-opacity">
            Watch Demo
          </button>
        </div>

        <div className="mt-12 flex flex-wrap items-center justify-center gap-6 text-xs sm:text-sm __MUTED_TEXT__">
          <div className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-emerald-400" /> Real-time Local Storage</div>
          <div className="flex items-center gap-2"><Zap className="w-4 h-4 text-amber-400" /> Multi-page View Routing</div>
          <div className="flex items-center gap-2"><Shield className="w-4 h-4 text-indigo-400" /> Category Analytics</div>
        </div>
      </div>
    </section>
  );
};
"""
    return (code
        .replace("__PROJECT_NAME__", project_name)
        .replace("__CLEAN_SUMMARY__", clean_summary)
        .replace("__SLUG__", slug)
        .replace("__BG__", t['bg'])
        .replace("__ACCENT__", t['accent'])
        .replace("__BUTTON__", t['button'])
        .replace("__TEXT__", t['text'])
        .replace("__CARD_BG__", t['card_bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_features_component(theme_name: str) -> str:
    t = get_theme(theme_name)
    code = """import React from 'react';
import { Cpu, Globe, Rocket, ShieldCheck, Layers, Sparkles } from 'lucide-react';

const featuresList = [
  {
    icon: Cpu,
    title: "Task Automation",
    description: "Intelligent task tracking designed to eliminate manual tracking."
  },
  {
    icon: Rocket,
    title: "Instant Search & Filter",
    description: "Filter tasks instantly by work, dev, personal, or urgent categories."
  },
  {
    icon: ShieldCheck,
    title: "Browser Storage Backup",
    description: "Tasks persist locally in browser storage with instant JSON export capabilities."
  }
];

export const Features: React.FC = () => {
  return (
    <section id="features" className="py-24 relative __BG__">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs sm:text-sm font-bold uppercase tracking-wider text-indigo-400 mb-3">
            Core Capability
          </h2>
          <p className="text-3xl sm:text-5xl font-extrabold tracking-tight __TEXT__">
            Everything you need to organize tasks
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {featuresList.map((f, idx) => {
            const Icon = f.icon;
            return (
              <div key={idx} className="p-8 rounded-2xl __CARD_BG__">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-tr __ACCENT__ flex items-center justify-center text-white mb-6">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold __TEXT__ mb-3">{f.title}</h3>
                <p className="text-sm __MUTED_TEXT__ leading-relaxed">{f.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};
"""
    return (code
        .replace("__BG__", t['bg'])
        .replace("__ACCENT__", t['accent'])
        .replace("__TEXT__", t['text'])
        .replace("__CARD_BG__", t['card_bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_pricing_component(theme_name: str) -> str:
    t = get_theme(theme_name)
    code = """import React from 'react';
import { Check } from 'lucide-react';

export const Pricing: React.FC = () => {
  return (
    <section id="pricing" className="py-24 relative __BG__">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-extrabold __TEXT__ mb-12">Predictable Pricing Plans</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto text-left">
          <div className="p-8 rounded-3xl __CARD_BG__">
            <h3 className="text-2xl font-bold __TEXT__">Free Community</h3>
            <div className="text-4xl font-extrabold __TEXT__ my-4">$0</div>
            <p className="text-xs __MUTED_TEXT__ mb-6">Perfect for personal task management.</p>
            <button className="w-full py-3 rounded-xl bg-slate-800 text-white font-bold text-xs">Start Free</button>
          </div>
          <div className="p-8 rounded-3xl bg-indigo-950/80 border-2 border-indigo-500">
            <h3 className="text-2xl font-bold __TEXT__">Pro Workspace</h3>
            <div className="text-4xl font-extrabold text-indigo-400 my-4">$29</div>
            <p className="text-xs __MUTED_TEXT__ mb-6">Ideal for team task synchronization.</p>
            <button className="w-full py-3 rounded-xl __BUTTON__ font-bold text-xs">Get Pro Workspace</button>
          </div>
        </div>
      </div>
    </section>
  );
};
"""
    return (code
        .replace("__BG__", t['bg'])
        .replace("__BUTTON__", t['button'])
        .replace("__TEXT__", t['text'])
        .replace("__CARD_BG__", t['card_bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_footer_component(project_name: str, theme_name: str) -> str:
    t = get_theme(theme_name)
    code = """import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="py-12 border-t border-slate-800/80 __BG__ text-center text-xs __MUTED_TEXT__">
      © {new Date().getFullYear()} __PROJECT_NAME__. All rights reserved. Multi-Page Web App built with OpenForge AI.
    </footer>
  );
};
"""
    return (code
        .replace("__PROJECT_NAME__", project_name)
        .replace("__BG__", t['bg'])
        .replace("__MUTED_TEXT__", t['muted_text'])
    )

def generate_app_tsx(project_name: str, components: List[str]) -> str:
    """Generates isolated multi-page view router in App.tsx."""
    imports = []
    for c in components:
        clean_c = c.replace(".tsx", "").replace("src/components/", "").strip()
        imports.append(f"import {{ {clean_c} }} from './components/{clean_c}';")
    
    imports_str = "\n".join(imports)

    template = """import React, { useState } from 'react';
__IMPORTS__

export function App() {
  const [activeTab, setActiveTab] = useState('Home');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 antialiased selection:bg-indigo-500 selection:text-white flex flex-col justify-between">
      {typeof Navbar !== 'undefined' && <Navbar activeTab={activeTab} onSelectTab={setActiveTab} />}
      
      {/* Isolated Multi-Page View Routing */}
      <main className="flex-1">
        {activeTab === 'Home' && (
          <div>
            {typeof Hero !== 'undefined' && <Hero />}
            {typeof Features !== 'undefined' && <Features />}
            {typeof Pricing !== 'undefined' && <Pricing />}
          </div>
        )}

        {(activeTab === 'Tasks' || activeTab === 'App') && (
          <div>
            {typeof TodoWorkspace !== 'undefined' ? <TodoWorkspace /> : (typeof TodoApp !== 'undefined' && <TodoApp />)}
          </div>
        )}

        {activeTab === 'Categories' && (
          <div>
            {typeof CategoryView !== 'undefined' ? <CategoryView /> : (typeof Features !== 'undefined' && <Features />)}
          </div>
        )}

        {activeTab === 'Analytics' && (
          <div>
            {typeof AnalyticsView !== 'undefined' ? <AnalyticsView /> : (typeof Features !== 'undefined' && <Features />)}
          </div>
        )}

        {activeTab === 'Settings' && (
          <div>
            {typeof SettingsView !== 'undefined' ? <SettingsView /> : (typeof Pricing !== 'undefined' && <Pricing />)}
          </div>
        )}
      </main>

      {typeof Footer !== 'undefined' && <Footer />}
    </div>
  );
}

export default App;
"""
    return template.replace("__IMPORTS__", imports_str)

def generate_main_tsx() -> str:
    return """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
