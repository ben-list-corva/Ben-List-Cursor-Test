export default async (
  { github, context, core, glob, io, exec, require },
  { _utils, _constants }
) => {
  const { PROJECTS, REF_NAME } = process.env;

  let affectedProjects;
  if (context.ref.startsWith('refs/tags')) {
    core.info('Loading the list of affected projects from Git tag...');
    affectedProjects = [context.ref.replace('refs/tags/', '').split('@')[0]];
    core.info(`Found affected projects: ${affectedProjects}`);
    const regexp = new RegExp('^(?:.*?@)?(.+)$');
    const version = REF_NAME.match(regexp)[1];
    core.info(`Extracted version ${version} from tag ${REF_NAME}`);
    core.setOutput('version', version);
  } else if (PROJECTS) {
    affectedProjects = await _utils.getManualProjects(core, PROJECTS);
  } else {
    affectedProjects = await _utils.getAffectedProjects(core, exec);
  }

  const projectDefinitions = await _utils.getProjectsDefinitions(
    core,
    exec,
    affectedProjects
  );
  await _utils.setProjectsOutputs(
    core,
    _constants.PROJECT_TYPES,
    projectDefinitions
  );

  core.setOutput(
    'timestamp',
    new Date()
      .toISOString()
      .replace(/[-:T.Z]/g, '')
      .slice(0, 14)
  );
};
