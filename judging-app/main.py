import json
import random

TIME_FOR_ONE_PROJECT = 5
TOTAL_TIME = 30
NUM_PROJECTS_PER_JUDGE = int(TOTAL_TIME/TIME_FOR_ONE_PROJECT)


def parse_project():
    with open('mock_projects.json') as f:
        return json.load(f)


def scheduling_conflict(curr_proj, assigns, curr_round):
    for judge in assigns:
        try:
            pot_conflict = assigns[judge][curr_round]
        except IndexError:
            pot_conflict = None

        if pot_conflict is not None and pot_conflict['name'] == curr_proj['name']:
            # print("Current project: ", curr_proj['name'])
            # print("Conflict with: ", pot_conflict['name'])
            # print()

            return True

    return False


def distribute_projects(projects, num_judges):
    assignments = {}

    # Assign projects for each judge
    for i in range(num_judges):
        for j in range(NUM_PROJECTS_PER_JUDGE):
            # Select project from list using random num
            proj = projects[random.randint(0, len(projects) - 1)]
            if i in assignments:
                # If project is already assigned to this judge, find another one
                while proj in assignments[i] or scheduling_conflict(proj, assignments, j):
                    proj = projects[random.randint(0, len(projects) - 1)]

                # Add to the list of judges for this project
                assignments[i].append(proj)
                assignments.update({i: assignments[i]})
            else:
                assignments[i] = [proj]

    return assignments

def dumpJson(assignments_dict):
  with open('results.json', 'w') as fp:
    json.dump(assignments_dict, fp)


projectObj = parse_project()
judge_assignments = distribute_projects(projectObj["projects"], 4)
dumpJson(judge_assignments)
# print(judge_assignments)
