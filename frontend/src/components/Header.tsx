import React from 'react';
import { Sparkles, Cpu, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-react';

interface HeaderProps {
  ollamaOnline: boolean;
  models: string[];
  selectedModel: string;
  onSelectModel: (m: string) => void;
  onRefreshModels: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  ollamaOnline,
  models,
  selectedModel,
  onSelectModel,
  onRefreshModels
}) => {
  return (
    <header className="glass-nav sticky top-0 z-50 py-3 px-4 sm:px-8">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 text-white shadow-lg shadow-indigo-500/30">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-xl tracking-tight text-white">OpenForge</span>
              <span className="px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 text-xs font-bold border border-indigo-500/30">
                AI
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">Local LLM SaaS Website Builder</p>
          </div>
        </div>

        {/* Right Section: Connectivity & Model Selector */}
        <div className="flex items-center gap-4">
          {/* Status Badge */}
          <div className={`hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold border ${
            ollamaOnline 
              ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' 
              : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
          }`}>
            {ollamaOnline ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>Ollama Online</span>
              </>
            ) : (
              <>
                <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
                <span>Fallback Mode Active</span>
              </>
            )}
          </div>

          {/* Model Dropdown */}
          <div className="flex items-center gap-2 bg-slate-900 border border-slate-800 rounded-xl px-3 py-1.5">
            <Cpu className="w-4 h-4 text-indigo-400" />
            <select
              value={selectedModel}
              onChange={(e) => onSelectModel(e.target.value)}
              className="bg-transparent text-xs font-medium text-slate-200 outline-none cursor-pointer pr-2"
            >
              {models.map((m) => (
                <option key={m} value={m} className="bg-slate-900 text-slate-200">
                  {m}
                </option>
              ))}
            </select>
            <button 
              onClick={onRefreshModels} 
              title="Refresh models"
              className="text-slate-400 hover:text-white transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};
