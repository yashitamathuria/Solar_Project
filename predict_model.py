
from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = Path(
    r"runs\detect\runs\solarsentinel\defect_detector-3\weights\best.pt"
)

TEST_DIR = Path(
    r"PV_Thermal_Defects_Dataset\Common_data\test\images"
)

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH.resolve()}")

if not TEST_DIR.exists():
    raise FileNotFoundError(f"Test images not found: {TEST_DIR.resolve()}")

# Load trained model
model = YOLO(str(MODEL_PATH))

# Run defect detection on test images
results = model.predict(
    source=str(TEST_DIR),
    imgsz=512,
    conf=0.25,
    device=0,
    save=True
)

print(f"Processed {len(results)} images.")

if results:
    print("Annotated images saved inside the prediction output folder.")
