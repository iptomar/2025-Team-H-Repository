import { writable } from 'svelte/store';
import type { Room } from '../Interfaces/Room';

export const rooms = writable<Room[]>([]);

export async function fetchRooms() {
    const response = await fetch('http://localhost:8000/rooms');
    const data: Room[] = await response.json();
    rooms.set(data);
}

export async function createRoom(room: Omit<Room, 'room_id'>) {
    const response = await fetch('http://localhost:8000/rooms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(room),
    });
    const newRoom: Room = await response.json();
    rooms.update((current) => [...current, newRoom]);
}

export async function updateRoom(room_id: number, room: Partial<Room>) {
    const response = await fetch(`http://localhost:8000/rooms/${room_id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(room),
    });
    const updatedRoom: Room = await response.json();
    rooms.update((current) =>
        current.map((r) => (r.room_id === room_id ? updatedRoom : r))
    );
}

export async function deleteRoom(room_id: number) {
    await fetch(`http://localhost:8000/rooms/${room_id}`, { method: 'DELETE' });
    rooms.update((current) => current.filter((r) => r.room_id !== room_id));
}