export enum UserRole {
    Administrator = "Administrator",
    School_Timetable_Committee = "School_Timetable_Committee",
    Course_Timetable_Committee = "Course_Timetable_Committee",
    Teacher = "Teacher",
  }

export interface User {
    user_id: number;
    username: string;
    password_hash?: string; // Optional if not sending hash
    role: UserRole;
    school_id?: number | null;
    course_id?: number | null;
  }