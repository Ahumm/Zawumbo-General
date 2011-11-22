import os,sys,re

T_NOTRUN = 0
T_RUNNING = 1
T_WAITING = 2
T_SKIP = 3
T_FAILED = 4
T_PASSED = 5


class Result(object):
    possible_outcomes = { T_NOTRUN : "NOT RUN",
                          T_RUNNING : "RUNNING",
                          T_WAITING : "WAITING",
                          T_SKIP : "SKIP",
                          T_FAILED : "FAILED",
                          T_PASSED : "PASSED" }

    def __init__(self,result=T_NOTRUN, message = '')                      
                          
class Test(object):
    _doc_keys = ["PARAMS", "REQ", "ID"]
    _waiting = Result(T_WAITING)
    
    def __init__(self,function,module=''):
        self.function = function
        self.name = function.__name__
        if module:
            self.testName = module.split('.')[-1] + '.' + self.name
        else:
            self.testName = self.name
        
        self.parse_doc(function.__doc__)
         
    def parse_doc(self, doc):
        for key in self._doc_keys:
            p = re.findall(r'^\s*' + key + ':(.*$)', str(doc),re.MULTILINE)
            print "%s: %s" % (key,str(p))
        
    def run_test(self):
        pass

def load_tests(testPath):
    testDirectory = import_from_string(testPath)
    tests = []
    if testDirectory:
        for testloc in testDirectory.__all__:
            # Strip file extension
            if testloc.endswith('.py'):
                testloc = testloc[:-3]
            testfile = "%s.%s" % (testPath,testloc)
            mod = import_from_string(testfile)
            for func in dir(mod):
                if func.startswith("test"):
                    tests.append(Test(getattr(mod,func),testfile))
            #for i in tests:
            #    i()
    
def run_tests(tests):
    for t in tests:
        if t.result = T_NOTRUN:
            run_test_tree(test)
        else:
            pass
    
def run_test_tree(test):
    if test.result == T_WAITING:
        return
    test.result = test._waiting
    
def import_from_string(name):
    try:
        mod = __import__(name)
        components = name.split('.')
        for comp in components[1:]:
            mod = getattr(mod,comp)
        return mod
    except ImportError:
        print "Error importing %s." % name
        return None
    
    
if __name__ == "__main__":
    load_tests("tests")