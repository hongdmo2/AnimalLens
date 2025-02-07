/**
 * Result Page Component
 * 
 * This component displays the analysis results for an uploaded image.
 * It fetches and displays the AI analysis results, including:
 * - Detected animal information
 * - Confidence score
 * - Detailed animal data (species, habitat, diet, etc.)
 * 
 * Features:
 * - Dynamic result fetching based on URL parameters
 * - Loading state handling
 * - Error state management
 * - Responsive image display
 * - Fallback image handling
 */

"use client"

import { useSearchParams } from "next/navigation"
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { getAnalysisResult, type AnalysisResult } from "@/lib/api"
import { PawPrint, AlertCircle, Loader2 } from "lucide-react"
import Image from 'next/image'

export default function ResultPage() {
  // State and parameter management
  const searchParams = useSearchParams()
  const id = searchParams.get("id")
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string>()

  // Fetch analysis result on component mount
  useEffect(() => {
    const fetchResult = async () => {
      try {
        if (!id) {
          throw new Error("No result ID provided")
        }
        const data = await getAnalysisResult(id)
        setResult(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load result")
      }
    }

    fetchResult()
  }, [id])

  // Error state UI
  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 sm:p-8 bg-gradient-to-br from-blue-100 to-purple-100">
        <div className="w-full max-w-3xl space-y-8 bg-white rounded-2xl shadow-xl p-8 transition-all duration-300 hover:shadow-2xl">
          <div className="flex items-center justify-center space-x-2 text-red-500">
            <AlertCircle className="w-8 h-8" />
            <div className="text-xl font-semibold">{error}</div>
          </div>
          <div className="flex justify-center">
            <Link href="/">
              <Button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-2 px-4 rounded-lg transition-all duration-300 ease-in-out hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                Try Again
              </Button>
            </Link>
          </div>
        </div>
      </main>
    )
  }

  // Loading state UI
  if (!result) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-4 sm:p-8 bg-gradient-to-br from-blue-100 to-purple-100">
        <div className="w-full max-w-3xl space-y-8 bg-white rounded-2xl shadow-xl p-8 transition-all duration-300 hover:shadow-2xl">
          <div className="flex items-center justify-center space-x-2">
            <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
            <div className="text-xl font-semibold text-gray-700">Loading...</div>
          </div>
        </div>
      </main>
    )
  }

  // Success state UI
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 sm:p-8 bg-gradient-to-br from-blue-100 to-purple-100">
      <div className="w-full max-w-3xl space-y-8 bg-white rounded-2xl shadow-xl p-8 transition-all duration-300 hover:shadow-2xl">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <PawPrint className="w-10 h-10 text-blue-600" />
            <h1 className="text-3xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
              Analysis Result
            </h1>
          </div>
        </div>

        {/* Image Display */}
        <div className="relative overflow-hidden rounded-lg bg-gray-100 shadow-inner">
          {result.image_url ? (
            <Image 
              src={result.image_url} 
              alt="Uploaded" 
              width={500}  // 적절한 크기로 조정
              height={300} 
              priority
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-500">Image not available</p>
            </div>
          )}
        </div>

        {/* Analysis Results */}
        <div className="space-y-6">
          <div className="bg-gray-50 rounded-lg p-6 space-y-4 shadow-inner">
            <h2 className="text-2xl font-semibold text-blue-600">Detected: {result.label}</h2>
            <p className="text-gray-600">Confidence: {result.confidence.toFixed(2)}%</p>
            {result.message && <p className="text-purple-600 mt-2 italic">{result.message}</p>}
          </div>

          {/* Animal Information (displayed only for known animals) */}
          {result.animal && (
            <div className="bg-gray-50 rounded-lg p-6 space-y-4 shadow-inner">
              <h2 className="text-2xl font-semibold text-blue-600">Animal Information</h2>
              <div className="space-y-2 text-gray-700">
                <p>
                  <strong className="text-blue-500">Species:</strong> {result.animal.species}
                </p>
                <p>
                  <strong className="text-blue-500">Habitat:</strong> {result.animal.habitat}
                </p>
                <p>
                  <strong className="text-blue-500">Diet:</strong> {result.animal.diet}
                </p>
                <p>
                  <strong className="text-blue-500">Description:</strong> {result.animal.description}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* New Analysis Button */}
        <div className="flex justify-center">
          <Link href="/">
            <Button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold py-2 px-6 rounded-lg transition-all duration-300 ease-in-out hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
              Analyze Another Image
            </Button>
          </Link>
        </div>

        <footer className="text-center text-sm text-gray-500 mt-8">
          Powered by AI Vision – Discover the wonders of the animal kingdom.
        </footer>
      </div>
    </main>
  )
}

