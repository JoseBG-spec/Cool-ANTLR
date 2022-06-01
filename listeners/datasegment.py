from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

from util import asm

from listeners.listenerTwo import listenerTwo

#from util.structure import _allClasses as classesDict, lookupClass

constants= [
    'int',
    'bool',
    'string'
]

default_size= {
    'Object':   3,
    'IO':       3,
    'Int':      4,
    'Bool':     4,
    'String':   5
}

class DataGenerator(coolListener):
    def __init__(self, dummy):
        self.result = ''
        self.constants = 0

        self.dummy= dummy

    #! ¿De que se encarga el datasegment?

    #! poner los metodos con el nombre que usamos en los listeners
    #!!

    #! Funciones para contruir el "header del output"

    def defaultLabels(self):

        #
        if self.dummy.klassDic.get('Int') == None:
            self.dummy.klassDic["Int"] = ""

        if self.dummy.klassDic.get('Bool') == None:
            self.dummy.klassDic["Bool"] = ""

        if self.dummy.klassDic.get('String') == None:
            self.dummy.klassDic["String"] = ""


        #!Prototype tags 
        prototype_tags = ""
        for classname in self.dummy.klassDic.keys():
            if classname == 'Object' or classname == 'Bool':
                continue
            prototype_tags += (
                asm.tpl_prototype_tag.substitute(
                    name=classname
                )
            )

        print("¿ proto_tags: ", prototype_tags)

        #!Class tags
        class_tags= ""
        for classname in constants:
            class_tags += (
                asm.tpl_global_class_tag.substitute(
                    name=classname
                )
            )

        print("¿ class_tags: ", class_tags)


        class_tags_id= ""
        i= 0
        for name in self.dummy.klassDic.keys():
            if name == 'Main':
                continue
            if name == 'String':
                i = 4
            if name == 'Bool':
                i = 3
            if name == 'Int':
                i = 2

            class_tags_id += asm.tpl_class_tag.substitute(
                name=name.lower(),
                n= i
            )

        #!Class tags ID
        print("¿ class_tags_IDs: ", class_tags_id)

        self.result += asm.tpl_global_tags_start.substitute(
            prototype_tags= prototype_tags,
            class_tags = class_tags
        )

        self.result += class_tags_id

        #MemMgr

        self.result += asm.tpl_MemMgr

        #!
        print("klasDic_keyes: ", self.dummy.klassDic.keys())

        #!!!! Create str obj, str type 4
        stringLen = len("String")
        self.result += asm.tpl_str_obj.substitute(
            const_no= 0,
            str_value= "Hello",
        )
        
        print("klasDic_keyes: ", self.dummy.klassDic)
        #!!!! Create int obj, int type 2
        self.result += asm.tpl_int_obj.substitute(
            int_no= 0,
            int_value= str(5),
        )
        #self.result += asm.tpl_mOne
        
        #for name in classesDict.keys():
        #for name in self.dummy.klassDic.keys():
        #    self.addStringConst(name)
            #byte = len(name)

            #print("Byte: ", byte, name)

            #if byte not in self.registered_ints:
                #self.addIntConst(byte)

        #! Create bool obj
        self.result += asm.tpl_bool





    def enterProgram(self, ctx: coolParser.ProgramContext):

        self.result += asm.tpl_start_data

        self.defaultLabels()



        

    def enterMethodCall(self, ctx: coolParser.MethodCallContext):
        self.result += asm.tpl_var_decl.substitute(
            varname = ctx.getChild(1).getText()
        )

    def enterSum(self, ctx: coolParser.MethodCallContext):
        self.result += asm.tpl_suma.substitute(
            varname = ctx.getChild(1).getText()
        )

    def exitProgram(self, ctx: coolParser.ProgramContext):
        self.result += "\n $$$$$$$$$$$$$$$$$$$$$$$$$$"

"""
    def enterDeclaracion(self, ctx: coolParser.DeclaracionContext):
        self.result += asm.tpl_var_decl.substitute(
            varname = ctx.getChild(1).getText()
        )
        ctx.code = ''

    def enterPrimaria_string(self, ctx: coolParser.Primaria_stringContext):
        self.constants = self.constants + 1
        ctx.label = "var{}".format(self.constants)
        self.result += asm.tpl_string_const_decl.substitute(
            name = ctx.label, content = ctx.getText()
        )
 """
