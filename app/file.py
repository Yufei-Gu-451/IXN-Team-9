import filetype
import os

# Return root directory 
def get_root_dir():
    return os.getcwd()

# Create a file
def create_file(filename):
    filename = get_root_dir() + os.sep + filename

    file = open(filename, 'w')
    file.close()

# Delete a file
# If file not exist, do nothing
def delete_file(filename):
    filename = get_root_dir() + os.sep + filename

    if exists_file(filename):
        os.remove(filename)

# Check if a file exists
def exists_file(filename):
    filename = get_root_dir() + os.sep + filename

    return os.path.exists(filename) and os.path.isfile(filename)

# Check if a directory exists
def exists_dir(directory):
    directory = get_root_dir() + os.sep + directory

    return os.path.exists(directory) and os.path.isdir(directory)

# Check file type according to the first 16 bit of the file
def check_file_type(filename, target_type):
    filename = get_root_dir() + os.sep + filename

    kind = filetype.guess(filename)

    # txt file cannot be identified
    if kind is None:
        if target_type == 'txt':
            try:
                with open(filename) as f:
                    f.close()
                    return True
            except Exception:
                return False

        return False
    
    return kind.extension == target_type


# Try to read a txt file and return its content in a string
# If file does not exist / not txt file, raise IOError
def read_txt_file(filename):
    filename = get_root_dir() + os.sep + filename

    if exists_file(filename) and check_file_type(filename, 'txt'):
        f = open(filename)
        file_content = ''

        for line in f:
            file_content += line + ' '

        return file_content
    else:
        raise IOError("read_txt_file: error file input: {}".format(filename)) # .format(e) ?

# Write text to the end of a file
# If append is true, add to file end
# If append is false, cover original content
# If file does not exist / not txt file, raise IOError
def write_txt_file(*, output_file_name, text, append):
    output_file_name = get_root_dir() + os.sep + output_file_name

    if exists_file(output_file_name) and check_file_type(output_file_name, 'txt'):
        if append:
            with open (output_file_name, 'a') as f:
                f.write(text)
                f.close()
        else:
            with open (output_file_name, 'w') as f:
                f.write(text)
                f.close()
    else:
        raise IOError('write_txt_file: error file input: {}'.format(output_file_name))