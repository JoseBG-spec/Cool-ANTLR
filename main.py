from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.dummy import dummyListener
from listeners.listenerTwo import listenerTwo
from listeners.listenerThree import listenerThree

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()

    ltwo= listenerTwo()
    walker.walk(ltwo, tree)
    print("########################################")
    print("Listener 2")
    print(vars(ltwo))

    dummy= dummyListener(
                        ltwo.predefined,
                        ltwo.main,
                        ltwo.redefineInt,
                        ltwo.anAttributeNamedSelf,
                        ltwo.inheritsBool,
                        ltwo.inheritsSelfType,
                        ltwo.inheritsString,
                        ltwo.letSelf,
                        ltwo.redefinedObject,
                        ltwo.selfAssignment,
                        ltwo.selfInformalParameter,
                        ltwo.selfTypeParameterPosition,
                        ltwo.selfTypeRedeclared,
                        ltwo.operation,
                        ltwo.badArith,

                        ltwo.klassDic,
                        ltwo.methodDic,
                        ltwo.klassInher,
                        ltwo.methodCalls,
                        ltwo.methodFormal,

                        ltwo.klassName,
                        ltwo.letCall,
                        ltwo.letID,
                        ltwo.letExit,
                        ltwo.strs,
                        ltwo.MethDeclType,
                        ltwo.caseSt,
                        ltwo.assocID,

                        ltwo.formalCh,
                        ltwo.badDispatch,
                        ltwo.badEqualityTest1,
                        ltwo.badEqualityTest2,
                        ltwo.missClass,
                        ltwo.methDeclY,
                        ltwo.tempFormal,
                        ltwo.tempFormalID
    ) 
    walker.walk(dummy, tree)
    print("########################################")
    print("Listener Dummy")
    print(vars(dummy))

    lthree= listenerTwo()
    walker.walk(lthree, tree)
    print("########################################")
    print("Listener 3")
    print(vars(lthree))


def dummy():
    raise SystemExit(1)

if __name__ == '__main__':
    #compile('resources/semantic/input/assignment.cool')
    #compile('resources/semantic/input/basic.cool')
    #compile('resources/semantic/input/basicclassestree.cool')
    ##compile('resources/semantic/input/cells.cool')
    #compile('resources/semantic/input/classes.cool') Check how to see fi there is no main
    #compile('resources/semantic/input/compare.cool')
    #compile('resources/semantic/input/comparisons.cool')  Check how to see fi there is no main
    #compile('resources/semantic/input/cycleinmethods.cool')
    #compile('resources/semantic/input/dispatch.cool')
    compile('resources/semantic/input/nomain.cool')
    #Forwards inherits needs to check all classes before
    #WTF hairyScary
