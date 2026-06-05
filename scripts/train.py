from ultralytics import YOLO

def train_model(model_dir):
    model = YOLO(model_dir)
    model.train(
        data="conf.yaml",
        epochs=50,
        patience=40,
        batch=-1,
        imgsz=1024,
        device=0,

        optimizer="AdamW",

        lr0=0.001,
        lrf=0.01,

        dropout=0.05,
        weight_decay=0.0005,

        mosaic=0.4,
        cutmix=0.05,
        copy_paste=0.1,

        save=True,
        save_period=10,
    )