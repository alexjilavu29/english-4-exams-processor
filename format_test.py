import os
import re

def process_files_in_folder(folder_path):
    # Ensure the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return
    
    # Regex pattern to match "B.", "C.", "D." and replace with "\nB.", "\nC.", "\nD."
    pattern = re.compile(r'(?<!\n)(B\.|C\.|D\.)')
    
    # Iterate through all text files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Process only text files
            file_path = os.path.join(folder_path, filename)
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Replace occurrences using regex
            updated_content = pattern.sub(r'\n\1', content)
            
            # Write updated content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            
            print(f"Processed: {filename}")

if __name__ == "__main__":
    folder_path = "./teste_text"
    process_files_in_folder(folder_path)
    print("Processing complete.")
