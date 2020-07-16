class Connection:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.weight = 1.0
        self.bias = 0.0
    

    def input(self):
        return self.a.value()

    def value(self):
        return self.weight * self.input() + self.bias

        

class Node:
    def getValue(self):
        return self._value

    def calculateValue(self):
        if self._value:
            return self._value
            
        val = 0.0
        for prev in self.prevs:
            val += min(1, max(0, prev.value()))

        self._value = val
        return val

    def value(self):
        pass

    def reset(self):
        if not self._initVal:
            self.value = self.calculateValue
            self._value = None

    def __init__(self, xs=[], value=None):
        self.xs = xs
        if value:
            self._initVal = value
            self._value = value
            self.value = self.getValue
        else:
            self.value = self.calculateValue
            self._initVal = None
            self._value = None
        self.prevs = list()
        self.nexts = list() 
        for x in xs:
            conn = Connection(x, self)
            self.prevs.append(conn)
            x.nexts.append(conn)
    
class Net:
    def __init__(self, inputs, outputs):
        self.percepts = []
        for inp in inputs:
            self.percepts = Node(val=inp)

            
if __name__ == "__main__":
    pass
    chrIn = None
    with open('input.chr', 'r') as f:
         chrIn = ord(f.read()[0])

    print(chrIn)

    
    perceptionLayer = [Node(value=chrIn)]

    outputLayer = [
        Node(xs=perceptionLayer), # 0
        Node(xs=perceptionLayer), # 1
        Node(xs=perceptionLayer), # 2
        Node(xs=perceptionLayer), # 3
        Node(xs=perceptionLayer), # 4
        Node(xs=perceptionLayer), # 5
        Node(xs=perceptionLayer), # 6
        Node(xs=perceptionLayer), # 7
        Node(xs=perceptionLayer), # 8
        Node(xs=perceptionLayer), # 9
        Node(xs=perceptionLayer)  # nan
    ]

    i = 0
    for output in outputLayer:
        i+=1
        print(i, output.value())


