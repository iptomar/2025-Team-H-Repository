import {
  UserRole,
  ClassType,
  ApprovalStatus,
  EventType,
  TimetablePhase,
} from './types';

import type {
  LocationCreate,
  LocationUpdate,
  Location,
  SchoolCreate,
  SchoolUpdate,
  School,
  UserCreate,
  UserUpdate,
  User,
  CourseCreate,
  CourseUpdate,
  Course,
  SubjectCreate,
  SubjectUpdate,
  Subject,
  RoomCreate,
  RoomUpdate,
  Room,
  ClassCreate,
  ClassUpdate,
  Class,
  ApprovalCreate,
  ApprovalResponse,
  Approval,
  ApiError,
  UserLogin,
  TokenResponse
} from './types';

const BASE_URL = 'http://localhost:8000';

class ApiClient {
  private token: string | null = null;

  constructor() {
    // Load token from localStorage on initialization
    if (typeof window !== 'undefined') {
      this.token = localStorage.getItem('access_token');
    }
  }

  private getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${BASE_URL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        ...this.getAuthHeaders(),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        // Handle authentication errors
        if (response.status === 401) {
          this.clearToken();
          throw new Error('Authentication failed. Please login again.');
        }

        const error: ApiError = await response.json().catch(() => ({ 
          detail: `HTTP ${response.status}: ${response.statusText}` 
        }));
        throw new Error(error.detail);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('An unexpected error occurred');
    }
  }

  setToken(token: string): void {
    this.token = token;
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', token);
    }
  }

  clearToken(): void {
    this.token = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
  }

  getToken(): string | null {
    return this.token;
  }

  isAuthenticated(): boolean {
    return this.token !== null;
  }

  // Authentication endpoints
  async login(credentials: UserLogin): Promise<TokenResponse> {
    const response = await this.request<TokenResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    // Automatically set the token
    this.setToken(response.access_token);
    
    return response;
  }

  async register(userData: UserCreate): Promise<User> {
    return this.request<User>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/auth/me');
  }

  logout(): void {
    this.clearToken();
  }

  // Location endpoints
  async createLocation(data: LocationCreate): Promise<Location> {
    return this.request<Location>('/locations/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getLocations(skip = 0, limit = 100): Promise<Location[]> {
    return this.request<Location[]>(`/locations/?skip=${skip}&limit=${limit}`);
  }

  async getLocation(id: number): Promise<Location> {
    return this.request<Location>(`/locations/${id}`);
  }

  async updateLocation(id: number, data: LocationUpdate): Promise<Location> {
    return this.request<Location>(`/locations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteLocation(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/locations/${id}`, {
      method: 'DELETE',
    });
  }

  // School endpoints
  async createSchool(data: SchoolCreate): Promise<School> {
    return this.request<School>('/schools/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getSchools(skip = 0, limit = 100): Promise<School[]> {
    return this.request<School[]>(`/schools/?skip=${skip}&limit=${limit}`);
  }

  async getSchool(id: number): Promise<School> {
    return this.request<School>(`/schools/${id}`);
  }

  async updateSchool(id: number, data: SchoolUpdate): Promise<School> {
    return this.request<School>(`/schools/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteSchool(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/schools/${id}`, {
      method: 'DELETE',
    });
  }

  // User endpoints
  async createUser(data: UserCreate): Promise<User> {
    return this.request<User>('/users/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getUsers(skip = 0, limit = 100): Promise<User[]> {
    return this.request<User[]>(`/users/?skip=${skip}&limit=${limit}`);
  }

  async getUser(id: number): Promise<User> {
    return this.request<User>(`/users/${id}`);
  }

  async updateUser(id: number, data: UserUpdate): Promise<User> {
    return this.request<User>(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteUser(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/users/${id}`, {
      method: 'DELETE',
    });
  }

  // Course endpoints
  async createCourse(data: CourseCreate): Promise<Course> {
    return this.request<Course>('/courses/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getCourses(skip = 0, limit = 100): Promise<Course[]> {
    return this.request<Course[]>(`/courses/?skip=${skip}&limit=${limit}`);
  }

  async getCourse(id: number): Promise<Course> {
    return this.request<Course>(`/courses/${id}`);
  }

  async updateCourse(id: number, data: CourseUpdate): Promise<Course> {
    return this.request<Course>(`/courses/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteCourse(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/courses/${id}`, {
      method: 'DELETE',
    });
  }

  // Subject endpoints
  async createSubject(data: SubjectCreate): Promise<Subject> {
    return this.request<Subject>('/subjects/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getSubjects(skip = 0, limit = 100): Promise<Subject[]> {
    return this.request<Subject[]>(`/subjects/?skip=${skip}&limit=${limit}`);
  }

  async getSubject(id: number): Promise<Subject> {
    return this.request<Subject>(`/subjects/${id}`);
  }

  async updateSubject(id: number, data: SubjectUpdate): Promise<Subject> {
    return this.request<Subject>(`/subjects/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteSubject(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/subjects/${id}`, {
      method: 'DELETE',
    });
  }

  // Room endpoints
  async createRoom(data: RoomCreate): Promise<Room> {
    return this.request<Room>('/rooms/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getRooms(skip = 0, limit = 100): Promise<Room[]> {
    return this.request<Room[]>(`/rooms/?skip=${skip}&limit=${limit}`);
  }

  async getRoom(id: number): Promise<Room> {
    return this.request<Room>(`/rooms/${id}`);
  }

  async updateRoom(id: number, data: RoomUpdate): Promise<Room> {
    return this.request<Room>(`/rooms/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteRoom(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/rooms/${id}`, {
      method: 'DELETE',
    });
  }

  // Class endpoints
  async createClass(data: ClassCreate): Promise<Class> {
    return this.request<Class>('/classes/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getClasses(skip = 0, limit = 100): Promise<Class[]> {
    return this.request<Class[]>(`/classes/?skip=${skip}&limit=${limit}`);
  }

  async getClass(id: number): Promise<Class> {
    return this.request<Class>(`/classes/${id}`);
  }

  async updateClass(id: number, data: ClassUpdate): Promise<Class> {
    return this.request<Class>(`/classes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async deleteClass(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/classes/${id}`, {
      method: 'DELETE',
    });
  }

  // Approval endpoints
  async createApproval(data: ApprovalCreate): Promise<Approval> {
    return this.request<Approval>('/approvals/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getApprovals(skip = 0, limit = 100): Promise<Approval[]> {
    return this.request<Approval[]>(`/approvals/?skip=${skip}&limit=${limit}`);
  }

  async getApproval(id: number): Promise<Approval> {
    return this.request<Approval>(`/approvals/${id}`);
  }

  async respondToApproval(id: number, response: ApprovalResponse): Promise<Approval> {
    return this.request<Approval>(`/approvals/${id}/respond`, {
      method: 'PUT',
      body: JSON.stringify(response),
    });
  }

  async deleteApproval(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/approvals/${id}`, {
      method: 'DELETE',
    });
  }

  async getPendingApprovals(): Promise<Approval[]> {
    return this.request<Approval[]>('/approvals/pending');
  }

  // Utility endpoints
  async getUserClasses(userId: number): Promise<Class[]> {
    return this.request<Class[]>(`/users/${userId}/classes`);
  }

  async getRoomClasses(roomId: number): Promise<Class[]> {
    return this.request<Class[]>(`/rooms/${roomId}/classes`);
  }

  async getSubjectClasses(subjectId: number): Promise<Class[]> {
    return this.request<Class[]>(`/subjects/${subjectId}/classes`);
  }
}

// Create singleton instance
export const apiClient = new ApiClient();

// Authentication helper functions
export const auth = {
  login: async (credentials: UserLogin): Promise<TokenResponse> => {
    return apiClient.login(credentials);
  },
  
  register: async (userData: UserCreate): Promise<User> => {
    return apiClient.register(userData);
  },
  
  logout: (): void => {
    apiClient.logout();
  },
  
  getCurrentUser: async (): Promise<User> => {
    return apiClient.getCurrentUser();
  },
  
  isAuthenticated: (): boolean => {
    return apiClient.isAuthenticated();
  },
  
  getToken: (): string | null => {
    return apiClient.getToken();
  }
};

// Convenience functions for common operations
export const locations = {
  create: (data: LocationCreate) => apiClient.createLocation(data),
  getAll: (skip?: number, limit?: number) => apiClient.getLocations(skip, limit),
  getById: (id: number) => apiClient.getLocation(id),
  update: (id: number, data: LocationUpdate) => apiClient.updateLocation(id, data),
  delete: (id: number) => apiClient.deleteLocation(id),
};

export const schools = {
  create: (data: SchoolCreate) => apiClient.createSchool(data),
  getAll: (skip?: number, limit?: number) => apiClient.getSchools(skip, limit),
  getById: (id: number) => apiClient.getSchool(id),
  update: (id: number, data: SchoolUpdate) => apiClient.updateSchool(id, data),
  delete: (id: number) => apiClient.deleteSchool(id),
};

export const users = {
  create: (data: UserCreate) => apiClient.createUser(data),
  getAll: (skip?: number, limit?: number) => apiClient.getUsers(skip, limit),
  getById: (id: number) => apiClient.getUser(id),
  update: (id: number, data: UserUpdate) => apiClient.updateUser(id, data),
  delete: (id: number) => apiClient.deleteUser(id),
  getClasses: (userId: number) => apiClient.getUserClasses(userId),
};

export const courses = {
  create: (data: CourseCreate) => apiClient.createCourse(data),
  getAll: (skip?: number, limit?: number) => apiClient.getCourses(skip, limit),
  getById: (id: number) => apiClient.getCourse(id),
  update: (id: number, data: CourseUpdate) => apiClient.updateCourse(id, data),
  delete: (id: number) => apiClient.deleteCourse(id),
};

export const subjects = {
  create: (data: SubjectCreate) => apiClient.createSubject(data),
  getAll: (skip?: number, limit?: number) => apiClient.getSubjects(skip, limit),
  getById: (id: number) => apiClient.getSubject(id),
  update: (id: number, data: SubjectUpdate) => apiClient.updateSubject(id, data),
  delete: (id: number) => apiClient.deleteSubject(id),
  getClasses: (subjectId: number) => apiClient.getSubjectClasses(subjectId),
};

export const rooms = {
  create: (data: RoomCreate) => apiClient.createRoom(data),
  getAll: (skip?: number, limit?: number) => apiClient.getRooms(skip, limit),
  getById: (id: number) => apiClient.getRoom(id),
  update: (id: number, data: RoomUpdate) => apiClient.updateRoom(id, data),
  delete: (id: number) => apiClient.deleteRoom(id),
  getClasses: (roomId: number) => apiClient.getRoomClasses(roomId),
};

export const classes = {
  create: (data: ClassCreate) => apiClient.createClass(data),
  getAll: (skip?: number, limit?: number) => apiClient.getClasses(skip, limit),
  getById: (id: number) => apiClient.getClass(id),
  update: (id: number, data: ClassUpdate) => apiClient.updateClass(id, data),
  delete: (id: number) => apiClient.deleteClass(id),
};

export const approvals = {
  create: (data: ApprovalCreate) => apiClient.createApproval(data),
  getAll: (skip?: number, limit?: number) => apiClient.getApprovals(skip, limit),
  getById: (id: number) => apiClient.getApproval(id),
  respond: (id: number, response: ApprovalResponse) => apiClient.respondToApproval(id, response),
  delete: (id: number) => apiClient.deleteApproval(id),
  getPending: () => apiClient.getPendingApprovals(),
};

// Example usage:
/*
// Login
try {
  const loginResponse = await auth.login({
    username: "john_doe",
    password: "securepassword"
  });
  console.log("Login successful:", loginResponse.user);
  console.log("Token expires in:", loginResponse.expires_in, "seconds");
} catch (error) {
  console.error("Login failed:", error.message);
}

// Register a new user
try {
  const newUser = await auth.register({
    username: "jane_doe",
    password: "securepassword",
    role: UserRole.Teacher,
    school_id: 1
  });
  console.log("User registered:", newUser);
} catch (error) {
  console.error("Registration failed:", error.message);
}

// Check if user is authenticated
if (auth.isAuthenticated()) {
  // User is logged in, can make authenticated requests
  const currentUser = await auth.getCurrentUser();
  console.log("Current user:", currentUser);
} else {
  // User needs to login
  console.log("Please login first");
}

// Get all schools (requires authentication)
try {
  const allSchools = await schools.getAll();
  console.log("Schools:", allSchools);
} catch (error) {
  console.error("Failed to fetch schools:", error.message);
}

// Logout
auth.logout();
console.log("User logged out");
*/
