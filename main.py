from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.dummy import dummyListener

def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    
    walker.walk(dummyListener(), tree)


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
