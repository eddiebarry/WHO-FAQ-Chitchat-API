"""
Creating the necessary JSON files to begin with, starting from the Excel
script updated by designers.
"""


from json import dump as json_dump
from os import getcwd
from os.path import join as os_join
from typing import Callable

from openpyxl import load_workbook


def create_initial_jsons_from_script_wrapper() -> Callable:
    """
    Wrapper setting the function docstring as the module docstring.
    """

    def create_initial_jsons_from_script_inner(json_files_dir: str,
                                               script_path: str) -> None:

        # loading the script:
        workbook = load_workbook(filename=script_path)

        # reading the script while updating the dictionaries to be written to
        # the respective JSON files:

        sheet = workbook['Chitchat']
        question_2_answer_mapping = {}
        question_2_label_mapping = {}

        # iterating through row cells of the first column - the first row
        # cell contains a header:
        for questions, answer in zip(sheet['A'][1:], sheet['B'][1:]):

            # designers leave questions/answers blank when the respective
            # answers/questions are not available/ready yet:
            if questions.value is None or answer.value is None:
                continue

            # removing evantual initial/final whitespaces:
            answer = answer.value.strip()

            # extracting question variations of the current Q&A pair:
            for question_variation in questions.value.split('/'):

                # removing evantual initial/final whitespaces:
                question_variation = question_variation.strip()

                # adding the question variation and the respective answer to
                # the dictionaries:
                question_2_answer_mapping[question_variation] = answer
                question_2_label_mapping[question_variation] = 1

        # saving the dictionaries to the respective JSON files:

        filename = os_join(json_files_dir, "chitchat_answers.json")
        with open(filename, 'w') as file:
            json_dump(question_2_answer_mapping, file)

        filename = os_join(json_files_dir, "labelled_data.json")
        with open(filename, 'w') as file:
            json_dump(question_2_label_mapping, file)

    # adding the docstring:
    create_initial_jsons_from_script_inner.__doc__ = __doc__

    return create_initial_jsons_from_script_inner


create_initial_jsons_from_script = create_initial_jsons_from_script_wrapper()


if __name__ == "__main__":

    OUTPUT_FILES_DIR = getcwd()
    SCRIPT_PATH = os_join(
        getcwd(),
        "Script-updated-database_updated_date_07-05-2021_time_11-36-18.xlsx"
    )

    create_initial_jsons_from_script(
        json_files_dir=OUTPUT_FILES_DIR,
        script_path=SCRIPT_PATH
    )
