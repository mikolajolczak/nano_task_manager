import type { Tag } from "./Tag";

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: "todo" | "in_progress" | "done";
  project_id: string;
  assignee_id?: string | null;
  tags: Tag[];
  tag_ids?: string[];
}
