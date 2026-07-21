import React from 'react';
import { CheckCircle2, Loader2, AlertTriangle, Terminal, Code, Palette, Package, Cpu, FileCheck, ShieldCheck } from 'lucide-react';
import { GenerationEvent } from '../types';

interface ProgressTrackerProps {
  currentStep: string;
  progressPercent: number;
  logs: GenerationEvent[];
  isGenerating: boolean;
  errorMsg: string | null;
}

const STEPS = [
  { id: 'intent_expander', name: '1. Intent Expander', icon: FileCheck, desc: 'Generates spec & acceptance criteria' },
  { id: 'planner', name: '2. Roadmap & UI Design', icon: Palette, desc: 'Defines phases & design tokens' },
  { id: 'code_generator', name: '3. Code Synthesizer', icon: Code, desc: 'Optimized TSX component code' },
  { id: 'validator', name: '4. Validator & Auto-Fix', icon: ShieldCheck, desc: 'Audits criteria & patches defects' },
  { id: 'exporter', name: '5. Export Agent', icon: Package, desc: 'Packages workspace into ZIP' }
];

export const ProgressTracker: React.FC<ProgressTrackerProps> = ({
  currentStep,
  progressPercent,
  logs,
  isGenerating,
  errorMsg
}) => {
  const getStepStatus = (stepId: string) => {
    const stepOrder = ['intent_expander', 'planner', 'code_generator', 'validator', 'exporter'];
    const currentIdx = stepOrder.indexOf(currentStep);
    const stepIdx = stepOrder.indexOf(stepId);

    if (errorMsg) return 'failed';
    if (currentIdx > stepIdx || progressPercent === 100) return 'completed';
    if (currentIdx === stepIdx && isGenerating) return 'in_progress';
    return 'pending';
  };

  return (
    <div className="glass-card rounded-3xl p-6 sm:p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-extrabold text-white flex items-center gap-2">
            <Cpu className="w-5 h-5 text-indigo-400" />
            Agent Validation Loop Pipeline (v2)
          </h3>
          <p className="text-xs text-slate-400 mt-1">Deterministic specs, prompt optimization, & auto-fix verification</p>
        </div>
        <div className="text-right">
          <span className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
            {progressPercent}%
          </span>
        </div>
      </div>

      {/* Main Progress Bar */}
      <div className="w-full bg-slate-900 rounded-full h-3 p-0.5 border border-slate-800 overflow-hidden">
        <div
          className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 h-full rounded-full transition-all duration-500"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {/* Error Alert */}
      {errorMsg && (
        <div className="p-4 rounded-2xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* 5 Steps Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        {STEPS.map((step) => {
          const status = getStepStatus(step.id);
          const Icon = step.icon;

          return (
            <div
              key={step.id}
              className={`p-3.5 rounded-2xl border transition-all ${
                status === 'completed'
                  ? 'bg-slate-900/90 border-emerald-500/30 text-slate-200'
                  : status === 'in_progress'
                  ? 'bg-indigo-950/60 border-indigo-500/50 shadow-lg shadow-indigo-500/10 text-white'
                  : status === 'failed'
                  ? 'bg-rose-950/40 border-rose-500/30 text-rose-200'
                  : 'bg-slate-900/40 border-slate-800/80 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className={`p-1.5 rounded-xl ${
                  status === 'completed' ? 'bg-emerald-500/20 text-emerald-400' :
                  status === 'in_progress' ? 'bg-indigo-500/20 text-indigo-400' :
                  'bg-slate-800 text-slate-400'
                }`}>
                  <Icon className="w-4 h-4" />
                </div>
                {status === 'completed' && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                {status === 'in_progress' && <Loader2 className="w-4 h-4 text-indigo-400 animate-spin" />}
              </div>
              <div className="text-xs font-extrabold">{step.name}</div>
              <div className="text-[10px] opacity-70 mt-1">{step.desc}</div>
            </div>
          );
        })}
      </div>

      {/* Live Terminal Log */}
      <div className="rounded-2xl bg-slate-950 border border-slate-800 p-4 font-mono text-xs text-slate-300">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2 mb-3">
          <div className="flex items-center gap-2 text-slate-400">
            <Terminal className="w-4 h-4 text-emerald-400" />
            <span>Agent Validation Stream Logs</span>
          </div>
          <span className="text-[10px] text-slate-500">{logs.length} events logged</span>
        </div>
        <div className="space-y-1.5 max-h-36 overflow-y-auto pr-2">
          {logs.length === 0 ? (
            <div className="text-slate-600 italic">Waiting for prompt submission...</div>
          ) : (
            logs.map((log, idx) => (
              <div key={idx} className="flex items-start gap-2">
                <span className="text-slate-600">[{new Date().toLocaleTimeString()}]</span>
                <span className={log.status === 'failed' ? 'text-rose-400' : log.percent === 100 ? 'text-emerald-400 font-bold' : 'text-slate-300'}>
                  {log.message}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
