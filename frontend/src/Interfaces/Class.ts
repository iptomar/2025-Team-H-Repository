export interface Class {
    class_id: number;
    subject_id: number;
    class_type: string;
    teacher_id: number;
    room_id: number;
    day_of_week?: number; 
    date?: string;        
    start_time: string;   
    end_time: string;     
    is_recurring: boolean;
    approval_status: string;
    version_id?: number;
  
    subject?: any;
    teacher?: any;
    room?: any;
    version?: any;
    approvals?: any[];
    class_groups?: any[];
  }
  