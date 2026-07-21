import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { PromptSection } from './components/PromptSection';
import { ProgressTracker } from './components/ProgressTracker';
import { CodeViewer } from './components/CodeViewer';
import { LivePreview } from './components/LivePreview';
import { ValidationReportView } from './components/ValidationReportView';
import { ThemeType, GenerationEvent, ProjectDetails } from './types';
import { Code, Eye, ShieldCheck, CheckCircle2 } from 'lucide-react';

export function App() {
  const [prompt, setPrompt] = useState('');
  const [theme, setTheme] = useState<ThemeType>('Modern Dark');
  const [selectedModel, setSelectedModel] = useState<string>('qwen3.6');
  const [ollamaOnline, setOllamaOnline] = useState<boolean>(false);
  const [models, setModels] = useState<string[]>(['qwen3.6', 'gemma3', 'qwen2.5:7b', 'llama3']);

  // Generation state
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentStep, setCurrentStep] = useState<string>('intent_expander');
  const [progressPercent, setProgressPercent] = useState<number>(0);
  const [logs, setLogs] = useState<GenerationEvent[]>([]);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Result project state
  const [project, setProject] = useState<ProjectDetails | null>(null);
  const [activeView, setActiveView] = useState<'code' | 'preview' | 'validation'>('code');
  const [isRegeneratingComp, setIsRegeneratingComp] = useState(false);

  // Check Ollama models on mount
  const fetchModels = async () => {
    try {
      const res = await fetch('/api/models');
      if (res.ok) {
        const data = await res.json();
        setOllamaOnline(data.ollama_online);
        if (data.models && data.models.length > 0) {
          setModels(data.models);
          if (!data.models.includes(selectedModel)) {
            setSelectedModel(data.recommended_model || data.models[0]);
          }
        }
      }
    } catch (e) {
      console.warn("API check failed:", e);
    }
  };

  useEffect(() => {
    fetchModels();
  }, []);

  const handleGenerate = async () => {
    if (!prompt.trim() || isGenerating) return;

    setIsGenerating(true);
    setProgressPercent(5);
    setCurrentStep('intent_expander');
    setLogs([]);
    setErrorMsg(null);
    setProject(null);

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          theme,
          model: selectedModel
        })
      });

      if (!res.ok || !res.body) {
        throw new Error(`Failed to initiate generation (${res.status})`);
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event: GenerationEvent = JSON.parse(line.replace('data: ', '').trim());
              setLogs((prev) => [...prev, event]);
              setProgressPercent(event.percent);
              if (event.step) setCurrentStep(event.step);

              if (event.status === 'failed') {
                setErrorMsg(event.message);
                setIsGenerating(false);
              }

              if (event.percent === 100 && event.data?.project_id) {
                await fetchProjectDetails(event.data.project_id);
              }
            } catch (err) {
              console.warn("Error parsing SSE JSON:", err);
            }
          }
        }
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Generation pipeline encountered an error.');
    } finally {
      setIsGenerating(false);
    }
  };

  const fetchProjectDetails = async (projectId: string) => {
    try {
      const res = await fetch(`/api/project/${projectId}`);
      if (res.ok) {
        const data = await res.json();
        setProject(data);
      }
    } catch (e) {
      console.error("Failed to fetch project workspace details:", e);
    }
  };

  const handleRegenerateComponent = async (compName: string, instructions: string) => {
    if (!project || isRegeneratingComp) return;

    setIsRegeneratingComp(true);
    try {
      const res = await fetch('/api/regenerate-component', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          project_id: project.project_id,
          component_name: compName,
          instructions,
          model: selectedModel
        })
      });

      if (res.ok) {
        const data = await res.json();
        setProject((prev) => {
          if (!prev) return prev;
          return {
            ...prev,
            files: {
              ...prev.files,
              [data.file_path]: data.code
            }
          };
        });
      }
    } catch (e) {
      console.error("Failed to regenerate component:", e);
    } finally {
      setIsRegeneratingComp(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Top Header */}
      <Header
        ollamaOnline={ollamaOnline}
        models={models}
        selectedModel={selectedModel}
        onSelectModel={setSelectedModel}
        onRefreshModels={fetchModels}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-8 py-8 space-y-10">
        {/* Prompt Input Form */}
        <PromptSection
          prompt={prompt}
          setPrompt={setPrompt}
          theme={theme}
          setTheme={setTheme}
          onGenerate={handleGenerate}
          isGenerating={isGenerating}
        />

        {/* Real-time Progress & Agent Stepper (visible during or after generation) */}
        {(isGenerating || logs.length > 0) && (
          <ProgressTracker
            currentStep={currentStep}
            progressPercent={progressPercent}
            logs={logs}
            isGenerating={isGenerating}
            errorMsg={errorMsg}
          />
        )}

        {/* Generated Workspace: Code Explorer, Live Preview & Validation */}
        {project && (
          <div className="space-y-6 pt-4">
            <div className="flex items-center justify-between flex-wrap gap-4 border-b border-slate-800 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-2xl font-black text-white">{project.spec?.project_name || project.plan?.project_name || 'Generated Website'}</h2>
                  <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-bold border border-emerald-500/30 flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Validated ({project.validation_report?.compliance_score || 100}% Score)
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-1">{project.spec?.description || project.plan?.description}</p>
              </div>

              {/* View Switcher Tabs */}
              <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 rounded-2xl p-1">
                <button
                  onClick={() => setActiveView('code')}
                  className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-colors ${
                    activeView === 'code' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Code className="w-4 h-4" />
                  <span>Code Explorer</span>
                </button>
                <button
                  onClick={() => setActiveView('preview')}
                  className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-colors ${
                    activeView === 'preview' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Eye className="w-4 h-4" />
                  <span>Live Preview</span>
                </button>
                <button
                  onClick={() => setActiveView('validation')}
                  className={`px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 transition-colors ${
                    activeView === 'validation' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Spec & Validation</span>
                </button>
              </div>
            </div>

            {/* Active Workspace View */}
            {activeView === 'code' && (
              <CodeViewer
                project={project}
                onRegenerateComponent={handleRegenerateComponent}
                isRegenerating={isRegeneratingComp}
              />
            )}
            {activeView === 'preview' && <LivePreview project={project} />}
            {activeView === 'validation' && <ValidationReportView project={project} />}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="py-6 border-t border-slate-900 text-center text-xs text-slate-500">
        OpenForge AI • Local LLM SaaS Website Builder • 100% Free & Local
      </footer>
    </div>
  );
}

export default App;
