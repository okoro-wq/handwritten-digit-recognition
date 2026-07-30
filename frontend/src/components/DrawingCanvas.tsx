import { forwardRef, useEffect, useImperativeHandle, useRef } from "react";

const CANVAS_SIZE = 400;
const STROKE_WIDTH = 20;

export interface DrawingCanvasHandle {
  clear: () => void;
  getImageDataUrl: () => string;
  isEmpty: () => boolean;
}

function paintBackground(ctx: CanvasRenderingContext2D) {
  ctx.fillStyle = "white";
  ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
}

const DrawingCanvas = forwardRef<DrawingCanvasHandle>((_props, ref) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const isDrawingRef = useRef(false);
  const hasDrawnRef = useRef(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) return;

    paintBackground(ctx);
    ctx.lineWidth = STROKE_WIDTH;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    ctx.strokeStyle = "black";
  }, []);

  useImperativeHandle(ref, () => ({
    clear: () => {
      const canvas = canvasRef.current;
      const ctx = canvas?.getContext("2d");
      if (!canvas || !ctx) return;

      paintBackground(ctx);
      hasDrawnRef.current = false;
    },
    getImageDataUrl: () => canvasRef.current?.toDataURL("image/png") ?? "",
    isEmpty: () => !hasDrawnRef.current,
  }));

  const pointFromEvent = (event: React.PointerEvent<HTMLCanvasElement>) => {
    const rect = event.currentTarget.getBoundingClientRect();
    return { x: event.clientX - rect.left, y: event.clientY - rect.top };
  };

  const handlePointerDown = (event: React.PointerEvent<HTMLCanvasElement>) => {
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx) return;

    event.currentTarget.setPointerCapture(event.pointerId);
    isDrawingRef.current = true;

    const { x, y } = pointFromEvent(event);
    ctx.beginPath();
    ctx.moveTo(x, y);
  };

  const handlePointerMove = (event: React.PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawingRef.current) return;

    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx) return;

    const { x, y } = pointFromEvent(event);
    ctx.lineTo(x, y);
    ctx.stroke();

    hasDrawnRef.current = true;
  };

  const stopDrawing = (event: React.PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawingRef.current) return;

    isDrawingRef.current = false;
    canvasRef.current?.releasePointerCapture(event.pointerId);
    canvasRef.current?.getContext("2d")?.beginPath();
  };

  return (
    <canvas
      ref={canvasRef}
      width={CANVAS_SIZE}
      height={CANVAS_SIZE}
      aria-label="Digit drawing canvas"
      role="img"
      className="touch-none rounded-lg border border-gray-300 bg-white shadow-sm"
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={stopDrawing}
      onPointerCancel={stopDrawing}
      onPointerLeave={stopDrawing}
    />
  );
});

DrawingCanvas.displayName = "DrawingCanvas";

export default DrawingCanvas;
