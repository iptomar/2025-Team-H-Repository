export enum UserRole {
  Administrator = "Administrator",
  School_Timetable_Committee = "School_Timetable_Committee",
  Course_Timetable_Committee = "Course_Timetable_Committee",
  Teacher = "Teacher"
}

export enum ClassType {
  P = "P",
  T = "T", 
  TP = "TP"
}

export enum ApprovalStatus {
  pending = "pending",
  approved = "approved",
  rejected = "rejected"
}

export enum EventType {
  holiday = "holiday",
  break_ = "break",
  other = "other"
}

export enum TimetablePhase {
  proposal = "proposal",
  adjustment = "adjustment"
}

// Authentication Types
export interface UserLogin {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// Location Types
export interface LocationCreate {
  name: string;
  is_campus?: boolean;
}

export interface LocationUpdate {
  name?: string;
  is_campus?: boolean;
}

export interface Location {
  location_id: number;
  name: string;
  is_campus: boolean;
}

export interface SchoolCreate {
  name: string;
  location_id: number;
}

export interface SchoolUpdate {
  name?: string;
  location_id?: number;
}

export interface School {
  school_id: number;
  name: string;
  location_id: number;
  location?: Location;
}

export interface UserCreate {
  username: string;
  password: string;
  role: UserRole;
  school_id?: number;
  course_id?: number;
}

export interface UserUpdate {
  username?: string;
  role?: UserRole;
  school_id?: number;
  course_id?: number;
  password?: string;
}

export interface User {
  user_id: number;
  username: string;
  role: UserRole;
  school_id?: number;
  course_id?: number;
  school?: School;
}

export interface CourseCreate {
  name: string;
  school_id: number;
  is_short_course?: boolean;
}

export interface CourseUpdate {
  name?: string;
  school_id?: number;
  is_short_course?: boolean;
}

export interface Course {
  course_id: number;
  name: string;
  school_id: number;
  is_short_course: boolean;
  school?: School;
}

export interface SubjectCreate {
  name: string;
  course_id: number;
}

export interface SubjectUpdate {
  name?: string;
  course_id?: number;
}

export interface Subject {
  subject_id: number;
  name: string;
  course_id: number;
  course?: Course;
}

export interface RoomCreate {
  name: string;
  capacity: number;
  location_id: number;
  owner_course_id?: number;
}

export interface RoomUpdate {
  name?: string;
  capacity?: number;
  location_id?: number;
  owner_course_id?: number;
}

export interface Room {
  room_id: number;
  name: string;
  capacity: number;
  location_id: number;
  owner_course_id?: number;
  location?: Location;
  owner_course?: Course;
}

export interface ClassCreate {
  subject_id: number;
  class_type: ClassType;
  teacher_id: number;
  room_id: number;
  day_of_week?: number;
  date?: string;
  start_time: string;
  end_time: string;
  is_recurring?: boolean;
  approval_status?: ApprovalStatus;
  version_id?: number;
  class_group_ids?: number[];
}

export interface ClassUpdate {
  subject_id?: number;
  class_type?: ClassType;
  teacher_id?: number;
  room_id?: number;
  day_of_week?: number;
  date?: string;
  start_time?: string;
  end_time?: string;
  is_recurring?: boolean;
  approval_status?: ApprovalStatus;
  version_id?: number;
  class_group_ids?: number[];
}

export interface Class {
  class_id: number;
  subject_id: number;
  class_type: ClassType;
  teacher_id: number;
  room_id: number;
  day_of_week?: number;
  date?: string;
  start_time: string;
  end_time: string;
  is_recurring: boolean;
  approval_status: ApprovalStatus;
  version_id?: number;
  subject?: Subject;
  teacher?: User;
  room?: Room;
}

export interface ApprovalCreate {
  class_id: number;
  requested_by: number;
  notes?: string;
}

export interface ApprovalResponse {
  approved_by: number;
  status: ApprovalStatus;
  notes?: string;
}

export interface Approval {
  approval_id: number;
  class_id: number;
  requested_by: number;
  approved_by?: number;
  status: ApprovalStatus;
  request_date: string;
  response_date?: string;
  notes?: string;
}

export interface ApiError {
  detail: string;
}

