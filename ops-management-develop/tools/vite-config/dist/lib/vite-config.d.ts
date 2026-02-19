import 'vitest/node';
interface CreateViteConfigArgs {
  name: string;
  pwd: string;
}
export declare const createViteConfig: ({
  name,
  pwd,
}: CreateViteConfigArgs) => import('vite').UserConfigFnPromise;
export {};
//# sourceMappingURL=vite-config.d.ts.map
