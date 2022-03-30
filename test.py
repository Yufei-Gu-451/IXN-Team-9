from app import file
file_content = file.read_txt_file('app/file/Result/Result.txt')

group = file_content.split('\n ')
group.pop()

sum = 0
for str in group:
    integer = int(str)
    print(integer)
    sum += integer

print(sum/100)