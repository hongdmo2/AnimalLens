/**
 * FileUpload Component
 * 
 * A reusable file upload component that provides drag and drop functionality.
 * Built with react-dropzone for handling file uploads.
 * 
 * Features:
 * - Drag and drop file upload
 * - File preview functionality
 * - Loading state handling
 * - Customizable styling
 * - File type restrictions
 * - Accessibility support
 */

"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Cloud, File, Loader2 } from "lucide-react";
import Image from "next/image";

import { cn } from "@/lib/utils";

// Define component props interface
interface FileUploadProps {
  onChange: (file?: File) => void;  // Callback function when file is selected
  value?: File;                     // Currently selected file
  disabled?: boolean;               // Disabled state of the upload component
}

export function FileUpload({
  onChange,
  value,
  disabled
}: FileUploadProps) {
  // State management
  const [preview, setPreview] = useState<string>();  // Image preview URL
  const [loading, setLoading] = useState(false);     // Loading state

  // Handle file drop callback
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    
    if (file) {
      setLoading(true);
      // Create file preview using FileReader
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
        setLoading(false);
      };
      reader.readAsDataURL(file);
      onChange(file);
    }
  }, [onChange]);

  // Configure dropzone settings
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif']  // Accepted file types
    },
    maxFiles: 1,  // Maximum number of files allowed
    disabled
  });

  return (
    // Dropzone container
    <div
      {...getRootProps()}
      className={cn(
        "border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition cursor-pointer",
        isDragActive && "border-primary",        // Active drag state styling
        disabled && "opacity-50 cursor-default"  // Disabled state styling
      )}
    >
      <input {...getInputProps()} />
      
      {/* Loading state UI */}
      {loading && (
        <div className="flex flex-col items-center">
          <Loader2 className="h-10 w-10 animate-spin text-gray-400" />
          <p className="mt-2 text-sm text-gray-500">Loading preview...</p>
        </div>
      )}
      
      {/* Initial state UI */}
      {!loading && !preview && (
        <div className="flex flex-col items-center">
          <Cloud className="h-10 w-10 text-gray-400" />
          <p className="mt-2 text-sm text-gray-500">
            Drag & drop your image here, or click to select
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Supported formats: JPEG, PNG, GIF
          </p>
        </div>
      )}
      
      {/* Image preview UI */}
      {!loading && preview && (
        <div className="relative h-64 w-full">
          <Image
            src={preview}
            alt="Preview"
            fill
            className="object-contain"
          />
        </div>
      )}
    </div>
  );
}