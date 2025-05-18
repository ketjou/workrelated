import pandas as pd
import os
import zipfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict

# Function to process each file and return duplicates with filenames
def process_file(file_path):
    seen_local = set()
    duplicates_local = defaultdict(list)
    
    try:
        # Load the first column as integers from a text file with specified encoding
        data = pd.read_csv(file_path, header=None, usecols=[0], dtype={0: 'int'}, encoding='latin1')
        
        # Identify duplicates and track filenames
        for id_value in data[0]:
            if id_value in seen_local:
                duplicates_local[id_value].append(os.path.basename(file_path))
            else:
                seen_local.add(id_value)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    
    return duplicates_local

# Function to extract files from a ZIP archive
def extract_zip(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main():
    # Get folder path from the user
    folder_path = input("Please enter the folder path containing the ZIP files: ")

    # Validate the folder path
    if not os.path.exists(folder_path):
        print("Error: The folder path does not exist.")
        return

    # Create a temporary directory to extract files
    temp_dir = os.path.join(folder_path, 'temp_extracted')
    os.makedirs(temp_dir, exist_ok=True)

    # List all ZIP file paths in the folder
    zip_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.zip')]

    if not zip_paths:
        print("Error: No ZIP files found in the specified folder.")
        return

    print(f"Found {len(zip_paths)} ZIP files in the folder. Extracting and starting the duplicate search...\n")

    # Extract all ZIP files
    for zip_path in zip_paths:
        extract_zip(zip_path, temp_dir)

    # List all extracted text file paths
    file_paths = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.txt')]

    # Track duplicates globally
    global_seen = set()
    global_duplicates = defaultdict(list)

    # Use parallel processing
    with ProcessPoolExecutor() as executor:
        # Submit tasks for each file
        future_to_file = {executor.submit(process_file, path): path for path in file_paths}
        
        # Collect results as they complete
        for future in as_completed(future_to_file):
            file_name = os.path.basename(future_to_file[future])
            try:
                duplicates_local = future.result()
                print(f"Processed file: {file_name}")
                
                # Update global duplicate tracking
                for id_value, filenames in duplicates_local.items():
                    if id_value in global_seen:
                        global_duplicates[id_value].extend(filenames)
                    else:
                        global_seen.add(id_value)
                        global_duplicates[id_value].extend(filenames)
            
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # If duplicates are found, save them to a file
    if global_duplicates:
        output_data = pd.DataFrame(
            [(id_value, ', '.join(set(filenames))) for id_value, filenames in global_duplicates.items()],
            columns=['ID', 'Filenames']
        )
        output_path = 'duplicates_with_filenames.csv'
        output_data.to_csv(output_path, index=False)
        
        print(f"\nDuplicate search complete. Duplicates have been found and logged into {output_path}.")
    else:
        print("\nNo duplicates were found across the files.")

    # Clean up the temporary directory
    import shutil
    shutil.rmtree(temp_dir)

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()