# Open the input text file (tab-delimited) and read its content
with open('dtm_patch_idrovora.txt', 'r') as infile:
    lines = infile.readlines()

# Reverse the order of columns in each row
flipped_lines = ['\t'.join(line.strip().split('\t')[::-1]) + '\n' for line in lines]

# Write the reversed content to a new file
with open('dtm_patch_idrovora_flipped.txt', 'w') as outfile:
    outfile.writelines(flipped_lines)

print("Columns reversed on each row and saved to 'dtm_patch_idrovora_flipped.txt'.")

