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

def recursiveProjectFinder(peopleLeft, rolesLeft):
    if len(rolesLeft) == 0:
        return []
    for index, person in enumerate(peopleLeft):
        if canDo(person, rolesLeft[0]):
            canFinish = recursiveProjectFinder(peopleLeft[:index] + peopleLeft[index+1:], rolesLeft[1:])
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

        for projectToCheck in projects:
            if currentDay - projectToCheck.lastCheckDay < 10:
                continue
            projectToCheck.lastCheckDay = currentDay
            # print("checking project" + projectToCheck.name)
            if amountAvailableToday < len(projectToCheck.roles):
                continue
            reco = recursiveProjectFinder(availablePeople, projectToCheck.roles)
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
if __name__ == "__main__":
    startTime = time.time()
    people, projects = readInput()
    projects.sort(key=lambda x: x.bestBefore)
    result = masterAlgorithm(people, projects)
    writeOutput(result)