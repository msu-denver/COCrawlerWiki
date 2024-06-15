"""
lfarchio@msudenver.edu | @j4eva | 6/10/2024
"""

import os

def count_words_in_file(filename):
    """
    Count the number of words in a text file.
    
    Args:
        filename (str): The path to the text file.
        
    Returns:
        int: The number of words in the file.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
        words = text.split()
        return len(words)

def count_words_in_folder(folder):
    """
    Count the total number of words in all text files within a folder,
    and keep track of files with less than 10 words.
    
    Args:
        folder (str): The path to the folder containing text files.
        
    Returns:
        tuple: A tuple containing the total number of words, the count of files 
               with less than 10 words, and a list of filenames with less than 10 words.
    """
    total_words = 0
    less_than_10_words_count = 0
    less_than_10_words_files = []

    # Iterate over all files in the folder
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            words_in_file = count_words_in_file(filepath)
            total_words += words_in_file
            print(f"{filename}: {words_in_file} words")

            # Track files with less than 10 words
            if words_in_file < 10:
                less_than_10_words_count += 1
                less_than_10_words_files.append(filename)

    return total_words, less_than_10_words_count, less_than_10_words_files

if __name__ == "__main__":
    folder = "Wiki"  # Specify the folder to check
    if os.path.exists(folder):
        total_word_count, less_than_10_count, less_than_10_files = count_words_in_folder(folder)
        print(f"Total number of words in all files: {total_word_count}")
        print(f"Number of files with less than 10 words: {less_than_10_count}")
        
        # Ask the user if they want to list the files with less than 10 words
        if less_than_10_count > 0:
            list_files = input("Do you want to list the files with less than 10 words? (yes/no): ").strip().lower()
            if list_files == 'yes':
                print("Files with less than 10 words:")
                for file in less_than_10_files:
                    print(file)
    else:
        print(f"The folder '{folder}' does not exist.")
