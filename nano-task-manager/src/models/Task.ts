export interface Task {
  id: number;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'done';
  project_id: number;
  assignee_id?: number | null;
}
