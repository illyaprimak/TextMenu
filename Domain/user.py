class User :
    def __init__(self,login,password):
        self.login = login
        self.password = password
        self.isAdmin = 0
        self.isBlocked = 0
        self.passwordRestriction = 0


