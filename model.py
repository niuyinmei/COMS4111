from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, id):
        self.id = id

class Customer(User):
    def __init__(self, id, name, memebership, addr):
        self.id = id
        self.name = name
        self.membership = memebership
        self.addr = addr
        


class Employee(User):
    pass