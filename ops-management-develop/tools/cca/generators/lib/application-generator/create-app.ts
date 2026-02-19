import {
  generateFiles,
  Tree,
  logger,
  addDependenciesToPackageJson,
  OverwriteStrategy,
  formatFiles,
  parseJson,
} from '@nx/devkit';
import * as fs from 'fs/promises';
import { $ } from 'execa';
import { basename, extname, join, resolve } from 'path';
import { applicationGenerator } from '@nx/react';
import { PackageJson } from 'nx/src/utils/package-json';
import { readFile } from 'fs/promises';
import { noop, pick, pickBy } from 'lodash';
import { CorvaSourcesGenerator } from '../types';

const updateTsconfig = async (
  options: GetApplicationOptions,
  originalPath: string
) => {
  const { tree, root } = options;

  const tsconfigPath = join(originalPath, 'tsconfig.json');
  if (!(await fs.stat(tsconfigPath).catch(() => false))) {
    return;
  }

  const tsconfig = parseJson(await fs.readFile(tsconfigPath, 'utf-8'))!;

  const tsconfigApp = tree.read(join(root, 'tsconfig.app.json'))!.toString();
  const tsconfigAppParsed = parseJson(tsconfigApp)!;

  const tsconfigJson = parseJson(
    tree.read(join(root, 'tsconfig.json'))!.toString()
  )!;
  const ensureReference = (references: Array<{ path: string }> | undefined) => {
    const addedRef = {
      path: '../../tools/vite-config',
    };
    const existing = references ?? [];
    if (existing.some((ref) => ref.path === addedRef.path)) {
      return existing;
    }
    return [...existing, addedRef];
  };
  tsconfigJson.references = ensureReference(tsconfigJson.references);
  tree.write(
    join(root, 'tsconfig.json'),
    JSON.stringify(tsconfigJson, null, 2)
  );

  const changes = {
    compilerOptions: tsconfigAppParsed.compilerOptions,
    references: ensureReference(tsconfigAppParsed.references),
  };

  if (tsconfig.compilerOptions?.paths) {
    const paths = {
      ...tsconfigAppParsed.compilerOptions.paths,
      ...tsconfig.compilerOptions.paths,
    };

    // `"react": ["./node_modules/@types/react"]` breaks the build
    delete paths['react'];

    changes.compilerOptions = {
      ...changes.compilerOptions,
      baseUrl: './',
      paths,
    };
  }

  tree.write(
    join(root, 'tsconfig.app.json'),
    JSON.stringify(
      {
        ...tsconfigAppParsed,
        ...changes,
      },
      null,
      2
    )
  );
};

const getAppFiles = async (options: GetApplicationOptions) => {
  const { tree, source, name: projectName, root } = options;

  const sourcesPath = await source.install();

  logger.debug((await $`ls -lah ${sourcesPath}`).stdout);

  const monorepoPackageJson = JSON.parse(
    tree.read('package.json')!.toString()
  )!;
  const reactAndReactDom = pick(monorepoPackageJson.dependencies!, [
    'react',
    'react-dom',
  ]);
  const testingLibs = pickBy(
    monorepoPackageJson.devDependencies!,
    (_, key) =>
      key.startsWith('@testing-library') ||
      ['@types/react', '@types/react-dom', '@types/node'].includes(key)
  );

  const originalPackageJson = JSON.parse(
    await fs.readFile(join(sourcesPath, 'package.json'), 'utf-8')
  )!;
  const originalVersion = originalPackageJson.version!;

  await applicationGenerator(tree, {
    directory: `apps/${projectName}`,
    linter: 'eslint',
    style: 'scss',
    name: projectName,
    unitTestRunner: 'vitest',
    e2eTestRunner: 'none',
    minimal: true,
    routing: false,
    port: 4200,
    bundler: 'vite',
  });

  tree.delete(join(root, 'public'));

  const generatedPackageJson = JSON.parse(
    tree.read(join(root, 'package.json'))!.toString()
  )!;

  generatedPackageJson.version = originalVersion;

  tree.write(
    join(root, 'package.json'),
    JSON.stringify(generatedPackageJson, null, 2)
  );

  const spec = JSON.parse(
    tree.read(join(root, 'tsconfig.spec.json'))!.toString()
  )!;

  tree.write(
    join(root, 'tsconfig.spec.json'),
    JSON.stringify(
      {
        ...spec,
        include: [
          ...spec.include,
          '__mocks__/**/*.ts',
          '__mocks__/**/*.tsx',
          '__mocks__/**/*.js',
          '__mocks__/**/*.jsx',
          'vitest.setup.ts',
          'vitest.global-setup.ts',
        ],
      },
      null,
      2
    )
  );

  const actual = JSON.parse(tree.read('package.json')!.toString())!;
  const patched = {
    ...actual,
    dependencies: {
      ...actual.dependencies!,
      ...reactAndReactDom,
    },
    devDependencies: {
      ...actual.devDependencies!,
      ...testingLibs,
    },
  };

  tree.write(join('package.json'), JSON.stringify(patched, null, 2));

  // Use the provided `tree` object to modify the file structure instead of using direct fs operations.
  // This is more idiomatic in Nx generators and ensures changes are tracked and applied atomically.

  // Remove the default src directory created by the application generator
  tree.delete(join(root, 'src'));
  tree.delete(join(root, 'index.html'));

  // Read the cloned app's src directory and manifest.json
  const clonedSrcPath = join(sourcesPath, 'src');
  const clonedManifestPath = join(sourcesPath, 'manifest.json');

  // Helper to recursively copy files from the cloned src to the new app's src using tree
  async function copyDirToTree(srcDir: string, destDir: string) {
    const cssModules = new Set<string>();
    // Read all entries in the source directory
    const entries = await fs.readdir(srcDir, { withFileTypes: true });
    for (const entry of entries) {
      const srcEntryPath = join(srcDir, entry.name);

      const destEntryPath = join(destDir, entry.name);
      if (entry.isDirectory()) {
        // Recursively copy subdirectories
        await copyDirToTree(srcEntryPath, destEntryPath);
      } else if (entry.isFile()) {
        // Read file content and write to tree
        const content = await fs.readFile(srcEntryPath);

        const hasClosingTag =
          /<\s*\/\s*>|<\s*>|<\/\s*[A-Za-z][A-Za-z0-9]*\s*>|<\s*[A-Za-z][A-Za-z0-9]*[^>]*\/>/;
        const hasCssModule = /import [A-z]+ from '(\.+\/.*)\.css'/;
        const hasSvgStartExport = /export \* as (.*) from (.*)\.svg/g;
        let normalizedEntryPath = destEntryPath;
        let normalizedContent = content.toString();

        if (
          (entry.name.endsWith('.js') || entry.name.endsWith('.ts')) &&
          (/^[A-Z]/.test(entry.name) || hasClosingTag.test(normalizedContent))
        ) {
          normalizedEntryPath = normalizedEntryPath + 'x';
        }

        if (
          normalizedEntryPath.match(/__tests__|__mocks__|\.test\.|\.spec\./)
        ) {
          normalizedContent = normalizedContent.replace(/(?<!\/)jest/g, 'vi');
        }

        const cssModule = normalizedContent.match(hasCssModule);
        if (cssModule) {
          cssModules.add(join(destDir, cssModule[1]));
          normalizedContent = normalizedContent.replace(
            cssModule[1] + '.css',
            cssModule[1] + '.module.css'
          );
        }

        if (normalizedContent.match(hasSvgStartExport)) {
          normalizedContent = normalizedContent.replace(
            hasSvgStartExport,
            'export { default as $1 } from $2.svg'
          );
        }

        tree.write(normalizedEntryPath, normalizedContent);
      }
      // Ignore other types (symlinks, etc) for simplicity
    }

    for (const cssModule of cssModules) {
      tree.rename(cssModule + '.css', cssModule + '.module.css');
    }
  }

  // Copy the src directory from the cloned repo into the new app's src directory
  await copyDirToTree(clonedSrcPath, join(root, 'src'));

  // Copy manifest.json if it exists
  try {
    const manifestContent = await fs.readFile(clonedManifestPath);
    tree.write(join(root, 'manifest.json'), manifestContent);
  } catch (e) {
    // If manifest.json does not exist, skip it
    logger.warn('manifest.json not found in cloned repo, skipping.');
  }

  await updateTsconfig(options, sourcesPath);

  return {
    sourcesPath,
    originalDeps: reactAndReactDom,
    originalDevDeps: testingLibs,
  };
};

interface GetApplicationOptions {
  tree: Tree;
  source: CorvaSourcesGenerator;
  name: string;
  root: string;
}

async function gatherApplicationSources(options: GetApplicationOptions) {
  const { tree, root, source } = options;

  if (tree.exists(join(root, 'package.json'))) {
    const sourcesPath = await source.install();
    await updateTsconfig(options, sourcesPath);

    return {
      install: noop,
    };
  }

  const { sourcesPath, originalDeps, originalDevDeps } = await getAppFiles(
    options
  );
  const sourcesPkgPath = resolve(sourcesPath, 'package.json');
  const sourcesPackageJson: PackageJson = JSON.parse(
    await fs.readFile(sourcesPkgPath, 'utf-8')
  );

  const ignoredIncludes = [
    'webpack',
    'babel',
    'typescript',
    'jest',
    'loader',
    'commitlint',
    'husky',
    'eslint',
  ];
  // react + @corva/ui peer

  const corvaUiDeps =
    (
      JSON.parse(
        await readFile(
          resolve(process.cwd(), 'node_modules/@corva/ui/package.json'),
          'utf-8'
        )
      ) as PackageJson
    ).peerDependencies ?? {};
  const ignoredExact = [
    'react',
    'react-dom',
    '@corva/create-app',
    '@corva/dc-platform-shared',
    'corva-convert-units',
    '@corva/ui',
    ...Object.keys(corvaUiDeps),
    'ts-node',
    'husky',
    'typescript',
    ...Object.keys(originalDeps),
    ...Object.keys(originalDevDeps),
  ];

  const filter = (deps: Record<string, string>) =>
    Object.fromEntries(
      Object.entries(deps).filter(
        ([key]) =>
          !ignoredExact.includes(key) &&
          !ignoredIncludes.some((i) => key.includes(i))
      )
    );

  const deps = filter(sourcesPackageJson.dependencies ?? {});
  const devDeps = filter(sourcesPackageJson.devDependencies ?? {});

  if (tree.exists(join(root, 'src', '__mocks__'))) {
    const mocks = tree.children(join(root, 'src', '__mocks__'));

    for (const mock of mocks) {
      if (
        Object.keys(deps).some((dep: string) =>
          dep.startsWith(basename(mock, extname(mock)))
        )
      ) {
        tree.rename(
          join(root, 'src', '__mocks__', mock),
          join(root, '__mocks__', mock)
        );
        tree.delete(join(root, 'src', '__mocks__', mock));
      }
    }
  }
  await updateReleasePleaseConfig(tree, root);
  await updateReleasePleaseManifest(tree, root);
  await updateProjectJson(tree, root);

  const install = addDependenciesToPackageJson(tree, deps, devDeps);

  return {
    install,
  };
}

async function updateReleasePleaseConfig(tree: Tree, root: string) {
  const config = tree.read(join('release-please-config.json'));

  if (!config) {
    logger.warn('release-please-config.json not found, skipping.');

    return;
  }

  const json = JSON.parse(config.toString())!;

  json.packages = json.packages ?? {};
  json.packages[root] = {
    component: root.split('/').pop()!,
    'release-type': 'node',
  };

  tree.write(join('release-please-config.json'), JSON.stringify(json, null, 2));
}

async function updateReleasePleaseManifest(tree: Tree, root: string) {
  const manifest =
    tree.read(join('.release-please-manifest.json')) || Buffer.from('{}');
  const json = JSON.parse(manifest.toString())!;

  const pkgJson = tree.read(join(root, 'package.json'))!;
  const pkgJsonJson = JSON.parse(pkgJson.toString())!;

  const version = pkgJsonJson.version!;

  json[root] = version;

  tree.write(
    join('.release-please-manifest.json'),
    JSON.stringify(json, null, 2)
  );
}

async function updateProjectJson(tree: Tree, root: string) {
  const projectJson = tree.read(join(root, 'project.json'))!;
  const projectJsonJson = JSON.parse(projectJson.toString())!;

  projectJsonJson.metadata = {
    type: 'app',
  };

  tree.write(
    join(root, 'project.json'),
    JSON.stringify(projectJsonJson, null, 2)
  );
}

export class ApplicationGenerator {
  static async build(options: GetApplicationOptions) {
    const { install } = await gatherApplicationSources(options);

    generateFiles(
      options.tree,
      join(__dirname, 'files'),
      options.root,
      {
        tmpl: '',
        name: options.name,
      },
      {
        overwriteStrategy: OverwriteStrategy.Overwrite,
      }
    );

    await formatFiles(options.tree);

    return async () => {
      install();
    };
  }
}
