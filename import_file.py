def import_file(fname):
    with open('data/' + fname, 'r') as f:
        N = int(file.readline())

        lines = []
        for i in range(N):
            line = file.readline().rstrip().split(" ")
            lines.append(line)

        return lines
