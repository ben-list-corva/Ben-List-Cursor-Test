import { ConfigEnv } from 'vite';
export interface GetVersionArgs {
    mode: ConfigEnv['mode'];
    version: string;
    refName?: string;
}
export declare const getVersion: ({ mode, version, refName, }: GetVersionArgs) => string;
//# sourceMappingURL=get-version.d.ts.map