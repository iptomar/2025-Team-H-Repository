export interface Room {
    room_id: number;
    name: string;
    capacity: number;
    location_id: number;
    owner_course_id: number | null;
}