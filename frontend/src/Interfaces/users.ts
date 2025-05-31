// users.ts

export enum UserRole {
  Administrator = "Administrator",
  SchoolTimetableCommittee = "School_Timetable_Committee",
  CourseTimetableCommittee = "Course_Timetable_Committee",
  Teacher = "Teacher",
}

export interface User {
  userId: number;
  username: string;
  role: UserRole;
  schoolId?: number | null;
  courseId?: number | null;
}