from hypothesis.strategies import integers, lists, sampled_from, runner
from hypothesis import given, Verbosity, settings, event
from hypothesis.stateful import rule, precondition, initialize, RuleBasedStateMachine, invariant
import unittest

class Ball:
    def __init__(self, name):
        self.name = name

class Person:
    def __init__(self):
        self.inventory = set()

    def addBall(self, ball):
        self.inventory.add(ball)

    def throwBall(self, ball, person):
        if ball in self.inventory:
            person.addBall(ball)
            self.inventory.remove(ball)

# class Alice(Person):
#     def addBall(self, ball):
#         if ball.name == "B":
#             self.inventory.add(Ball("C"))
#         else:
#             self.inventory.add(ball)

# class Bank(Person):
#     def addBall(self, ball):
#         if ball.name == "A":
#             self.inventory.add(Ball("B"))
#         else:
#             self.inventory.add(ball)

class TossMachine(RuleBasedStateMachine):
    Alice = Person()
    Bob = Person()
    Bank = Person()
    
    # def __init__(self):
    #     super().__init__()

    #     self.Alice = Person()
    #     self.Bob = Person()
    #     self.Bank = Person()

    @initialize()
    def initial_balls(self):
        self.Alice.addBall(Ball("A"))
    
    @precondition(lambda self: len(self.Alice.inventory) != 0)
    @rule()
    def AliceBob(self):
        ball = sampled_from(self.Alice.inventory)
        self.Alice.throwBall(ball, self.Bob)

    @precondition(lambda self: len(self.Bob.inventory) != 0)
    @rule()
    def BobBank(self):
        ball = sampled_from(self.Bob.inventory)
        if ball.name == "A":
            self.Bank.addBall(Ball("B"))
        else:
            self.Bob.throwBall(ball, self.Bank)

    @precondition(lambda self: len(self.Bank.inventory) != 0)
    @rule()
    def BankBob(self):
        ball = sampled_from(self.Bank.inventory)
        self.Bank.throwBall(ball, self.Bob)

    @precondition(lambda self: len(self.Bob.inventory) != 0)
    @rule()
    def BobAlice(self):
        ball = sampled_from(self.Bob.inventory)
        if ball.name == "B":
            self.Alice.addBall(Ball("C"))
            event("Alice gets Ball C")
        else:
            self.Bob.throwBall(ball, self.Alice)

    def BallC(self, balls):
        for ball in balls:
            if ball.name == "C":
                return True
        return False

    @invariant()
    #@settings(verbosity = Verbosity.verbose)
    def bob_sucks(self):
        #print(TossMachine.runner())
        assert not self.BallC(self.Bob.inventory)
        assert len({ball for ball in self.Bob.inventory if ball.name == "C"}) == 0


TestToss = TossMachine.TestCase

if __name__ == "__main__":
    unittest.main()
    #pytest --hypothesis-show-teststatistics

    