"use client"; // 클라이언트 사이드 컴포넌트임을 명시

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone"; // 드래그 앤 드롭 기능을 위한 라이브러리
import { Cloud, File, Loader2 } from "lucide-react"; // UI 아이콘
import Image from "next/image";

import { cn } from "@/lib/utils";

// 컴포넌트 props 타입 정의
interface FileUploadProps {
  onChange: (file?: File) => void; // 파일 선택 시 호출될 콜백
  value?: File;                    // 현재 선택된 파일
  disabled?: boolean;              // 비활성화 상태
}

export function FileUpload({
  onChange,
  value,
  disabled
}: FileUploadProps) {
  // 상태 관리
  const [preview, setPreview] = useState<string>();  // 이미지 미리보기 URL
  const [loading, setLoading] = useState(false);     // 로딩 상태

  // 파일이 드롭되거나 선택되었을 때 실행되는 콜백
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    
    if (file) {
      setLoading(true);
      // FileReader를 사용하여 이미지 미리보기 생성
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
        setLoading(false);
      };
      reader.readAsDataURL(file);
      onChange(file);
    }
  }, [onChange]);

  // react-dropzone 설정
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif'] // 허용되는 파일 형식
    },
    maxFiles: 1,  // 최대 1개 파일만 허용
    disabled
  });

  return (
    // 드래그 앤 드롭 영역
    <div
      {...getRootProps()}
      className={cn(
        "border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition cursor-pointer",
        isDragActive && "border-primary",        // 드래그 중일 때 스타일
        disabled && "opacity-50 cursor-default"  // 비활성화 상태 스타일
      )}
    >
      <input {...getInputProps()} />
      
      {/* 로딩 상태 UI */}
      {loading && (
        <div className="flex flex-col items-center">
          <Loader2 className="h-10 w-10 animate-spin text-gray-400" />
          <p className="mt-2 text-sm text-gray-500">Loading preview...</p>
        </div>
      )}
      
      {/* 초기 상태 UI */}
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
      
      {/* 이미지 미리보기 UI */}
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