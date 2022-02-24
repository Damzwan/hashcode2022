class Person:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills

class Project:
    def __init__(self, name, timeNeeded, score, bestBefore, roles):
        self.name = name
        self.bestBefore = bestBefore
        self.timeNeeded = timeNeeded
        self.score = score
        self.roles = roles # List of tuples (skill, level)


def readInput():
    print("Input yayaya")
    with open("data/" + input() + ".txt") as f:
        people = []
        projects = []
        first = f.readline()
        contributorAmount, projectAmount = first.split(" ")
        contributorAmount, projectAmount = int(contributorAmount), int(projectAmount)
        for c in range(contributorAmount):
            name, skillAmount = f.readline().split(" ")
            skillAmount = int(skillAmount)
            skills = {}
            for s in range(skillAmount):
                skillName, skillLevel = f.readline().split(" ")
                skills[skillName] = int(skillLevel)
            people.append(Person(name, skills))

        for p in range(projectAmount):
            name, timeNeeded, score, bestBefore, roleAmount = f.readline().split(" ")
            timeNeeded, score, bestBefore, roleAmount = int(timeNeeded), int(score), int(bestBefore), int(roleAmount)
            roles = []
            for r in range(roleAmount):
                roleName, roleLevel = f.readline().split(" ")
                roles.append((roleName, int(roleLevel)))
            projects.append(Project(name, timeNeeded, score, bestBefore, roles))

    return people, projects


def writeOutput(intersections):
    open('o.txt', 'w').close()
    with open("o.txt", "a") as f:
        pass


if __name__ == "__main__":
    people, projects = readInput()
    print(people)