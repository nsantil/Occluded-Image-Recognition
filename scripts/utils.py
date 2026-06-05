import random
import shutil

from pathlib import Path

def create_pairs(pairs: list, image_extensions, source_dir):
    image_extensions = {ext if ext.startswith('.') else f'.{ext}' for ext in image_extensions}

    for extention in image_extensions:
        for image_path in source_dir.rglob(f"*{extention}"):
                labels_path = image_path.with_suffix('.txt')

                if labels_path.exists():
                    pairs.append((image_path,labels_path))
                else:
                    print(f"Missing label for {image_path.name}")

    random.shuffle(pairs)
    return pairs

def populate_train_and_val(train_pairs:list, val_pairs:list, image_train_target_dir, labels_train_target_dir, image_val_target_dir, labels_val_target_dir):
    
    image_train_target_dir.mkdir(parents=True, exist_ok=True)
    labels_train_target_dir.mkdir(parents=True, exist_ok=True)

    image_val_target_dir.mkdir(parents=True, exist_ok=True)
    labels_val_target_dir.mkdir(parents=True, exist_ok=True)
    
    for image_path, labels_path in train_pairs:
        shutil.move(image_path, image_train_target_dir/image_path.name)
        shutil.move(labels_path, labels_train_target_dir/labels_path.name)

    for image_path,labels_path in val_pairs:
        shutil.move(image_path, image_val_target_dir/image_path.name)
        shutil.move(labels_path, labels_val_target_dir/labels_path.name)

    assert len(list(image_train_target_dir.iterdir())) == len(list(labels_train_target_dir.iterdir()))
    assert len(list(image_val_target_dir.iterdir())) == len(list(labels_val_target_dir.iterdir()))

# def remove_duplicates(source_dir):
#     image_train_dir = Path('./images/train')
#     image_val_dir = Path('./images/val')

#     existing_images = {image.name for image in image_train_dir.iterdir()} | {image.name for image in image_val_dir.iterdir()}

#     for image in source_dir.iterdir():
#         image_path = Path(source_dir/image.name)

#         if image.name in existing_images:
#             image_path.unlink(missing_ok=True)