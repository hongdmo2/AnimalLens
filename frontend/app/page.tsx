"use client"

import { UploadForm } from "@/components/upload-form"
import { PawPrint } from "lucide-react"
import { useRouter } from "next/navigation"
import { useState } from "react"
import { uploadImage } from "@/lib/api"

export default function Home() {
  const router = useRouter()
  const [error, setError] = useState<string | null>(null)
  const [uploading, setUploading] = useState(false)

  async function onSubmit(data: FormData) {
    try {
      setUploading(true);
      const file = data.get('image') as File;

      // upload image and get result id
      const result = await uploadImage(file);

      // move to result page with new result id
      router.push(`/result?id=${result.id}`);

    } catch (error) {
      console.error('Upload failed:', error);
      setError('Failed to upload and analyze image');
    } finally {
      setUploading(false);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 sm:p-8 bg-gradient-to-br from-blue-100 to-purple-100">
      <div className="w-full max-w-3xl space-y-8 bg-white rounded-2xl shadow-xl p-8 transition-all duration-300 hover:shadow-2xl">
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center space-x-2">
            <PawPrint className="w-10 h-10 text-blue-600" />
            <h1 className="text-4xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
              Animal Lens
            </h1>
          </div>
          <p className="text-lg text-gray-600">Upload an image to identify animals and learn about them</p>
        </div>

        <UploadForm onSubmit={onSubmit} />

        <footer className="text-center text-sm text-gray-500 mt-8">
          Changoh-Hong - Discover the wonders of the animal kingdom.
        </footer>
      </div>
    </main>
  )
}

