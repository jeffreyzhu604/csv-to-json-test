import subprocess
import pandas as pd
import pytest
import os

def get_path(relative_path):
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(absolute_path, relative_path)

    return file_path

command_line_map = {
    'semicolon' : '\'[";"]\'',
    'comma' : '\'[","]\'',
    'tab' : '\'["\t"]\'',
    'colcon' : '\'[":"]\'',
    'fieldname' : '\'["fname","lname","age","countryOfResidence","slogan.best","slogan.best"]\'',
    'none' : 'none'
}

def read_csv(file_path):
    df = pd.read_csv(
        file_path,
        delimiter=',',        # Match the delimiter used in the CSV file
        quotechar='"',        # Match the quote used in the CSV file
        escapechar='\\',      # Escape character if needed
        on_bad_lines='skip',  # Skip bad lines
        header=0              # Use the first row as header
    )

    # Directly assign expected strings if delimiter or header match criteria
    df['delimiter'] = df['delimiter'].map(lambda x : command_line_map[x])
    df['header'] = df['header'].map(lambda x : command_line_map[x])

    return df


def execute_command_line_option(params, csv, test_case_number):
    command = (
        "csvtojson "
        f"--delimiter={params['delimiter']} "
        f"--quote={params['quote']} "
        f"--trim={'true' if params['trim'] else 'false'} "
        f"--ignoreEmpty={'true' if params['ignoreempty'] else 'false'} "
        f"--noheader={'true' if params['noheader'] else 'false'} "
        f"{'--headers=' + params['header'] if params['header'] != 'none' else ''} "
        f"--flatKeys={'true' if params['flatkeys'] else 'false'} "
        f"--checkType={'true' if params['checktype'] else 'false'} "
        f"--maxRowLength={params['maxrowlength']} "
        f"--checkColumn={'true' if params['checkcolumn'] else 'false'} "
        f"--quiet={'true' if params['quiet'] else 'false'} "
        f"--escape={params['escape']} "
        f"--nullObject={'true' if params['nullobject'] else 'false'} "
        f"--downstreamFormat={params['downstreamformat']} "
        f"{csv}  > ../tests/expected_output/test{test_case_number}_output.json" 
    )

    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.stdout, process.stderr


def test_csv_to_json():
    csv_path = get_path('../tests/test_files/command_line_options.csv')    
    test_params_df = read_csv(csv_path)

    if test_params_df.empty:
        print("No test parameters found. Exiting.")
        return

    test_case_number = 1  

    for _, row in test_params_df.iterrows():
        params = row.to_dict()  
        print(f'Test Case {test_case_number}:')
        print("Parameters:", params)

        result_stdout, result_stderr = execute_command_line_option(params, get_path(f"../tests/test_files/test{test_case_number}.csv"), test_case_number)

        print("Output:")
        print(result_stdout)
        print("Error (if any):")
        print(result_stderr)
        print("\n" + "=" * 40 + "\n")

        test_case_number += 1  


if __name__ == "__main__":
    pytest.main()
