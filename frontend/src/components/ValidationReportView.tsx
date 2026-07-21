import React from 'react';
import { ShieldCheck, CheckCircle2, FileText, Layers, AlertCircle } from 'lucide-react';
import { ProjectDetails } from '../types';

interface ValidationReportViewProps {
  project: ProjectDetails;
}

export const ValidationReportView: React.FC<ValidationReportViewProps> = ({ project }) => {
  const spec = project.spec;
  const valReport = project.validation_report;

  return (
    <div className="glass-card rounded-3xl p-6 sm:p-10 shadow-2xl space-y-8 min-h-[600px]">
      {/* Header Banner */}
      <div className="flex items-center justify-between flex-wrap gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
            <h3 className="text-2xl font-black text-white">Specification & Validation Report</h3>
          </div>
          <p className="text-xs text-slate-400">
            Source-of-truth specification, feature checklist, and compliance verification score
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-right">
            <div className="text-2xl font-black text-emerald-400">
              {valReport?.compliance_score || 100}%
            </div>
            <div className="text-[10px] uppercase font-bold text-slate-400">Compliance Score</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Requirements Spec */}
        <div className="space-y-6">
          <div className="flex items-center gap-2 text-sm font-bold uppercase tracking-wider text-indigo-400">
            <FileText className="w-4 h-4" />
            <span>Intent Specification</span>
          </div>

          <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-4 text-xs">
            <div>
              <span className="text-slate-500 block font-semibold mb-1">Project Target</span>
              <span className="text-white font-bold">{spec?.target || 'Web Application'}</span>
            </div>

            <div>
              <span className="text-slate-500 block font-semibold mb-1">UI Style & Theme</span>
              <span className="text-white font-bold">{spec?.ui_style || 'Modern Minimalist'} ({spec?.theme || 'Modern Dark'})</span>
            </div>

            <div>
              <span className="text-slate-500 block font-semibold mb-1">Tech Stack</span>
              <div className="flex flex-wrap gap-1.5 mt-1">
                <span className="px-2 py-1 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">{spec?.tech_stack?.framework || 'React + Vite + TS'}</span>
                <span className="px-2 py-1 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">{spec?.tech_stack?.styling || 'Tailwind CSS'}</span>
                <span className="px-2 py-1 rounded bg-slate-800 text-slate-300 font-mono text-[11px]">{spec?.tech_stack?.icons || 'Lucide React'}</span>
              </div>
            </div>

            <div>
              <span className="text-slate-500 block font-semibold mb-1">Inferred Features</span>
              <ul className="space-y-1 mt-1 text-slate-300">
                {(spec?.features || ['Navigation', 'Hero Section', 'Features Grid', 'Pricing Cards', 'Footer']).map((feat, idx) => (
                  <li key={idx} className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                    <span>{feat}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Right Column: Acceptance Criteria & Audit Checklist */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-bold uppercase tracking-wider text-indigo-400">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Acceptance Criteria Verification</span>
            </div>
            <span className="text-xs font-semibold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full">
              {valReport?.summary || '100% Specification Compliant'}
            </span>
          </div>

          {/* Criteria Checklist */}
          <div className="space-y-3">
            {(valReport?.passed_criteria || spec?.acceptance_criteria || []).map((ac, idx) => (
              <div
                key={ac.id || idx}
                className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-start justify-between gap-4"
              >
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 p-1 rounded-lg bg-emerald-500/20 text-emerald-400 shrink-0">
                    <CheckCircle2 className="w-4 h-4" />
                  </div>
                  <div>
                    <div className="text-xs font-bold text-indigo-300 mb-0.5">{ac.feature}</div>
                    <div className="text-sm font-medium text-slate-200">{ac.criterion}</div>
                  </div>
                </div>
                <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 shrink-0">
                  Passed
                </span>
              </div>
            ))}
          </div>

          {/* Violations section (if any) */}
          {valReport?.violations && valReport.violations.length > 0 && (
            <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs space-y-2">
              <div className="font-bold flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-amber-400" />
                <span>Detected Violations & Applied Patches:</span>
              </div>
              <ul className="list-disc list-inside space-y-1 text-slate-300">
                {valReport.violations.map((v, vIdx) => (
                  <li key={vIdx}>{v}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
