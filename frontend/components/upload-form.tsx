"use client";

import { useState } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { Button } from "@/components/ui/button";
import { uploadImage } from "@/lib/api";
import { Loader2 } from "lucide-react";

export function UploadForm() {
  // 상태 관리
  const [file, setFile] = useState<File>();              // 선택된 파일 상태
  const [isUploading, setIsUploading] = useState(false); // 업로드 진행 상태
  const [error, setError] = useState<string>();          // 에러 메시지 상태
  const [uploadProgress, setUploadProgress] = useState(0); // 업로드 진행률 상태
  
  // 파일 선택/드래그 앤 드롭 핸들러
  const handleFileChange = (selectedFile?: File) => {
    if (selectedFile) {
      // 파일 크기 제한: 5MB
      if (selectedFile.size > 5 * 1024 * 1024) {
        setError("File size must be less than 5MB");
        return;
      }
      // 이미지 파일 타입 검증
      if (!selectedFile.type.startsWith('image/')) {
        setError("Only image files are allowed");
        return;
      }
    }
    setFile(selectedFile);
    setError(undefined); // 새 파일 선택시 에러 초기화
  };

  // 이미지 분석 시작 핸들러
  const handleAnalyze = async () => {
    if (!file) return;

    // 업로드 상태 초기화
    setIsUploading(true);
    setError(undefined);
    setUploadProgress(0);

    try {
      // 파일 업로드 및 진행률 업데이트
      const response = await uploadImage(file, (progress) => {
        setUploadProgress(progress);
      });
      // 업로드 성공 시 결과 페이지로 이동
      window.location.href = `/result?id=${response.upload_id}`;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      // 상태 초기화
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="space-y-4">
      {/* 파일 업로드 컴포넌트 */}
      <FileUpload
        onChange={handleFileChange}
        value={file}
        disabled={isUploading}
      />
      
      {/* 에러 메시지 표시 */}
      {error && (
        <div className="text-red-500 text-sm text-center">
          {error}
        </div>
      )}
      
      {/* 업로드 진행률 표시 */}
      {isUploading && uploadProgress > 0 && (
        <div className="w-full max-w-xs mx-auto">
          {/* 진행률 바 */}
          <div className="bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-blue-600 h-2.5 rounded-full transition-all duration-300"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
          {/* 진행률 퍼센트 */}
          <p className="text-sm text-gray-500 text-center mt-1">
            {Math.round(uploadProgress)}%
          </p>
        </div>
      )}
      
      {/* 분석 버튼 */}
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