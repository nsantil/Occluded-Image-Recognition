import random
import shutil
import scripts.utils as utils

from pathlib import Path

def create_chunk_dirs(chunk_id, base_output_dir, obj_data, obj_names):
    chunk_dir = base_output_dir / f'dataset_chunk_{chunk_id}'
    image_dir = chunk_dir / 'images'
    label_dir = chunk_dir / 'images'

    image_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(obj_data, chunk_dir/'obj.data')
    shutil.copyfile(obj_names, chunk_dir/'obj.names')

    train_file = chunk_dir/'train.txt'
    train_file.write_text('')

    return chunk_dir, image_dir, label_dir, train_file

def finalize_chunk(chunk_dir):
    zip_path = shutil.make_archive(str(chunk_dir), 'zip', chunk_dir)
    print(f"Created: {zip_path}")


def generate_random_chunks(target_size, source_dir, base_output_dir, obj_data, obj_names, image_extensions):
    chunk_id = 0
    current_size = 0

    pairs = []
    utils.create_pairs(pairs, image_extensions, source_dir)

    chunk_dir, image_target_dir, label_target_dir, train_file = create_chunk_dirs(chunk_id, base_output_dir, obj_data, obj_names)


    for image_path, labels_path in pairs:
        pair_size = image_path.stat().st_size + labels_path.stat().st_size

        if current_size + pair_size > target_size:
            finalize_chunk(chunk_dir)

            chunk_id += 1
            current_size = 0
            chunk_dir, image_target_dir, label_target_dir, train_file = create_chunk_dirs(chunk_id, base_output_dir, obj_data, obj_names)

        shutil.move(str(image_path), image_target_dir / image_path.name)
        shutil.move(str(labels_path), label_target_dir / labels_path.name)

        with open(train_file, 'a') as f:
            f.write(f"images/{image_path.name}\n")

        current_size += pair_size

    finalize_chunk(chunk_dir)