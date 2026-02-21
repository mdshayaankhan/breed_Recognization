import { useState, useRef } from "react";
import { Upload, X, Image as ImageIcon } from "lucide-react";
import { toast } from "sonner";

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  selectedImage: string | null;
  onClear: () => void;
}

const ImageUpload = ({ onImageSelect, selectedImage, onClear }: ImageUploadProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
      onImageSelect(file);
    } else {
      toast.error("Please upload a valid image file");
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageSelect(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div id="upload" className="w-full max-w-2xl mx-auto animate-scale-in">
      {!selectedImage ? (
        <div
          onClick={handleClick}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`
            relative border-2 border-dashed rounded-xl p-12 text-center cursor-pointer
            transition-all duration-300 bg-gradient-card
            ${isDragging 
              ? "border-primary bg-primary/5 scale-105" 
              : "border-border hover:border-primary hover:shadow-elegant"
            }
          `}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
          />
          
          <div className="flex flex-col items-center gap-4">
            <div className="p-4 rounded-full bg-primary/10">
              <Upload className="w-12 h-12 text-primary" />
            </div>
            <div>
              <p className="text-xl font-semibold text-foreground mb-2">
                Upload Cattle or Buffalo Image
              </p>
              <p className="text-muted-foreground">
                Drag and drop or click to browse
              </p>
              <p className="text-sm text-muted-foreground mt-2">
                Supports JPG, PNG, WEBP
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="relative rounded-xl overflow-hidden shadow-elegant bg-card">
          <button
            onClick={onClear}
            className="absolute top-4 right-4 z-10 p-2 rounded-full bg-destructive text-destructive-foreground hover:bg-destructive/90 transition-all"
          >
            <X className="w-5 h-5" />
          </button>
          <img
            src={selectedImage}
            alt="Selected livestock"
            className="w-full h-auto max-h-[500px] object-contain"
          />
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
