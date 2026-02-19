import { defineConfig, UserConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteStaticCopy } from 'vite-plugin-static-copy';
import license from 'rollup-plugin-license';
import { join, resolve } from 'path';

import dotenv from 'dotenv';
import { expand } from 'dotenv-expand';
import chalk from 'chalk';
import castArray from 'lodash.castarray';

import {
  CORVA_API_ENVS,
  CORVA_API_ENV_VARIABLES,
  CORVA_GLOBAL_DEPENDENCIES,
  // TODO: create proper types
  // @ts-expect-error: No type definitions available for vite-multiple-assets
} from '@corva/dc-platform-shared/cjs/devcenter/webpack/constants.js';
import { DynamicPublicDirectory } from 'vite-multiple-assets';
import { readFile } from 'fs/promises';
import { readFileSync, writeFileSync, unlinkSync, existsSync } from 'fs';
import { visualizer } from 'rollup-plugin-visualizer';
import presetEnv from 'postcss-preset-env';
import 'vitest/node';
import { getVersion } from './get-version.js';

interface CreateViteConfigArgs {
  name: string;
  pwd: string;
}

export const createViteConfig = ({ name, pwd }: CreateViteConfigArgs) => {
  const __dirname = pwd;
  expand(dotenv.config());

  const packageJson = JSON.parse(
    readFileSync(resolve(__dirname, './package.json'), 'utf-8')
  );
  const rootPackageJson = JSON.parse(
    readFileSync(resolve(__dirname, '../../package.json'), 'utf-8')
  );
  const manifestJson = JSON.parse(
    readFileSync(resolve(__dirname, './manifest.json'), 'utf-8')
  );

  const {
    application: { key: appKey },
  } = manifestJson;

  const getAppIdentifier = (version = packageJson.version) => {
    const appIdentifier = appKey.replace(/\./g, '_');
    return `${appIdentifier}-${version}`;
  };

  const getAlias = async () => {
    const tsconfig = JSON.parse(
      await readFile(join(__dirname, 'tsconfig.app.json'), 'utf-8')
    )!;

    if (!tsconfig.compilerOptions?.paths) {
      return {};
    }

    const alias = Object.fromEntries(
      Object.entries(tsconfig.compilerOptions.paths).map(([key, value]) => [
        key.replace('/*', ''),
        resolve(__dirname, (value as string[])[0].replace('/*', '')),
      ])
    );
    return alias;
  };

  const getCorvaApiEnvVariables = () => {
    const apiEnv = process.env.CORVA_API_ENV || CORVA_API_ENVS.production;
    if (apiEnv in CORVA_API_ENVS) return CORVA_API_ENV_VARIABLES[apiEnv];

    console.log(
      chalk.red(
        `CORVA_API_ENV should be one of [${Object.keys(CORVA_API_ENVS).join(
          ', '
        )}]`
      )
    );
    return process.exit(1);
  };

  const CORVA_EXTERNALS: [string, RegExp][] = Object.keys(
    CORVA_GLOBAL_DEPENDENCIES
  ).map((libName) => [
    libName,
    new RegExp(`(^${libName}$|^${libName}\/)([^]+)?`), // eslint-disable-line no-useless-escape
  ]);

  // NOTE: These imports should be always bundled
  const SKIP_IN_EXTERNALS = ['react/jsx-runtime', 'highcharts/'];

  const staticGlobals: Record<string, string> = {};

  // Add all Corva global dependencies as externals
  // Convert package names to valid JavaScript identifiers for IIFE format
  Object.keys(CORVA_GLOBAL_DEPENDENCIES as Record<string, string>).forEach(
    (libName) => {
      if (
        libName.startsWith('react/jsx-runtime') ||
        libName.startsWith('highcharts/')
      ) {
        return;
      }
      // Convert @scope/package-name to valid JS identifier
      staticGlobals[
        libName
      ] = `this["${libName}"].default || this["${libName}"]`;
    }
  );

  const deps = Object.keys(CORVA_GLOBAL_DEPENDENCIES);

  // Create externals configuration for Vite to match webpack externals
  const createGlobals = () => {
    return (id: string) => {
      if (staticGlobals[id]) {
        return staticGlobals[id];
      }

      const dep = deps.find((dep) => id.startsWith(dep));

      if (!dep) {
        throw new Error(`Unknown dependency: ${id}`);
      }

      return `this["${dep}"]${id.replace(dep, '').replace(/\//g, '.')}`;
    };
  };

  return defineConfig(async (args): Promise<UserConfig> => {
    const nodeEnv = args.command === 'serve' ? 'development' : 'production';
    const version = getVersion({
      mode: args.mode,
      version: packageJson.version,
      refName: process.env.GITHUB_HEAD_REF || process.env.GITHUB_REF_NAME,
    });

    const host = process.env.HOST || 'app.local.corva.ai';
    const port = process.env.PORT
      ? +process.env.PORT > 0
        ? +process.env.PORT
        : 8080
      : 8080;
    const config: UserConfig = {
      root: __dirname,
      cacheDir: `../../node_modules/.vite/apps/${name}`,
      server: {
        port: port,
        host: host,
        open: args.command === 'serve' && args.mode === 'development',
      },
      css: {
        postcss: {
          plugins: [
            presetEnv({
              stage: 3,
              // TODO: create proper types
            }) as any,
          ],
        },
      },
      preview: {
        port: port,
        host: host,
      },
      plugins: [react()],
      // Uncomment this if you are using workers.
      // worker: {
      //  plugins: [ nxViteTsPaths() ],
      // },
      build: {
        outDir: `../../dist/apps/${name}`,
        emptyOutDir: true,
        reportCompressedSize: true,
        sourcemap: true,
        // Disable CSS code splitting to inline all CSS into the JS bundle
        cssCodeSplit: false,

        commonjsOptions: {
          transformMixedEsModules: true,
        },
        rollupOptions: {
          input: {
            main: resolve(__dirname, 'src/index.js'),
          },
          output: {
            entryFileNames: 'build/app.js',
            // chunkFileNames: 'app.js',
            chunkFileNames: 'chunks/[name]-[hash].js',
            generatedCode: {
              reservedNamesAsProps: true,
            },
            // manualChunks: () => null, // disables code splitting
            // Configure externals to match webpack externals
            globals: createGlobals(),
            exports: 'named',
          },
          // Add externals configuration to exclude Corva global dependencies
          external: (source, importer, isResolved) => {
            for (let i = 0; i < SKIP_IN_EXTERNALS.length; i += 1) {
              if (source.startsWith(SKIP_IN_EXTERNALS[i])) return false;
            }

            for (let i = 0; i < CORVA_EXTERNALS.length; i += 1) {
              const [, libRegex] = CORVA_EXTERNALS[i];
              const match = libRegex.exec(source);

              if (match !== null) {
                return true;
              }
            }
            return false;
          },
        },
      },

      resolve: {
        alias: await getAlias(),
      },
      test: {
        watch: false,
        globals: true,
        environment: 'jsdom',
        include: [
          '{src,tests}/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}',
        ],
        includeSource: ['src/**/*.{js,mjs,cjs,ts,mts,cts,jsx,tsx}'],
        reporters: ['default'],
        coverage: {
          reportsDirectory: './test-output/vitest/coverage',
          provider: 'v8' as const,
        },
        setupFiles: ['./vitest.setup.ts'],
        globalSetup: ['./vitest.global-setup.ts'],
      },
    };

    if (args.command === 'build') {
      config.build = {
        ...config.build,
        // Ensure CSS is inlined in production build
        cssCodeSplit: false,
        lib: {
          entry: resolve(__dirname, 'src/index.js'),
          name: getAppIdentifier(version),
          // the proper extensions will be added
          fileName: 'build/app.js',
          formats: ['iife'],
        },
        rollupOptions: {
          ...config.build?.rollupOptions,
          plugins: [
            ...castArray(config.build?.rollupOptions?.plugins),
            // TODO: create proper types
            (license as any)({
              thirdParty: {
                output: join(
                  config.build?.outDir || `../../dist/apps/${name}`,
                  'build/app.js.LICENSE.txt'
                ),
              },
            }),
            args.mode === 'development' &&
              visualizer({
                open: true,
                filename: `../../dist/apps/${name}/stats.html`,
              }),
          ],
        },
        minify: 'esbuild',
      };

      config.esbuild = {
        ...config.esbuild,
        drop: ['console', 'debugger'],
        legalComments: 'none',
      };

      config.optimizeDeps = {
        ...(config.optimizeDeps || {}),
        exclude: [
          ...(config.optimizeDeps?.exclude || []),
          // Exclude all Corva global dependencies from optimization
          ...Object.keys(CORVA_GLOBAL_DEPENDENCIES as Record<string, string>),
        ],
      };

      config.plugins?.push(
        viteStaticCopy({
          targets: [
            {
              src: 'manifest.json',
              dest: '.',
            },
            {
              src: 'manifest.json',
              dest: 'build',
            },
            {
              src: 'package.json',
              dest: '.',
              transform: (content, filename) => {
                const s = JSON.parse(content);
                const highchartsVersion =
                  rootPackageJson?.dependencies?.highcharts ||
                  s?.dependencies?.highcharts;

                return `${JSON.stringify(
                  {
                    ...s,
                    ...(args.mode === 'development' ? { version } : {}),
                    dependencies: {
                      highcharts: highchartsVersion,
                    },
                  },
                  null,
                  2
                )}\n`;
              },
            },
          ],
        })
      );

      // Custom plugin to inline CSS into the JavaScript bundle
      config.plugins?.push({
        name: 'inline-css',
        closeBundle() {
          const outDir = config.build?.outDir || `../../dist/apps/${name}`;
          const jsPath = join(outDir, 'build/app.js');
          const cssPath = join(outDir, 'build/app.js.css');
          if (!existsSync(cssPath)) {
            return;
          }
          try {
            // Read the CSS file
            const cssContent = readFileSync(cssPath, 'utf-8');

            // Read the JS file
            const jsContent = readFileSync(jsPath, 'utf-8');

            // Create a style element with the CSS content
            const cssInjection = `(function(){var s=document.createElement('style');s.textContent=${JSON.stringify(
              cssContent
            )};document.head.appendChild(s)})();`;

            // Insert the CSS injection at the beginning of the JS file
            const updatedJsContent = cssInjection + jsContent;

            // Write the updated JS file
            writeFileSync(jsPath, updatedJsContent);

            // Remove the CSS file
            try {
              unlinkSync(cssPath);
              console.log('✓ CSS inlined and CSS file removed');
            } catch (err) {
              console.log('Warning: Could not remove CSS file:', err);
            }
          } catch (err) {
            console.log('Warning: Could not inline CSS:', err);
          }
        },
      });

      config.define = {
        ...(config.define || {}),
        'process.env': {
          NODE_ENV: 'production',
        },
      };
    } else {
      const fallbackForEnv = Object.entries(process.env).reduce(
        (acc, [key, value]) => {
          if (key.startsWith('VITE_')) {
            acc[key.replace('VITE_', 'REACT_APP_')] = value || '';
          }
          return acc;
        },
        {
          DEV_CENTER_APP_PATH: '',
          NODE_ENV: nodeEnv,
          REACT_APP_ENVIRONMENT: nodeEnv,
          ...getCorvaApiEnvVariables(),
        } as Record<string, string>
      );

      config.define = {
        ...(config.define || {}),
        'import.meta.vitest': undefined,
        'process.env': fallbackForEnv,
        global: {},
      };

      config.plugins?.push(
        DynamicPublicDirectory([
          '../../public/**',
          {
            // Copy assets from @corva/dc-platform-shared to static/media
            input: '../../node_modules/@corva/dc-platform-shared/assets/**',
            output: 'static/media',
          },
          {
            // Copy assets from @corva/ui to static/media
            input: '../../node_modules/@corva/ui/assets/**',
            output: 'static/media',
          },
        ])
      );
    }

    return config;
  });
};
