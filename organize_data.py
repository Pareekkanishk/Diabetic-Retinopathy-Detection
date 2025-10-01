import os
import shutil
import pandas as pd
from pathlib import Path

# define the DR categories
DR_CATEGORIES = {
    0: "0_NO_DR",
    1: "1_Mild_DR",
    2: "2_Moderate_DR",
    3: "3_Severe_DR",
    4: "4_Proliferative_DR"
}

def organize_aptos_dataset(base_path="."):

    base_path = Path(base_path)
    
    # source folders
    dataset_info = [
        ("train_images", "train_1.csv"),
        ("test_images", "test.csv"),
        ("val_images", "valid.csv")
    ]

    output_dir = base_path / "organized_dataset"
    output_dir.mkdir(exist_ok=True)
    
    # creating category folders
    for category_name in DR_CATEGORIES.values():
        category_path = output_dir / category_name
        category_path.mkdir(exist_ok=True)
        print(f"Created folder: {category_path}")
    
    
    total_images = 0
    category_counts = {cat: 0 for cat in DR_CATEGORIES.values()}
    
    for folder_name, csv_file in dataset_info:
        folder_path = base_path / folder_name
        csv_path = base_path / csv_file
        
        # checking if folder and CSV exist
        if not folder_path.exists():
            print(f"Folder '{folder_name}' not found.")
            continue
        
        if not csv_path.exists():
            print(f"CSV file '{csv_file}' not found.")
            continue
        
        # Read CSV file
        try:
            df = pd.read_csv(csv_path)
            print(f"Loaded {len(df)} records from {csv_file}")
            
            # process each image
            for idx, row in df.iterrows():
                if 'id_code' in df.columns:
                    image_name = str(row['id_code'])
                elif 'image' in df.columns:
                    image_name = str(row['image'])
                else:
                    # define first column as image name
                    image_name = str(row.iloc[0])
                
                if 'diagnosis' in df.columns:
                    diagnosis = int(row['diagnosis'])
                else:
                    # define second column as diagnosis
                    diagnosis = int(row.iloc[1])
                
                image_file = None
                for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
                    potential_file = folder_path / f"{image_name}{ext}"
                    if potential_file.exists():
                        image_file = potential_file
                        break
                
                if image_file is None:
                    print(f"  Warning: Image not found for {image_name}")
                    continue
                
             
                category_name = DR_CATEGORIES[diagnosis]
                dest_folder = output_dir / category_name
                

                dest_filename = f"{folder_name.split('_')[0]}_{image_file.name}"
                dest_path = dest_folder / dest_filename
                
                # copy image to category folder
                try:
                    shutil.copy2(image_file, dest_path)
                    total_images += 1
                    category_counts[category_name] += 1
                except Exception as e:
                    print(f"  Error copying {image_file.name}: {e}")
            
            print(f"  Processed {folder_name} successfully")
            
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            continue


if __name__ == "__main__":

    organize_aptos_dataset()
    print("Done")