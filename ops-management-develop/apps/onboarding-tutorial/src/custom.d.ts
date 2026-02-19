// CSS Module declarations
declare module '*.module.css' {
  const classes: { readonly [key: string]: string };
  export default classes;
}

declare module '*.css';
declare module '*.svg';
declare module '*.png';
declare module '*.jpg';
declare module '*.jpeg';
declare module '*.gif';

// Corva UI declarations
declare module '@corva/ui/componentsV2' {
  export const AppContainer: React.FC<{
    header?: React.ReactNode;
    testId?: string;
    children: React.ReactNode;
  }>;
  export const AppHeader: React.FC;
}

declare module '@corva/ui/effects' {
  export function useAppCommons(): {
    appKey: string;
  };
}

declare module '@corva/ui/clients' {
  export const corvaDataAPI: {
    get: <T = unknown>(url: string, params?: Record<string, unknown>) => Promise<T>;
    post: <T = unknown>(url: string, data?: unknown) => Promise<T>;
    put: <T = unknown>(url: string, data?: unknown) => Promise<T>;
    delete: <T = unknown>(url: string) => Promise<T>;
  };
  
  export const socketClient: {
    subscribe: (
      config: { provider: string; dataset: string; assetId: number },
      callbacks: { onDataReceive: (event: { data: unknown[] }) => void }
    ) => (() => void) | undefined;
  };
}
