import type { PredictionResponse } from "../types";

interface PredictionResultProps {
  status: "idle" | "loading" | "success" | "error";
  result: PredictionResponse | null;
  errorMessage: string | null;
}

function PredictionResult({ status, result, errorMessage }: PredictionResultProps) {
  if (status === "idle") return null;

  if (status === "loading") {
    return (
      <p className="text-sm text-gray-500" role="status">
        Predicting…
      </p>
    );
  }

  if (status === "error") {
    return (
      <p className="text-sm text-red-600" role="alert">
        {errorMessage ?? "Something went wrong."}
      </p>
    );
  }

  if (!result) return null;

  return (
    <div className="text-center" role="status">
      <p className="text-lg">
        Digit: <span className="font-semibold">{result.digit}</span>
      </p>
      <p className="text-sm text-gray-500">
        Confidence: {(result.confidence * 100).toFixed(1)}%
      </p>
    </div>
  );
}

export default PredictionResult;
