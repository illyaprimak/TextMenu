def initDb():
    try:
        repository = open("repository_db.txt", "r+")
    except FileNotFoundError:
        repository = open("repository_db.txt", "w+")
    body = repository.readlines()
    data = []
    for line in body:
        if line != "":
            data.append(parseLine(line))
    repository.close()
    return data


def parseLine(line):
    parsed = line.split()
    result = []
    for item in parsed:
        if item == "empty":
            result.append("")
        else:
            result.append(item)
    return result

def saveDb(data):
    repository = open("repository_db.txt", "w+")

    for line in data:
        string = ""
        for element in line:
            if element == "":
                string = string + "empty" + " "
            else:
                string = string + str(element) + " "
        repository.write(string + "\n")

