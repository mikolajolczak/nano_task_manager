import type { Project } from "@/models/Project";
import type { Tag } from "@/models/Tag";
import type { Task } from "@/models/Task";
import type { User } from "@/models/User";
import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const getUsers = (): Promise<{ data: { total: number; users: User[] } }> =>
  api.get("/users");
export const getUserById = (id: string): Promise<{ data: User }> => api.get(`/users/${id}`);
export const createUser = (data: User) => api.post("/users", data);
export const updateUser = (id: string, data: User) => api.patch(`/users/${id}`, data);
export const deleteUser = (id: string) => api.delete(`/users/${id}`);

export const getProjects = (): Promise<{ data: { total: number; projects: Project[] } }> =>
  api.get("/projects");
export const createProject = (data: Project) => api.post("/projects", data);
export const getProjectById = (id: string): Promise<{ data: Project }> =>
  api.get(`/projects/${id}`);
export const updateProject = (id: string, data: Project) => api.patch(`/projects/${id}`, data);
export const deleteProject = (id: string) => api.delete(`/projects/${id}`);

export const getTasks = (): Promise<{ data: { total: number; tasks: Task[] } }> =>
  api.get("/tasks");
export const getTaskById = (id: string): Promise<{ data: Task }> => api.get(`/tasks/${id}`);
export const createTask = (data: Task) => api.post("/tasks", data);
export const updateTask = (id: string, data: Task) => api.patch(`/tasks/${id}`, data);
export const deleteTask = (id: string) => api.delete(`/tasks/${id}`);

export const getTags = (): Promise<{ data: { total: number; tags: Tag[] } }> => api.get("/tags");
export const createTag = (data: Tag): Promise<{ data: Tag }> => api.post("/tags", data);
export const updateTag = (id: string, data: Tag): Promise<{ data: Tag }> =>
  api.patch(`/tags/${id}`, data);
export const deleteTag = (id: string) => api.delete(`/tags/${id}`);

export default api;
