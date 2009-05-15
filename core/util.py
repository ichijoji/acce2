import yaml
from vec2 import Vec2
from vec3 import Vec3
from quat import Quat

def getFuncs(self, prefix):
    return dict([(name[len(prefix):],getattr(self,name)) for name in filter(lambda name: name.startswith(prefix), dir(self))])

def evalStr(s):
    try:
        return eval(s,dict(Vec2 = Vec2, Vec3 = Vec3, Quat = Quat))
    except:
        return s

def evalDict(d):
    newd = {}
    for key, val in d.iteritems():
        if type(val) is dict:
            newd[key] = evalDict(val)
        elif type(val) is str:
            newd[key] = evalStr(val)
        else:
            newd[key] = val
    return newd

def load(filename):
    return evalDict(yaml.load(open(filename)))

def save(filename, data):
    yaml.dump(data,open(filename,"w"))

def capitalize(s):
    return s[:1].upper() + s[1:]
    
def dynload(name):
    try:
        exec "from %s import %s as c" % (name,capitalize(name.split('.')[-1])) in locals()
    except ImportError:
        raise RuntimeError("unable to dynload class %s" % name)
    return c
