from hypothesis.strategies import integers, lists
from hypothesis import given
from hypothesis.stateful import rule, precondition, initialize, RuleBasedStateMachine, Bundle
import unittest

# try to model village attacks? like a village can get attacked and then sometimes attack another village or somthing?

class Player():
    def __init__(self):
        self.left_fingers = 1
        self.right_fingers = 1
    
    def add_left(self, num):
        if self.left_fingers + num >= 5 or self.left_fingers + num <= 0:
            self.left_fingers = 0
        else:
            self.left_fingers = self.left_fingers + num
        

    def add_right(self, num):
        if self.left_fingers + num >= 5 or self.left_fingers + num <= 0:
            self.left_fingers = 0
        else:
            self.left_fingers = self.left_fingers + num
    
    def left(self):
        return self.left_fingers
    
    def right(self):
        return self.right_fingers
    
    #overconstrained: should be modulo 2, just want to check that it's even
    def can_split(self):
        return (self.left_fingers + self.right_fingers // 2 == 0)
    
    def split(self):
        self.left_fingers = (self.right_fingers + self.left_fingers) // 2
        self.right_fingers = (self.right_fingers + self.left_fingers) // 2


class SticksMachine(RuleBasedStateMachine):
    # player1 = Bundle("player1")
    # player2 = Bundle("player2")
    # cannot use preconditions with bundles
    Players = Bundle("players")
    turn = 0

    # def __init__(self):
    #     self.player1 = Player()
    #     self.player2 = Player()
    #     self.turn = 1

    @initialize(target=Players)
    def init_player1(self):
        return Player()
    
    @initialize(target=Players)
    def init_player2(self):
        return Player()

    #two attacks on turns 2, 4, 6...
    @precondition(lambda self: self.turn // 2 == 0)
    @rule(player1 = Players, player2 = Players)
    def attack_1_left_left(self, player1, player2):
        player1.add_left(player2.left())
        self.turn += 1
    
    @precondition(lambda self: self.turn // 2 == 0)
    @rule(player1 = Players, player2 = Players)
    def attack_1_right_left(self, player1, player2):
        player1.add_right(player2.left())
        self.turn += 1
    
    @precondition(lambda self: self.turn // 2 == 0)
    @rule(player1 = Players, player2 = Players)
    def attack_1_left_right(self, player1, player2):
        player1.add_left(player2.right())
        self.turn += 1
    
    @precondition(lambda self: self.turn // 2 == 0)
    @rule(player1 = Players, player2 = Players)
    def attack_1_right_right(self, player1, player2):
        player1.add_right(player2.right())
        self.turn += 1

    #one attacks on turns 1, 3, 5...
    @precondition(lambda self: self.turn // 2 == 1)
    @rule(player1 = Players, player2 = Players)
    def attack_2_left_left(self, player1, player2):
        old_left = player2.left()
        player2.add_left(player1.left())
        self.turn += 1
        # should fail when it's greater than 5
        # it does fail when it is > 5!
        #how to do invariance checks
        #assert player2.left() >= old_left
    
    @precondition(lambda self: self.turn // 2 == 1)
    @rule(player1 = Players, player2 = Players)
    def attack_2_right_left(self, player1, player2):
        player2.add_right(player1.left())
        self.turn += 1

    @precondition(lambda self: self.turn // 2 == 1)
    @rule(player1 = Players, player2 = Players)
    def attack_2_left_right(self, player1, player2):
        player2.add_left(player1.right())
        self.turn += 1
    
    @precondition(lambda self: self.turn // 2 == 1)
    @rule(player1 = Players, player2 = Players)
    def attack_2_right_right(self, player1, player2):
        player2.add_right(player1.right())
        self.turn += 1

    @precondition(lambda self: (self.turn // 2 == 0)) # and (player2.can_split()))
    @rule(player2 = Players)
    def two_split(self, player2):
        #self.player2.split()
        if player2.can_split():
            player2.split()
            assert (player2.left() + player2.right()) % 2 == 0
    
    @precondition(lambda self: (self.turn // 2 == 1)) # and (self.player1.can_split()))
    @rule(player1 = Players)
    def one_split(self, player1):
        #self.player1.split()
        if player1.can_split():
            player1.split()
            assert (player1.left() + player1.right()) % 2 == 0

    #would use invariant, but cannot access bundles
    @rule(player1 = Players)
    def valid_values(self, player1):
        assert player1.left() >= 0


TestHeaps = SticksMachine.TestCase

if __name__ == "__main__":
    #test_pop_in_sorted_order()
    unittest.main()