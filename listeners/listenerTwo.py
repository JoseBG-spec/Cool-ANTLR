from asyncio.windows_events import NULL
from xmlrpc.client import Boolean

from pyparsing import empty
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class listenerTwo(coolListener):
    def __init__(self):
        self.predefined = ['Object','Int','String','Boolean','SELF_TYPE','IO','Bool']
        self.main                   = False
        self.redefineInt            = False
        self.anAttributeNamedSelf   = False
        self.inheritsBool           = False
        self.inheritsSelfType       = False
        self.inheritsString         = False
        self.letSelf                = False
        self.redefinedObject        = False
        self.selfAssignment         = False
        self.selfInformalParameter  = False
        self.selfTypeParameterPosition  = False
        self.selfTypeRedeclared     = False
        self.operation              = ''
        self.badArith               = False
        
        self.klassDic               = {}
        self.methodDic              = {}
        self.klassInher             = {}
        self.methodCalls            = {}
        self.methodFormal           = {}
        self.klassName              = ''

        self.klassName              = ''
        self.letCall                = ''
        self.letID                  = ''
        self.letExit                = False
        self.strs                   = ''
        self.MethDeclType           = ''
        self.caseSt                 = []
        self.assocID                = ''
        

        self.formalCh               = ''
        self.badDispatch            = False
        self.badEqualityTest1       = False
        self.badEqualityTest2       = False
        self.missClass              = False
        self.methDeclY              = False
        self.tempFormal             = []
        self.tempFormalID           = []

    def enterKlass(self, ctx:coolParser.KlassContext):
        self.klassName = ctx.TYPE(0).getText()
        self.klassDic[self.klassName] = ''
        self.klassInher[self.klassName]=''
        
        #print(ctx.TYPE(1))
        if (ctx.TYPE(1) is not None):
            self.klassInher[self.klassName]+= ctx.TYPE(1).getText() + ","

    
    def enterMethodCall(self, ctx: coolParser.MethodCallContext):
        self.methodCalls[ctx.ID().getText()] = ''
        for parms in ctx.params:
            if parms.getText() == "self":
                self.methodCalls[ctx.ID().getText()] += self.klassName + ','
            elif parms.getText().isnumeric():
                self.methodCalls[ctx.ID().getText()] += "Int" + ','
            else:
                self.methodCalls[ctx.ID().getText()] += parms.getText() + ','
    
    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.ID() is not None:
            print('Buenas8',ctx.ID().getText(),self.klassDic[self.klassName].split(","),self.klassName);
            if self.methDeclY:
                if ctx.ID().getText() == "self":
                    raise selfassignment()
                
                self.methDeclY = False
            
        if self.letID is not None:
            if ctx.ID() is not None:
                if ctx.ID().getText() == self.letID:
                    if self.letExit:
                        self.letExit = False
                        raise outofscope()
        if self.operation is not None:
            if self.operation == 'equ':
                if ctx.STRING() is not None:
                    print('nn',ctx.STRING().getText())
                    self.strs = 'String'
                    self.operation = ''

                elif ctx.FALSE() is not None:
                    print('nn False')
                    self.strs = 'Boolean'
                    self.operation = ''

                elif ctx.TRUE() is not None:
                    print('nn True')
                    self.strs = 'Boolean'
                    self.operation = ''
        
        if self.operation is not None:
            #print('Gamer',ctx.getText());
            if self.operation == 'sum':
                if ctx.ID() is not None:
                    if ctx.ID().getText() in self.methodDic.keys():
                        print(ctx.getText())
                elif ctx.INTEGER() is None:
                    print("check",ctx.getText())
                    self.operation = ''
                    self.badArith = True

    def enterMethodDecl2(self, ctx: coolParser.MethodDecl2Context):
        self.methodDic[ctx.ID().getText()] = ""
                

        self.MethDeclType = ctx.TYPE().getText()
        self.klassDic[self.klassName] += ctx.ID().getText() + ","
        self.methodDic[ctx.ID().getText()] += ctx.TYPE().getText() + ","
        self.methDeclY = True

    def exitMethodDecl2(self, ctx: coolParser.MethodDecl2Context):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()

    def enterMethodDecl(self, ctx: coolParser.MethodDeclContext):
        self.methodFormal[ctx.ID().getText()] = ""
        for x in ctx.formal():
            self.tempFormal.append(x.getText().split(':')[1])
            self.tempFormalID.append(x.getText().split(':')[0])
            self.methodFormal[ctx.ID().getText()] += x.getText() + '|'
        self.klassDic[self.klassName] += ctx.ID().getText() + ","
        self.methodDic[ctx.ID().getText()] = ""
        self.methodDic[ctx.ID().getText()] += ctx.TYPE().getText() + ","
        #DupFormals
        print("Duplicates?", self.tempFormalID, set(self.tempFormalID), self.tempFormal)
        if len(self.tempFormalID) != len(set(self.tempFormalID)):
                raise dupformals()

        #raise badargs1()---------------------------------------
        if ctx.ID().getText() in self.methodCalls.keys():
            print('OJO',len(ctx.formal()),len(self.methodCalls[ctx.ID().getText()].split(',')))
            if len(ctx.formal()) == len(self.methodCalls[ctx.ID().getText()].split(','))-1:
                for x in range(len(ctx.formal())):                    
                    if ctx.formal()[x].getText().split(':')[1] != self.methodCalls[ctx.ID().getText()].split(',')[x]:
                        raise badargs1()
    
    ##!!!
    def enterWhileLoop(self, ctx: coolParser.WhileLoopContext):
        if ctx.expr(0).getText() == self.tempFormalID:
            if self.formalCh != 'Int':
                raise badwhilecond()
    
    def enterMethod(self, ctx: coolParser.MethodContext):
        if(ctx.params):
            print('badmethodcallsitself',ctx.params[0].getText(),self.tempFormal)
        if self.tempFormal:
            if self.tempFormal[0] == "Int":
                if not ctx.params[0].getText().isnumeric():
                    raise badmethodcallsitself()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        print('let',ctx.TYPE().getText())
        self.letCall = ctx.TYPE().getText()
        self.letID = ctx.ID().getText()
        if (ctx.ID().getText() == 'self'):
            self.letSelf = True
        if ctx.expr() is not None:
            print('let2',ctx.expr().getText())
            if "new" in ctx.expr().getText():
                print('let3',self.klassInher.keys())
                if  ctx.expr().getText().split('new')[1] not in self.klassInher.keys():
                    if ctx.expr().getText().split('new')[1] != self.letCall:
                        raise letbadinit()
    
    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        if (self.letSelf):
            raise letself()

    #print("method formal", self.methodFormal)
    def exitMethodDecl(self, ctx: coolParser.MethodDeclContext):
        self.MethDeclType = ctx.TYPE().getText()
        self.tempFormal = []
        self.tempFormalID = [] 

    def printObj(self):
        print("***From Listener two, print obj_________________________________")
        print("FINAL klass Dic",            self.klassDic)
        print("FINAL method Dic",           self.methodDic)
        print("FINAL klass inher",          self.klassInher)
        print("FINAL klass Method Calls",   self.methodCalls)
        print("FINAL klass Method Formal",  self.methodFormal)
        print("INIT LAST",                  self.tempFormalID)
        print("***From Listener two, print obj_________________________________")


