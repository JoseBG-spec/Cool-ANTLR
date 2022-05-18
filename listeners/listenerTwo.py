from asyncio.windows_events import NULL
from xmlrpc.client import Boolean

from pyparsing import empty
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class listenerTwo(coolListener):
    def __init__(self):
        self.predefined = ['Object','Int','String','Boolean','SELF_TYPE','IO','Bool']
        self.main = True
        self.redefineInt = False
        self.anAttributeNamedSelf = False
        self.inheritsBool = False
        self.inheritsSelfType = False
        self.inheritsString = False
        self.letSelf = False
        self.redefinedObject = False
        self.selfAssignment = False
        self.selfInformalParameter = False
        self.selfTypeParameterPosition = False
        self.selfTypeRedeclared = False
        self.operation = ''
        self.badArith = False
        self.klassDic = {}
        self.methodDic = {}
        self.klassInher = {}
        self.methodCalls = {}
        self.methodFormal = {}
        self.klassName = ''

        self.letCall= ''
        self.letID = ''
        self.letExit = False
        self.strs = ''
        self.MethDeclType = ''
        self.caseSt = []
        self.assocID = ''
        

        self.formalCh = ''
        self.badDispatch = False
        self.badEqualityTest1 = False
        self.badEqualityTest2 = False
        self.missClass = False
        self.methDeclY = False
        self.tempFormal = []
        self.tempFormalID =[]

    def enterKlass(self, ctx:coolParser.KlassContext):
        if ctx.TYPE(0).getText() in self.klassDic.keys():
            raise redefinedclass()
        self.klassName = ctx.TYPE(0).getText()
        self.klassDic[self.klassName] = ''
        self.klassInher[self.klassName]=''
        
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True
        if ctx.TYPE(0).getText() == 'Int':
            self.redefineInt = True
        if ctx.TYPE(0).getText() == 'Object':
            self.redefinedObject = True
        if ctx.TYPE(0).getText() == 'SELF_TYPE':
            self.selfTypeRedeclared = True
        #print(ctx.TYPE(1))
        if (ctx.TYPE(1) is not None):
            self.klassInher[self.klassName]+= ctx.TYPE(1).getText() + ","
            if ctx.TYPE(1).getText() not in self.klassDic.keys():
                if ctx.TYPE(1).getText() == 'Bool':
                    self.inheritsBool = True
                if ctx.TYPE(1).getText() == 'SELF_TYPE':
                    self.inheritsSelfType = True
                if ctx.TYPE(1).getText() == 'String':
                    self.inheritsString = True
                elif(ctx.TYPE(1).getText() not in self.predefined):
                    self.missClass = True
            #self.inherits[self.klassNo] = ctx.TYPE(1).getText()
    
    def exitKlass(self, ctx:coolParser.KlassContext):
        if (not self.main):
            raise nomain()
        if (self.redefineInt):
            raise badredefineint()
        #print(self.inheritsBool)
        if (self.inheritsBool):
            raise inheritsbool()
        if (self.inheritsSelfType):
            raise inheritsselftype()
        if (self.inheritsString):
            raise inheritsstring()
        if (self.redefinedObject):
            raise redefinedobject()
        if (self.selfTypeRedeclared):
            raise selftyperedeclared()
        if (self.missClass):
            raise missingclass()
        
        print("Class Name",self.klassName,"Classes:", self.klassDic[self.klassName])
        print("Class Name",self.klassName,"Inherits:", self.klassInher[self.klassName])
        print("DicMethod",self.methodDic)
        self.methodDic = {}
    
    def enterMethodCall(self, ctx: coolParser.MethodCallContext):
        self.methodCalls[ctx.ID().getText()] = ''
        for parms in ctx.params:
            if parms.getText() == "self":
                self.methodCalls[ctx.ID().getText()] += self.klassName + ','
            elif parms.getText().isnumeric():
                self.methodCalls[ctx.ID().getText()] += "Int" + ','
            else:
                self.methodCalls[ctx.ID().getText()] += parms.getText() + ','

        print("method calls",self.methodCalls)
    
    def enterMethodDecl(self, ctx: coolParser.MethodDeclContext):
        if ctx.ID().getText() in self.methodFormal.keys():
            print('Casio',self.methodFormal[ctx.ID().getText()],self.methodFormal[ctx.ID().getText()].split('|'),len(ctx.formal()))
            if len(ctx.formal()) == len(self.methodFormal[ctx.ID().getText()].split('|'))-1:
                for tempFormalID in ctx.formal():
                    for l in range(len(self.methodFormal[ctx.ID().getText()].split('|'))):
                        if tempFormalID.getText().split(':')[0] in self.methodFormal[ctx.ID().getText()].split('|')[l].split(':')[0]:
                            if tempFormalID.getText().split(':')[1] != self.methodFormal[ctx.ID().getText()].split('|')[l].split(':')[1]:
                                print('Game',tempFormalID.getText().split(':')[1],self.methodFormal[ctx.ID().getText()].split('|')[l].split(':')[1])
                                raise overridingmethod4()
            else:
                raise signaturechange() 

        self.methodFormal[ctx.ID().getText()] = ""
        for x in ctx.formal():
            self.tempFormal.append(x.getText().split(':')[1])
            self.tempFormalID.append(x.getText().split(':')[0])
            self.methodFormal[ctx.ID().getText()] += x.getText() + '|'
        self.klassDic[self.klassName] += ctx.ID().getText() + ","
        self.methodDic[ctx.ID().getText()] = ""
        self.methodDic[ctx.ID().getText()] += ctx.TYPE().getText() + ","

        print("method formal", self.methodFormal)
    
    def printObj(self):
        print("_________________________________")
        print("FINAL klass Dic",        self.klassDic)
        print("FINAL method Dic",       self.methodDic)
        print("FINAL klass inher",      self.klassInher)
        print("FINAL klass Method",     self.methodCalls)

