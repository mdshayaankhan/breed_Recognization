import { useState } from "react";
import Hero from "@/components/Hero";
import ImageUpload from "@/components/ImageUpload";
import DetectionResults from "@/components/DetectionResults";
import { toast } from "sonner";

// Backend API configuration (overridden in production via VITE_API_URL)
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:5000";

interface DetectionResult {
  breed: string;
  confidence: number;
}

const Index = () => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<DetectionResult | null>(null);

  const handleImageSelect = async (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setSelectedImage(e.target?.result as string);
      setResult(null);
    };
    reader.readAsDataURL(file);
    toast.success("Image uploaded successfully");
    
    // Call real API
    await detectBreed(file);
  };

  const detectBreed = async (file: File) => {
    setIsLoading(true);
    
    try {
      // Create form data
      const formData = new FormData();
      formData.append('image', file);
      
      // Call backend API
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error('Failed to get prediction from server');
      }
      
      const data = await response.json();
      
      // Map API response to frontend format
      const detectionResult: DetectionResult = {
        breed: data.breed,
        confidence: data.confidence,
      };
      
      setResult(detectionResult);
      
      // Show success toast
      toast.success(`Detected: ${data.breed} (${data.confidence.toFixed(1)}% confidence)`);
      
    } catch (error) {
      console.error('Prediction error:', error);
      toast.error('Failed to detect breed. Make sure the backend server is running on http://localhost:5000');
      setResult(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setSelectedImage(null);
    setResult(null);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-background">
      <Hero />
      
      <section className="container px-4 py-16 mx-auto">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
              Upload & Detect
            </h2>
            <p className="text-lg text-muted-foreground">
              Get instant breed identification powered by advanced AI
            </p>
          </div>

          <ImageUpload
            onImageSelect={handleImageSelect}
            selectedImage={selectedImage}
            onClear={handleClear}
          />

          <DetectionResults result={result} isLoading={isLoading} />
        </div>
      </section>

      <section className="container px-4 py-16 mx-auto">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-foreground mb-12">
            Key Features
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-gradient-card rounded-xl p-6 shadow-elegant border border-border">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2">High Accuracy</h3>
              <p className="text-muted-foreground">
                Advanced AI models trained on thousands of livestock images for precise breed identification
              </p>
            </div>
            <div className="bg-gradient-card rounded-xl p-6 shadow-elegant border border-border">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <span className="text-2xl">⚡</span>
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2">Instant Results</h3>
              <p className="text-muted-foreground">
                Get breed detection results in seconds with confidence scores and detailed information
              </p>
            </div>
            <div className="bg-gradient-card rounded-xl p-6 shadow-elegant border border-border">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <span className="text-2xl">📱</span>
              </div>
              <h3 className="text-xl font-semibold text-foreground mb-2">Easy to Use</h3>
              <p className="text-muted-foreground">
                Simple drag-and-drop interface works seamlessly on any device, anywhere
              </p>
            </div>
          </div>
        </div>
      </section>

      <section
        id="learn-more"
        className="border-t border-border/60 bg-muted/30"
      >
        <div className="container px-4 py-16 mx-auto">
          <div className="max-w-4xl mx-auto bg-gradient-card rounded-xl p-8 shadow-elegant border border-border text-left">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-6">
              Learn More
            </h2>
            <p className="text-lg text-muted-foreground mb-4 leading-relaxed">
              India is home to one of the world's largest and most diverse cattle populations, with 41 recognized indigenous cattle breeds, each adapted to specific climatic conditions and agricultural needs. Accurate identification of cattle breeds plays a crucial role in livestock management, genetic conservation, dairy productivity, and sustainable farming practices.
            </p>
            <p className="text-lg text-muted-foreground mb-4 leading-relaxed">
              The Cattle Breed Prediction Model is designed to automatically identify cattle breeds using machine learning and image-based analysis. By analyzing key visual features such as body structure, coat pattern, horn shape, facial characteristics, and color distribution, the system predicts the most likely breed from the available dataset of Indian cattle breeds.
            </p>
            <p className="text-lg text-muted-foreground mb-4 leading-relaxed">
              This solution helps reduce dependency on manual identification, which often requires expert knowledge and is prone to human error. The model can assist farmers, veterinarians, researchers, and government agencies in making informed decisions related to breeding programs, health monitoring, and policy implementation.
            </p>
            <p className="text-lg text-muted-foreground leading-relaxed">
              Aligned with the <b>Smart India Hackathon (SIH) 2025 problem statement</b>, this project aims to promote digital transformation in agriculture and animal husbandry. It supports initiatives such as breed preservation, productivity enhancement, and data-driven livestock management, contributing to the growth of India's rural economy and sustainable agricultural development.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Index;
