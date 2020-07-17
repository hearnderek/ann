import random
import math

class Connection:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.weight = 1.0
        self.bias = 0.0
        self.negativity = 0.0 
    

    def input(self):
        return self.a.value()

    def value(self):
        value = self.input()
        return max(0, self.weight * value - self.negativity * value + self.bias)
    
    def learn(self, actual):
        value = self.value()
        if value > 0:
            error = actual - value
            noBias = value - self.bias
            noBiasError = actual - noBias
            biasCorrection = (noBiasError - self.bias)*0.01
            newBias =  self.bias + biasCorrection
            #print("Bias:", self.bias, newBias, self.value())

            if self.input() != 0:
                bestWeight = (actual - self.bias + self.negativity * value) / self.input()
                newWeight = self.weight + (bestWeight - self.weight)*0.5
                #print("Weight:", self.weight, newWeight, self.value())

                bestNegativity = (actual - self.bias - self.weight * value) / self.input()
                newNegativity = self.negativity + ((bestNegativity - self.negativity)*0.01)
                self.weight = newWeight
                self.negativity = newNegativity
            
            self.bias = newBias
            #print(actual, self.value(), self.bias, self.weight, self.negativity)


        

class Node:
    def getValue(self):
        return self._value

    def calculateValue(self):
        val = 0.0
        for prev in self.prevs:
            val += prev.value()
            #print(val)
        val = val / len(self.prevs)
        self._value = val
        self.value = self.getValue
        return val

    def value(self):
        pass

    def reset(self):
        if not self._initVal:
            self.value = self.calculateValue
            self._value = None
        for n in self.nexts:
            n.b.reset()

    def learn(self, actual):
        for prev in self.prevs:
            prev.learn(actual)
        self.reset()

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
            self.percepts = Node(value=inp)

def tf(stmt):
    if stmt:
        return 1.0
    return 0.0

if __name__ == "__main__":
    pass
    chrIn = None
    with open('input.chr', 'r') as f:
         chrIn = ord(f.read()[0])

    print(chrIn)

    nets = []
    answers = "0123456789"
    inNode = Node(value=chrIn)
    perceptionLayer = [inNode, Node(value=48)]
    for n in range(10):

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
        ]

        c = answers[n]
        for y in range(2000):
            i = 0
            inNode._value = ord(c)

            for j in range(10):
                outputLayer[j].learn(tf(c==str(j)))
        
        for i in range(10):
            inNode._value = ord(str(i))
            for ol in outputLayer:
                ol.reset()
            print(i, outputLayer[i].value())
        
        for ol in outputLayer:
            nets.append(ol)
        
    outputLayer = [
        Node(xs=nets), # 0
        Node(xs=nets), # 1
        Node(xs=nets), # 2
        Node(xs=nets), # 3
        Node(xs=nets), # 4
        Node(xs=nets), # 5
        Node(xs=nets), # 6
        Node(xs=nets), # 7
        Node(xs=nets), # 8
        Node(xs=nets), # 9
    ]
    for y in range(2000):
        i = 0
        c = str(random.choice(answers))
        # print("input:", c)
        inNode._value = ord(c)
        inNode.reset()

        for j in range(10):
            outputLayer[j].learn(tf(c==str(j)))

    for i in range(10):
        inNode._value = ord(str(i))
        for ol in outputLayer:
            ol.reset()
        print(i, outputLayer[i].value())
        # for j in range(10):