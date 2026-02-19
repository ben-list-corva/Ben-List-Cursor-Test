import { join } from 'path';
import { CorvaSourcesGenerator } from '../../lib/types';
import { tmpdir } from 'os';
import { mkdtemp } from 'fs/promises';
import { createCommand } from '@corva/create-app/lib/commands/create';
import { CreateGeneratorSchema } from '../schema';

export class CreateCorvaApp implements CorvaSourcesGenerator {
  constructor(private readonly props: CreateGeneratorSchema) {}

  async install() {
    const tmpPath = await mkdtemp(join(tmpdir(), 'import-'));

    const cmd = [
      tmpPath,
      '--no-dependencies-install',
      '--no-git-init',
      '--appType',
      'ui',
      '--segments',
      this.props.segment,
      '--runtime',
      'ui',
      '--appKey',
      getAppKey(this.props),
      '--appName',
      this.props.name,
      '--category',
      this.props.category,
      '-t',
      '--silent',
    ];

    await createCommand.parseAsync(cmd, { from: 'user' });

    return tmpPath;
  }
}

const getAppKey = (props: CreateGeneratorSchema) => {
  if (props.key) {
    return props.key;
  }

  return `${props.provider || 'corva'}.${props.name
    .toLowerCase()
    .replace(/[^a-z\d]/g, '_')}.ui`;
};
