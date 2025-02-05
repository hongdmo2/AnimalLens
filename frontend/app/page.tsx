import { UploadForm } from "@/components/upload-form";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="w-full max-w-3xl space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold tracking-tight">
            Animal Lens
          </h1>
          <p className="text-lg text-gray-500">
            Upload an image to identify animals and learn about them
          </p>
        </div>
        
        <UploadForm />
      </div>
    </main>
  );
}
