import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

def split_organized_dataset(
    source_dir="organized_dataset",
    train_dir="train_dataset",
    val_dir="val_dataset",
    train_ratio=0.8,
    val_ratio=0.2,
    random_seed=42
):
 
    random.seed(random_seed)
    
    source_path = Path(source_dir)
    train_dir = Path(train_dir)
    val_dir = Path(val_dir)
    
    # checking if source directory exists
    if not source_path.exists():
        print(f"Source directory '{source_dir}' not found.")
        return

    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    
    # getting all the category folders
    category_folders = [f for f in source_path.iterdir() if f.is_dir()]
    
    if not category_folders:
        print(f"No category folders found in '{source_dir}'!")
        return
    
    
    total_train = 0
    total_val = 0
    split_summary = []
    
    for category_folder in sorted(category_folders):
        category_name = category_folder.name
        print(f"\nProcessing category: {category_name}")
        
        train_category = train_dir / category_name
        val_category = val_dir / category_name
        
        train_category.mkdir(exist_ok=True)
        val_category.mkdir(exist_ok=True)
        
        # getting all the images in this category
        image_files = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']:
            image_files.extend(list(category_folder.glob(ext)))
        
        total_images = len(image_files)
        
        if total_images == 0:
            print(f"No images found in {category_name}")
            continue
        
        # shuffling immages
        random.shuffle(image_files)
        
        train_count = int(total_images * train_ratio)
        
        # split images
        train_images = image_files[:train_count]
        val_images = image_files[train_count:]
        
        # copy train images
        for img in train_images:
            dest = train_category / img.name
            shutil.copy2(img, dest)
        
        # copy validation images
        for img in val_images:
            dest = val_category / img.name
            shutil.copy2(img, dest)
        
        total_train += len(train_images)
        total_val += len(val_images)

if __name__ == "__main__":

    split_organized_dataset(
        source_dir="organized_dataset",
        train_dir="train_dataset",
        val_dir="val_dataset",
        train_ratio=0.8,
        val_ratio=0.2,
        random_seed=42
    )
    print("Done")