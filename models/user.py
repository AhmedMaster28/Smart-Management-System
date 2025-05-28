class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

class Cashier(User):
    def __init__(self, username, password, cashier_id):
        super().__init__(username, password)
        self.cashier_id = cashier_id 