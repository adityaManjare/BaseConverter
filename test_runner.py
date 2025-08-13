import csv
import math
import sys
import os
from fastapi.exceptions import HTTPException
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import module_1 as converter
import module_2 as arithmeticOps
def test_base_conversion_roundtrip():
    """
    Reads base_conversion_input.csv, performs a roundtrip conversion,
    and writes the results to base_conversion_output.csv.
    """
    input_filename = 'base_conversion_input.csv'
    output_filename = 'base_conversion_output.csv'
    
    # Header for the output file
    output_header = ['number', 'base_1', 'base_2', 'output1', 'output2', 'match', 'error']
    
    output_rows = [output_header]

    print(f"--- Starting Part A: Base Conversion Roundtrip Test ---")
    print(f"Reading from {input_filename}...")

    try:
        with open(input_filename, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                original_number_str = row['number']
                base_1 = int(row['base_1'])
                base_2 = int(row['base_2'])
                
                output1, output2, match, error = '', '', '', ''

                try:
                    # Task 1: Convert from base_1 to base_2
                    output1 = converter.baseConverter(
                        type('', (), {'number': original_number_str,
                                      'from_base': base_1,
                                      'to_base': base_2})()
                    )

                    # Task 2: Convert back from base_2 to base_1
                    output2 = converter.baseConverter(
                        type('', (), {'number': output1,
                                      'from_base': base_2,
                                      'to_base': base_1})()
                    )

                    # Task 3: Check for a match
                    if '.' in original_number_str:
                        original_float = float(original_number_str)
                        output2_float = float(output2)
                        match = math.isclose(original_float, output2_float, rel_tol=1e-6)
                    else:
                        match = (original_number_str == output2)

                except ValueError as e:
                    error = str(e)
                    match = False

                except HTTPException as e:
                    error = str(e.detail)
                    match = False
                
                output_rows.append([original_number_str, base_1, base_2, output1, output2, match, error])

        # Write all results to the output file
        with open(output_filename, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(output_rows)
        
        print(f"Success! Results written to {output_filename}")

    except FileNotFoundError:
        print(f"ERROR: Input file not found: {input_filename}")
    
    print("-" * 50)


def test_binary_arithmetic():
    """
    Reads binary_arithmetic_input.csv, performs the specified operation,
    and writes the results to binary_arithmetic_output.csv.
    """
    input_filename = 'binary_arithmetic_input.csv'
    output_filename = 'binary_arithmetic_output.csv'
    
    output_header = ['num1', 'num2', 'representation', 'operation', 'bit_width', 'result', 'overflow', 'error']
    output_rows = [output_header]

    print(f"--- Starting Part B: Binary Arithmetic Processor ---")
    print(f"Reading from {input_filename}...")

    # A map to easily call the correct function
    # Maps (representation, operation) to a function from arithmeticOps
    ops_map = {
        ('unsigned', 'add'): arithmeticOps.binary_addition,
        ('unsigned', 'sub'): arithmeticOps.binary_subtraction,
        ('unsigned', 'mul'): arithmeticOps.binary_multiplication,
        ('unsigned', 'div'): arithmeticOps.binary_division,
        ('signed_magnitude', 'add'): arithmeticOps.signed_binary_addition,
        ('signed_magnitude', 'sub'): arithmeticOps.signed_binary_subtraction,
        ('signed_magnitude', 'mul'): arithmeticOps.signed_binary_multiplication,
        ('signed_magnitude', 'div'): arithmeticOps.signed_binary_division,
        ('ones_complement', 'add'): arithmeticOps.ones_complement_addition,
        ('ones_complement', 'sub'): arithmeticOps.ones_complement_subtraction,
        ('ones_complement', 'mul'): arithmeticOps.ones_complement_multiplication,
        ('ones_complement', 'div'): arithmeticOps.ones_complement_division,
        ('twos_complement', 'add'): arithmeticOps.twos_complement_addition,
        ('twos_complement', 'sub'): arithmeticOps.twos_complement_subtraction,
        ('twos_complement', 'mul'): arithmeticOps.twos_complement_multiplication,
        ('twos_complement', 'div'): arithmeticOps.twos_complement_division,
    }

    try:
        with open(input_filename, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                num1, num2, rep, op, bits = row['num1'], row['num2'], row['representation'], row['operation'], int(row['bit_width'])
                result, overflow, error = '', False, ''

                try:
                    # Find the correct function to call
                    func_to_call = ops_map.get((rep, op))
                    if not func_to_call:
                        raise ValueError(f"Unsupported operation '{op}' for representation '{rep}'")
                    
                    # Call the function and get the result
                    calc_result = func_to_call(num1, num2, bits)

                    # Division returns a tuple (quotient, remainder), format it
                    if isinstance(calc_result, tuple):
                        result = f"Quotient: {calc_result[0]}, Remainder: {calc_result[1]}"
                    else:
                        result = calc_result

                except ValueError as e:
                    error = str(e)
                    # Check if the error message indicates an overflow
                    if 'overflow' in error.lower():
                        overflow = True
                
                output_rows.append([num1, num2, rep, op, bits, result, overflow, error])

        with open(output_filename, mode='w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(output_rows)

        print(f"Success! Results written to {output_filename}")

    except FileNotFoundError:
        print(f"ERROR: Input file not found: {input_filename}")

    print("-" * 50)


if __name__ == '__main__':
    # Run both parts of the assignment
    test_base_conversion_roundtrip()
    test_binary_arithmetic()
