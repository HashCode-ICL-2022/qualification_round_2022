def load(file_name):
    with open(file_name, 'r') as file:

        # Read first line
        C, P = [int(i) for i in file.readline().rstrip().split(' ')]

        print(f"[{file_name}] Loading {C} Contributors and {P} Projects")

        contributors = []
        for i in tqdm(range(C), desc='Contribs'):
            name, N = file.readline().rstrip().split(' ')
            skills = []
            for j in range(int(N)):
                s, lvl = file.readline().rstrip().split(' ')
                skills += [(s, int(lvl))]

            contributors += [dict(name=name, skills=skills)]

        projects = []
        for i in tqdm(range(P), desc='Projects'):
            name, D, S, B, R = file.readline().rstrip().split(' ')
            roles = []
            for j in range(int(R)):
                s, lvl = file.readline().rstrip().split(' ')
                roles += [(s, int(lvl))]

            projects += [
                dict(name=name,
                     D=int(D),
                     S=int(S),
                     B=int(B),
                     R=int(R),
                     roles=roles)
            ]

        return contributors, projects