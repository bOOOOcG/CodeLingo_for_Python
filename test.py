def file_operations(filename):
    with open(filename, 'r') as file:
        content = file.read()
        print(content, end='')  # 保留文件内容中的换行符
        file.seek(0)
        lines = file.readlines()
        for line in lines:
            print(len(line.strip()))

file_operations('level10_example.txt')