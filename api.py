from pathlib import Path
from uuid import uuid4

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "best.pt"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))
app = FastAPI(title="SolarSentinel API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/results", StaticFiles(directory=str(RESULTS_DIR)), name="results")

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/bmp"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}

@app.get("/api/health")
def health():
    return {"status": "ok", "model_loaded": True}

@app.post("/api/analyze")
async def analyze(request: Request, file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    if file.content_type not in ALLOWED_TYPES and suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(415, "Upload a JPG, PNG, WEBP, or BMP image.")

    contents = await file.read(MAX_FILE_SIZE + 1)
    if not contents:
        raise HTTPException(400, "The uploaded file is empty.")
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(413, "Image exceeds the 10 MB limit.")

    image = cv2.imdecode(np.frombuffer(contents, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(400, "Could not decode this image.")

    try:
        result = model.predict(source=image, imgsz=512, conf=0.25, verbose=False)[0]
        boxes = result.boxes
        num_defects = len(boxes) if boxes is not None else 0
        detected = num_defects > 0
        labels, scores, bboxes = [], [], []

        if detected:
            for box in boxes:
                class_id = int(box.cls.item())
                label = model.names.get(class_id, str(class_id))
                labels.append(label)
                scores.append(float(box.conf.item()))
                if hasattr(box, "xyxy") and len(box.xyxy) > 0:
                    bboxes.append([round(float(c), 2) for c in box.xyxy[0].tolist()])

        status = "Anomaly" if detected else "Healthy"
        confidence = round(max(scores) * 100, 2) if scores else 0.0

        ok, encoded = cv2.imencode(".jpg", result.plot())
        if not ok:
            raise RuntimeError("Could not encode annotated prediction.")
        output_name = f"{uuid4().hex}.jpg"
        (RESULTS_DIR / output_name).write_bytes(encoded.tobytes())

        base_url = str(request.base_url).rstrip("/")
        highlighted_image_url = f"{base_url}/results/{output_name}"

        if detected:
            defect_classes = sorted(set(labels))
            class_str = ", ".join(defect_classes)
            defect_word = "defect" if num_defects == 1 else "defects"
            summary = f"Model detected {num_defects} {defect_word} ({class_str})."
            recommendation = "Review the highlighted regions and confirm with a qualified technician before maintenance."
            severity = "High" if confidence >= 85 else "Medium"
        else:
            summary = "The model did not detect any trained defect class in this image."
            recommendation = "No trained defect class was detected. Continue routine monitoring and follow site procedures."
            severity = "None"

        return {
            "status": status,
            "confidence": confidence,
            "severity": severity,
            "summary": summary,
            "recommendation": recommendation,
            "highlighted_image_url": highlighted_image_url,
            "num_defects": num_defects,
            "detected_classes": sorted(set(labels)),
            "boxes": bboxes,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(500, f"Model inference failed: {exc}") from exc
