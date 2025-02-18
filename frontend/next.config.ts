import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    domains: [
      'animal-lens-data-bucket-test.s3.us-east-1.amazonaws.com'
    ],
  }
};

export default nextConfig;
