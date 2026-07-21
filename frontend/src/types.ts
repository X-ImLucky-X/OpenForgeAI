export interface GenerationEvent {
  project_id: string;
  step: 'intent_expander' | 'planner' | 'code_generator' | 'validator' | 'exporter' | 'error';
  status: 'in_progress' | 'completed' | 'failed';
  message: string;
  percent: number;
  data?: any;
}

export interface AcceptanceCriterion {
  id: string;
  feature: string;
  criterion: string;
  status?: 'passed' | 'failed';
}

export interface IntentSpec {
  project_name: string;
  target: string;
  theme: string;
  description: string;
  features: string[];
  ui_style: string;
  tech_stack: {
    framework: string;
    styling: string;
    icons: string;
  };
  acceptance_criteria: AcceptanceCriterion[];
}

export interface ValidationReport {
  is_valid: boolean;
  compliance_score: number;
  passed_criteria: AcceptanceCriterion[];
  violations: string[];
  summary: string;
}

export interface ProjectDetails {
  project_id: string;
  spec?: IntentSpec;
  plan?: {
    project_name: string;
    theme: string;
    description: string;
    components: string[];
  };
  validation_report?: ValidationReport;
  files: Record<string, string>;
  zip_url: string;
}

export type ThemeType = 'Modern Dark' | 'Minimal Light' | 'Cyberpunk Neon' | 'Glassmorphism' | 'Sunset Vibrant';
