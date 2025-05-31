import { writable, get } from 'svelte/store';
import type { User } from '../Interfaces/auth/user';
import type { Token } from '../Interfaces/auth/token';
import type { RegisterData } from '../Interfaces/auth/registerData';
import type { LoginData } from '../Interfaces/auth/loginData';

const API_URL = 'http://localhost:8000/auth';

// Main auth store
const auth = writable<{
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
}>({
  user: null,
  token: localStorage.getItem('token') || null,
  isLoading: false,
  error: null,
});

async function register(data: RegisterData): Promise<User | null> {
  auth.update((state) => ({ ...state, isLoading: true, error: null }));
  try {
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const errorData = await res.json();
      auth.update((state) => ({
        ...state,
        isLoading: false,
        error: errorData.detail || 'Registration failed',
      }));
      return null;
    }
    const created = await res.json();
    auth.update((state) => ({ ...state, user: created, isLoading: false }));
    return created;
  } catch (error) {
    auth.update((state) => ({
      ...state,
      isLoading: false,
      error: 'Registration failed: ' + (error instanceof Error ? error.message : 'Unknown error'),
    }));
    return null;
  }
}

async function login(data: LoginData): Promise<boolean> {
  auth.update((state) => ({ ...state, isLoading: true, error: null }));
  try {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        username: data.username,
        password: data.password,
      }).toString(),
    });
    if (!res.ok) {
      const errorData = await res.json();
      auth.update((state) => ({
        ...state,
        isLoading: false,
        error: errorData.detail || 'Login failed',
      }));
      return false;
    }
    const token: Token = await res.json();
    localStorage.setItem('token', token.accessToken);
    auth.update((state) => ({ ...state, token: token.accessToken }));

    // Fetch user details after login
    const user = await checkToken();
    return !!user;
  } catch (error) {
    auth.update((state) => ({
      ...state,
      isLoading: false,
      error: 'Login failed: ' + (error instanceof Error ? error.message : 'Unknown error'),
    }));
    return false;
  }
}

async function checkToken(): Promise<User | null> {
  const state = get(auth);
  if (!state.token) {
    auth.update((state) => ({ ...state, user: null, error: 'No token found' }));
    return null;
  }
  auth.update((state) => ({ ...state, isLoading: true, error: null }));
  try {
    const res = await fetch(`${API_URL}/token_checker`, {
      headers: { Authorization: `Bearer ${state.token}` },
    });
    if (!res.ok) {
      const errorData = await res.json();
      auth.update((state) => ({
        ...state,
        user: null,
        token: null,
        isLoading: false,
        error: errorData.detail || 'Token validation failed',
      }));
      localStorage.removeItem('token');
      return null;
    }
    const user: User = await res.json();
    auth.update((state) => ({ ...state, user, isLoading: false }));
    return user;
  } catch (error) {
    auth.update((state) => ({
      ...state,
      user: null,
      token: null,
      isLoading: false,
      error: 'Token validation failed: ' + (error instanceof Error ? error.message : 'Unknown error'),
    }));
    localStorage.removeItem('token');
    return null;
  }
}

function logout() {
  localStorage.removeItem('token');
  auth.set({ user: null, token: null, isLoading: false, error: null });
}

export const authStore = {
  auth,
  register,
  login,
  checkToken,
  logout,
};