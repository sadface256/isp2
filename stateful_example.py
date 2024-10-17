from hypothesis.strategies import integers, lists
from hypothesis import given
from hypothesis.stateful import rule, precondition, RuleBasedStateMachine, Bundle
import unittest

def heapnew():
    return []


def heapempty(heap):
    return not heap


def heappush(heap, value):
    heap.append(value)
    index = len(heap) - 1
    while index > 0:
        parent = (index - 1) // 2
        if heap[parent] > heap[index]:
            heap[parent], heap[index] = heap[index], heap[parent]
            index = parent
        else:
            break


def heappop(heap):
    return heap.pop(0)


@given(lists(integers()))
def test_pop_in_sorted_order(ls):
    h = heapnew()
    for l in ls:
        heappush(h, l)
    r = []
    while not heapempty(h):
        r.append(heappop(h))
    assert r == sorted(ls)


# class HeapMachine(RuleBasedStateMachine):
#     def __init__(self):
#         super(HeapMachine, self).__init__()
#         self.heap = []

#     @rule(value=integers())
#     def push(self, value):
#         heappush(self.heap, value)

#     @rule()
#     @precondition(lambda self: self.heap)
#     def pop(self):
#         correct = min(self.heap)
#         result = heappop(self.heap)
#         assert correct == result

#------------#

def heapmerge(x, y):
    x, y = sorted((x, y))
    return x + y

class HeapMachine(RuleBasedStateMachine):
    Heaps = Bundle('heaps')

    @rule(target=Heaps)
    def newheap(self):
        return []

    @rule(heap=Heaps, value=integers())
    def push(self, heap, value):
        heappush(heap, value)

    @rule(heap=Heaps.filter(bool))
    def pop(self, heap):
        correct = min(heap)
        result = heappop(heap)
        assert correct == result

    @rule(target=Heaps, heap1=Heaps, heap2=Heaps)
    def merge(self, heap1, heap2):
        return heapmerge(heap1, heap2)


TestHeaps = HeapMachine.TestCase

if __name__ == "__main__":
    #test_pop_in_sorted_order()
    unittest.main()