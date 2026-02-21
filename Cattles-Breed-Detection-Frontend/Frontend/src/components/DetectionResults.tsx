import { CheckCircle } from "lucide-react";

interface DetectionResult {
  breed: string;
  confidence: number;
}

interface DetectionResultsProps {
  result: DetectionResult | null;
  isLoading: boolean;
}

const DetectionResults = ({ result, isLoading }: DetectionResultsProps) => {
  if (isLoading) {
    return (
      <div className="w-full max-w-2xl mx-auto mt-8 animate-scale-in">
        <div className="bg-gradient-card rounded-xl p-8 shadow-elegant">
          <div className="flex items-center justify-center gap-3">
            <div className="w-6 h-6 border-3 border-primary border-t-transparent rounded-full animate-spin" />
            <p className="text-lg font-medium text-foreground">Analyzing image...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!result) return null;

  return (
    <div className="w-full max-w-2xl mx-auto mt-8 animate-scale-in">
      <div className="bg-gradient-card rounded-xl p-8 shadow-elegant border-2 border-primary">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 rounded-full bg-primary/10">
            <CheckCircle className="w-6 h-6 text-primary" />
          </div>
          <h2 className="text-2xl font-bold text-foreground">Detection Results</h2>
        </div>

        <div className="space-y-6">
          <div>
            <p className="text-sm text-muted-foreground mb-2">Detected Breed</p>
            <p className="text-3xl font-bold text-primary">{result.breed}</p>
          </div>

          <div>
            <p className="text-sm text-muted-foreground mb-3">Confidence Score</p>
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-2xl font-bold text-foreground">
                  {result.confidence.toFixed(2)}%
                </span>
              </div>
              <div className="w-full bg-muted rounded-full h-4 overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-primary to-accent transition-all duration-500 ease-out rounded-full"
                  style={{ width: `${Math.min(result.confidence, 100)}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DetectionResults;
