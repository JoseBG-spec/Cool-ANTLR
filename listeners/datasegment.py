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
klass_lst= []

klass_W_methods_dic= {}

currentKlass= ""

class DataGenerator(coolListener):
    def __init__(self, dummy):
        self.result = ''
        self.constants = 0

        self.dummy= dummy

    #Este método crea el header deafult del .asm
    # desde ".data" hasta "-MemMgr_TEST"

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

    #Esta funcion genera el resto del segmento de datos
    def stringLabels(self):
        #! Falta ver lo del int_const8, el tamaño del string en objeto
        #!poner el atributo es entero es un 0,
        #! si el atributo es string es vacio 
        #! si el atributo es un int es 

        """str_const - Create string class"""
        #       .word	-1
        #str_const#!0
            #   .word   tipo de dato (4)
            #   .word   #!tamaño de (esta) clase 
            #   .word   String_dispTab
            #   .word   #!apuntador al numero creado
            #   .ascii	#!STRING
            #   .byte	0	
            #   .align	2
            #   .word   -1

        for i in range(0, len(str_lst)):

            #print("String: ", str_lst[i], len(str_lst[i]))
            stringLen = len(str_lst[i])

            int_lst.append(stringLen)
            #print("No. Pointer: ", int_lst, len(int_lst)-1)

            self.result += asm.tpl_str_obj.substitute(
                const_no= i,
                pointer= "Int_cons"+str(len(int_lst)-1),
                str_value= '"'+str_lst[i]+'"',
            )
        
        """Int_const0 - Create int class"""
        #       .word	-1
        #!Int_const0
            #   .word   tipo de dato (2)
            #   .word   tamaño de (esta) clase  
            #   .word   Int_dispTab
            #   .word   #!valor del int

        for i in range(0, len(int_lst)):
            self.result += asm.tpl_int_obj.substitute(
                int_no= i,
                int_value= str(int_lst[i]),
            )

        """bool_const0 - Create bool obj"""
        self.result += asm.tpl_bool

        print("str_lst", str_lst)
        print("int_lst", int_lst)

        """ """
        #!Class nameTab
        #klass_lst + los del usuario
        # .word por cada nombre de la clase representado en cool 
        # object, IO, etc...
        self.result += asm.tlp_class_nametab

        print("klass_W_methods_dic", klass_W_methods_dic)


        """class_objTab"""
        #sobre cada clase ponemos los apuntadores su _prot***, **_init
        #iterar sobre la lista de clases
        self.result += asm.tpl_class_objTab

        """Object_dispTab"""
        #!Object_dispTab, clases con metodos, incluyendo herencia
        #Fijos
        self.result += asm.tpl_set_dispTab

        #Dinámicos (main)
        self.result += asm.tpl_dispTab

        """Proto Objects"""
        #!Proto obj (atributos)
        ##todos son fijos excepto string
        #Fijos
        self.result += asm.tpl_default_protoObj

        #String
        self.result += asm.tpl_string_protoObj

        """Main_protObj"""
        #!Main_protObj
        #atributos del main
        self.result += asm.tpl_main_protoObj


        """heap_start - (es fijo)"""
        self.result += asm.tpl_heap_start


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
