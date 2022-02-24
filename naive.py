
from operator import itemgetter
from import_file import load
#from export_file import export

from copy import deepcopy
from pprint import pprint

def has_skill_level(c, role, workers):
    skills, levels = zip(*c.get("skills"))

    if role[0] not in skills and role[1] > 1:
        return False

    level = levels[skills.index(role[0])] \
        if role[0] in skills else 0

    if role[1] <= level:
        return True
    elif role[1] == level + 1:
        for w in workers:
            if has_skill_level(w, role, []):
                return True

    return False
    

def project_score(p, t):
    return min(p.get("S"), max(p.get("S") - (p.get("D") + t - p.get("B")), 0))

def naive(contributors, projects):
    available_contributors = deepcopy(contributors)
    projects_available = sorted(deepcopy(projects), key=itemgetter("B"))

    projects_in_progress = list()
    organised_projects = list()

    time = 0

    while len(projects_available) > 0:

        for i, (project, workers, end_time) in enumerate(deepcopy(projects_in_progress)):
            if end_time > time:
                continue

            projects_in_progress.pop(i)
            available_contributors.extend(workers)

        for project in deepcopy(projects_available):
            if project_score(project, time) == 0:
                projects_available.remove(project)                

            workers = list()

            for role in project.get("roles"):
                satisfied = False

                for c in available_contributors:
                    if has_skill_level(c, role, workers) and c not in workers:
                        workers.append(c)
                        satisfied = True
                        break

                if not satisfied:
                    break    
                
            if not satisfied:
                continue

            [available_contributors.remove(c) for c in workers]
            
            end_time = time + project.get("D")

            projects_in_progress.append((project, workers, end_time))
            organised_projects.append((project, workers))

            projects_available.remove(project)

        time += 1

    return organised_projects

if __name__ == "__main__":
    fname = "a_an_example.in.txt"
    c, p = load(f"data/{fname}")

    results = naive(c, p)
    pprint(results)
    #export(results, f"output/{fname}")
