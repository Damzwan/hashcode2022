class Person:
    def __init__(self, name, skills):
        self.name = name
        self.skills = skills
        self.busyUntil = -1

    def __repr__(self):
         return self.name
    def __str__(self):
         return self.name

class Project:
    def __init__(self, name, timeNeeded, score, bestBefore, roles):
        self.name = name
        self.bestBefore = bestBefore
        self.timeNeeded = timeNeeded
        self.score = score
        self.roles = roles # List of tuples (skill, level)
        self.peopleAssigned = []


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


totalScore = 0
def assignProject(currentDay, project, peopleAreObjects): #peopleROles is llijst vna mensen in volgorde van project skills :)
    for index, person in enumerate(peopleAreObjects):
        personSkillLevel = person.skills.get(project.roles[index][0], 0)
        if project.roles[index][1] > personSkillLevel + 1 or person.busyUntil > currentDay:
            print("uh oh dumbo")
            print(project.roles[index][1])
            print(personSkillLevel + 1)
            exit()
        person.busyUntil = currentDay + project.timeNeeded
        if personSkillLevel <= project.roles[index][1]:
            person.skills[project.roles[index][0]] = personSkillLevel + 1
    project.peopleAssigned = peopleAreObjects
    global totalScore
    totalScore += max(project.score + min(currentDay + project.timeNeeded - project.bestBefore, 0), 0)


def assignRecursive(people, projects):
    pass
            
def canDo(person, role):
    return person.busyUntil <= currentDay and person.skills.get(role[0], 0) >= role[1]


def recursiveProjectFinder(peopleLeft, rolesLeft):
    print("Doing recursive with ", peopleLeft, "and roles", rolesLeft)
    if len(rolesLeft) == 0:
        return []
    for index, person in enumerate(peopleLeft):
        if canDo(person, rolesLeft[0]):
            canFinish = recursiveProjectFinder(peopleLeft[:index] + peopleLeft[index+1:], rolesLeft[1:])
            if canFinish is not None:
                return [person] + canFinish
    return None


currentDay = -1
def masterAlgorithm(people, projects):
    global currentDay
    projectAssignments = []
    someoneBusyYesterday = True
    while any([p.busyUntil > currentDay for p in people]) or someoneBusyYesterday:
        someoneBusyYesterday = any([p.busyUntil > currentDay for p in people])
        currentDay += 1

        for projectToCheck in projects:
            print("checking project" + projectToCheck.name)
            if len(people) < len(projectToCheck.roles):
                continue
            reco = recursiveProjectFinder(people, projectToCheck.roles)
            print("found", reco)
            if reco is not None:
                assignProject(currentDay, projectToCheck, reco)
                projectAssignments.append(projectToCheck)
                projects.remove(projectToCheck)
        
    return projectAssignments


if __name__ == "__main__":
    people, projects = readInput()
    result = masterAlgorithm(people, projects)
    print(result)