import subprocess
import pandas as pd
import pytest

command_line_map = {
    'default_delim' : 'default',
    'semicolon' : '\'[";"]\'',
    'dash' : '\'["-"]\'',
    'tab' : '\'["\t"]\'',
    'colon' : '\'[":"]\'',

    'default_quote': 'default',
    'off' : 'off',
    '$' : '$',
    '#' : '#',  

    'false' : 'false',
    'true_no_error' : 'true_no_error',
    'true_checkCol_error' : 'true_checkCol_error',
    'true_maxRow_error' : 'true_maxRow_error',
    
    'default_escape' : 'default',
    'back_slash' : '\\',
    'foward_slash' : '/',
    
    'fieldname' : '\'["fname","lname","age","countryOfResidence","slogan.best","slogan.best"]\'',
    'none' : 'none'
}

def read_csv(file_path):
    df = pd.read_csv(
        file_path,
        delimiter=',',        
        quotechar='"',       
        escapechar='\\',      
        on_bad_lines='skip',  
        header=0              
    )

    df['delimiter'] = df['delimiter'].map(lambda x : command_line_map[x])
    df['quote'] = df['quote'].map(lambda x: command_line_map[x])
    df['quiet'] = df['quiet'].map(lambda x : command_line_map[x])
    df['escape'] = df['escape'].map(lambda x : command_line_map[x])
    df['header'] = df['header'].map(lambda x : command_line_map[x])

    return df


def execute_command_line_option(params, csv, test_case_number):
    print(csv)
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
    csv_path = '../resources/command_line_options.csv'
    test_params_df = read_csv(csv_path)

    if test_params_df.empty:
        print("No test parameters found. Exiting.")
        return

    test_case_number = 1  

    for _, row in test_params_df.iterrows():
        params = row.to_dict()  
        print(f'Test Case {test_case_number}:')
        print("Parameters:", params)

        result_stdout, result_stderr = execute_command_line_option(params, f"../tests/test_files/test{test_case_number}.csv", test_case_number)

        print("Output:")
        print(result_stdout)
        print("Error (if any):")
        print(result_stderr)
        print("\n" + "=" * 40 + "\n")

        test_case_number += 1  


if __name__ == "__main__":
    pytest.main()
