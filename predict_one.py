
from pathlib import Path
from ultralytics import YOLO

model_path = Path(
    r"runs\detect\runs\solarsentinel\defect_detector-3\weights\best.pt"
)

test_dir = Path(
    r"PV_Thermal_Defects_Dataset\Common_data\test\images"
)

# Select the first available image
images = list(test_dir.glob("*"))
images = [p for p in images if p.suffix.lower() in
          [".jpg", ".jpeg", ".png", ".bmp", ".webp"]]

if not images:
    raise FileNotFoundError("No test images found.")

model = YOLO(str(model_path))
image_path = images[0]

print("Input image:", image_path)

results = model.predict(
    source=str(image_path),
    imgsz=512,
    conf=0.25,
    device=0,
    save=True
)

print("Prediction complete.")
