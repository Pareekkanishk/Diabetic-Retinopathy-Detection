import os
import shutil
import pandas as pd
from pathlib import Path

test_csv = pd.read_csv('new_test_data.csv')  

source_folder = "new_test_images" 

output_folder = "test_organized"


categories = {
    0: "0_No_DR",
    1: "1_Mild_DR",
    2: "2_Moderate_DR",
    3: "3_Severe_DR",
    4: "4_Proliferative_DR"
}

for category_name in categories.values():
    Path(output_folder, category_name).mkdir(parents=True, exist_ok=True)


processed = 0
not_found = 0

for idx, row in test_csv.iterrows():
    
    if 'id_code' in test_csv.columns:
        image_name = str(row['id_code'])
    else:
        image_name = str(row.iloc[0])  
    
    diagnosis = int(row['diagnosis'])
    
    src_file = None
    for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
        potential_file = os.path.join(source_folder, f"{image_name}{ext}")
        if os.path.exists(potential_file):
            src_file = potential_file
            break
    
    if src_file:
        dst_file = os.path.join(output_folder, categories[diagnosis], os.path.basename(src_file))
        shutil.copy2(src_file, dst_file)
        processed += 1
    else:
        print(f"Warning: {image_name} not found")
        not_found += 1

print("ORGANIZATION COMPLETE!")
print(f"Images organized: {processed}")
print(f"Images not found: {not_found}")
print(f"Output folder: {output_folder}")
