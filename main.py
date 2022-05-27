from antlr4 import *
from antlr.coolLexer import coolLexer
from antlr.coolParser import coolParser

from listeners.dummy import dummyListener
from listeners.listenerTwo import listenerTwo
from listeners.listenerThree import listenerThree

from listeners.tree import TreePrinter

from listeners.datasegment import DataGenerator

from listeners.gencode import GenCode


def compile(file):
    parser = coolParser(CommonTokenStream(coolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()

    ltwo= listenerTwo()
    walker.walk(ltwo, tree)
    #print("########################################")
    #print("Listener 2")
    #print(ltwo.printObj())

    dummy= dummyListener(
                        ltwo.predefined,
                        ltwo.klassDic,
                        ltwo.methodDic,
                        ltwo.klassInher,
                        ltwo.methodCalls,
                        ltwo.methodFormal,

                        ltwo.klassName,

                        ltwo.tempFormal,
                        ltwo.tempFormalID
    ) 
    walker.walk(dummy, tree)
    print("########################################")
    print("Listener Dummy")
    print(dummy.printObj())

    print("########################################")
    print("tree printer")
    walker.walk(TreePrinter(), tree)

    print("########################################")

    Dg = DataGenerator(dummy)
    walker.walk(Dg, tree)

    Cg = GenCode()
    walker.walk(Cg, tree)

    with open('test.asm', "w") as writer:
        writer.write(Dg.result)
        writer.write(Cg.result)
    writer.close()


def dummy():
    raise SystemExit(1)

if __name__ == '__main__':

    #compile('resources/semantic/input/io.cool')

    #Input.txt has the code of io.cool 
    compile('input.txt')