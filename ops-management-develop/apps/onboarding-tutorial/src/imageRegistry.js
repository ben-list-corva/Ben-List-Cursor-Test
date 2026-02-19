// Dynamic image registry using webpack's require.context
// This imports all images from training-assets and creates a lookup map

// Import all images from training-assets folders
const importAll = (requireContext) => {
  const images = {};
  requireContext.keys().forEach((key) => {
    // key is like "./1jVvTIFJcurxsWwpkhv6gbc-YutuzA3pIohgT3pPgUbI/73f55930d893.png"
    // We want to map it to "training-assets/1jVvTIFJcurxsWwpkhv6gbc-YutuzA3pIohgT3pPgUbI/73f55930d893.png"
    const normalizedKey = 'training-assets' + key.substring(1); // Remove leading "."
    images[normalizedKey] = requireContext(key);
    
    // Also store with leading slash for compatibility
    images['/' + normalizedKey] = requireContext(key);
    
    // Store just the filename for fallback matching
    const filename = key.split('/').pop();
    if (!images[filename]) {
      images[filename] = requireContext(key);
    }
  });
  return images;
};

// Use require.context to import all PNG images from training-assets
const trainingImages = importAll(
  require.context('./assets/training-assets', true, /\.png$/)
);

// Function to get image URL by path
export function getImageUrl(path) {
  if (!path) return null;
  
  // Try exact match first
  if (trainingImages[path]) {
    return trainingImages[path];
  }
  
  // Try with leading slash
  if (trainingImages['/' + path]) {
    return trainingImages['/' + path];
  }
  
  // Try without leading slash
  const withoutSlash = path.startsWith('/') ? path.substring(1) : path;
  if (trainingImages[withoutSlash]) {
    return trainingImages[withoutSlash];
  }
  
  // Try just the filename
  const filename = path.split('/').pop();
  if (trainingImages[filename]) {
    return trainingImages[filename];
  }
  
  // Try matching the last two path segments (folder/file.png)
  const parts = withoutSlash.split('/');
  if (parts.length >= 2) {
    const lastTwo = parts.slice(-2).join('/');
    for (const key of Object.keys(trainingImages)) {
      if (key.endsWith(lastTwo)) {
        return trainingImages[key];
      }
    }
  }
  
  console.warn('Image not found in registry:', path);
  return null;
}

// Export the full registry for debugging
export const imageRegistry = trainingImages;

export default getImageUrl;
