#maybe, you know what? just make a good guy and a bad guy

public_keys = {}

class Message:
    def __init__(self, content, publickey):
        self.content = content
        self.publickey = publickey

class Person:
    def __init__(self, name, key):
        self.name = name
        self.private_key = key
        self.received_messages = []
        self.secrets = {}
        public_keys[self] = name + str(1)

    def receiveMessage(Message):
        pass
        

class GoodPerson(Person):
    pass

class BadPerson(Person):
    None