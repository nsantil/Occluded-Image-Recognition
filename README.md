# Occluded Image Recognition
Occlusion-aware object detection pipeline using iterative model-assisted labeling and human-in-the-loop validation.

This project aims to create an object detection model that is lightweight enough to fit on an FPV drone, while robust enough to still detect both vehicles and humans with various levels of occlusion.

The dataset selected for this project is the Natural, Occluded, Multi-scale Aerial Dataset, for Emergency Response Scenarios ([NOMAD])(https://github.com/artruss/nomad), developed by Arturo Miguel Russell Bernal, Walter Scheirer, Jane Cleland-Huang.

While the original NOMAD dataset primarily focuses on occluded images of people, this project extends the dataset by adding custom bounding boxes for vehicles, enabling multi-class detection in dense and occluded scenes.

The current pipeline is structured to flow as the diagram below depicts:

      [NOMAD Dataset]
            ↓
      prep_dataset.py
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

During the annotation process, YOLOv26n is used as a teacher model to generate pseudo-labels which are then refined through human validation. YOLOv8n is subsequently trained on the verified dataset for final deployment.

Script explanations:

      prep_dataset.py <DEST_DIR>:
        Extracts and consolidates images from the NOMAD Actor folders into a unified dataset. 
        Inputs: 
            DEST_DIR: 
                  Destination directory where extracted images will be moved. 
                  Example: 
                        Path("./images and labels")

      train.py <MODEL_DIR>:
        Handles YOLO model training and hyperparameter configuration for each run. 
        Inputs: 
            MODEL_DIR: 
                  Path to a YOLO model or checkpoint to train from. 
                  Examples:
                        "./runs/detect/train2/weights/best.pt"
                        "yolov8n.pt"

      utils.py:
            create_pairs(<IMAGE_EXTENSIONS>, <SOURCE_DIR>) 
                  Creates image/label pairs and randomly shuffles them. 
                  
                  IMAGE_EXTENSIONS: Set of image extensions to search for. 
                        Example: {".jpg"} 
                  
                  SOURCE_DIR: Directory containing image and label files. Example: Path("./images and labels")
                  
                  split_pairs(<PAIRS>, <TRAIN_RATIO=0.8>) 
                        Splits image/label pairs into training and validation sets. 
                        
                        PAIRS: 
                              Output returned by create_pairs(). 
                              
                        TRAIN_RATIO: 
                              Percentage of data allocated to training. 
                              Default: 
                                    0.8 (80% train / 20% validation) 

            populate_train_and_val(<TRAIN_PAIRS>, <VAL_PAIRS>) 
                  Moves image/label pairs into the training and validation directories. 
                  
                  TRAIN_PAIRS: Output returned by split_pairs(). 
                  
                  VAL_PAIRS: Output returned by split_pairs(). 
                  
                  Note: 
                        Output directories are currently hardcoded as: 
                              ./images/train
                              ./images/val
                              ./labels/train
                              ./labels/val 
                              
            remove_duplicates(<SOURCE_DIR>) 
                  Removes images and labels that already exist in the training or validation directories. 

                  SOURCE_DIR: 
                        Directory to scan for duplicate image/label pairs.

      generate_labels.py <MODEL_DIR>:
            Generates pseudo-labels using a trained YOLO model to accelerate annotation and dataset expansion. 
            
            Inputs: 
                  MODEL_DIR: 
                        Path to the YOLO model used for inference.

            Notes: 
                  The inference source directory is currently hardcoded as: 
                        "./images and labels" 
                        
                  Generated labels are automatically moved back into the source directory.

      export_data.py <SOURCE_DIR>, <OBJ_DATA>, <OBJ_NAMES>, <IMAGE_EXTENSIONS> 
            Creates CVAT-compatible dataset chunks (~3.8 GB each) by packaging image/label pairs for annotation and validation workflows. 
            
            Inputs: 
                  SOURCE_DIR: 
                        Directory containing image/label pairs to export. 

                  OBJ_DATA:
                        Path to the YOLO obj.data configuration file.
                  
                  OBJ_NAMES: 
                        Path to the YOLO obj.names file.

                  IMAGE_EXTENSIONS:
                        Set of image extensions to include. 
                        
                        Example: 
                              {".jpg"} 
                              
            Notes: 
                  Output directory is currently hardcoded as: 
                        ./dataset_chunks 
                        
                  Chunk size is currently hardcoded to approximately 3.8 GB to remain below CVAT's 4 GB import limit.

In summary, this project builds a continuously improving dataset for occlusion-heavy object detection by integrating model-assisted annotation with human validation. Verified annotations are continuously incorporated into the training set, enabling progressive refinement of detection performance over time. The resulting lightweight model is intended for deployment on an FPV drone for real-time inference.
