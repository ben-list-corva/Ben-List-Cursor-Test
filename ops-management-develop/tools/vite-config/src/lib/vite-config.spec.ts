import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { vi } from 'vitest';

vi.mock('fs', async () => {
  const actual = await vi.importActual<typeof import('fs')>('fs');

  return {
    ...actual,
    readFileSync: (path: string | URL, options?: any) => {
      const filename = path.toString();

      if (/[\\/]tools[\\/]package\.json$/.test(filename)) {
        return JSON.stringify({ dependencies: {} });
      }

      return actual.readFileSync(path, options);
    },
  };
});

describe('createViteConfig', () => {
  it('should work', async () => {
    const { createViteConfig } = await import('./vite-config.js');
    const testFilesDir = join(
      dirname(fileURLToPath(import.meta.url)),
      '..',
      '..',
      'test-files'
    );
    const viteConfig = createViteConfig({
      name: 'test',
      pwd: testFilesDir,
    });
    expect(viteConfig).to.be.a('function');
    expect(
      await viteConfig({ command: 'serve', mode: 'development' })
    ).to.be.an('object');
  });
});
