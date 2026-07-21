import React, { useState } from 'react';
import { FileCode, Folder, Copy, Check, Download, RefreshCw, Layers } from 'lucide-react';
import { ProjectDetails } from '../types';

interface CodeViewerProps {
  project: ProjectDetails;
  onRegenerateComponent: (compName: string, instructions: string) => Promise<void>;
  isRegenerating: boolean;
}

export const CodeViewer: React.FC<CodeViewerProps> = ({
  project,
  onRegenerateComponent,
  isRegenerating
}) => {
  const fileKeys = Object.keys(project.files).sort();
  const [selectedFile, setSelectedFile] = useState<string>(
    fileKeys.find((f) => f === 'src/App.tsx') || fileKeys[0] || ''
  );
  const [copied, setCopied] = useState(false);

  // Component Tuner state
  const [regenInstructions, setRegenInstructions] = useState('');

  const currentCode = project.files[selectedFile] || '// Select a file to view code';

  const handleCopy = () => {
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isComponentFile = selectedFile.startsWith('src/components/') && selectedFile.endsWith('.tsx');
  const componentName = isComponentFile ? selectedFile.replace('src/components/', '').replace('.tsx', '') : '';

  const handleRegenSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (componentName && regenInstructions.trim()) {
      onRegenerateComponent(componentName, regenInstructions);
      setRegenInstructions('');
    }
  };

  return (
    <div className="glass-card rounded-3xl overflow-hidden shadow-2xl flex flex-col md:flex-row h-[600px]">
      {/* File Explorer Sidebar */}
      <div className="w-full md:w-64 bg-slate-950 border-r border-slate-800 p-4 flex flex-col justify-between shrink-0">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-slate-400 mb-4 px-2">
            <Folder className="w-4 h-4 text-indigo-400" />
            <span>Workspace Files ({fileKeys.length})</span>
          </div>
          
          <div className="space-y-1 overflow-y-auto max-h-[460px] pr-1">
            {fileKeys.map((fname) => {
              const isSelected = fname === selectedFile;
              return (
                <button
                  key={fname}
                  onClick={() => setSelectedFile(fname)}
                  className={`w-full text-left px-3 py-2 rounded-xl text-xs font-mono flex items-center gap-2 transition-colors ${
                    isSelected
                      ? 'bg-indigo-500/20 text-indigo-300 font-bold border border-indigo-500/30'
                      : 'text-slate-400 hover:text-white hover:bg-slate-900'
                  }`}
                >
                  <FileCode className={`w-3.5 h-3.5 shrink-0 ${isSelected ? 'text-indigo-400' : 'text-slate-500'}`} />
                  <span className="truncate">{fname}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Download ZIP Button */}
        <div className="pt-4 border-t border-slate-800">
          <a
            href={project.zip_url}
            download
            className="w-full py-2.5 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-extrabold text-xs flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 transition-all"
          >
            <Download className="w-4 h-4" />
            <span>Download website.zip</span>
          </a>
        </div>
      </div>

      {/* Main Code View Area */}
      <div className="flex-1 flex flex-col bg-slate-900/90 overflow-hidden">
        {/* Header */}
        <div className="px-6 py-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-mono text-indigo-300">
            <FileCode className="w-4 h-4 text-indigo-400" />
            <span>{selectedFile}</span>
          </div>

          <button
            onClick={handleCopy}
            className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs text-slate-300 flex items-center gap-1.5 transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied!' : 'Copy Code'}</span>
          </button>
        </div>

        {/* Code Content */}
        <div className="flex-1 p-6 overflow-auto font-mono text-xs text-slate-200 leading-relaxed bg-slate-950/60 selection:bg-indigo-500 selection:text-white">
          <pre>
            <code>{currentCode}</code>
          </pre>
        </div>

        {/* Component Regenerator Bar (if component selected) */}
        {isComponentFile && (
          <div className="p-4 bg-slate-950 border-t border-slate-800">
            <form onSubmit={handleRegenSubmit} className="flex items-center gap-3">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-400 shrink-0">
                <Layers className="w-4 h-4 text-indigo-400" />
                <span>Regenerate `{componentName}`:</span>
              </div>
              <input
                type="text"
                value={regenInstructions}
                onChange={(e) => setRegenInstructions(e.target.value)}
                placeholder="e.g. Add dark mode toggle or change primary CTA text..."
                className="flex-1 bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
              <button
                type="submit"
                disabled={isRegenerating || !regenInstructions.trim()}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs flex items-center gap-1.5 disabled:opacity-50 transition-all shrink-0"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${isRegenerating ? 'animate-spin' : ''}`} />
                <span>Refine</span>
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};
