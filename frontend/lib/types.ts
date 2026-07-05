export type WorkflowItem = {
  id: string;
  source: string;
  title: string;
  sender: string | null;
  intent: string | null;
  assigned_agent_key: string | null;
  priority: string;
  status: string;
  extracted_data: Record<string, any>;
  suggested_action: string | null;
  ai_summary: string | null;
  model_tier: string | null;
  model_used: string | null;
  created_at: string;
  updated_at: string;
};

export type Agent = {
  id: string;
  key: string;
  name: string;
  description: string;
  status: string;
  accuracy: number;
  tasks_handled: number;
  current_task: string | null;
};

export type ActivityEntry = {
  id: string;
  workflow_item_id: string | null;
  actor: string;
  action: string;
  detail: string;
  model_used: string | null;
  model_tier: string | null;
  created_at: string;
};

export type Analytics = {
  emails_processed: number;
  documents_reviewed: number;
  tasks_automated: number;
  hours_saved: number;
  cost_saved_usd: number;
  ai_accuracy: number;
  approval_rate: number;
  active_agents: number;
  model_tier_breakdown: Record<string, number>;
};
