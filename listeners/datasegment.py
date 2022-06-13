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

default_klasses=["Object", "IO", "Int", "String", "Boolean"]

klass_W_methods_dic= {
    "Object":   ["POINTER", "abort", "type_name", "copy"], 
    "IO":       ["POINTER","out_string", "out_int", "in_string", "in_int"],  
    "Int":      ["POINTER"],  
    "String":   ["POINTER","length", "concat", "substr"],
    "Boolean":  ["POINTER"]
}

currentKlass= ""
currentKlassMethods= []

class DataGenerator(coolListener):
    def __init__(self, dummy):
        self.result = ''
        self.constants = 0

        self.dummy= dummy

    #Este método crea el header deafult del .asm
    #desde ".data" hasta "-MemMgr_TEST"
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

        #print("¿ proto_tags: ", prototype_tags)

        #Class tags
        class_tags= ""
        for classname in constants:
            class_tags += (
                asm.tpl_global_class_tag.substitute(
                    name=classname
                )
            )

        #print("¿ class_tags: ", class_tags)


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
        #print("¿ class_tags_IDs: ", class_tags_id)
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
            pointer= "Int_cons"+str(len(int_lst))

            int_lst.append(stringLen)
            #print("No. Pointer: ", int_lst, len(int_lst)-1)

            #ADD    pointer as the FIRST ELEMENT of array 
            #       on the klass_W_methods_dic
            some_key = str_lst[i]
            if some_key in klass_W_methods_dic.keys():
                #print("Key: ",                some_key)
                #print("-klass method arr",   klass_W_methods_dic[some_key])

                klass_W_methods_dic[some_key][0] = pointer
                #print("--pointer",            klass_W_methods_dic[some_key][0])
            else:
                print("-key "+some_key+" doesn\'t exist")

            self.result += asm.tpl_str_obj.substitute(
                const_no= i,
                pointer= pointer,
                str_value= str_lst[i],
            )

        #Int tamaño cero
        self.result += asm.tpl_string_empty.substitute(
                str_no= str(len(str_lst)+1),
                pointer= "int_const"+str(len(int_lst)+1),
            )


        """Int_const0 - Create int class"""
        #       .word	-1
        #!Int_const0
            #   .word   tipo de dato (2)
            #   .word   tamaño de (esta) clase  
            #   .word   Int_dispTab
            #   .word   #!valor del int

            
            #! se redonde al asiguiente multplo de 4
            #logitud dle objeto string
            # se divide entre 4 para que me o de en words
            #y le sumo 3

            #multiple * (number / multiple)

        #Int tamaño cero
        self.result += asm.tpl_int_empty.substitute(
                int_no= str(len(int_lst)+1),
            )

        for i in range(0, len(int_lst)):
            self.result += asm.tpl_int_obj.substitute(
                int_no= i,
                val= round(  (  ( 4*( int(int_lst[i]) / 4) ) / 4  ) + 3 ),
                int_value= int_lst[i],
            )

        """bool_const0 - Create bool obj"""
        self.result += asm.tpl_bool

        print("*str_lst", str_lst)
        print("*int_lst", int_lst)

        """class_nameTab"""
        # .word por cada nombre de las clases representadas en cool 
        # + los del usuario
        #Agarramos el primer elemento del array de cada key en klass_W_methods_dic
        # el cual es el apuntador a esa clase

        #!USAR EL TEMPLATE DE STRING
        self.result += asm.tlp_class_nametab
        for arr in klass_W_methods_dic.values():
            self.result += asm.tlp_word.substitute(
                value= arr[0],
            )
        print("klass_W_methods_dic", klass_W_methods_dic)

        """class_objTab"""
        #sobre cada clase ponemos los apuntadores su _prot***, **_init
        #iterar sobre la lista de clases
        self.result += asm.tpl_class_objTab
        for key in klass_W_methods_dic.keys():
            self.result += asm.tlp_objTab_word.substitute(
                klass= key,
            )

        """Object_dispTab"""
        #Object_dispTab, clases con metodos, incluyendo herencia
        #Fijos
        self.result += asm.tpl_set_dispTab

        #Dinámicos (main + los del usuario)
        for key in klass_W_methods_dic.keys():
            if key in default_klasses:
                continue
            else:  
                self.result += asm.tpl_dynamic_dispTab.substitute(
                        klass= key,
                    )
                ### Checar la herencia (por defult todos heredan de object)
                self.result += asm.tpl_dispTab_Object

                inher= self.dummy.klassInher[key]
                ##el string de herencia tiene un - , - 
                inher= inher.replace(",", "")

                inher_methods= klass_W_methods_dic[inher]

                #print("inher", self.dummy.klassInher)
                #print("inher_methods", inher_methods)

                #Añadir metodos de herencia
                #desde el 1 para evitar el apuntador
                for i in range(1, len(inher_methods)):
                    self.result += asm.tpl_dynamic_dispTab_word.substitute(
                            klass= inher,
                            method= inher_methods[i],
                        )

                #Añadir metodos propios de la clase
                #desde el 1 para evitar el apuntador
                for i in range(1, len(klass_W_methods_dic[key])):
                    self.result += asm.tpl_dynamic_dispTab_word.substitute(
                            klass= key,
                            method= klass_W_methods_dic[key][i],
                        )

        """Proto Objects (atributos)"""
        ##todos son fijos excepto string
        #Fijos
        self.result += asm.tpl_default_protoObj

        #!String
        #!int con tamaño cero y ese es el pauntador de aca
        self.result += asm.tpl_string_protoObj.substitute(
                pointer= "int_const"+str(len(int_lst)+1),
            )

        """Main_protObj"""
        #!Main_protObj
        #! INT - int con tamaño cero y ese es el pauntador de aca
        #! STRING VACIO - int con tamaño cero y ese es el pauntador de aca
        #atributos del main
        self.result += asm.tpl_main_protoObj.substitute(
                int_pointer= "int_const"+str(len(int_lst)+1),
                str_pointer= "str_const"+str(len(str_lst)+1),
            )

        """heap_start - (es fijo)"""
        self.result += asm.tpl_heap_start

    def enterProgram(self, ctx: coolParser.ProgramContext):

        self.result += asm.tpl_start_data

        self.defaultLabels()

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        #print("ctx", ctx.getText())

        if ctx.ID() != None:
            print("beunas")
        elif ctx.STRING() != None:
            str_lst.append(str(ctx.STRING().getText())[1:-1])
        elif ctx.INTEGER() != None:
            int_lst.append(ctx.INTEGER().getText())
            
    def enterKlass(self, ctx: coolParser.KlassContext):
        #print("enter klass ctx", ctx.getText())
        
        #for i in ctx.TYPE():
            #print("kLASS", i.getText())

        currentKlass= ctx.TYPE(0).getText()
        #print("CURRENT klass:::", currentKlass)
        #ADD classes to the klass_W_methods_dic
        some_key = currentKlass
        if some_key in klass_W_methods_dic.keys():
            print("key "+some_key+" already exist")
        else:
            #added value to the methods dic
            klass_W_methods_dic[some_key]= ["POINTER"]

        if not currentKlass in str_lst:
            str_lst.append(some_key)

    def exitKlass(self, ctx: coolParser.KlassContext):
        #print("***currentKlassMethods:", currentKlassMethods) 
        currentKlass= ctx.TYPE(0).getText()
        #print("***currentKlass:", currentKlass)
        #print("***klass_W_methods_dic:", klass_W_methods_dic)

        for i in range(0, len(currentKlassMethods)):
            klass_W_methods_dic[currentKlass].append(currentKlassMethods[i])
        
    def enterMethodDecl(self, ctx: coolParser.MethodDeclContext):
        #print("***enter method ctx:", ctx.TYPE().getText())
        #print("***enter method ctx:", ctx.ID().getText())

        #print("***klass ", currentKlass)

        currentKlassMethods.append(ctx.ID().getText())

    def exitProgram(self, ctx: coolParser.ProgramContext):
        self.stringLabels()