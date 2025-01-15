/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  compress: true,
  images: {
    domains: ['localhost'],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    formats: ['image/webp'],
  },
  webpack: (config, { dev, isServer }) => {
    // Optimizaciones solo para producción
    if (!dev) {
      config.optimization = {
        ...config.optimization,
        runtimeChunk: 'single',
        splitChunks: {
          chunks: 'all',
          maxInitialRequests: 25,
          minSize: 20000,
          cacheGroups: {
            default: false,
            vendors: false,
            framework: {
              chunks: 'all',
              name: 'framework',
              test: /(?<!node_modules.*)[\\/]node_modules[\\/](react|react-dom|scheduler|prop-types|use-subscription)[\\/]/,
              priority: 40,
              enforce: true,
            },
            mui: {
              name: 'mui',
              test: /[\\/]node_modules[\\/]@mui[\\/]/,
              chunks: 'all',
              priority: 30,
            },
            commons: {
              name: 'commons',
              minChunks: 2,
              priority: 20,
            },
            lib: {
              test: /[\\/]node_modules[\\/]/,
              chunks: 'all',
              name(module, chunks, cacheGroupKey) {
                const moduleFileName = module
                  .identifier()
                  .split('/')
                  .reduceRight((item) => item);
                return `${cacheGroupKey}-${moduleFileName}`;
              },
              priority: 10,
              minChunks: 2,
              reuseExistingChunk: true,
            },
          },
        },
      };
    }

    return config;
  },
  experimental: {
    optimizeCss: true,
    scrollRestoration: true,
  },
  poweredByHeader: false,
  generateEtags: true,
  compress: true,
  productionBrowserSourceMaps: false,
};

module.exports = nextConfig;
