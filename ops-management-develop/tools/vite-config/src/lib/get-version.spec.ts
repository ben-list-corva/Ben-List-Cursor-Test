import { getVersion } from './get-version.js';

describe('getVersion', () => {
  beforeAll(() => {
    vi.useFakeTimers({
      now: new Date('2025-01-01T00:00:00Z'),
      toFake: ['Date'],
    });
    process.env.GITHUB_SHA = '1234567';
  });

  afterAll(() => {
    vi.useRealTimers();
  });

  it.each([
    ['development', '1.0.0', '', '1.0.0-development1735689600000'],
    ['production', '1.0.0', '', '1.0.0'],
    ['production', '1.0.0', 'develop', 'dev-1234567'],
    ['production', '1.0.0', 'main', 'dev-1234567'],
    ['production', '1.0.0', 'feature/1234567', 'feature|1234567'],
    [
      'production',
      '1.0.0',
      'feature/1234567/some-branch',
      'feature|1234567|some-branch',
    ],
    ['production', '1.0.0', '1234567@some-branch', '1.0.0'],
  ])(
    'should return the version for %s mode',
    (mode: string, version: string, refName: string, expected: string) => {
      const result = getVersion({ mode, version, refName }) as string;
      expect(result).toBe(expected);
    }
  );
});
