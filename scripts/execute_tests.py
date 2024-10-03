import subprocess
import pandas as pd
import ast
import pytest

def read_csv(file_path):
    """Read and parse the CSV file."""
    try:
        # Read the CSV file with quotes handled properly
        df = pd.read_csv(
            file_path, 
            delimiter=',', 
            quotechar='"', 
            escapechar='\\', 
            on_bad_lines='skip', 
            header=0
        )

        # Define expected columns
        expected_columns = [
            "delimiter", "quote", "trim", "checktype", "ignoreempty",
            "noheader", "header", "flatkeys", "maxrowlength", 
            "checkcolumn", "eol", "quiet", "escape", 
            "colparser", "alwayssplitateol", "nullobject", "downstreamformat"
        ]

        # Check if the number of columns matches the expected count
        if df.shape[1] != len(expected_columns):
            raise ValueError(f"Expected {len(expected_columns)} columns, but got {df.shape[1]}.")

        # Rename the columns
        df.columns = expected_columns

        # Convert 'delimiter' to a list of strings with escape handling
        df['delimiter'] = df['delimiter'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # Clean and convert other fields
        df['quote'] = df['quote'].apply(lambda x: x.strip().lower() if isinstance(x, str) else x)
        df['trim'] = df['trim'].astype(bool)
        df['checktype'] = df['checktype'].astype(bool)
        df['ignoreempty'] = df['ignoreempty'].astype(bool)
        df['noheader'] = df['noheader'].astype(bool)
        df['flatkeys'] = df['flatkeys'].astype(bool)
        df['quiet'] = df['quiet'].astype(bool)
        df['alwayssplitateol'] = df['alwayssplitateol'].astype(bool)
        df['nullobject'] = df['nullobject'].astype(bool)

        # Handle 'header' which is a string representation of a list
        df['header'] = df['header'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # Handle the escape character and ensure it's treated properly
        df['escape'] = df['escape'].apply(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Convert 'maxrowlength' to int, handling potential exceptions
        df['maxrowlength'] = df['maxrowlength'].apply(lambda x: int(x) if isinstance(x, str) and x.isdigit() else x)

        # Optionally handle colparser and downstreamformat if needed
        df['colparser'] = df['colparser'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        df['downstreamformat'] = df['downstreamformat'].apply(lambda x: x.strip() if isinstance(x, str) else x)

        return df

    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

def escape_array(arr):
    """Convert array to a string with escaped quotes and wrap in single quotes."""
    return "'[{}]'".format(', '.join(f'\\"{item}\\"' for item in arr))

def escape_object(obj):
    """Convert a dictionary to a string with escaped quotes and wrap in single quotes."""
    return "'{" + ', '.join(f'\\"{key}\\": \\"{value}\\"' for key, value in obj.items()) + "}'"

def execute_command_line_option(params, csv):
    """Construct and execute the csvtojson command."""
    command = (
        f"csvtojson "
        f"--delimiter={escape_array(params['delimiter'])} "  # Escape delimiter with single quotes
        f"--quote={params['quote']} "
        f"--trim={'true' if params['trim'] else 'false'} "
        f"--checkType={'true' if params['checktype'] else 'false'} "
        f"--ignoreEmpty={'true' if params['ignoreempty'] else 'false'} "
        f"--noheader={'true' if params['noheader'] else 'false'} "
        f"--headers={escape_array(params['header'])} "  # Escape headers with single quotes
        f"--flatKeys={'true' if params['flatkeys'] else 'false'} "
        f"--maxRowLength={params['maxrowlength']} "
        f"--checkColumn={'true' if params['checkcolumn'] else 'false'} "
        f"--eol={params['eol']} "
        f"--quiet={'true' if params['quiet'] else 'false'} "
        f"--escape={params['escape']} "
        f"--colParser={escape_object(params['colparser'])} "  # Escape colParser object with single quotes
        f"--alwaysSplitAtEOL={'true' if params['alwayssplitateol'] else 'false'} "
        f"--nullObject={'true' if params['nullobject'] else 'false'} "
        f"--downstreamFormat={params['downstreamformat']} "
        f"{csv}"
    )

    print('Command:', command)  # Debug output

    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    return process.stdout, process.stderr

# Example of reading and testing the command with parameters
def test_csv_to_json():
    # Read the CSV file with test parameters
    test_params_df = read_csv('../tests/test_files/draft.csv')
    print('test\n', test_params_df)
    for index, row in test_params_df.iterrows():
        params = row.to_dict()  # Convert row to dictionary for easier access
        print('index\n', index)
        print('row\n', row)
        print('params\n', params)
        print(f'params for test case {index + 1}: {params}')

        # Execute command with parsed parameters
        result_stdout, result_stderr = execute_command_line_option(params, '../tests/test_files/test1.csv')

        print(f"Test Case {index + 1}:")
        print("Parameters:", params)
        print("Output:")
        print(result_stdout)
        print("Error (if any):")
        print(result_stderr)
        print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    pytest.main()
