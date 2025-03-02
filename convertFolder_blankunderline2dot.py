import os
from docx import Document

# Set the folder path
folder_path = r"C:\Proiecte\English4Exams\Materiale_NOU"  # Folder containing .docx files

# Loop through all .docx files
for file in os.listdir(folder_path):
    if file.endswith(".txt"):
        file_path = os.path.join(folder_path, file)
        doc = Document(file_path)

        # Iterate through paragraphs and replace underlined blank spaces
        for para in doc.paragraphs:
            for run in para.runs:
                if run.underline and run.text.strip() == "":
                    run.text = "…………………"  # Replace blank underlined spaces with dots
                    run.underline = False  # Remove underlining

        # Save the updated file (overwrite the original)
        doc.save(file_path)
        print(f"Updated: {file}")

print("✅ All underlined blank spaces replaced with dots in Materiale_NOU!")
