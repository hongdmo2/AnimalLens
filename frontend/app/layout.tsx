/**
 * Root Layout Component
 * 
 * This is the root layout component for the Animal Lens application.
 * It provides the base HTML structure and global styles for all pages.
 * 
 * Features:
 * - Global font configuration (Geist Sans and Geist Mono)
 * - Basic HTML structure with metadata
 * - Global styling and font variables
 * - Antialiasing for better text rendering
 */

import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

// Configure Geist Sans font
// Sets up the font as a CSS variable for global use
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

// Configure Geist Mono font (monospace)
// Used for code display and special text elements
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// Define website metadata
// Used for SEO and browser tab information
export const metadata: Metadata = {
  title: "Animal Lens",
  description: "Upload and analyze images to detect animals using AI",
};

// Root layout component
// Provides the base structure for all pages
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        // Apply font variables and enable antialiasing
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
