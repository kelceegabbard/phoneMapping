import os
from docx import Document

# Directory where the .docx files are stored
directory = './'
output_file = 'all_words.txt'

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # Iterate through each file in the directory
    for filename in sorted(os.listdir(directory)):
        # Check if the file is a .docx file
        if filename.endswith('.docx'):
            # Load the .docx file
            doc = Document(os.path.join(directory, filename))
            # Read each paragraph in the document
            for para in doc.paragraphs:
                # Write each paragraph to the output file
                outfile.write(para.text + '\n')

print(f"All words have been combined into {output_file}")
