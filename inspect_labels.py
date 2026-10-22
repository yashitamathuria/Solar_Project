
from pathlib import Path
from collections import Counter

# Find the dataset configuration file
yaml_files = list(Path(".").rglob("data.yaml"))

if not yaml_files:
    print("ERROR: data.yaml not found.")
    raise SystemExit

yaml_path = yaml_files[0]
dataset_root = yaml_path.parent

print("DATASET YAML:", yaml_path)
print("\n========== data.yaml CONTENT ==========")
print(yaml_path.read_text(encoding="utf-8"))

print("\n========== FOLDER CHECK ==========")
for split in ["train", "valid", "test"]:
    image_dir = dataset_root / split / "images"
    label_dir = dataset_root / split / "labels"

    print(f"\n{split.upper()}")
    print("Images folder exists:", image_dir.exists())
    print("Labels folder exists:", label_dir.exists())

    if image_dir.exists():
        print("Images:", len(list(image_dir.glob("*"))))

    if label_dir.exists():
        print("Label files:", len(list(label_dir.glob("*.txt"))))

print("\n========== SAMPLE ANNOTATIONS ==========")

label_files = list(dataset_root.rglob("*.txt"))
label_files = [
    p for p in label_files
    if p.parent.name == "labels"
]

class_counts = Counter()
annotation_count = 0
empty_files = 0

for label_file in label_files:
    lines = label_file.read_text(
        encoding="utf-8"
    ).splitlines()

    if not lines:
        empty_files += 1

    for line in lines:
        parts = line.split()

        if parts:
            class_counts[parts[0]] += 1
            annotation_count += 1

print("Label files found:", len(label_files))
print("Total annotations:", annotation_count)
print("Empty label files:", empty_files)
print("Class ID counts:", dict(class_counts))

shown = 0
for label_file in label_files:
    lines = label_file.read_text(
        encoding="utf-8"
    ).splitlines()

    if lines:
        print(f"\n{label_file}:")
        for line in lines[:3]:
            print(" ", line)

        shown += 1

    if shown >= 3:
        break
