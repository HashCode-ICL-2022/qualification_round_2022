
from operator import itemgetter
from import_file import load
from export_file import export

from copy import deepcopy
from pprint import pprint

from tqdm import tqdm

def has_skill_level(c, role, workers):
    skills, levels = zip(*c.get("skills"))

    if role[0] not in skills and role[1] > 1:
        return False, None

    level = levels[skills.index(role[0])] \
        if role[0] in skills else 0

    if role[1] <= level:
        return True, role[1] == level
    elif role[1] == level + 1:
        for w in workers:
            can_mentor, _ = has_skill_level(w, role, [])
            if can_mentor:
                return True, True

    return False, None
    

def project_score(p, t):
    return min(p.get("S"), max(p.get("S") - (p.get("D") + t - p.get("B")), 0))

def naive(contributors, projects):
    available_contributors = deepcopy(contributors)
    projects_available = sorted(deepcopy(projects), key=itemgetter("B"))

    projects_in_progress = list()
    organised_projects = list()

    time = 0

    print("Running Naive Algorithm")

    pbar = tqdm(total=len(projects_available))

    project_allocated = True

    while project_allocated or len(projects_in_progress) > 0:

        for i, (project, workers, level_ups, end_time) in enumerate(deepcopy(projects_in_progress)):
            if end_time > time:
                continue

            projects_in_progress.remove((project, workers, level_ups, end_time))

            if any(level_ups):

                for lu, w, role in zip(level_ups, workers, project.get("roles")):

                    if lu:
                        role_name, _ = role
                        worker_skills = w.get("skills")
                        skill_names = list(map(itemgetter(0), worker_skills))

                        if role_name in skill_names:
                            i = skill_names.index(role_name)
                            _, workers_level = worker_skills[i]

                            w.get("skills").pop(i)
                        
                        else:
                            workers_level = 0

                        w.get("skills").append((role_name, workers_level + 1))

                    available_contributors.append(w)
            
            else:
                available_contributors.extend(workers)

        project_allocated = False

        for project in deepcopy(projects_available):
            if project_score(project, time) == 0:
                projects_available.remove(project)    
                continue            

            workers = list()
            level_ups = list()

            for role in project.get("roles"):
                satisfied = False

                for c in available_contributors:
                    is_skilled, level_up = has_skill_level(c, role, workers)
                    
                    if is_skilled and c not in workers:

                        level_ups.append(level_up)
                        workers.append(c)
                        satisfied = True

                        break

                if not satisfied:
                    break    
                
            if not satisfied:
                continue

            project_allocated = True
            [available_contributors.remove(c) for c in workers]
            
            end_time = time + project.get("D")

            projects_in_progress.append((project, workers, level_ups, end_time))
            organised_projects.append((project, workers))

            projects_available.remove(project)

        if len(projects_in_progress) > 0:
            time = min(map(itemgetter(3), projects_in_progress))
        else:
            time += 1

        pbar.set_postfix(in_progress=len(projects_in_progress),
                         organised=len(organised_projects),
                         available=len(projects_available),
                         time=time)

        pbar.update()

    return organised_projects

if __name__ == "__main__":
    #fname = "a_an_example.in.txt"
    fname = "b_better_start_small.in.txt"
    #fname = "c_collaboration.in.txt"
    #fname = "d_dense_schedule.in.txt"
    #fname = "e_exceptional_skills.in.txt"
    #fname = "f_find_great_mentors.in.txt"

    c, p = load(f"data/{fname}")

    results = naive(c, p)
    pprint(results)

    export(results, f"outputs/{fname}")