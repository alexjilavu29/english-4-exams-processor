import os

def create_test_files():
    # Define the directory path
    dir_path = "./key_text/"
    os.makedirs(dir_path, exist_ok=True)  # Create the directory if it doesn't exist
    
    # Define the years and file prefixes
    years = range(2007, 2024)
    prefixes = ["cae", "cpe", "fce", "pet"]
    
    # Create the files
    for year in years:
        for prefix in prefixes:
            file_name = f"{prefix}_{year}_key.txt"
            file_path = os.path.join(dir_path, file_name)
            
            with open(file_path, "w") as f:
                f.write(f"This is the {prefix.upper()} test file for the year {year}.\n")
            
            print(f"Created: {file_path}")

if __name__ == "__main__":
    create_test_files()
