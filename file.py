import filetype
import os

# Write text to the end of a file
# Will not cover original text
def write_to_file(*, output_file_name, text, append):
    if append:
        with open (output_file_name, 'a') as f:
            f.write(text)
            f.close()
    else:
        with open (output_file_name, 'w') as f:
            f.write(text)
            f.close()

# Check file type according to the first 16 bit of the file
def check_file_type(filename, target_type):
    kind = filetype.guess(filename)

    # txt file cannot be identified
    if target_type == 'txt':
        try:
            with open(filename, 'w') as f:
                f.close()
        except IOError:
            print("filetype: Cannot access txt file")
        return True
    elif kind is None:
        print("filetype: Cannot guess file type")
        return False
    elif kind.extension == target_type:
        return True
    else:
        print("filetype: File type error: %s should be %s but is %s", filename, target_type, kind.extension)
        return False


# Try to read a file and return its content in a list of string
def read_file(filename):
    f = open(filename)
    file_content = []

    try:
        for line in f:
            file_content.append(line)
    except IOError:
        print("Cannot access file content")
        return ''

    return file_content


# Check if a file exists
def exists_file(file):
    return os.path.exists(file) and os.path.isfile(file)

# Check if a directory exists
def exists_dir(dir):
    return os.path.exists(dir) and os.path.isdir(dir)