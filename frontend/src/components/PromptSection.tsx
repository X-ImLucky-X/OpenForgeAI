import React, { useState } from 'react';
import { Sparkles, Wand2, Palette, Layers, Paintbrush } from 'lucide-react';
import { ThemeType } from '../types';

interface PromptSectionProps {
  prompt: string;
  setPrompt: (p: string) => void;
  theme: ThemeType;
  setTheme: (t: ThemeType) => void;
  onGenerate: () => void;
  isGenerating: boolean;
}

const PRESETS = [
  "Build a working Todo App with dark mode, task categories, search, and local storage",
  "SaaS Platform with interactive metrics dashboard, pricing, and contact form",
  "Minimalist Photography Portfolio with filterable gallery & contact form",
  "E-Commerce Store with product grid, shopping cart drawer, and checkout modal",
  "Modern Agency Website with multi-page navigation and features"
];

const THEMES: ThemeType[] = [
  'Modern Dark',
  'Minimal Light',
  'Cyberpunk Neon',
  'Glassmorphism',
  'Sunset Vibrant'
];

const FRAMEWORKS = [
  'React + Vite + TS',
  'React + Tailwind'
];

const COLORS = [
  'Indigo & Purple',
  'Blue & Cyan',
  'Emerald & Teal',
  'Rose & Violet',
  'Amber & Orange'
];

export const PromptSection: React.FC<PromptSectionProps> = ({
  prompt,
  setPrompt,
  theme,
  setTheme,
  onGenerate,
  isGenerating
}) => {
  const [selectedFramework, setSelectedFramework] = useState('React + Vite + TS');
  const [selectedColor, setSelectedColor] = useState('Indigo & Purple');

  return (
    <div className="glass-card rounded-3xl p-6 sm:p-10 shadow-2xl relative overflow-hidden">
      <div className="absolute -right-20 -top-20 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute -left-20 -bottom-20 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="relative z-10 space-y-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 text-indigo-400 text-xs font-semibold mb-4 border border-indigo-500/20">
            <Sparkles className="w-3.5 h-3.5" />
            <span>OpenForge Functional App Engine Ready</span>
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-white tracking-tight">
            Generate fully working <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
              multi-page SaaS & web apps
            </span>
          </h1>
          <p className="text-sm sm:text-base text-slate-400 mt-2">
            Local LLM agents generate complete React + Vite applications with state, multi-page routing, and local storage persistence.
          </p>
        </div>

        {/* Prompt Input Form */}
        <div className="space-y-3">
          <label className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
            <Wand2 className="w-3.5 h-3.5 text-indigo-400" />
            Application Description & Prompt
          </label>
          <div className="relative">
            <textarea
              rows={3}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g. Build a working Todo App with dark mode, search, categories, and local storage state persistence..."
              className="w-full bg-slate-900/90 border border-slate-800 rounded-2xl p-4 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 transition-colors resize-none"
            />
          </div>
        </div>

        {/* Preset Chips */}
        <div className="flex flex-wrap gap-2 pt-1">
          <span className="text-xs text-slate-400 font-medium py-1">Quick Ideas:</span>
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              onClick={() => setPrompt(p)}
              className="px-3 py-1 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs text-slate-300 transition-colors hover:text-white"
            >
              {p.split(' ')[0]} {p.split(' ')[1]} {p.split(' ')[2]} {p.split(' ')[3]}...
            </button>
          ))}
        </div>

        {/* Configurations Row */}
        <div className="pt-4 border-t border-slate-800/80 flex flex-col lg:flex-row items-center justify-between gap-4">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 w-full lg:w-auto">
            {/* Theme Selector */}
            <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2">
              <Palette className="w-4 h-4 text-indigo-400 shrink-0" />
              <span className="text-xs text-slate-400 font-medium shrink-0">Theme:</span>
              <select
                value={theme}
                onChange={(e) => setTheme(e.target.value as ThemeType)}
                className="bg-transparent text-xs font-semibold text-white outline-none cursor-pointer w-full"
              >
                {THEMES.map((t) => (
                  <option key={t} value={t} className="bg-slate-900 text-slate-200">
                    {t}
                  </option>
                ))}
              </select>
            </div>

            {/* Framework Selector */}
            <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2">
              <Layers className="w-4 h-4 text-purple-400 shrink-0" />
              <span className="text-xs text-slate-400 font-medium shrink-0">Framework:</span>
              <select
                value={selectedFramework}
                onChange={(e) => setSelectedFramework(e.target.value)}
                className="bg-transparent text-xs font-semibold text-white outline-none cursor-pointer w-full"
              >
                {FRAMEWORKS.map((fw) => (
                  <option key={fw} value={fw} className="bg-slate-900 text-slate-200">
                    {fw}
                  </option>
                ))}
              </select>
            </div>

            {/* Color Selector */}
            <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2">
              <Paintbrush className="w-4 h-4 text-pink-400 shrink-0" />
              <span className="text-xs text-slate-400 font-medium shrink-0">Accent:</span>
              <select
                value={selectedColor}
                onChange={(e) => setSelectedColor(e.target.value)}
                className="bg-transparent text-xs font-semibold text-white outline-none cursor-pointer w-full"
              >
                {COLORS.map((c) => (
                  <option key={c} value={c} className="bg-slate-900 text-slate-200">
                    {c}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Action Button */}
          <button
            onClick={onGenerate}
            disabled={isGenerating || !prompt.trim()}
            className={`w-full lg:w-auto px-8 py-3.5 rounded-2xl font-extrabold text-sm flex items-center justify-center gap-3 transition-all ${
              isGenerating || !prompt.trim()
                ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                : 'bg-gradient-to-r from-indigo-500 via-purple-600 to-pink-600 hover:from-indigo-600 hover:to-pink-700 text-white shadow-xl shadow-indigo-500/25 hover:scale-[1.02]'
            }`}
          >
            {isGenerating ? (
              <>
                <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                <span>Agents Synthesizing App...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Generate Application</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
