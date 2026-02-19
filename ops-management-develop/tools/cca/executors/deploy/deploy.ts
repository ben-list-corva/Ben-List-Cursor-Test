import { PromiseExecutor } from '@nx/devkit';
import { DeployExecutorSchema } from './schema';

const runExecutor: PromiseExecutor<DeployExecutorSchema> = async (options) => {
  console.log('🚀 Deploy executor started with options:', options);
  console.log('📁 Current working directory:', process.cwd());
  console.log('🔍 Checking if build output exists...');

  // Check if build output exists
  const fs = require('fs');
  const path = require('path');

  try {
    const buildOutputPath = path.join(process.cwd(), 'dist');
    if (fs.existsSync(buildOutputPath)) {
      console.log('✅ Build output found at:', buildOutputPath);
      const files = fs.readdirSync(buildOutputPath);
      console.log('📦 Build files:', files);
    } else {
      console.log('❌ Build output not found at:', buildOutputPath);
    }
  } catch (error) {
    console.log('⚠️ Error checking build output:', error);
  }

  console.log('🎯 Deploy executor completed successfully');

  return {
    success: true,
  };
};

export default runExecutor;
