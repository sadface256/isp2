from hypothesis.strategies import integers, lists
from hypothesis import given
from hypothesis.stateful import rule, precondition, initialize, RuleBasedStateMachine, Bundle, consumes
import unittest

class Village():
    def __init__(self, num_population):
        self.healthy_population = num_population
        self.zombie_population = 0

    def zombies(self):
        return self.zombie_population
    
    def people(self):
        return self.healthy_population
    
    def overrun(self):
        if self.zombie_population > self.healthy_population:
            self.zombie_population = self.healthy_population + self.zombie_population
            self.healthy_population = 0
            #self.zombie_population = 0
    
    def move_in(self, num):
        if num > 0:
            self.healthy_population = self.healthy_population + num
        self.overrun()
    
    def move_out(self, num):
        if self.healthy_population - num >= 0:
            self.healthy_population = self.healthy_population - num
        else:
            self.healthy_population = 0
        self.overrun()

    def horde_advances(self, num):
        self.zombie_population += num
        self.overrun()
    
    def zombie_attack(self):
        #this is faulty-- if there are more zombies than villagers than healthy pop becomes negative
        # which also makes the zombie pop negative
        #self.overrun()
        self.healthy_population = self.healthy_population - self.zombie_population
        self.zombie_population += self.healthy_population - self.zombie_population
        self.overrun()
    
class AttackMachine(RuleBasedStateMachine):
    Villages = Bundle("villages")

    pop_strat = integers(min_value=0, max_value=30)

    @rule(target=Villages, num = pop_strat)
    def init_village(self, num):
        return Village(num)

    @rule(village = Villages, num = pop_strat)
    def move_in(self, village, num):
        village.move_in(num)
    
    #i want to say that the number moving out should be people in the village, but i don't know how
    @rule(village = Villages, num = pop_strat)
    def move_out(self, village, num):
        old_pop = village.people()
        village.move_out(num)
        assert village.people() >= 0
        assert village.people() <= old_pop
    
    @rule(village = Villages, zombies = pop_strat)
    def infected(self, village, zombies):
        village.horde_advances(zombies)
    
    @rule(village1 = Villages, village2 = consumes(Villages))
    def merge(self, village1, village2):
        village1.move_in(village2.people())
        village1.horde_advances(village2.zombies())
    
    @rule(village = Villages)
    def attack(self, village):
        village.zombie_attack()
    
TestVillages = AttackMachine.TestCase

#add front/back
#delete element from mid, add to mid

if __name__ == "__main__":
    #test_pop_in_sorted_order()
    unittest.main()
