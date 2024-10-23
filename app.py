import streamlit as st
import json
import re
from datetime import datetime

def parse_text_file(file_content):
    # Split content into individual questions using a regex pattern
    questions = re.split(r'(?=\nQUESTION \d+)', file_content.strip())

    json_data = []

    for index, question_content in enumerate(questions, start=1):
        question_match = re.search(r'QUESTION \d+\s*(.+?)(?=\nAnswer:)', question_content, re.DOTALL)
        question_text = question_match.group(1).strip() if question_match else "(NONE)"

        options = re.findall(r'([A-D])\. (.+)', question_content)
        options_list = [option[1].strip() for option in options]

        answer_match = re.search(r'Answer: ([A-D])', question_content)
        answer_letter = answer_match.group(1).strip() if answer_match else "(NONE)"
        answer_index = ord(answer_letter) - ord('A') if answer_letter != "(NONE)" else -1

        section_match = re.search(r'Section:\s*(.+)', question_content)
        section_text = section_match.group(1).strip() if section_match else "(NONE)"

        explanation_match = re.search(r'Explanation\s*(.*?)\n(?:Explanation/Reference:|Reference:)', question_content, re.DOTALL)
        explanation_text = explanation_match.group(1).strip() if explanation_match else "(NONE)"

        reference_match = re.search(r'Reference:\s*(.+)', question_content)
        reference_text = reference_match.group(1).strip() if reference_match else "(NONE)"

        question_json = {
            "question_number": index,
            "question": question_text,
            "type": "multiple-choice",
            "options": options_list,
            "answer": options[answer_index][1].strip() if answer_index >= 0 else "(NONE)",
            "section": section_text,
            "explanation": explanation_text,
            "reference": reference_text
        }

        json_data.append(question_json)

    return json_data

def main():
    st.title("Question Parser")

    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")
        json_data = parse_text_file(file_content)

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"questions_{current_time}.json"

        with open(output_file, 'w') as file:
            json.dump(json_data, file, indent=4)

        st.success(f"JSON data has been saved to {output_file}")
        st.json(json_data)  # Display JSON data in the app

if __name__ == '__main__':
    main()
