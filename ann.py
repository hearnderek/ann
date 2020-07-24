import random
import math


def c(activation, desired):
    """ cost function """
    
    # inputs -1 - 1, 
    #print("c",((activation - desired)/2)**2, (activation+1), (desired+1))
    # if activation <= -0.5:
    #     return 1
    return ((max(0,activation) - max(0,desired))/2)**2

def z(weight, previous, bias):
    return weight * previous + bias

def a(z):
    """ activation function  """
    return relu(z)

def relu(x):
    return max(0, x)

# def d()

class Connection:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.weight = random.random() * 2 - 1
        self.bias = 0.0
        self.weightUpdate = 0.0
        self.biasUpdate = 0.0
        self.learnCount = 0
    

    def input(self):
        return self.a.value()

    def value(self):
        value = self.input()
        return min(1, max(-1, self.weight * value + self.bias))
    


    def learn(self, actual):
        self.learnCount += 1
        value = self.value()

        error = actual - value
        errorSqr = c(value, actual)
        #print("How:", value, actual, errorSqr)
        noBias = value - self.bias
        noBiasError = actual - noBias
        biasCorrection = (noBiasError - self.bias) * 0.1 * errorSqr * random.random()
        self.biasUpdate += biasCorrection
        
        #newBias =  self.bias + biasCorrection



        if value != 0:

            if self.weight != 0:
                # o = w*a + b
                # actual + w*a + b
                # (actual - b) / w = prev.actual

                prevActual = min(1, max(-1,(actual - self.bias) / self.weight))
                #print("prevActual", prevActual)
                self.a.learn(prevActual)
            

            if self.input() != 0:
                bestWeight = (actual - self.bias) / self.input()
                # print("errorSqr", errorSqr)
                self.weightUpdate += (bestWeight - self.weight) * 0.1 * errorSqr
                #newWeight = self.weight + self.weightUpdate
                # self.weight = newWeight
            
        # self.bias = newBias

    def sleep(self):
        self.weight += self.weightUpdate / self.learnCount
        self.weightUpdate = 0.0

        self.bias += self.biasUpdate / self.learnCount
        self.biasUpdate = 0.0

        self.learnCount = 0


class Worst:
    def __init__(self, ins, outs):
        self.ins = ins
        self.outs = outs
        

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
            #print("reset")
        else:
            #print("reset input")
            pass
        for n in self.nexts:
            n.b.reset()

    def learn(self, actual):
        if self._initVal:
            # print("no init val learning")
            return
        
        for prev in random.choices(self.prevs, k=max(1,int(0.1*len(self.prevs)))):
        #for prev in self.prevs:
            prev.learn(actual)
        self.reset()

    def sleep(self):
        if self._initVal:
            return
        
        for prev in self.prevs:
            prev.sleep()

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
    def __init__(self, inputs, outputCount, hiddenLayers=3, hiddenNodesPerLayer=10):
        self.percepts = []
        for inp in inputs:
            self.percepts.append(Node(value=inp))


        self.layers = [self.percepts]
        
        # first layer equals number input neurons
        # pLen = len(self.percepts)
        # lev = []
        # for i in range(pLen):
        #     lev.append(Node(self.percepts))
        # self.layers.append(lev)

        for i in range(hiddenLayers):
            plev = self.layers[-1]
            self.layers.append([Node(plev) for j in range(hiddenNodesPerLayer)])
        
        plev = self.layers[-1]
        self.layers.append([Node(plev) for i in range(outputCount)])

        # (0, [0.53], [0.0, 1.0])
        self.worsts = list()

    def sleep(self):
        tmpWorsts = self.worsts

        for i in range(500):
            for j in tmpWorsts:
                (_, w) = j 
                cost = self.learn(w.ins, w.outs, w)
                j = (cost, w)
        
        self.worsts = self.worsts[3:4]
        
        for n in self.layers[-1]:
            n.sleep()

        # if any(tmpWorsts):
        #     for bad in tmpWorsts:
        #         print(bad[0],bad[1].ins,bad[1].outs)

    def learn(self, genIn, genOut, worst=None):
        ins = genIn() if callable(genIn) else genIn
        outs = genOut(ins) if callable(genOut) else genOut
            
        i = 0
        for inp in ins:
            self.layers[0][i]._value = inp
            self.layers[0][i].reset()
            i+=1
        
        cost = 0
        for (node, out) in zip(self.layers[-1],outs):
            cost += c(node.value(), out)
            # print("out:", out)
            node.learn(out)

        cost = cost / len(outs)


        if not worst:
            self.worsts.append((cost, Worst(ins, outs)))
            self.worsts.sort(key=lambda l: l[0], reverse=True)
            self.worsts = self.worsts[0:10]

        return cost

    def print(self):
        print("\nWhole net")
        for l in self.layers:
            print([n.value() for n in l])


        

def tf(stmt):
    if stmt:
        return 1.0
    return 0.0


def nord(x):
    o = ord(x)/255.0
    print(o)
    return min(1, max(0,o))


def m2():
    answers = "0123456789"
    
    net = Net([nord(str(random.choice(answers)))], len(answers))
    inputs = net.percepts
    outputs = net.layers[-1]

    count = 1
    print("\nWhole net")
    for l in net.layers:
        print([n.value() for n in l])

    for y in range(1000):
        i = 0
        c = str(random.choice(answers))
        inputs[0]._value = nord(c)
        inputs[0].reset()

        avgError = 0
        outputs[int(c)].learn(1.0)

        for j in random.choices(range(10), k=4):
            avgError += abs(1 - outputs[j].value())
            # print(c,j,outputs[j].value(), tf(c==str(j)))
            outputs[j].learn(tf(c==str(j)))
        print(count, "AvgError:", avgError)
        count += 1
        # for i in range(10):
        #     inputs[0]._value = nord(str(i))
        #     inputs[0].reset()
        #     print("\n",i,"Whole net")
        #     for l in net.layers:
        #         print([n.value() for n in l])

    for i in range(10):
        inputs[0]._value = nord(str(i))
        inputs[0].reset()
        for ol in outputs:
            ol.reset()
        print("\nWhole net")
        for l in net.layers:
            print([n.value() for n in l])
        # m = (0, outputs[0].value())
        # for j in range(10):
        #     print(inputs[0].value(), j, outputs[j].value())
        #     if m[1] < outputs[j].value():
        #         m = (j, outputs[j].value())
        # print(m)

        print()
        
def m1():
    
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

def sn():
    def inpu(x=None):
        if x is None:
            x = random.random()
        return x*2-1

    def out(x):

        if x > 0:
            return [0, 1]
        else:
            return [1, 0]

    initial = inpu()
    net = Net([initial], 2, 1, 10)
    inputs = net.percepts
    outputs = net.layers[-1]

    
    count = 1
    print("\nWhole net")
    for l in net.layers:
        print([n.value() for n in l])

    #for y1 in range(100):
    while True:
        n = 10000
        k = 1000
        avgError = 0
        for y in range(int(n*random.random())+k):
            
            i = 0
            inputs[0]._value = random.random()*2-1
            inputs[0].reset()

            actual = out(inputs[0]._value)
            for j in range(2):
                avgError += c(outputs[j].value(),actual[j])
                outputs[j].learn(actual[j])
            count += 1

        cost = avgError/n/2
        print("\nWhole net")
        for l in net.layers:
            print([n.value() for n in l])

        print(count, "AvgError:", cost)
        if(cost < 0.01):
            break
        net.sleep()

    for i in [x / 5 - 1 for x in range(11)]:
        inputs[0]._value = i
        inputs[0].reset()
        for ol in outputs:
            ol.reset()
        print("\nWhole net")
        for l in net.layers:
            print([n.value() for n in l])

        actual = out(inputs[0]._value)
        for j in range(2):
            print(inputs[0].value(), actual[j], outputs[j].value())

        print()

    def positive(net, x):
        net.layers[0][0]._value = x
        net.layers[0][0].reset()
        if(net.layers[-1][0].value() < net.layers[-1][1].value()):
            return f"{x} is positive"
        else:
            return f"{x} is negative"

    for x in [x / 5 - 1 for x in range(11)]:
        print(positive(net, x))

def posneg():
    def inpu(x=None):
        if x is None:
            x = random.random()
        return [x*2-1]

    def out(x):
        if x[0] > 0:
            return [0, 1]
        else:
            return [1, 0]

    initial = inpu()
    net = Net(initial, len(out(initial)), 0, 5)

    
    count = 1
    #for y1 in range(100):
    while True:

        n = int( 10000 *random.random()) + 100
        cost = 0
        for y in range(n):
            cost += net.learn(inpu, out)
        
        net.print()
        if(cost / n < 0.1):
            break

        print("cost:", cost / n)
        net.sleep()


        for (i, layer) in enumerate(net.layers):
            for node in layer:
                print(i, [(conn.weight, conn.bias) for conn in node.prevs])

    def positive(net, x):
        net.layers[0][0]._value = x
        net.layers[0][0].reset()
        if(net.layers[-1][0].value() < net.layers[-1][1].value()):
            return f"{x} is positive"
        else:
            return f"{x} is negative"

    for x in [x / 5 - 1 for x in range(11)]:
        print(positive(net, x))

if __name__ == "__main__":
    
    
    posneg()