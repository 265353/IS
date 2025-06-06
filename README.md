if you want use yolo to for segmentation,you need follew this steps:
    first convert dataset for yolo
        1 download MVtecAD dataset
        2 use convert_mask_yolo.py ,convert the category you want to use in MVTec,you should change the path in the code 
        3 check the file ,and find the dataset.yaml,this file will be used in train and val
    second train and test
        1 use train.py to train and test,you will find result in ./runs/segamentation/trainx,while x is the number
        2for the fact that yolo do not provide the auroc,we should cal it ,you can use AUROC_CAL.py to cal for one folder;you can also use auto_cal.py to cal more then one file ,remember the folder name must be trainx,for exemple ,if the folder is train1 train3,you should rename them before you use it 
if you want use anomalib for this task you need follow this steps\
    first,environment;
        you can find environment request file for windows and linux,It is recommended not to use the latest versions of NumPy and Anomalib environments, as both have recently undergone major version updates.
    secone run scripts
        You can find scripts provided for both Windows and Linux.