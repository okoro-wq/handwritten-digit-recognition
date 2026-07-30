import type { PredictionResponse } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class PredictionError extends Error {}

export async function predictDigit(
  imageDataUrl: string,
): Promise<PredictionResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageDataUrl }),
    });
  } catch {
    throw new PredictionError(
      "Couldn't reach the prediction server. Is the backend running?",
    );
  }

  if (!response.ok) {
    throw new PredictionError(`Prediction failed (${response.status}).`);
  }

  return (await response.json()) as PredictionResponse;
}
