import { UserRole } from './userRole';

export interface RegisterData {
  username: string;
  password: string;
  role: UserRole;
  schoolId?: number | null;
  courseId?: number | null;
}