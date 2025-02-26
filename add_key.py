import csv
import re


def load_key_file(key_filename):
    """
    Reads the key file and returns a mapping of question_id to correct answer letter.
    """
    key_map = {}
    # Pattern to match lines like: "1.  D"
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
    Reads the existing CSV file, adds a new column 'correct_answer'
    by mapping the key file's answer letter to the appropriate answer text,
    and writes the updated rows back to the CSV file.
    """
    updated_rows = []
    # Read the original CSV file
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Create new fieldnames with the additional column
        fieldnames = reader.fieldnames + ['correct_answer']
        for row in reader:
            qid = row['question_id']
            answer_letter = key_map.get(qid, None)
            if answer_letter:
                # Map the letter to the corresponding answer column
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

    # Write the updated rows back to the CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in updated_rows:
            writer.writerow(row)


def main():
    csv_filename = 'fce-2024-test-final.csv'
    key_filename = 'fce-key.txt'

    # Load the correct answer mapping from the key file
    key_map = load_key_file(key_filename)

    # Update the CSV file with the correct_answer column
    add_correct_answer_to_csv(csv_filename, key_map)

    print("CSV file has been updated with the correct_answer column.")


if __name__ == '__main__':
    main()