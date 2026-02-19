export default async (
  { github, context, core, glob, io, exec, require },
  { _utils, _constants }
) => {
  const affectedProjects = await _utils.getAffectedProjects(core, exec);

  const prLabelsRaw = await github.rest.issues.listLabelsOnIssue({
    owner: context.issue.owner,
    repo: context.issue.repo,
    issue_number: context.issue.number,
  });
  core.debug(prLabelsRaw);

  const nonProjectLabels = prLabelsRaw.data.map((label) => {
    if (!label.name.startsWith('project:')) {
      return label.name;
    }
  });

  const finalLabels = nonProjectLabels
    .concat(affectedProjects.map((project) => `project:${project}`))
    .filter(Boolean);
  core.info(`Setting final set of labels: ${finalLabels}`);
  await github.rest.issues.setLabels({
    owner: context.issue.owner,
    repo: context.issue.repo,
    issue_number: context.issue.number,
    labels: finalLabels,
  });

  core.summary.addHeading('Projects affected by this PR:', '2');
  core.summary.addList(affectedProjects);
  core.summary.write();
};
