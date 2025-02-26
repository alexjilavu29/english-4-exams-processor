import re
import csv


def generate_csv(txt_file_path, csv_file_path):
    # Open and read the text file
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Regular expression patterns:
    # Matches a question line that starts with a number followed by a period and then the question text.
    question_pattern = re.compile(r'^\s*(\d+)\.\s+(.*)$')
    # Matches answer options starting with A., B., C. or D.
    answer_pattern = re.compile(r'^[A-D]\.\s+(.*)$')

    questions = []
    current_question_id = None
    current_question_text = ""
    current_answers = []

    # Process each line in the file
    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        # Check if the line is a question line
        question_match = question_pattern.match(line)
        if question_match:
            # If there is an existing question, save it to the list
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

        # Check if the line is an answer option
        answer_match = answer_pattern.match(line)
        if answer_match:
            current_answers.append(answer_match.group(1))
            continue

        # If the line is neither a new question nor an answer,
        # assume it's a continuation of the current question text.
        if current_question_id is not None and not current_answers:
            current_question_text += " " + line

    # Append the last question if present
    if current_question_id is not None:
        if len(current_answers) != 4:
            print(f"Warning: question {current_question_id} does not have 4 answers (found {len(current_answers)}).")
        questions.append((current_question_id, current_question_text,
                          current_answers[0] if len(current_answers) > 0 else "",
                          current_answers[1] if len(current_answers) > 1 else "",
                          current_answers[2] if len(current_answers) > 2 else "",
                          current_answers[3] if len(current_answers) > 3 else ""))

    # Write the parsed questions and answers to a CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['question_id', 'question_text', 'answer_1', 'answer_2', 'answer_3', 'answer_4'])
        for row in questions:
            writer.writerow(row)


generate_csv('CPE 2024 TEST final.txt', 'cpe-2024-test-final.csv')