export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role_id: number | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at: string;
  last_login: string | null;
}

export interface CreateUserRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  is_active?: boolean;
  is_verified?: boolean;
}

export interface Role {
  id: number;
  role_name: string;
  role_description: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface RoleMapping {
  id: number;
  user_id: number;
  role_id: number;
  is_active: boolean;
  assigned_at: string;
  assigned_by: number | null;
  revoked_at: string | null;
  revoked_by: number | null;
}

export interface AssignRoleRequest {
  user_id: number;
  role_id: number;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
}

export interface ApiError {
  success: false;
  error: string;
}
