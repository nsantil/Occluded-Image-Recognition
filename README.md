# Occluded Image Recognition
Occlusion-aware Object Detection pipeline using iterative model-assisted labeling and human-in-the-loop validation.

This project aims to create an object detection model that is lightweight enough to fit on an FPV drone, while robust enough to still detect both vehicles and humans with various levels of occlusion.

The dataset selected for this project was Natural, Occluded, Multi-scale Aerial Dataset, for Emergency Response Scenarios, aka [NOMAD](https://github.com/artruss/nomad), developed by Arturo Miguel Russell Bernal, Walter Scheirer, Jane Cleland-Huang.

While the original NOMAD dataset primarily focuses on occluded images of people, this project extends the dataset by adding custom bounding boxes for vehicles, enabling multi-class detection in dense and occluded scenes.

The current pipeline is structured to flow as the diagram below depicts:

[NOMAD Dataset]

      ↓
prepare_dataset.py

      ↓
[Cleaned Image Pool]

      ↓
train.py (YOLO Model)

      ↓
generate_labels.py (Pseudo-label generation)

      ↓
export_data.py (CVAT chunking)

      ↓
[CVAT Review & Validation]

      ↓
[Verified Dataset]

      ↓
train.py (retraining loop)


The models used in this project are YOLOv26n and YOLOv8n. The end goal of this project is for an FPV drone to provide real-time feedback using YOLOv8n due to its lightweight architecture and inference speed. 

During the annotation process YOLOv26n is used as a teacher model to generate pseudo-labels which are then refined through human validation. YOLOv8n is subsequently trained on the verified dataset for final deployment.


Script explanations:

    prep_dataset.py:
        Extracts and consolidates the images from the Actor based folders into a unified dataset.

    train.py:
        Handles model training and hyperparameter configuration for each run.

    utils.py:
        Image/label pairing
        Train/validation splitting
        Randomized sampling for dataset chunk generation

    generate_labels.py:
        Generates pseudo-labels using a trained YOLO model to accelerate dataset annotation and expansion

    export_data.py:
        Creates CVAT-compatible dataset chunks (~3.8GB each) by packaging image-label pairs for annotation and validation workflows.

In summary, this project builds a continuously improving dataset for occlusion-heavy object detection by integrating model-assisted annotation with human validation, enabling progressive refinement of detection performance over time, which is then deployed using a lightweight model on an FPV drone for real-time inference.
