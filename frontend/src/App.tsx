import { useRef, useState } from "react";
import DrawingCanvas, {
  type DrawingCanvasHandle,
} from "./components/DrawingCanvas";
import PredictionResult from "./components/PredictionResult";
import { predictDigit, PredictionError } from "./lib/api";
import type { PredictionResponse } from "./types";

type Status = "idle" | "loading" | "success" | "error";

function App() {
  const canvasRef = useRef<DrawingCanvasHandle>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleClear = () => {
    canvasRef.current?.clear();
    setStatus("idle");
    setResult(null);
    setErrorMessage(null);
  };

  const handlePredict = async () => {
    const canvas = canvasRef.current;
    if (!canvas || canvas.isEmpty()) {
      setStatus("error");
      setErrorMessage("Draw a digit first.");
      return;
    }

    setStatus("loading");
    setErrorMessage(null);

    try {
      const prediction = await predictDigit(canvas.getImageDataUrl());
      setResult(prediction);
      setStatus("success");
    } catch (error) {
      const message =
        error instanceof PredictionError
          ? error.message
          : "Something went wrong.";
      setErrorMessage(message);
      setStatus("error");
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center gap-6 bg-gray-100 px-4 py-12">
      <header className="text-center">
        <h1 className="text-3xl font-semibold text-gray-900">
          Handwritten Digit Recognition
        </h1>
        <p className="mt-1 text-gray-500">Draw a digit below</p>
      </header>

      <DrawingCanvas ref={canvasRef} />

      <div className="flex gap-3">
        <button
          type="button"
          onClick={handleClear}
          className="rounded bg-red-500 px-4 py-2 text-white transition-colors hover:bg-red-600"
        >
          Clear
        </button>
        <button
          type="button"
          onClick={handlePredict}
          disabled={status === "loading"}
          className="rounded bg-blue-600 px-4 py-2 text-white transition-colors hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Predict
        </button>
      </div>

      <PredictionResult
        status={status}
        result={result}
        errorMessage={errorMessage}
      />
    </div>
  );
}

export default App;
