import { useRef } from "react";

export default function DrawingCanvas() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  return (
    <canvas
        ref={canvasRef} 
        width={400}
        height={400}
    />
  );
}