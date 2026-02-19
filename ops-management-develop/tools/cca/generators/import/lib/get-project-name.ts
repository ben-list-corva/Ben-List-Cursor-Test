import { logger } from '@nx/devkit';
import { basename } from 'node:path';

export const getProjectName = (repository: string) => {
  // Extract the project name from the repo URL using the given pattern.
  // The project name should be the basename of the repo, with the prefix ^([a-z]-)?dc-fe- removed.
  // Example: "git@github.com:org/a-dc-fe-foo-bar.git" -> "foo-bar"
  // Example: "https://github.com/org/dc-fe-baz.git" -> "baz"
  // This code is simple and uses regex for clarity.

  // Get the repo basename (strip trailing .git if present)
  const repoBase = basename(repository).replace(/\.git$/, '');

  // Remove the prefix using regex as specified
  const projectName = repoBase.replace(/^([a-z-]+)?dc-fe-/, '');

  // Log for debugging and clarity
  logger.info(`Derived project name: ${projectName}`);

  return projectName;
};
