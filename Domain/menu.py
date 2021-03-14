from pip._vendor.distlib.compat import raw_input
import re
from Domain import user
from Repository import dbwork

ariphmetic = {"=", "-", "+", "<", ">"}
numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 0}
punctuation = {".", ",", ":", ";", "-"}


def initMenu():
    global data
    data = dbwork.initDb()
    if not data:
        data.append(["ADMIN","",1,0,0])
    startMenu()


def startMenu():
    print(startMenuText())
    n = raw_input("Enter your option: ")
    if n == "1":
        login()
    elif n == "2":
        help()
    elif n == "3":
        exitProgram()
    else:
        print("Chose correct option: ")
        startMenu()


def exitProgram():
    print("Bye bye")
    dbwork.saveDb(data)


def startMenuText():
    return "1.Login\n" \
           "2.Help\n" \
           "3.End program\n"


def userMenuText():
    return "1.Change password\n" \
           "2.End program\n"


def adminMenuText():
    return "1.Change password\n" \
           "2.All users list\n" \
           "3.Add new user\n" \
           "4.Block user\n" \
           "5.Block user\n" \
           "6.Restrict user\n" \
           "7.Restrict user\n" \
           "8.Restrict all users\n" \
           "9.Restrict all users\n" \
           "0.End program\n"


def login():
    username = raw_input("Enter your login: ")
    password = raw_input("Enter your password: ")
    newUser = user.User(username, password)
    findUsages(newUser)


def help():
    print("Програма виконана Поліною Ракович ФБ-83.\nВаріант 14 .\nОбмеження паролю : наявність цифр, розділових знаків і знаків арифметичних операцій")
    startMenu()

def findUsages(newUser):
    username = newUser.login
    password = newUser.password
    counter = 0
    passwordCounter = 0
    for item in data:
        if item[0] == username:
            counter += 1
            if item[1] == password:
                print("Successfully authorized")
                newUser.isAdmin = item[2]
                newUser.isBlocked = item[3]
                newUser.passwordRestriction = item[4]
                authorized(newUser)
                break
            else:
                passwordCounter += 1
                if passwordCounter == 3:
                    exitProgram()
                else:
                    print("Incorrect password, try again")
                    counter = 0
                    login()
                    break
    if counter == 0:
        print("There are no user with this username, try again")
        login()


def authorized(User):
    if User.isAdmin == "0":
        if User.isBlocked == "1":
            print("You are blocked, returning to main menu")
            startMenu()
        else:
            print(userMenuText())
            n = raw_input("Enter your option: ")
            if n == "1":
                changePassword(User)
            elif n == "2":
                exitProgram()
            else:
                print("Chose correct option: ")
                startMenu()
    else:
        authorizedAdmin(User)


def authorizedAdmin(User):
    print(adminMenuText())
    n = raw_input("Enter your option: ")
    if n == "1":
        changePassword(User)
    elif n == "2":
        allUsersList(User)
    elif n == "3":
        addNewUser(User)
    elif n == "4":
        blockUser(User)
    elif n == "5":
        unblockUser(User)
    elif n == "6":
        restrictUser(User)
    elif n == "7":
        unrestrictUser(User)
    elif n == "8":
        restrictAllUsers(User)
    elif n == "9":
        unrestrictAllUsers(User)
    elif n == "0":
        exitProgram()
    else:
        print("Chose correct option: ")
        authorizedAdmin()


def allUsersList(User):
    print("List of all users: ")
    for item in data:
        print("     Username : " + item[0])
        print("     Password : " + item[1])
        print("     isAdmin : " + str(item[2]))
        print("     isBlocked : " + str(item[3]))
        print("     isRestricted : " + str(item[4]) + "\n")

    authorizedAdmin(User)


def addNewUser(User):
    n = raw_input("Enter username for new user: ")
    newUser = user.User(n, "")
    data.append(newUser)
    print("User with username : " + n + " successfully added")
    authorizedAdmin(User)


def blockUser(User):
    n = raw_input("Enter username for block: ")
    for item in data:
        if item[0] == n:
            item[3] = 1
    print("User with username : " + n + " successfully blocked")
    authorizedAdmin(User)


def unblockUser(User):
    n = raw_input("Enter username for unblock: ")
    for item in data:
        if item[0] == n:
            item[3] = 0
    print("User with username : " + n + " successfully unblocked")
    authorizedAdmin(User)


def restrictUser(User):
    n = raw_input("Enter username for restrict password: ")
    for item in data:
        if item[0] == n:
            item[4] = 1
    print("User with username : " + n + " successfully restricted")
    authorizedAdmin(User)


def unrestrictUser(User):
    n = raw_input("Enter username for unrestrict password: ")
    for item in data:
        if item[0] == n:
            item[4] = 0
    print("User with username : " + n + " successfully unrestricted")
    authorizedAdmin(User)


def restrictAllUsers(User):
    for item in data:
        item[4] = 1
    print("All users restricted")
    authorizedAdmin(User)


def unrestrictAllUsers(User):
    for item in data:
        item[4] = 0
    print("All users unrestricted")
    authorizedAdmin(User)


def changePassword(User):
    password1 = raw_input("Enter your password: ")
    password2 = raw_input("Repeat your password: ")
    if password1 != password2:
        print("Passwords doesn't match , try again")
        changePassword(User)
    else:
        if User.passwordRestriction == 1:
            if restrict(password1) == 1:
                print("Successful changing")
                User.password = password1
                change(User)
            else:
                print("Password doesn't match restriction(minimum one number, punctuation and arithmetic , try again")
                changePassword(User)
        else:
            print("Successful changing")
            User.password = password1
            change(User)


def restrict(password):
    first = 0
    second = 0
    third = 0
    for letter in password:
        if letter in ariphmetic:
            first += 1
        if letter in numbers:
            second += 1
        if letter in punctuation:
            third += 1
    if first > 0 | second > 0 | third > 0:
        result = 1
    else:
        result = 0
    return result


def change(User):
    for item in data:
        if item[0] == User.login:
            item[1] = User.password
    authorized(User)
