class User:

    def __init__(self, name, username, email, phone_num, password, discordId = None, phoneVerified = False):
        self.name = name
        self.username = username
        self.email = email
        self.phone_num = phone_num
        self.password = password
        self.discordId = discordId
        self.phoneVerified = phoneVerified
        self.id = None

    def __str__(self):
        return f"{self.name} ({self.username})"

    def __repr__(self):
        return f"{self.name} ({self.username})"


    def to_dict(self, ):
        return {
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "phone_num": self.phone_num,
            "password": self.password,
            "discordId": self.discordId,
            "phoneVerified": self.phoneVerified,
            "id": self.id
        }
    
    def from_dict(self, data):
        self.name = data["name"]
        self.username = data["username"]
        self.email = data["email"]
        self.phone_num = data["phone_num"]
        self.password = data["password"]
        self.discordId = data["discordId"]
        self.phoneVerified = data["phoneVerified"]
        self.id = data["id"]
        return self