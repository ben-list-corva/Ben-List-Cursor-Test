import {
  addProjectConfiguration,
  formatFiles,
  generateFiles,
  Tree,
} from '@nx/devkit';
import * as path from 'path';
import { CreateGeneratorSchema } from './schema';
import { join } from 'path';
import { CreateCorvaApp } from './lib/create-corva-app-source';
import { ApplicationGenerator } from '../lib/application-generator/create-app';

export async function createGenerator(
  tree: Tree,
  options: CreateGeneratorSchema
) {
  const name = options.name.toLowerCase().replace(/[^a-z\d]/g, '-');
  const root = join('apps', name);

  const source = new CreateCorvaApp(options);

  return ApplicationGenerator.build({ tree, source, name, root });
}

export default createGenerator;
