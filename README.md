If you want to use YOLO for segmentation, you need to follow these steps:

### YOLO Segmentation Steps

1. **Convert Dataset for YOLO**
   - Download MVtecAD dataset
   - Use `convert_mask_yolo.py` to convert the category you want to use in MVTec
     - *Note*: You should change the path in the code
   - Check the files and find `dataset.yaml`
     - This file will be used in training and validation

2. **Train and Test**
   - Use `train.py` to train and test
     - Results will be saved in `./runs/segmentation/trainx` (where x is the number)
   - Since YOLO doesn't provide AUROC, you need to calculate it:
     - Use `AUROC_CAL.py` to calculate for one folder
     - Use `auto_cal.py` to calculate for multiple files
       - *Important*: Folder names must be in format `trainx` (e.g., `train1`, `train3`)
       - Rename folders before using if needed

---

If you want to use Anomalib for this task, follow these steps:

### Anomalib Implementation Steps

1. **Environment Setup**
   - Environment requirement files are available for both Windows and Linux
   - *Recommendation*: 
     ```markdown
     Do NOT use the latest versions of:
     - NumPy
     - Anomalib
     ```
     As both have recently undergone major version updates

2. **Run Scripts**
   - Scripts are provided for both Windows and Linux platforms
