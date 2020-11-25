import enum
import re
import json

class Error:
    def __init__(self,msg,status = 400):
        if type(msg) != dict:
            msg = {'msg': msg}
        self.msg = msg
        self.status = status

class Success:
    def __init__(self,msg,status=200):
        if type(msg) != dict:
            msg = {'msg': msg}
        self.msg = msg
        self.status = status

class NODE_TYPE(enum.Enum):
    COMPUTER = 'COMPUTER'
    REPEATER = 'REPEATER'

    @classmethod
    def isPresent(cls,nodeType):
        for member in NODE_TYPE:
            if member.name == nodeType:
                return True
        return False

class Node:
    def __init__(self,name,type):
        self.name = name 
        self.type = NODE_TYPE[type]
        self.strength = 5
        self.targets = []

    def updateStrengh(self,strength):
        self.strength = strength

class Network:
    def __init__(self):
        self.nodes = {}

    def createNode(self, data):
        name = data.get('name')
        nodeType = data.get('type')
        if name is None or nodeType is None:
            return Error("Invalid Command.")
        if type(name) != str or type(nodeType) !=str:
            return Error("Invalid Command.")
        if not NODE_TYPE.isPresent(nodeType):
            return Error("type '{}' is not supported".format(nodeType))
        if name in self.nodes:
            return Error("Device '{}' already exists".format(name))
        self.nodes[name] = Node(name, nodeType)
        return Success("Successfully added {}".format(name))
    
    def modifyStrength(self, device, data):
        if device not in self.nodes:
            return Error("Device Not Found", 404)
        strength = data.get('value')
        if type(strength) != int:
            return Error("value should be an integer")
        self.nodes[device].updateStrengh(strength)
        return Success("Successfully defined strength")

    def addConnection(self, data):
        source = data.get('source')
        targets = data.get('targets')
        if source is None or targets is None:
            return Error("Invalid command syntax")
        if type(targets) != list or type(source) != str:
            return Error("Invalid command syntax")
        if source in targets:
            return Error("Cannot connect device to itself")
        for name in targets + [source]:
            if name not in self.nodes:
                return Error("Node '{}' not found".format(name))
        sourceNode = self.nodes[source]
        for target in targets:
            if target in sourceNode.targets:
                return Error("Devices are already connected")
        for target in targets:
            sourceNode.targets.append(target)
            self.nodes[target].targets.append(source)
        return Success("Successfully connected")
    
    def fetchDevices(self):
        devices = [{"type": device.type.value, "name": device.name} for _,device in self.nodes.items()]
        return Success({'devices':devices})

    def findRoute(self, start, end):
        if start is None or end is None:
            return Error("Invalid Request")
        startNode = self.nodes.get(start)
        endNode = self.nodes.get(end)
        if startNode is None:
            return Error("Node '{}' not found".format(start))
        if endNode is None:
            return Error("Node '{}' not found".format(end))
        if startNode.type == NODE_TYPE.REPEATER or endNode.type == NODE_TYPE.REPEATER:
            return Error("Route cannot be calculated with repeater")
        return self.traceRoute(startNode, endNode)

    def traceRoute(self, startNode, endNode):
        if startNode.name==endNode.name:
            return Success("Route is {}->{}".format(startNode.name,endNode.name))
        visited = [startNode.name]
        distances = {startNode.name : startNode.strength}
        fromNode = {startNode.name :startNode.name}
        while True:
            nonVisited = [i[1] for i in self.nodes.items() if i[0] not in visited]
            for d in nonVisited:
                for v in visited:
                    if v in  d.targets:
                        newDistance = distances[v] 
                        if d.type == NODE_TYPE.REPEATER:
                            newDistance = 2 * newDistance
                        if d.type == NODE_TYPE.COMPUTER:
                            newDistance = newDistance - 1
                        if distances.get(d.name) is None:
                            distances[d.name] = newDistance
                            fromNode[d.name] = v
                        elif newDistance > distances.get(d.name):
                            distances[d.name] = newDistance
                            fromNode[d.name] = v
            newVisit,to = None,''
            for d in nonVisited:
                nd = distances.get(d.name)
                if nd is None:
                    continue
                if newVisit is None or newVisit<nd:
                    newVisit = nd 
                    to = d.name 
            if newVisit is None:
                return Error("Route not found",404)
            if to == endNode.name:
                n = endNode.name
                ans = [n]
                while n!= startNode.name: 
                    n = fromNode[n]
                    ans.append(n)
                ans = "->".join(ans[::-1])
                return Success("Route is {}".format(ans))
            visited.append(to)    
        return Error("Route not found",404)
    
    def parseModify(self, data):
        data = data.strip()
        r = re.match("\/devices\/(\S+)\/strength\s+(content\-type : application\/json)\s+(.*)",data)
        if r and len(r.groups())==3:
            groups = r.groups()
            try:
                data = json.loads(groups[-1])
                return self.modifyStrength(groups[0],data)
            except:
                return Error("Invalid Command.")
        else:
            return Error("Invalid Command.")

    def parseCreate(self, data):
        data = data.strip()
        if data=="/devices":
            return Error("Invalid Command.")
        if data=="/connections" :
            return Error("Invalid command syntax")
        r = re.match("\/((devices)|(connections))\s+(content\-type\s+:\s+application\/json)\s+(.*)",data)
        if r is None:
            return Error("Invalid Command.") 
        try:
            groups = r.groups()
            data = json.loads(groups[-1])
            if groups[0] == 'devices':
                return self.createNode(data)
            elif groups[0] == 'connections':
                return self.addConnection(data)
            return Error("Invalid Command.")
        except:
            return Error("Invalid Command.")

    def parseFetch(self,data):
        data = data.strip()
        if data == '/devices':
            return self.fetchDevices()
        r = re.match("\/info\-routes\?from=(\S+)&to=(\S+)",data)
        if r and len(r.groups())==2:
            groups = r.groups()
            return self.findRoute(groups[0],groups[1])
        else:
            return Error("Invalid Request")   

    def parse(self,text):
        r = re.match("((MODIFY)|(CREATE)|(FETCH))\s+(.*)",text)
        if r:
            method,data = r.groups()[0],r.groups()[-1]
            if method == 'CREATE':
                return self.parseCreate(data)
            elif method == 'MODIFY':
                return self.parseModify(data)
            elif method == 'FETCH':
                return self.parseFetch(data)
            return Error("Invalid Command.")
        else:
            return Error("Invalid Command.")