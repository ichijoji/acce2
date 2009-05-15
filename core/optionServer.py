from fileServer import fileServer
import util
import sys

class OptionServer(dict):
    def __init__(self):
        map(self.update,map(util.load,fileServer.filesByType.get('cfg',())))
        
        for i, s in enumerate(sys.argv):
            if s.startswith('+'):
                self[s[1:]] = True
            elif s.startswith('-'):
                self[s[1:]] = False
            elif s == "=" and i > 0 and i < len(sys.argv)-1:
                self[sys.argv[i-1]] = util.evalStr(sys.argv[i+1])
            elif "=" in s:
                pos = s.find("=")
                self[s[:pos]] = util.evalStr(s[pos+1:])

optionServer = OptionServer()

if __name__ == "__main__":
    print optionServer
