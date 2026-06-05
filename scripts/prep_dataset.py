import shutil
from pathlib import Path

def unzip_data(dest_dir):
    root_dir = Path('.')
    dest_dir.mkdir(parents=True, exist_ok=True)

    for zip_file in root_dir.glob('Actor*.zip'):
        shutil.unpack_archive(zip_file, root_dir)

    for actor_dir in root_dir.glob('Actor*'):
        if actor_dir.is_dir():
            for image in actor_dir.rglob('*.jpg'):
                shutil.move(str(image), dest_dir/image.name)

    for actor_dir in root_dir.glob('Actor*'):
        if actor_dir.is_dir():
            shutil.rmtree(actor_dir)
        if actor_dir.is_file():
            actor_dir.unlink()

