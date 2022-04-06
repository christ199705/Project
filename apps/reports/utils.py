def get_file(file_path):
    with open(file_path, encoding="gbk") as f:
        while True:
            c = f.read(512)
            if c:
                yield c
            else:
                break
