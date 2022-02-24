def export(results, fname):

    with open(fname, "w") as file:
        file.write(str(len(results)) + '\n')

        for res in results:
            file.write(res[0]['name'] + '\n')
            file.write(' '.join([person['name'] for person in res[1]]) + "\n")
