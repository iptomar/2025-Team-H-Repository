import { UserRole } from './userRole';

export interface User {
  userId: number;
  username: string;
  role: UserRole;
  schoolId?: number | null;
  courseId?: number | null;
}