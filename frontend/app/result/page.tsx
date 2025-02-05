"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { getAnalysisResult, AnalysisResult } from "@/lib/api";

/**
 * 분석 결과 페이지 컴포넌트
 * 역할:
 * 1. 분석 결과 데이터 조회 및 표시
 * 2. 이미지 표시
 * 3. 동물 정보 표시
 * 4. 사용자 인터페이스 제공
 */

export default function ResultPage() {
  const searchParams = useSearchParams();
  const id = searchParams.get("id");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string>();

  useEffect(() => {
    const fetchResult = async () => {
      try {
        if (id) {
          const data = await getAnalysisResult(id);
          setResult(data);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load result");
      }
    };

    fetchResult();
  }, [id]);

  if (error) {
    return (
      <div className="container max-w-2xl mx-auto p-4 space-y-4">
        <div className="text-red-500 text-center">{error}</div>
        <div className="flex justify-center">
          <Link href="/">
            <Button>Try Again</Button>
          </Link>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="container max-w-2xl mx-auto p-4">
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  return (
    <div className="container max-w-2xl mx-auto p-4 space-y-6">
      <h1 className="text-2xl font-bold text-center">Analysis Result</h1>
      
      {/* 이미지 표시 */}
      <div className="aspect-video relative overflow-hidden rounded-lg bg-gray-100">
        {result.image_url ? (
          <img
            src={result.image_url}
            alt={result.label}
            className="object-contain w-full h-full"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.src = '/placeholder-image.png'; // 에러 시 대체 이미지
            }}
          />
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Image not available</p>
          </div>
        )}
      </div>

      {/* 분석 결과 */}
      <div className="space-y-4">
        <div className="bg-white shadow rounded-lg p-6 space-y-4">
          <h2 className="text-xl font-semibold">
            Detected: {result.label}
          </h2>
          <p className="text-gray-600">
            Confidence: {result.confidence.toFixed(2)}%
          </p>
          {result.message && (
            <p className="text-blue-600 mt-2">
              {result.message}
            </p>
          )}
        </div>

        {/* 동물 정보 (알려진 동물인 경우에만 표시) */}
        {result.animal && (
          <div className="bg-white shadow rounded-lg p-6 space-y-4">
            <h2 className="text-xl font-semibold">Animal Information</h2>
            <div className="space-y-2">
              <p><strong>Species:</strong> {result.animal.species}</p>
              <p><strong>Habitat:</strong> {result.animal.habitat}</p>
              <p><strong>Diet:</strong> {result.animal.diet}</p>
              <p><strong>Description:</strong> {result.animal.description}</p>
            </div>
          </div>
        )}
      </div>

      {/* 새로운 분석 버튼 */}
      <div className="flex justify-center">
        <Link href="/">
          <Button>Analyze Another Image</Button>
        </Link>
      </div>
    </div>
  );
} 