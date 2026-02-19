import {
  CreateNodesContextV2,
  CreateNodesV2,
  TargetConfiguration,
  createNodesFromFiles,
} from '@nx/devkit';
import { readdirSync, readFileSync } from 'fs';
import { dirname, join } from 'path';

// Expected format of the plugin options defined in nx.json
export interface CcaPluginOptions {
  deployTargetName?: string;
}

// File glob to find all the configuration files for this plugin
// We'll look for package.json files to identify projects
const projectConfigGlob = '**/package.json';

// Entry function that Nx calls to modify the graph
export const createNodesV2: CreateNodesV2<CcaPluginOptions> = [
  projectConfigGlob,
  async (configFiles, options, context) => {
    return await createNodesFromFiles(
      (configFile, options, context) =>
        createNodesInternal(configFile, options || {}, context),
      configFiles,
      options,
      context
    );
  },
];

async function createNodesInternal(
  configFilePath: string,
  options: CcaPluginOptions,
  context: CreateNodesContextV2
) {
  const projectRoot = dirname(configFilePath);

  // Do not create a project if project.json isn't there or if it's not a valid project
  const siblingFiles = readdirSync(join(context.workspaceRoot, projectRoot));
  if (!siblingFiles.includes('project.json')) {
    return {};
  }

  // Check if the project has a build target by looking for manifest.json and package.json
  const hasBuildTarget =
    siblingFiles.includes('manifest.json') &&
    siblingFiles.includes('package.json');

  // Only add deploy target if the project has build capabilities
  if (!hasBuildTarget) {
    return {};
  }

  const manifestContent = readFileSync(
    join(context.workspaceRoot, projectRoot, 'manifest.json'),
    'utf8'
  );

  // Inferred task final output
  const deployTarget: TargetConfiguration = {
    executor: '@corva/cca:deploy',
    dependsOn: ['build'],
    options: {
      manifest: manifestContent,
      // Default options for deployment
      // These can be overridden in project.json or when running the command
    },
  };

  // Project configuration to be merged into the rest of the Nx configuration
  return {
    projects: {
      [projectRoot]: {
        targets: {
          [options.deployTargetName || 'deploy']: deployTarget,
        },
      },
    },
  };
}
