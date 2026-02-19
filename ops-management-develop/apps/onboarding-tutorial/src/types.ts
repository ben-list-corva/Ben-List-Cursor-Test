/**
 * Corva Platform Type Definitions
 * 
 * Based on Corva FE Rules documentation
 */

// ============ WELL ============
export interface Well {
  name: string;
  asset_id: number;
  id: string;
  status: string;
  last_active_at: string;
  settings?: WellSettings;
}

export interface WellSettings {
  [key: string]: unknown;
}

// ============ RIG (Drilling) ============
export interface Rig {
  name: string;
  id: string;
  asset_id: number;
}

// ============ FRAC FLEET (Completion) ============
export interface FracFleet {
  type: string;
  id: string;
  name: string;
  current_pad_id: number;
  program: Program;
  pad_frac_fleets: PadFracFleet[];
}

export interface Program {
  id: number;
  name: string;
}

export interface PadFracFleet {
  id: number;
  pad_id: number;
}

// ============ USER ============
export interface User {
  id: number;
  company_id: number;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
  settings: UserSettings;
  company: CompanyInfo;
}

export interface UserSettings {
  [key: string]: unknown;
}

export interface CompanyInfo {
  id: number;
  name: string;
}

// ============ COORDINATES ============
export interface Coordinates {
  w: number;
  h: number;
  x: number;
  y: number;
  pixelHeight: number;
  pixelWidth: number;
}

// ============ APP INSTANCE ============
export interface AppInstance {
  id: number;
  app: { app_key: string; platform: string };
  package: AppManifestPackage;
  settings: Record<string, unknown>;
}

export interface AppManifestPackage {
  name: string;
  version: string;
}

// ============ LAYOUT ENVIRONMENT ============
export interface LayoutEnvironment {
  type: string;
  [key: string]: unknown;
}

// ============ DEV CENTER ROUTER ============
export interface DevCenterRouter {
  push: (path: string) => void;
  replace: (path: string) => void;
  [key: string]: unknown;
}

// ============ MENU ITEMS ============
export interface MenuItem {
  key: string;
  label: string;
  icon?: React.ReactNode;
  onClick?: () => void;
}

// ============ APP HEADER DATA ============
export interface AppHeaderData {
  title?: string;
  well?: Well;
  [key: string]: unknown;
}

// ============ MAIN APP PROPS ============
export interface AppProps {
  // ============ COMPLETION SEGMENT (Frac) ============
  fracFleet?: FracFleet;
  wells?: Well[];
  fracFleetId?: number;
  padId?: number;

  // ============ DRILLING SEGMENT ============
  rig?: Rig;
  rigId?: number;
  wellId?: number;

  // ============ SHARED ============
  well?: Well;

  // ============ COMMON PROPS ============
  app: AppInstance;
  package: string;
  coordinates: Coordinates;
  currentUser: User;
  devCenterRouter: DevCenterRouter;
  segment: string;
  appHeaderProps: AppHeaderData;
  isNative: boolean;
  layoutEnvironment: LayoutEnvironment;

  // ============ METHODS ============
  onSettingChange: (key: string, value: unknown) => void;
  onSettingsChange: (settings: Record<string, unknown>) => void;
  setIsFullscreenModalMode: (isFullscreenModalMode: boolean) => Promise<void>;
  setIsMaximized: (isMaximized: boolean) => void;
  setMainMenuItems: (mainMenuItems: MenuItem[]) => void;
  setSecondaryMenuItems: (secondaryMenuItems: MenuItem[]) => void;
}

// ============ APP SETTINGS PROPS ============
export interface AppSettingsProps {
  settings: Record<string, unknown>;
  onSettingChange: (key: string, value: unknown) => void;
  onSettingsChange: (settings: Record<string, unknown>) => void;
}

// ============ CUSTOM APP SETTINGS ============
export interface CustomAppSettings {
  showProgress?: boolean;
}

// ============ DATA RECORD ============
export interface DataRecord {
  _id: string;
  company_id: number;
  asset_id: number;
  timestamp: number;
  data: Record<string, unknown>;
}

// ============ TRAINING PROGRESS ============
export interface TrainingProgressRecord {
  _id?: string;
  user_id: number;
  module_slug: string;
  section_id: string;
  completed: boolean;
  quiz_score?: number;
  completed_at?: string;
  timestamp?: number;
}

// ============ TRAINING MODULE ============
export interface TrainingModule {
  moduleSlug: string;
  title: string;
  sections: TrainingSection[];
}

export interface TrainingSection {
  id: string;
  title: string;
  order: number;
  content: ContentBlock[];
  images: ImageReference[];
  subsections?: TrainingSubsection[];
  quiz?: QuizQuestion[];
}

export interface TrainingSubsection {
  id: string;
  title: string;
  order: number;
  content: ContentBlock[];
  images: ImageReference[];
}

export interface ContentBlock {
  type: string;
  body?: string;
  heading?: string;
  items?: string[];
  [key: string]: unknown;
}

export interface ImageReference {
  localPath: string;
  figureNumber?: string;
  caption?: string;
}

export interface QuizQuestion {
  id: string;
  question: string;
  type: 'single' | 'multi';
  choices: QuizChoice[];
  correctAnswer?: string;
  correctAnswers?: string[];
  explanation?: string;
}

export interface QuizChoice {
  id: string;
  text: string;
}
