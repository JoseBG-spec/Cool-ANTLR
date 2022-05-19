from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.dummy import dummyListener
from listeners.listenerTwo import listenerTwo

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()

    ltwo= listenerTwo()
    walker.walk(ltwo, tree)
    ltwo.printObj()

    dummy= dummyListener(ltwo.klassDic,
                        ltwo.methodDic,
                        ltwo.klassInher,
                        ltwo.methodCalls,
                        ltwo.methodFormal,
    )
    
    walker.walk(dummy, tree)
    dummy.printObj()


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
    compile('resources/semantic/input/dispatch.cool')
    #Forwards inherits needs to check all classes before
    #WTF hairyScary
