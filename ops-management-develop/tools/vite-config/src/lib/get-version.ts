import { ConfigEnv } from 'vite';

export interface GetVersionArgs {
  mode: ConfigEnv['mode'];
  version: string;
  refName?: string;
}

export const getVersion = ({
  mode,
  version,
  refName,
}: GetVersionArgs): string => {
  if (mode === 'development') {
    return `${version}-development${Date.now()}`;
  }

  if (refName) {
    if (['main', 'develop'].includes(refName)) {
      return `dev-${process.env.GITHUB_SHA!.slice(0, 7)}`;
    }

    if (!refName.includes('@')) {
      return `${refName.replace(/\//g, '|')}`;
    }
  }

  return version;
};
