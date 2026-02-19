import { $ } from 'execa';
import { mkdtemp } from 'fs/promises';
import { tmpdir } from 'os';
import { join } from 'path';
import { CorvaSourcesGenerator } from '../../lib/types';

interface GitRepositoryProps {
  url: string;
}

export class GitRepositorySource implements CorvaSourcesGenerator {
  constructor(private readonly props: GitRepositoryProps) {}

  async install() {
    const tmpPath = await mkdtemp(join(tmpdir(), 'import-'));
    await $`git clone ${this.props.url} ${tmpPath}`;
    return tmpPath;
  }
}
