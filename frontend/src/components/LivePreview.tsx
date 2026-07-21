import React, { useState } from 'react';
import { Monitor, Tablet, Smartphone, ExternalLink, RefreshCw, Sparkles, CheckCircle2, Zap, Shield, Star, Layers, Cpu, Globe, Rocket, ShieldCheck } from 'lucide-react';
import { ProjectDetails } from '../types';

interface LivePreviewProps {
  project: ProjectDetails;
}

export const LivePreview: React.FC<LivePreviewProps> = ({ project }) => {
  const [device, setDevice] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');
  const [viewMode, setViewMode] = useState<'interactive' | 'visual'>('interactive');
  const [iframeKey, setIframeKey] = useState<number>(0);

  const deviceWidths = {
    desktop: 'w-full',
    tablet: 'w-[768px]',
    mobile: 'w-[375px]'
  };

  const previewUrl = `/api/preview/${project.project_id}`;

  const handleRefresh = () => {
    setIframeKey((prev) => prev + 1);
  };

  const projectName = project.spec?.project_name || project.plan?.project_name || 'Forge App';
  const description = project.spec?.description || project.plan?.description || 'A next-generation web experience generated directly by OpenForge AI.';
  const themeName = project.spec?.theme || project.plan?.theme || 'Modern Dark';

  return (
    <div className="glass-card rounded-3xl overflow-hidden shadow-2xl flex flex-col h-[750px]">
      {/* Top Toolbar */}
      <div className="px-6 py-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between flex-wrap gap-4">
        {/* Device Mode Selector */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
          <button
            onClick={() => setDevice('desktop')}
            className={`p-1.5 rounded-lg text-xs flex items-center gap-1 font-semibold transition-colors ${
              device === 'desktop' ? 'bg-indigo-500 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            <Monitor className="w-4 h-4" />
            <span className="hidden sm:inline">Desktop</span>
          </button>
          <button
            onClick={() => setDevice('tablet')}
            className={`p-1.5 rounded-lg text-xs flex items-center gap-1 font-semibold transition-colors ${
              device === 'tablet' ? 'bg-indigo-500 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            <Tablet className="w-4 h-4" />
            <span className="hidden sm:inline">Tablet</span>
          </button>
          <button
            onClick={() => setDevice('mobile')}
            className={`p-1.5 rounded-lg text-xs flex items-center gap-1 font-semibold transition-colors ${
              device === 'mobile' ? 'bg-indigo-500 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            <Smartphone className="w-4 h-4" />
            <span className="hidden sm:inline">Mobile</span>
          </button>
        </div>

        {/* View Mode Toggle */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1 text-xs">
          <button
            onClick={() => setViewMode('interactive')}
            className={`px-3 py-1 rounded-lg font-bold transition-colors ${
              viewMode === 'interactive' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Live Server View
          </button>
          <button
            onClick={() => setViewMode('visual')}
            className={`px-3 py-1 rounded-lg font-bold transition-colors ${
              viewMode === 'visual' ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white'
            }`}
          >
            Visual Components
          </button>
        </div>

        {/* Address Bar Simulation & Controls */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleRefresh}
            title="Refresh Live Preview"
            className="p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
          <a
            href={previewUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs font-bold text-indigo-400 hover:text-indigo-300 flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-900 border border-slate-800"
          >
            <span>Open New Tab</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>

      {/* Workspace Display Area */}
      <div className="flex-1 bg-slate-950 p-4 sm:p-6 overflow-auto flex justify-center items-center">
        <div className={`${deviceWidths[device]} h-full transition-all duration-300 rounded-2xl overflow-hidden border border-slate-800 shadow-2xl bg-slate-950 relative`}>
          {viewMode === 'interactive' ? (
            <iframe
              key={iframeKey}
              src={previewUrl}
              title="Live Generated Website Preview"
              className="w-full h-full border-0 bg-slate-950"
            />
          ) : (
            <div className="w-full h-full overflow-y-auto p-6 sm:p-10 space-y-12 bg-slate-950 text-slate-100 selection:bg-indigo-500 selection:text-white">
              {/* Navbar Visual */}
              <nav className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 text-white">
                    <Sparkles className="w-5 h-5" />
                  </div>
                  <span className="font-extrabold text-xl tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">
                    {projectName}
                  </span>
                </div>
                <div className="hidden sm:flex items-center gap-6 text-xs text-slate-400 font-medium">
                  <span>Features</span>
                  <span>Pricing</span>
                  <span>Testimonials</span>
                  <button className="px-4 py-2 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-bold">
                    Get Started
                  </button>
                </div>
              </nav>

              {/* Hero Visual */}
              <section className="py-12 text-center space-y-6">
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300">
                  <span className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
                  <span>Next Generation Platform • Powered by AI</span>
                </div>
                <h1 className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight leading-tight max-w-3xl mx-auto">
                  Build Smarter with <br />
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
                    {projectName}
                  </span>
                </h1>
                <p className="text-base text-slate-400 max-w-xl mx-auto leading-relaxed">
                  {description}
                </p>
                <div className="flex items-center justify-center gap-4 pt-2">
                  <button className="px-7 py-3.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 text-white font-extrabold text-sm shadow-xl shadow-indigo-500/20">
                    Start Free Trial →
                  </button>
                  <button className="px-7 py-3.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-200 font-bold text-sm">
                    Watch Demo
                  </button>
                </div>

                <div className="pt-8 max-w-4xl mx-auto rounded-2xl p-6 bg-slate-900 border border-slate-800 text-left">
                  <div className="flex items-center gap-2 border-b border-slate-800 pb-3 mb-6">
                    <div className="w-3 h-3 rounded-full bg-rose-500" />
                    <div className="w-3 h-3 rounded-full bg-amber-500" />
                    <div className="w-3 h-3 rounded-full bg-emerald-500" />
                    <span className="text-xs text-slate-500 font-mono ml-2">{projectName.toLowerCase().replace(/\s+/g, '')}.app/dashboard</span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                      <div className="text-xs text-slate-400 font-semibold">Total Active Users</div>
                      <div className="text-2xl font-extrabold text-white mt-1">48,290</div>
                      <div className="text-xs text-emerald-400 mt-1 font-medium">↑ +24% this week</div>
                    </div>
                    <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                      <div className="text-xs text-slate-400 font-semibold">Generation Speed</div>
                      <div className="text-2xl font-extrabold text-white mt-1">1.2s avg</div>
                      <div className="text-xs text-indigo-400 mt-1 font-medium">⚡ Ultra low latency</div>
                    </div>
                    <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                      <div className="text-xs text-slate-400 font-semibold">Satisfaction Score</div>
                      <div className="text-2xl font-extrabold text-white mt-1">99.4%</div>
                      <div className="text-xs text-amber-400 mt-1 font-medium">★ ★ ★ ★ ★ (4.9/5)</div>
                    </div>
                  </div>
                </div>
              </section>

              {/* Features Visual */}
              <section className="py-8 space-y-6">
                <div className="text-center">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-indigo-400">Features</h3>
                  <p className="text-3xl font-extrabold text-white mt-1">Everything you need to scale</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
                  {[
                    { icon: Cpu, title: 'AI Automation', desc: 'Intelligent workflows designed to eliminate manual setup.' },
                    { icon: Rocket, title: 'Lightning Speed', desc: 'Built on next-gen architecture for instant load times.' },
                    { icon: ShieldCheck, title: 'Bank-Grade Security', desc: 'End-to-end encryption & automated compliance.' }
                  ].map((f, idx) => {
                    const Icon = f.icon;
                    return (
                      <div key={idx} className="p-6 rounded-2xl bg-slate-900 border border-slate-800">
                        <div className="w-10 h-10 rounded-xl bg-indigo-600 text-white flex items-center justify-center mb-4">
                          <Icon className="w-5 h-5" />
                        </div>
                        <h4 className="font-bold text-lg text-white mb-2">{f.title}</h4>
                        <p className="text-xs text-slate-400 leading-relaxed">{f.desc}</p>
                      </div>
                    );
                  })}
                </div>
              </section>

              {/* Pricing Visual */}
              <section className="py-8 space-y-6">
                <div className="text-center">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-indigo-400">Pricing</h3>
                  <p className="text-3xl font-extrabold text-white mt-1">Simple & Predictable</p>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 max-w-2xl mx-auto">
                  <div className="p-8 rounded-3xl bg-slate-900 border border-slate-800">
                    <h4 className="text-xl font-bold text-white">Starter</h4>
                    <div className="text-3xl font-extrabold text-white mt-3 mb-4">$0 <span className="text-xs text-slate-400 font-normal">/ month</span></div>
                    <p className="text-xs text-slate-400 mb-6">Perfect for individuals and side projects.</p>
                    <button className="w-full py-3 rounded-xl bg-slate-800 text-white font-bold text-xs">Start Free</button>
                  </div>
                  <div className="p-8 rounded-3xl bg-indigo-950/80 border-2 border-indigo-500 relative">
                    <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-indigo-500 text-white text-[10px] font-bold uppercase tracking-widest">Most Popular</div>
                    <h4 className="text-xl font-bold text-white">Pro Plan</h4>
                    <div className="text-3xl font-extrabold text-indigo-400 mt-3 mb-4">$29 <span className="text-xs text-slate-400 font-normal">/ month</span></div>
                    <p className="text-xs text-slate-400 mb-6">Ideal for growing teams and professionals.</p>
                    <button className="w-full py-3 rounded-xl bg-indigo-600 text-white font-bold text-xs shadow-lg">Get Pro Plan</button>
                  </div>
                </div>
              </section>

              {/* Footer */}
              <footer className="pt-8 border-t border-slate-800 text-center text-xs text-slate-500">
                © {new Date().getFullYear()} {projectName}. All rights reserved. Built with OpenForge AI.
              </footer>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
