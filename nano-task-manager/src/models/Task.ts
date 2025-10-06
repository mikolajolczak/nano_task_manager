import type { Project } from "./Project";
import type { Tag } from "./Tag";
import type { User } from "./User";

export interface Task {
  id: string;
  title: string;
  description?: string;
  status: "todo" | "in_progress" | "done";
  project_id?: string;
  project?: Project;
  assignee_id?: string;
  assignee?: User;
  tags: Tag[];
  tag_ids?: string[];
}
