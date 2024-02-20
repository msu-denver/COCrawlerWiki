import os
import re

# Define the path to the folder containing the text files
folder_path = 'S:\\Web_Crawler\\ColoradoWikiPages'

# Regex pattern to match 'Talk:', 'Special:WhatLinksHere/', 'Template_', and 'Template:Editnotices/Page/'
pattern = re.compile(r'Talk:|Special:WhatLinksHere/|Template_|Template:Editnotices/Page/')

# Iterate over each file in the directory
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):  # Check if the file is a text file
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
        
        # Remove matched patterns from the contents
        modified_contents = re.sub(pattern, '', contents)
        
        # Write the modified contents back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_contents)

print("Process completed.")
