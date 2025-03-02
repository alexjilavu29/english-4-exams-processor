import os
import win32com.client

# Set input (source) and output (destination) folder paths
input_folder = r"C:\Proiecte\English4Exams\Materiale"  # Folder containing .doc files
output_folder = r"C:\Proiecte\English4Exams\Materiale_NOU"  # Folder to save converted .docx files

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Ensure no interfering Word instances
try:
    word = win32com.client.GetActiveObject("Word.Application")
    word.Quit()  # Close any existing Word instances
except:
    pass  # If no active Word instances, continue

# Start a fresh Word application instance
word = win32com.client.Dispatch("Word.Application")
word.Visible = False  # Keep Word hidden

# Loop through all .doc files and convert them to .docx
for file in os.listdir(input_folder):
    if file.endswith(".doc"):
        doc_path = os.path.join(input_folder, file)
        docx_path = os.path.join(output_folder, file.replace(".doc", ".docx"))

        try:
            doc = word.Documents.Open(doc_path)
            doc.SaveAs(docx_path, FileFormat=16)  # 16 = .docx format
            doc.Close()
            print(f"Converted: {file} -> {os.path.basename(docx_path)}")
        except Exception as e:
            print(f"Error converting {file}: {e}")

# Quit Word application
word.Quit()
print(f"✅ Conversion completed! All .docx files saved in: {output_folder}")
