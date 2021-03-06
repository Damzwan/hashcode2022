import time
from random import randint

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
        self.lastCheckDay = randint(0, 25) * -1

case = "q"
def readInput():
    print("Input yayaya")
    global case; case = input()
    with open("data/" + case + ".txt") as f:
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





totalScore = 0
def assignProject(currentDay, project, peopleAreObjects): #peopleROles is llijst vna mensen in volgorde van project skills :)
    for index, person in enumerate(peopleAreObjects):
        personSkillLevel = person.skills.get(project.roles[index][0], 0)
        if project.roles[index][1] > personSkillLevel + 1 or person.busyUntil > currentDay:
            print(project.roles[index][1] > personSkillLevel + 1, person.busyUntil > currentDay)
            print("uh oh dumbo")
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
    return person.skills.get(role[0], 0) >= role[1]


def recursiveProjectFinder(peopleTaken, rolesLeft):
    if len(rolesLeft) == 0:
        return []

    available_people = organized_people[rolesLeft[0][0]]
    available_people = [v for k, v in available_people.items() if int(k) >= rolesLeft[0][1]]
    available_people = [item for sublist in available_people for item in sublist]
    available_people = [person for person in available_people if
                        person.busyUntil < currentDay and person not in peopleTaken]

    for index, person in enumerate(available_people):
        canFinish = recursiveProjectFinder(peopleTaken + [person], rolesLeft[1:])
        if canFinish is not None:
            return [person] + canFinish
    return None

def getLastDay(projects):
    return max(project.bestBefore + project.score for project in projects)

currentDay = -1
def getAvailablePeople(people):
    return [p for p in people if p.busyUntil <= currentDay]

def masterAlgorithm(people, projects):
    global currentDay
    projectAssignments = []
    amountAvailableLastDay = -1
    lastDay = getLastDay(projects)
    while currentDay <= lastDay:
        availablePeople = getAvailablePeople(people)
        amountAvailableToday = len(availablePeople)
        currentDay += 1
        if amountAvailableToday == len(people) and amountAvailableLastDay == len(people):
            break

        if amountAvailableToday == amountAvailableLastDay:
            amountAvailableLastDay = amountAvailableToday
            continue

        amountAvailableLastDay = len(availablePeople)
        timeStr =  "("+str(round(time.time()-startTime))+"s)"
        print("[day " + str(currentDay) + "/" + str(lastDay) + "]", "projects left:", len(projects), "people available:", len(availablePeople), timeStr)
        timeStr = "(" + str(round(time.time() - startTime)) + "s)"
        print("[day " + str(currentDay) + "]", "projects left:", len(projects), "people available:",
              len(availablePeople), timeStr)

        for projectToCheck in projects:
            if currentDay - projectToCheck.lastCheckDay < 10:
                continue
            projectToCheck.lastCheckDay = currentDay
            # print("checking project" + projectToCheck.name)
            if amountAvailableToday < len(projectToCheck.roles):
                continue
            reco = recursiveProjectFinder([], projectToCheck.roles)
            # print("found", reco)
            if reco is not None:
                assignProject(currentDay, projectToCheck, reco)
                projectAssignments.append(projectToCheck)
                projects.remove(projectToCheck)
                for pp in reco:
                    availablePeople.remove(pp)
        
    return projectAssignments

def writeOutput(projects):
    open('o' + case + '.txt', 'w').close()
    with open("o" + case + ".txt", "a") as f:
        f.write(str(len(projects)) + "\n")
        for project in projects:
            f.write(project.name + "\n" + " ".join([x.name for x in project.peopleAssigned]) + "\n")

startTime = -1


def organize_people(people: [Person]):
    organizedPeople = {}
    for person in people:
        for skill, score in person.skills.items():
            if skill not in organizedPeople:
                organizedPeople[skill] = {}

            if score not in organizedPeople[skill]:
                organizedPeople[skill][score] = []

            organizedPeople[skill][score].append(person)

    return organizedPeople


if __name__ == "__main__":
    startTime = time.time()
    people, projects = readInput()
    organized_people = organize_people(people)
    projects.sort(key=lambda x: x.bestBefore)
    result = masterAlgorithm(people, projects)
    writeOutput(result)