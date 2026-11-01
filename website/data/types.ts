export interface HardwareSpec {
  icon: string;
  label: string;
  value: string;
  detail?: string;
}

export interface SoftwareItem {
  name: string;
  version: string;
  category: string;
  note: string;
  url?: string;
}

export interface ObsLayerSegment {
  text: string;
  url?: string;
}

export interface ObsLayerItem {
  segments: ObsLayerSegment[];
}

export interface ObsPlugin {
  name: string;
  version: string;
  source: "OBS 内置" | "第三方" | "OBS 生态";
  purpose: string;
  url?: string;
}

export interface ProjectCardData {
  name: string;
  version: string;
  description: string;
  repo: string;
  preview: string;
  accent: string;
  topics: string[];
}
