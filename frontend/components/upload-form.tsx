"use client";

/**
 * UploadForm Component
 * 
 * This component handles the image upload functionality for animal detection.
 * Features:
 * - File selection via drag & drop or file browser
 * - File validation (size & type)
 * - Upload progress tracking
 * - Error handling
 * - Redirects to results page after successful upload
 */

import { useState } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { Button } from "@/components/ui/button";
import { uploadImage } from "@/lib/api";
import { Loader2 } from "lucide-react";

interface UploadFormProps {
  onSubmit: (data: FormData) => Promise<void>;
}

export function UploadForm({ onSubmit }: UploadFormProps) {
  // State management
  const [file, setFile] = useState<File>();              // Selected file state
  const [isUploading, setIsUploading] = useState(false); // Upload progress state
  const [error, setError] = useState<string>();          // Error message state
  const [uploadProgress, setUploadProgress] = useState(0); // Upload progress percentage state

  // File selection/drag & drop handler
  const handleFileChange = (selectedFile?: File) => {
    if (selectedFile) {
      // File size limit: 5MB
      if (selectedFile.size > 5 * 1024 * 1024) {
        setError("File size must be less than 5MB");
        return;
      }
      // Image file type validation
      if (!selectedFile.type.startsWith('image/')) {
        setError("Only image files are allowed");
        return;
      }
    }
    setFile(selectedFile);
    setError(undefined); // Reset error when new file is selected
  };

  // Image analysis start handler
  const handleAnalyze = async () => {
    if (!file) return;

    setIsUploading(true);
    setError(undefined);
    setUploadProgress(0);

    try {
      // Upload file and update progress
      const response = await uploadImage(file, (progress) => {
        setUploadProgress(progress);
      });

      // Redirect directly using the response
      if (response && response.id) {
        window.location.href = `/result?id=${response.id}`;
      } else {
        console.log(response, "response");
        console.log(response.id, "response.id");
        throw new Error('Invalid response from server');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* File upload component */}
      <FileUpload
        onChange={handleFileChange}
        value={file}
        disabled={isUploading}
      />

      {/* Error message display */}
      {error && (
        <div className="text-red-500 text-sm text-center">
          {error}
        </div>
      )}

      {/* Upload progress display */}
      {isUploading && uploadProgress > 0 && (
        <div className="w-full max-w-xs mx-auto">
          {/* Progress bar */}
          <div className="bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
          {/* Progress percentage */}
          <p className="text-sm text-gray-500 text-center mt-1">
            {Math.round(uploadProgress)}%
          </p>
        </div>
      )}

      {/* Analysis button */}
      <div className="flex justify-center">
        <Button
          size="lg"
          className="w-full max-w-xs"
          disabled={!file || isUploading}
          onClick={handleAnalyze}
        >
          {isUploading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              {uploadProgress > 0 ? 'Uploading...' : 'Processing...'}
            </>
          ) : (
            'Analyze Image'
          )}
        </Button>
      </div>
    </div>
  );
} 