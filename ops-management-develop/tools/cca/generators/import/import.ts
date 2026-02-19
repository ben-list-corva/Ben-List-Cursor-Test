import { join } from 'node:path';
import { ApplicationGenerator } from '../lib/application-generator/create-app';
import { GitRepositorySource } from './lib/git-repository-source';
import { ImportDcAppGeneratorSchema } from './schema';
import { Tree } from '@nx/devkit';
import { getProjectName } from './lib/get-project-name';

export async function importDcAppGenerator(
  tree: Tree,
  options: ImportDcAppGeneratorSchema
) {
  const name = getProjectName(options.repository);
  const root = join('apps', name);

  const source = new GitRepositorySource({ url: options.repository });

  return ApplicationGenerator.build({ tree, source, name, root });
}

export default importDcAppGenerator;
