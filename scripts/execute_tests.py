import subprocess
import pandas as pd
import pytest

command_line_map = {
    'default_delim' : 'default',
    'semicolon' : '[\";\"]',
    'dash' : '[\"-\"]',
    'exclamation' : '[\"!\"]',
    'colon' : '[\":\"]',

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
    'forward_slash' : '/',
    
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
        header=6        
    )

    df['delimiter'] = df['delimiter'].map(lambda x : command_line_map[x])
    df['quote'] = df['quote'].map(lambda x: command_line_map[x])
    df['quiet'] = df['quiet'].map(lambda x : command_line_map[x])
    df['escape'] = df['escape'].map(lambda x : command_line_map[x])
    df['headers'] = df['headers'].map(lambda x : command_line_map[x])

    df = df.sort_values(by=["maxRowLength"], ascending=True) 
    return df


def execute_command_line_option(params, csv, test_case_number):

    command = (
        "csvtojson "
        f"--delimiter={params['delimiter']} "
        f"{'--quote=' + params['quote'] if params['quote'] != 'default' else ''} "  
        f"--trim={'true' if params['trim'] else 'false'} "
        f"--ignoreEmpty={'true' if params['ignoreEmpty'] else 'false'} "
        f"--noheader={'true' if params['noheader'] else 'false'} "
        f"{'--headers=' + params['headers'] if params['headers'] != 'none' else ''} "
        f"--flatKeys={'true' if params['flatKeys'] else 'false'} "
        f"--checkType={'true' if params['checkType'] else 'false'} "
        f"--maxRowLength={params['maxRowLength']} "
        f"--checkColumn={'true' if params['checkColumn'] else 'false'} "
        f"--quiet={'true' if params['quiet'] else 'false'} "
        f"--escape={params['escape']} "
        f"--nullObject={'true' if params['nullObject'] else 'false'} "
        f"--downstreamFormat={params['downstreamFormat']} "
        f"{csv} > ../tests/expected_output/test{test_case_number}_output.json"
    )
    
    print(command)

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
