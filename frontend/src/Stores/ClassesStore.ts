import { writable } from 'svelte/store';
import type { Class } from '../Interfaces/Class';

const API_URL = 'http://localhost:8000/classes';

// Main class list store
const classes = writable<Class[]>([]);

async function fetchAllClasses() {
  const res = await fetch(`${API_URL}`);
  const data = await res.json();
  classes.set(data);
}

async function fetchOneClass(id: number): Promise<Class | null> {
  const res = await fetch(`${API_URL}/${id}`);
  if (!res.ok) return null;
  return res.json();
}

async function createClass(newClass: Omit<Class, 'class_id'>) {
  const res = await fetch(`${API_URL}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newClass),
  });
  const created = await res.json();
  classes.update((list) => [...list, created]);
  return created;
}

async function updateClass(id: number, updates: Partial<Class>) {
  const res = await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates),
  });
  const updated = await res.json();
  classes.update((list) =>
    list.map((c) => (c.class_id === id ? updated : c))
  );
  return updated;
}

async function deleteClass(id: number) {
  const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
  if (res.ok) {
    classes.update((list) => list.filter((c) => c.class_id !== id));
    return true;
  }
  return false;
}

export const classStore = {
  classes,
  fetchAllClasses,
  fetchOneClass,
  createClass,
  updateClass,
  deleteClass,
};
