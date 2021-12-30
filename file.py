import filetype

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