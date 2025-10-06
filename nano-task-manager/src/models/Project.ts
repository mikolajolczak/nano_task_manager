import type { User } from "./User";

export interface Project {
  id: string;
  name: string;
  description?: string;
  owner_id?: string;
  owner?: User;
}
