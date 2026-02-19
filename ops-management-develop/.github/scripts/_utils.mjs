import * as path from 'path';
import { readFile, rm } from 'fs/promises';

export async function getAffectedProjects(core, exec) {
  core.info('Loading the list of affected projects from NX...');
  const { stdout: affectedProjectsRaw } = await exec.getExecOutput(
    'npx',
    [
      'nx',
      'show',
      'projects',
      '--affected',
      '--type=app',
      "--exclude='*-e2e'",
      '--json',
    ],
    { silent: true }
  );
  const affectedProjects = JSON.parse(affectedProjectsRaw);
  core.info(`Found affected projects: ${affectedProjects}`);
  return affectedProjects;
}

export async function getManualProjects(core, projectString) {
  core.info('Loading the list of affected projects supplied manually...');
  const affectedProjects = projectString
    .split(',')
    .map((project) => project.trim().replace(/['"]/g, ''));
  core.info(`Found affected projects: ${affectedProjects}`);
  return affectedProjects;
}

export async function getProjectsDefinitions(core, exec, projectList) {
  const projectGraphFile = './graph.json';
  await exec.exec('npx', ['nx', 'graph', `--file=${projectGraphFile}`], {
    silent: true,
  });
  const projectGraphRaw = await readFile(path.resolve(projectGraphFile), {
    encoding: 'utf8',
  });
  const projectGraph = JSON.parse(projectGraphRaw);
  await rm(path.resolve(projectGraphFile));

  const projectsDefinitions = [];
  for (const project of projectList) {
    if (!Object.keys(projectGraph.graph.nodes).includes(project)) {
      core.setFailed(`${project} does not seem to be a valid project name`);
      process.exit();
    }

    const projectDefinition = projectGraph.graph.nodes[project].data;
    if (projectDefinition.metadata) {
      delete projectDefinition.targets;
      projectsDefinitions.push(projectDefinition);
    } else {
      core.setFailed(
        `Project ${projectDefinition.name} has no metadata defined!`
      );
      process.exit();
    }
  }
  core.debug(projectsDefinitions);

  const sortedProjectsDefinitions = projectsDefinitions.reduce((acc, cur) => {
    acc[cur.metadata.type] = [...(acc[cur.metadata.type] || []), cur];
    return acc;
  }, {});
  core.info(
    `Sorted affected projects: ${JSON.stringify(sortedProjectsDefinitions)}`
  );
  return sortedProjectsDefinitions;
}

export async function setProjectsOutputs(
  core,
  projectTypes,
  projectDefinitions
) {
  projectTypes.map((projectType) => {
    core.setOutput(
      `hasAffected${capitalizeFirstLetter(projectType)}s`,
      Object.hasOwn(projectDefinitions, projectType)
    );
    core.setOutput(
      `affected${capitalizeFirstLetter(projectType)}s`,
      projectDefinitions[projectType]
        ? { include: projectDefinitions[projectType] }
        : []
    );
  });
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
