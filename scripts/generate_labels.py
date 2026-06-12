import shutil
from pathlib import Path

from ultralytics import YOLO

def detect(MODEL_DIR):
    model = YOLO(MODEL_DIR)
    source = Path("./images and labels")
    labels_dir = Path("./runs/detect/labels_only/labels")
    labels_only_dir = Path('./runs/detect/labels_only')
    results = model.predict(source=source, save_txt=True, name="labels_only", stream=True)

    for result in results:
        pass

    for txt_file in labels_dir.glob("*.txt"):
        shutil.move(str(txt_file), source / txt_file.name)

    shutil.rmtree(labels_only_dir)