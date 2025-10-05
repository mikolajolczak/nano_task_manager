import type { Project } from '@/models/Project';
import type { Tag } from '@/models/Tag';
import type { Task } from '@/models/Task';
import type { User } from '@/models/User';
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.API_URL,
})

export const getUsers = () => api.get('/users');
export const getUserById = (id: number) => api.get(`/users/${id}`);
export const createUser = (data: User) => api.post('/users', data);
export const updateUser = (id: number, data: User) => api.patch(`/users/${id}`, data);
export const deleteUser = (id: number) => api.delete(`/users/${id}`);

export const getProjects = () => api.get('/projects');
export const createProject = (data: Project) => api.post('/projects', data);

export const getTasks = () => api.get('/tasks');
export const createTask = (data: Task) => api.post('/tasks', data);
export const updateTask = (id: number, data: Task) => api.patch(`/tasks/${id}`, data);
export const deleteTask = (id: number) => api.delete(`/tasks/${id}`);

export const getTags = () => api.get('/tags');
export const createTag = (data:Tag) => api.post('/tags', data);

export default api
