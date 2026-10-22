
from pathlib import Path
from collections import Counter

# Change this path if your dataset is stored elsewhere
DATASET_PATH = Path("PV_Thermal_Defects_Dataset")

if not DATASET_PATH.exists():
    print("Dataset folder not found!")
    print("Please check the folder path.")
else:
    print("\nDATASET INSPECTION REPORT")
    print("=" * 40)

    # Count all files and file types
    all_files = [p for p in DATASET_PATH.rglob("*") if p.is_file()]
    extensions = Counter(
        p.suffix.lower() or "[no extension]"
        for p in all_files
    )

    print("Total files:", len(all_files))
    print("\nFile types:")

    for ext, count in extensions.most_common():
        print(f"{ext}: {count}")

    print("\nFolder structure (first 60 entries):")

    entries = sorted(DATASET_PATH.rglob("*"))

    for path in entries[:60]:
        print(path.relative_to(DATASET_PATH))

    print("\nPossible image count:")

    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    images = [
        p for p in all_files
        if p.suffix.lower() in image_extensions
    ]

    print("Images found:", len(images))

    print("\nFirst 10 image paths:")

    for image_path in images[:10]:
        print(image_path)
