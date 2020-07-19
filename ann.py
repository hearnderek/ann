import random
import math

class Connection:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.weight = random.random()
        self.bias = 0.0
    

    def input(self):
        return self.a.value()

    def value(self):
        value = self.input()
        return min(1, max(0, self.weight * value + self.bias))
    
    def learn(self, actual):

        value = self.value()

        error = actual - value
        noBias = value - self.bias
        noBiasError = actual - noBias
        biasCorrection = (noBiasError - self.bias) *0.001
        newBias =  self.bias + biasCorrection

        if value > 0:

            if self.weight != 0:
                # o = w*a + b
                # actual + w*a + b
                # (actual - b) / w = prev.actual

                prevActual = (actual - self.bias) / self.weight

                self.a.learn(prevActual)
            

            if self.input() != 0:
                bestWeight = (actual - self.bias) / self.input()

                newWeight = self.weight + (bestWeight - self.weight)*0.001

                self.weight = newWeight
            
        self.bias = newBias



        

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
        else:
            print("reset input")
        for n in self.nexts:
            n.b.reset()

    def learn(self, actual):
        if self._initVal:
            # print("no init val learning")
            return
        
        for prev in self.prevs:
            prev.learn(actual)
        self.reset()

        # for 


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
    def __init__(self, inputs, outputCount):
        self.percepts = []
        for inp in inputs:
            self.percepts.append(Node(value=inp))


        self.layers = [self.percepts]
        
        # first layer equals number input neurons
        pLen = len(self.percepts)
        lev = []
        for i in range(pLen):
            lev.append(Node(self.percepts))
        self.layers.append(lev)

        for i in range(3):
            plev = self.layers[-1]
            self.layers.append([Node(plev) for j in range(5)])
        
        plev = self.layers[-1]
        self.layers.append([Node(plev) for i in range(outputCount)])






        

def tf(stmt):
    if stmt:
        return 1.0
    return 0.0

if __name__ == "__main__":
    answers = "0123456789"
    
    net = Net([ord(str(random.choice(answers)))], len(answers))
    inputs = net.percepts
    outputs = net.layers[-1]

    for y in range(20):
        i = 0
        c = str(random.choice(answers))
        inputs[0]._value = ord(c)
        inputs[0].reset()

        for j in range(10):
            outputs[j].learn(tf(c==str(j)))

    for i in range(10):
        inputs[0]._value = ord(str(i))
        inputs[0].reset()
        for ol in outputs:
            ol.reset()
        m = (0, outputs[0].value())
        for j in range(10):
            print(inputs[0].value(), j, outputs[j].value())
            if m[1] < outputs[j].value():
                m = (j, outputs[j].value())
        print(m)

        print()

if False:
    
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