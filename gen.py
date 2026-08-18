# flake8: noqa
import random
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Team seed - CHANGE THIS to your team's assigned seed once you get it from the instructor
SEED = 1015  # placeholder: Group 10, Project 15
random.seed(SEED)

# 3 disease classes, 2 features each (texture, colour), 8-bit range 0-255
centroids = [
    {"label": "healthy",       "texture": 40,  "colour": 180},
    {"label": "black_pod",     "texture": 150, "colour": 60},
    {"label": "swollen_shoot", "texture": 90,  "colour": 120},
]

with open(BASE_DIR / "centroids.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["label", "texture", "colour"])
    w.writeheader()
    for c in centroids:
        w.writerow(c)

# Generate N noisy samples around each centroid, clipped to 0-255
N_PER_CLASS = 20
NOISE = 15  # max +/- noise added to each feature

rows = []
sample_id = 1
for c in centroids:
    for _ in range(N_PER_CLASS):
        texture = max(0, min(255, c["texture"] + random.randint(-NOISE, NOISE)))
        colour  = max(0, min(255, c["colour"]  + random.randint(-NOISE, NOISE)))
        rows.append({
            "sample_id": sample_id,
            "texture": texture,
            "colour": colour,
            "true_label": c["label"],
        })
        sample_id += 1

random.shuffle(rows)
for i, r in enumerate(rows, start=1):
    r["sample_id"] = i

with open(BASE_DIR / "features.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["sample_id", "texture", "colour", "true_label"])
    w.writeheader()
    w.writerows(rows)

print(f"Generated {len(centroids)} centroids and {len(rows)} feature samples (seed={SEED})")
