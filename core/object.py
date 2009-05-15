import util
from fileServer import fileServer

from vec2 import Vec2
from vec3 import Vec3
from quat import Quat

class Object:
    objects = {}
    
    def __init__(self, name = None, parent = None, vars = None, children = None):
        self.parent = None
        self.children = {}
        
        name = name or "object"
        
        if name not in Object.objects:
            self.name = name
        else:
            i = 2
            self.name = "%s_%d" % (name,i)
            while self.name in Object.objects:
                i += 1
                self.name = "%s_%d" % (name,i)
        Object.objects[self.name] = self
        
        self.msgFuncs = util.getFuncs(self,"msg_")
        self.unmsgFuncs = util.getFuncs(self,"unmsg_")
        
        if parent:
            assert isinstance(parent,Object)
            self.attachToParent(parent)
            
        if vars:
            self.__dict__.update(vars)
            
        if children:
            self.addChildren(children)
            
        self.defaultVar = self.__dict__.setdefault
            
    def load(self, filename):
        self.addChildren(util.load(fileServer.getFile(filename)))
        
    def addChildren(self, data):
        for name, data in data.iteritems():
            childType = data.pop("type","core.object")
            data["name"] = name
            self.addChild(util.dynload(childType)(**data))

    def save(self, filename):
        data = {}
        for childName, child in self.children.iteritems():
            data[childName] = child.doSave()
        util.save(filename,data)

    def doSave(self):
        data = {}
        data['type'] = self.__class__.__module__

        varTypes = [bool,int,float,str,Vec2,Vec3,Quat]
        
        data['vars'] = {}
        for key, val in self.__dict__.iteritems():
            if key != 'name' and not key.startswith('_') and any([isinstance(val,type) for type in varTypes]):
                data['vars'][key] = val
        data['children'] = {}
        for childName, child in self.children.iteritems():
            data['children'][childName] = child.doSave()
        return data
            
    def delete(self):
        for child in self.children.itervalues():
            child.delete()
        self.detachFromParent()
        assert Object.objects.pop(self.name) == self
            
    def onAttach(self):
        pass
    
    def onDetach(self):
        pass

    def publish(self, cmd, **args):
        self.getRoot().receive(cmd,args)
        
    def receive(self, cmd, args):
        stop = None
        if cmd in self.msgFuncs:
            stop = self.msgFuncs[cmd](args)
        if stop == None:
            for child in self.children.itervalues():
                child.receive(cmd,args)
        if cmd in self.unmsgFuncs:
            self.unmsgFuncs[cmd](args)

    def log(self, *v):
        print "%s: %s" % (self.getPath(), ' '.join(map(str,v)))
    
    def getRoot(self):
        if self.parent:
            return self.parent.getRoot()
        else:
            return self
            
    def getPath(self):
        if not self.parent:
            return "/"
        elif not self.parent.parent:
            return "/%s" % self.name
        else:
            return "%s/%s" % (self.parent.getPath(),self.name)
            
    def getObjectByName(self, name):
        return Object.objects.get(name)
        
    def getObject(self, path):
        if path.startswith("/"):
            return self.getRoot().getObject(path[1:])
        elif "/" in path:
            pos = path.find("/")
            childName = path[:pos]
            restPath = path[pos+1:]
            if childName == ".":
                return self.getObject(restPath)
            elif childName == "..":
                assert self.parent, "path underflow"
                return self.parent.getObject(restPath)
            else:
                assert childName in self.children, "no child %s" % childName
                return self.children[childName].getObject(restPath)
        else:
            if path == ".":
                return self
            elif path == "..":
                assert self.parent, "path underflow"
                return self.parent
            else:
                assert path in self.children, "no child %s" % path
                return self.children[path]
    
    def addChild(self, child):
        if child.name not in self.children:
            self.children[child.name] = child
            child.attachToParent(self)
            
    def attachToParent(self, parent):
        if parent != self.parent:
            self.detachFromParent()
            self.parent = parent
            self.parent.addChild(self)
            self.onAttach()
            
    def removeChild(self, child):
        if child.name in self.children:
            self.children.pop(child.name).detachFromParent()
            
    def detachFromParent(self):
        if self.parent:
            parent = self.parent
            self.parent = None
            parent.removeChild(self)
            self.onDetach()
            
    @staticmethod
    def filter(cond):
        return filter(cond,Object.objects.values())
        
    @staticmethod
    def search(cond):
        for obj in Object.objects.itervalues():
            if cond(obj):
                return obj
                
    def getAncestors(self):
        obj = self.parent
        while obj:
            yield obj
            obj = obj.parent

    def filterAncestors(self, cond):
        return filter(cond,self.getAncestors())
        
    def searchAncestors(self, cond):
        for obj in self.getAncestors():
            if cond(obj):
                return obj
                
if __name__ == "__main__":
    root = Object()
    assert root.name == "object"
    
    child1 = Object("child1",root)
    child2 = Object("child2",child1)
    
    assert child2.getPath() == "/child1/child2"
    assert child2.getObject(child2.getPath()) == child2
    assert child2.getObject("..") == child1
    assert child2.getObject("../.") == child1
    assert child2.getObject(".././..") == root
    assert child2.getObject(".././../child1/./child2") == child2
    
    child1.removeChild(child2)
    assert not child1.children.get("child2")
    assert not child2.parent
    
    child1.detachFromParent()
    assert not child1.parent
    assert not root.children
    
    class PublishTest(Object):
        def __init__(self):
            Object.__init__(self)
            self.received = False
            
        def msg_test(self, args):
            self.received = True
            assert args.get('foo') == 50
            
    publishTest = PublishTest()
    root.addChild(publishTest)

    Object(parent = root).publish("test", foo = 50)
    assert publishTest.received
    
    class AttachDetachTest(Object):
        def __init__(self):
            Object.__init__(self)
            self.attached = False
            self.detached = False
        
        def onAttach(self):
            self.attached = True
            
        def onDetach(self):
            self.detached = True
            
    attachDetachTest = AttachDetachTest()
    assert not attachDetachTest.attached
    root.addChild(attachDetachTest)
    assert attachDetachTest.attached
    assert not attachDetachTest.detached
    root.removeChild(attachDetachTest)
    assert attachDetachTest.detached
