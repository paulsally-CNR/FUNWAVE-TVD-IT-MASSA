# Python script to flip the rows of a matrix in a text file
import sys
import numpy as np

if len(sys.argv) > 1:
    input_file = sys.argv[1]
else:
    print('No file passed.')
    exit()

def flip_txt_rows(input_file, output_file=None):
    # Read the matrix from the text file
    with open(input_file, 'r') as file:
        # Read all lines from the file
        lines = file.readlines()

    # Convert the lines into a 2D numpy array
    matrix = np.array([list(map(float, line.split())) for line in lines])

    # Flip the matrix upside down (flip the rows)
    flipped_matrix = np.flipud(matrix)

    # Define the output file (same as input if not specified)
    if output_file is None:
        output_file = input_file

    # Write the flipped matrix back to the text file
    np.savetxt(output_file, flipped_matrix, fmt='%.6f')

    print(f"Matrix flipped successfully and saved to {output_file}")

flip_txt_rows(input_file, input_file + ".flipped")
