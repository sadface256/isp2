from hypothesis.strategies import integers, lists
from hypothesis import given
from hypothesis.stateful import rule, precondition, initialize, RuleBasedStateMachine, Bundle, consumes
import unittest

class Node():
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList():
    def __init__(self):
        self.head = None

    def addFirst(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    
    def addLast(self, data):
        if self.head == None:
            self.head = Node(data)
        else:
            new_node = Node(data)
            temp = self.head
            while temp.next != None:
                temp = temp.next
            temp.next = new_node
    
    def addMid(self, data, index):
        if index == 0:
            self.addFirst(data)
        #comment out
        if self.head == None:
            return
        
        current_position = 0
        new_node = Node(data)
        temp = self.head
        while current_position != index - 1:
            if temp.next == None:
                return
            temp = temp.next
            current_position += 1
            #not checking if index is in range
        
        previous = temp
        future_next = temp.next
        previous.next = new_node
        new_node.next = future_next
    
    def popFirst(self):
        #to be commented out
        if self.head == None:
            return None
        old_head = self.head
        self.head = self.head.next
        return old_head.data
    
    def popLast(self):
        if self.head == None:
            return None
        if self.head.next == None:
            old_node = self.head
            self.head = None
            return old_node.data
        temp = self.head
        while temp.next.next != None:
            temp = temp.next
        old_end = temp.next
        temp.next = None
        return old_end.data

    def popMid(self, index):
        if index == 0:
            return self.popFirst()
        if self.head == None:
            return None
        if index > self.length() - 1:
            return None
        
        current_position = 0
        temp = self.head
        while current_position != index - 1:
            #temp.next
            if temp.next == None:
                return None
            temp = temp.next
            current_position += 1
        
        old_node = temp.next
        new_next = old_node.next if old_node != None else None
        temp.next = new_next

        return old_node.data
    
    def length(self):
        current_len = 0

        temp = self.head
        while temp != None:
            current_len += 1
            temp = temp.next
        
        return current_len
    
    def merge(self, other_list):
        if self.head == None:
            self.head = other_list.head
        else:
            new_node = other_list.head
            temp = self.head
            while temp.next != None:
                temp = temp.next
            temp.next = new_node
        


    
class ListMachine(RuleBasedStateMachine):

    Lists = Bundle("lists")

    num_strat = integers()

    @rule(target=Lists)
    def new_list(self):
        return LinkedList()
    
    @rule(ex_list = Lists, num = num_strat)
    def addFirst(self, ex_list, num):
        old_len = ex_list.length()
        old_start = ex_list.head

        ex_list.addFirst(num)
        assert ex_list.length() == old_len + 1
        assert ex_list.head != old_start
    
    @rule(ex_list = Lists, num = num_strat)
    def addLast(self, ex_list, num):
        old_len = ex_list.length()

        ex_list.addLast(num)

        assert ex_list.length() == old_len + 1

    
    index_strat = integers(0, 5)

    @rule(ex_list = Lists, num = num_strat, index = index_strat)
    def addMid(self, ex_list, num, index):
        old_len = ex_list.length()

        ex_list.addMid(num, index)

        if index < old_len:
            assert ex_list.length() == old_len + 1


    @rule(ex_list = Lists)
    def popFirst(self, ex_list):
        old_len = ex_list.length()

        popped_data = ex_list.popFirst()

        if popped_data == None:
            assert ex_list.length() == old_len
        else:
            assert ex_list.length() == old_len - 1
    
    @rule(ex_list = Lists)
    def popLast(self, ex_list):
        old_len = ex_list.length()

        popped_data = ex_list.popLast()

        if popped_data == None:
            assert ex_list.length() == old_len
        else:
            assert ex_list.length() == old_len - 1
    
    @rule(ex_list = Lists, index = index_strat)
    def popMid(self, ex_list, index):
        old_len = ex_list.length()

        popped_data = ex_list.popMid(index)

        if popped_data == None:
            assert ex_list.length() == old_len
        else:
            assert ex_list.length() == old_len - 1
    
    @rule(target = Lists, ex_list = Lists, other_list = Lists)
    def mergeList(self, ex_list, other_list):
        return ex_list.merge(other_list)

    

TestList = ListMachine.TestCase

#threat model
#dolev-yao threat model, conceptual
# -- i have to send you messages across a medium. the medium is the attacker.
# -- anything that the medium can do, the attacker can do

if __name__ == "__main__":
    #test_pop_in_sorted_order()
    LL = LinkedList()
    LL.popMid(1)
    unittest.main()

