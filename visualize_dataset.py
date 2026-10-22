
from pathlib import Path
import random
import cv2
import yaml
import matplotlib.pyplot as plt

yaml_path = Path("PV_Thermal_Defects_Dataset/Common_data/data.yaml")
dataset_root = yaml_path.parent

with open(yaml_path, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

image_dir = dataset_root / "train" / "images"
label_dir = dataset_root / "train" / "labels"

images = list(image_dir.glob("*.jpg"))

if not images:
    print("No JPG images found. Check the dataset path.")
    raise SystemExit

random.seed(42)
samples = random.sample(images, min(6, len(images)))

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
axes = axes.flatten()

for ax, image_path in zip(axes, samples):
    image = cv2.imread(str(image_path))

    if image is None:
        ax.set_title("Could not read image")
        ax.axis("off")
        continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    height, width = image.shape[:2]

    label_path = label_dir / f"{image_path.stem}.txt"

    if label_path.exists():
        for line in label_path.read_text().splitlines():
            parts = line.split()

            if len(parts) != 5:
                continue

            class_id, xc, yc, bw, bh = map(float, parts)

            x1 = int((xc - bw / 2) * width)
            y1 = int((yc - bh / 2) * height)
            x2 = int((xc + bw / 2) * width)
            y2 = int((yc + bh / 2) * height)

            cv2.rectangle(
                image, (x1, y1), (x2, y2), (0, 255, 0), 2
            )

    ax.imshow(image)
    ax.set_title(image_path.name[:25])
    ax.axis("off")

for ax in axes[len(samples):]:
    ax.axis("off")

plt.tight_layout()
plt.show()
