import subprocess
import pandas as pd
import pytest

command_line_map = {
    'default_delim' : 'default',
    'semicolon' : '[\";\"]',
    'dash' : '[\"-\"]',
    'exclamation' : '[\"!\"]',
    'colon' : '[\":\"]',

    '20' : '\'["fname","lname","age"]\'',
    '40' : '\'["fname","lname","age","countryOfResidence"]\'',
    '60' : '\'["fname","lname","age","countryOfResidence","slogan.best","slogan.worst"]\'',
    '0' : '\'["fname.nickname","lname","age","countryOfResidence.city.town","slogan.best","slogan.worst"]\'',

    'default_quote': 'default',
    'off' : 'off',
    '$' : '$',
    '#' : '#',  

    'true' : 'true',
    'false_no_error' : 'false_no_error',
    'false_checkCol_error' : 'false_checkCol_error',
    'false_maxRow_error' : 'false_maxRow_error',
    
    'default_escape' : 'default',
    'back_slash' : '\\',
    'forward_slash' : '/',
    
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
    df['headers'] = df['headers'].map(lambda x: command_line_map[x] if x == 'none' else x)

    df = df.sort_values(by=["maxRowLength"], ascending=True) 
    df.to_csv('sorted.csv', index=False)
    # print(df)
    return df

def fetch_error_file(error_type, test_case_number):
    if error_type == 'false_no_error':
        return f"../tests/test_files/test{test_case_number}_no_error.csv"
    elif error_type == 'false_checkCol_error':
        return f"../tests/test_files/test{test_case_number}_check_col_error.csv"
    else:
        return f"../tests/test_files/test{test_case_number}_max_row_error.csv"

def select_delimiter(param):
    if param == 'default':
        return ''
    else:
        return f"--delimiter=\'{param}\' "


def execute_command_line_option(params, csv, test_case_number):

    if params['noheader'] == 'true_header_excluded':
        print(csv)
        with open(csv, 'r') as csvfile:
            data = csvfile.readlines()[1:]  

        error_type = params['quiet']
        temp_csv = ''
        if error_type == 'false_no_error':
            temp_csv = f"../tests/test_files/test{test_case_number}_no_error.csv"
        elif error_type == 'false_checkCol_error':
            temp_csv = f"../tests/test_files/test{test_case_number}_check_col_error.csv"
        elif error_type == 'false_maxRow_error':
            temp_csv = f"../tests/test_files/test{test_case_number}_max_row_error.csv"
        else:
            temp_csv = f"../tests/test_files/temp_test{test_case_number}.csv"
        with open(temp_csv, 'w') as temp_file:
            temp_file.writelines(data)
        csv = temp_csv        
    else:
        csv = csv if params['quiet'] == 'true' else fetch_error_file(params['quiet'], test_case_number)


    command = (
        "csvtojson "
        f"{select_delimiter(params['delimiter'])}"
        f"{'--quote=' + params['quote'] if params['quote'] != 'default' else ''} "  
        f"--trim={'true' if params['trim'] else 'false'} "
        f"--ignoreEmpty={'true' if params['ignoreEmpty'] else 'false'} "
        f"--noheader={'false' if params['noheader'] == 'false' else 'true'} "
        f"{'--headers=' + command_line_map[str(params['maxRowLength'])] if params['headers'] != 'none' else ''} "
        f"--flatKeys={'true' if params['flatKeys'] else 'false'} "
        f"--checkType={'true' if params['checkType'] else 'false'} "
        f"--maxRowLength={params['maxRowLength']} "
        f"--checkColumn={'true' if params['checkColumn'] else 'false'} "
        f"--quiet={'true' if params['quiet'] == 'true' else 'false'} "
        f"{'--escape=' + params['escape'] if params['escape'] != 'default_escape' else ''} "
        f"--nullObject={'true' if params['nullObject'] else 'false'} "
        f"--downstreamFormat={params['downstreamFormat']} "
        # f"{csv} > ../tests/expected_output/test{test_case_number}_output.json"
        f"{csv}"
    )
    
    print(command)

    process = subprocess.run(command, shell=True, capture_output=True, text=True)

    output_file_path = f'../tests/actual_output/test{test_case_number}_output.json'
    with open(output_file_path, 'w') as output_file:
        if process.stdout.strip():
            output_file.write(process.stdout)
        else:
            output_file.write('[]')

    with open(f'../tests/logs/test_case_{test_case_number}_log.txt', 'w') as log_file:
        log_file.write(f"Test Case {test_case_number}:\n")
        log_file.write("command\n"+command+"\n")
        log_file.write("Output:\n"+process.stdout+"\n")
        log_file.write("Error:\n")
        if process.stderr.strip():
            log_file.write(process.stderr + "\n")
        else:
            log_file.write("No Error Captured\n")


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