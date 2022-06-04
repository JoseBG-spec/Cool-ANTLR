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

int_lst= []
str_lst= ["Object", "IO", "Int", "String", "Boolean"]

klass_W_methods_dic= {}

currentKlass= ""

class DataGenerator(coolListener):
    def __init__(self, dummy):
        self.result = ''
        self.constants = 0

        self.dummy= dummy

    def defaultLabels(self):
        if self.dummy.klassDic.get('Int') == None:
            self.dummy.klassDic["Int"] = ""

        if self.dummy.klassDic.get('Bool') == None:
            self.dummy.klassDic["Bool"] = ""

        if self.dummy.klassDic.get('String') == None:
            self.dummy.klassDic["String"] = ""


        #Prototype tags 
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

        #Class tags
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

        #Class tags ID
        print("¿ class_tags_IDs: ", class_tags_id)

        self.result += asm.tpl_global_tags_start.substitute(
            prototype_tags= prototype_tags,
            class_tags = class_tags
        )

        self.result += class_tags_id

        #MemMgr
        self.result += asm.tpl_MemMgr

    def stringLabels(self):

        # STR CONST - Create str obj, str type 4
        #! Falta ver lo del int_const8, el tamaño del string en objeto
        #!poner el atributo es entero es un 0,
        #! si el atributo es string es vacio 
        #! si el atributo es un int es 

        #!Int_const0
            #tipo de dato (4)
            #tamaño de la clase 
            #String_dispTab
            # apuntador al 
            #!.ascii	STRING
            #.byte	0	
            #.align	2
            #.word	-1


        for i in range(0, len(str_lst)):
            stringLen = len("String")
            self.result += asm.tpl_str_obj.substitute(
                const_no= i,
                str_value= str_lst[i],
            )
            int_lst.append(stringLen)
        
        # INT CONTS - Create int obj, int type 2
        
        #!Int_const0
            #tipo de dato (2)
            #tamaño de la clase 
            #Int_dispTab
            # apuntador al 
            #!valor del int

        for i in range(0, len(int_lst)):

            self.result += asm.tpl_int_obj.substitute(
                int_no= i,
                int_value= str(int_lst[i]),
            )

        # BOOL CONST - Create bool obj
        self.result += asm.tpl_bool

        print("str_lst", str_lst)
        print("int_lst", int_lst)

        #!Class nameTab
        #str_lst + los del ususario
        ## .word por cada el nomrbe de la clase representado en cool object, IO, etc...
        self.result +="""
class_nameTab:
    .word	str_const4
    .word	str_const5
    .word	str_const6
    .word	str_const7
    .word	str_const8
    .word	str_const9"""

        print("klass_W_methods_dic", klass_W_methods_dic)


        
        #!class_dispTab
        #sobre cada clase ponemos los apuntadores su _prot***, **_init
        #iterar sobre la lista de clases
        self.result += asm.tpl_dispTab

        #!Object_dispTab, metodos incluyendo herencia


        #self.result += asm.tpl_mOne
        
        #for name in classesDict.keys():
        #for name in self.dummy.klassDic.keys():
        #    self.addStringConst(name)
            #byte = len(name)

            #print("Byte: ", byte, name)

            #if byte not in self.registered_ints:
                #self.addIntConst(byte)


        #!Proto obj (atributos)
        #todos son fijos hasta string


        #!Main_protObj
        #atributos del main

        #!heap_start es fijo



    def enterProgram(self, ctx: coolParser.ProgramContext):

        self.result += asm.tpl_start_data

        self.defaultLabels()

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        print("ctx", ctx.getText())

        if ctx.ID() != None:
            print("beunas")
        elif ctx.STRING() != None:
            str_lst.append(ctx.STRING().getText())
        elif ctx.INTEGER() != None:
            int_lst.append(ctx.INTEGER().getText())

            
    def enterKlass(self, ctx: coolParser.KlassContext):
        print("enter klass ctx", ctx.getText())

        
        for i in ctx.TYPE():
            print("kLASS", i.getText())

        currentKlass= ctx.TYPE(0).getText()
        print("CURRENT klass:::", currentKlass)

        for keys in self.dummy.klassDic.keys():
            if (keys != "Bool") and (keys != "String") and (keys != "Int"):
                klass_W_methods_dic[keys] = []
        
    def enterMethodDecl(self, ctx: coolParser.MethodDeclContext):
        print("enter method ctx", ctx.expr().getText())

        klass_W_methods_dic["Main"].append("method 3")

        #klass_W_methods_dic["klass_name"].append("method 4")
    def enterExp(self, ctx: coolParser.ExpContext):
        #for i in ctx.expr():
        #    print(i.getText())
        pass

    def enterExpr(self, ctx: coolParser.ExprContext):
        print("enter exp ctx", ctx.getText())

    def exitProgram(self, ctx: coolParser.ProgramContext):
        self.stringLabels()
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
