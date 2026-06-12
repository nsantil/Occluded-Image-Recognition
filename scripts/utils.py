import random
import shutil

from pathlib import Path

IMAGE_TRAIN_TARGET_DIR = Path('./images/train')
LABELS_TRAIN_TARGET_DIR = Path('./labels/train')
IMAGE_VAL_TARGET_DIR = Path('./images/val')
LABELS_VAL_TARGET_DIR = Path('./labels/val')

def create_pairs(image_extensions, SOURCE_DIR):

    pairs = []

    image_extensions = {ext if ext.startswith('.') else f'.{ext}' for ext in image_extensions}

    for extention in image_extensions:
        for image_path in SOURCE_DIR.rglob(f"*{extention}"):
                labels_path = image_path.with_suffix('.txt')

                if labels_path.exists():
                    pairs.append((image_path,labels_path))
                else:
                    print(f"Missing label for {image_path.name}")

    random.shuffle(pairs)

    print(f"Found {len(pairs)} image-label pairs")

    return pairs


def split_pairs(pairs, train_ratio=0.8):
    split_idx = int(len(pairs) * train_ratio)
    train_pairs = pairs[:split_idx]
    val_pairs = pairs[split_idx:]

    return train_pairs, val_pairs


def populate_train_and_val(train_pairs:list, val_pairs:list):
    
    IMAGE_TRAIN_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    LABELS_TRAIN_TARGET_DIR.mkdir(parents=True, exist_ok=True)

    IMAGE_VAL_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    LABELS_VAL_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    for image_path, labels_path in train_pairs:
        shutil.move(image_path, IMAGE_TRAIN_TARGET_DIR/image_path.name)
        shutil.move(labels_path, LABELS_TRAIN_TARGET_DIR/labels_path.name)

    for image_path,labels_path in val_pairs:
        shutil.move(image_path, IMAGE_VAL_TARGET_DIR/image_path.name)
        shutil.move(labels_path, LABELS_VAL_TARGET_DIR/labels_path.name)

    assert len(list(IMAGE_TRAIN_TARGET_DIR.iterdir())) == len(list(LABELS_TRAIN_TARGET_DIR.iterdir()))
    assert len(list(IMAGE_VAL_TARGET_DIR.iterdir())) == len(list(LABELS_VAL_TARGET_DIR.iterdir()))

def remove_duplicates(SOURCE_DIR):
    image_train_dir = Path('./images/train')
    image_val_dir = Path('./images/val')

    if not image_train_dir.exists():
        image_train_dir.mkdir(parents=True, exist_ok=True)

    if not image_val_dir.exists():
        image_val_dir.mkdir(parents=True, exist_ok=True)

    existing_images = {image.name for image in image_train_dir.iterdir()} | {image.name for image in image_val_dir.iterdir()}
    
    for image in SOURCE_DIR.iterdir():
        image_path = Path(SOURCE_DIR/image.name)
        label_path = image_path.with_suffix('.txt')

        if image.name in existing_images:
            image_path.unlink(missing_ok=True)
            label_path.unlink(missing_ok=True)