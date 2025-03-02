import os
import glob
import re
import csv

def generate_csv(txt_file_path, csv_file_path):
    """
    Reads a text file with questions and answer options, and writes the data to a CSV file.
    """
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Regular expression patterns:
    question_pattern = re.compile(r'^\s*(\d+)\.\s+(.*)$')
    answer_pattern = re.compile(r'^[A-D]\.\s*(.*)$')

    questions = []
    current_question_id = None
    current_question_text = ""
    current_answers = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        question_match = question_pattern.match(line)
        if question_match:
            if current_question_id is not None:
                if len(current_answers) != 4:
                    print(f"Warning: question {current_question_id} does not have 4 answers (found {len(current_answers)}).")
                questions.append((current_question_id, current_question_text,
                                  current_answers[0] if len(current_answers) > 0 else "",
                                  current_answers[1] if len(current_answers) > 1 else "",
                                  current_answers[2] if len(current_answers) > 2 else "",
                                  current_answers[3] if len(current_answers) > 3 else ""))
                current_answers = []
            current_question_id = question_match.group(1)
            current_question_text = question_match.group(2)
            continue

        answer_match = answer_pattern.match(line)
        if answer_match:
            current_answers.append(answer_match.group(1))
            continue

        # If not a question or answer, append the line to the current question text.
        if current_question_id is not None and not current_answers:
            current_question_text += " " + line

    # Append the last question if present.
    if current_question_id is not None:
        if len(current_answers) != 4:
            print(f"Warning: question {current_question_id} does not have 4 answers (found {len(current_answers)}).")
        questions.append((current_question_id, current_question_text,
                          current_answers[0] if len(current_answers) > 0 else "",
                          current_answers[1] if len(current_answers) > 1 else "",
                          current_answers[2] if len(current_answers) > 2 else "",
                          current_answers[3] if len(current_answers) > 3 else ""))

    # Write the questions to a CSV file.
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['question_id', 'question_text', 'answer_1', 'answer_2', 'answer_3', 'answer_4'])
        for row in questions:
            writer.writerow(row)

def load_key_file(key_filename):
    """
    Reads the key file and returns a mapping of question_id to correct answer letter.
    Expected format per line: "1.  D"
    """
    key_map = {}
    pattern = re.compile(r'^\s*(\d+)\.\s*([A-D])\s*$')
    with open(key_filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.match(line)
            if match:
                qid = match.group(1)
                answer_letter = match.group(2)
                key_map[qid] = answer_letter
            else:
                print(f"Warning: Line did not match expected format: {line}")
    return key_map

def add_correct_answer_to_csv(csv_filename, key_map):
    """
    Reads the CSV file, adds a new column 'correct_answer'
    by mapping the key file's answer letter to the corresponding answer text,
    and writes the updated rows back to the CSV file.
    """
    updated_rows = []
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames + ['correct_answer']
        for row in reader:
            qid = row['question_id']
            answer_letter = key_map.get(qid, None)
            if answer_letter:
                if answer_letter == 'A':
                    row['correct_answer'] = row.get('answer_1', '')
                elif answer_letter == 'B':
                    row['correct_answer'] = row.get('answer_2', '')
                elif answer_letter == 'C':
                    row['correct_answer'] = row.get('answer_3', '')
                elif answer_letter == 'D':
                    row['correct_answer'] = row.get('answer_4', '')
                else:
                    row['correct_answer'] = ''
            else:
                row['correct_answer'] = ''
            updated_rows.append(row)

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in updated_rows:
            writer.writerow(row)

def process_files():
    """
    Finds all test files matching the pattern <difficulty>_<year>_test.txt,
    then processes each one by generating the CSV file and adding correct answers
    from the corresponding key file (<difficulty>_<year>_key.txt).
    The output CSV is saved as <difficulty>_<year>.csv in the target directory.
    """
    # Adjust the glob pattern as needed based on your directory structure.
    test_files = glob.glob('./teste_text/*_test.txt')
    
    for test_file in test_files:
        # Extract the base filename.
        base = os.path.basename(test_file)
        # Assuming the filename format is: <difficulty>_<year>_test.txt
        # For example: "CPE_2024_test.txt" 
        parts = base.split('_')
        if len(parts) < 3:
            print(f"Skipping file with unexpected format: {base}")
            continue

        difficulty = parts[0]
        year = parts[1]
        
        # Build file paths.
        key_file_path = os.path.join('./key_text', f"{difficulty}_{year}_key.txt")
        csv_file_path = os.path.join('./csv_teste', f"{difficulty}_{year}.csv")
        
        print(f"Processing: {base}")
        print(f"  Test file: {test_file}")
        print(f"  Key file: {key_file_path}")
        print(f"  Output CSV: {csv_file_path}")
        
        try:
            generate_csv(test_file, csv_file_path)
        except Exception as e:
            print(f"Error generating CSV from {test_file}: {e}")
            continue
        
        try:
            key_map = load_key_file(key_file_path)
        except Exception as e:
            print(f"Error loading key file {key_file_path}: {e}")
            continue
        
        try:
            add_correct_answer_to_csv(csv_file_path, key_map)
        except Exception as e:
            print(f"Error updating CSV {csv_file_path}: {e}")
            continue
        
        print(f"Finished processing {difficulty}_{year}\n")

if __name__ == '__main__':
    process_files()
