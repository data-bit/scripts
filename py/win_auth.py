# ==============================================================
# DESC:     Example Windows Authentication - SSO
# ============================================================
import getpass
username = getpass.getuser()
print(username)



# ==============================================================
# DESC:     Example User class - NO SSO
# ============================================================

class Credentials:
    def __init__(self):
        self.username='xxx'
        self.password='xxx'

    def GetUserName(self):
        return self.username

    def GetPassword(self):  
        return self.password
