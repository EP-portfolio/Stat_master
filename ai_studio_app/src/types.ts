export enum ViewState {
  HOME = "HOME",
  LESSON = "LESSON",
  PRACTICE = "PRACTICE",
  ASSESSMENT = "ASSESSMENT",
  TUTOR = "TUTOR",
}

export interface DataSet {
  values: number[];
  sortedValues: number[];
  mean: number;
  median: number;
  range: number;
  totalCount: number;
}

export interface ChatMessage {
  role: "user" | "model";
  text: string;
  isError?: boolean;
}

export interface LessonTopic {
  id: string;
  title: string;
  description: string;
  content: React.ReactNode;
}

