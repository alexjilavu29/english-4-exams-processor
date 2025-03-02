import os
import re
from docx import Document

# Set the path to the file (update this with your actual file path)
file_path = r"C:\Proiecte\English4Exams\Materiale_NOU\example.docx"

# Load the document
doc = Document(file_path)

# Define the words to count
choices = ["A.", "B.", "C.", "D."]
counts = {choice: 0 for choice in choices}

# Regular expression to match whole words
pattern = r"\b(A\.|B\.|C\.|D\.)\b"

# Read the document content
for para in doc.paragraphs:
    matches = re.findall(pattern, para.text)
    for match in matches:
        counts[match] += 1

# Print results
print("🔹 Count of A., B., C., and D. in the file:")
for choice, count in counts.items():
    print(f"{choice}: {count}")

print("✅ Counting complete!")
