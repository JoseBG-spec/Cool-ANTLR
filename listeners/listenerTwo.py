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
            

    
    def enterMethodCall(self, ctx: coolParser.MethodCallContext):
        self.methodCalls[ctx.ID().getText()] = ''
        for parms in ctx.params:
            if parms.getText() == "self":
                self.methodCalls[ctx.ID().getText()] += self.klassName + ','
            elif parms.getText().isnumeric():
                self.methodCalls[ctx.ID().getText()] += "Int" + ','
            else:
                self.methodCalls[ctx.ID().getText()] += parms.getText() + ','

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


        #print("method formal", self.methodFormal)
    def exitMethodDecl(self, ctx: coolParser.MethodDeclContext):
        self.MethDeclType = ctx.TYPE().getText()
        self.tempFormal = []
        self.tempFormalID = [] 
    
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
        print('Buenas7',ctx.ID().getText())
        self.methodDic[ctx.ID().getText()] = ""
        if self.klassInher[self.klassName] is not empty:
            for methods in self.klassInher[self.klassName].split(','):
                if methods != '' and methods not in self.predefined:
                    print(ctx.ID().getText(),methods)
                    if ctx.ID().getText() in self.klassDic[methods]:
                        raise attroverride()
        if ctx.ID().getText() == "self":
            self.anAttributeNamedSelf = True
        elif(ctx.expr() is not None):
            if ctx.expr().getText() not in self.klassDic[self.klassName].split(",") and "new" not in ctx.expr().getText() and len(ctx.expr().getText()) != 0 and '""' not in ctx.expr().getText():
                print(ctx.expr().getText(),self.klassDic[self.klassName].split(","),len(ctx.expr().getText()),'""')
                if(ctx.expr().getText() == "self"):
                    self.selfAssignment = True
                elif(ctx.expr().getText() == "true"):
                    print("true")
                elif(not ctx.expr().getText().isnumeric()):
                    raise attrbadinit()
                

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
    
    def enterMethod(self, ctx: coolParser.MethodContext):
        if(ctx.params):
            print('Methodddddd',ctx.params[0].getText(),self.tempFormal)
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

    def enterIfThenElse(self, ctx: coolParser.IfThenElseContext):
        print("enterIfThenElse",ctx.expr()[1].getText())
        for expr in ctx.expr()[1:]:
            print('ThenElse',expr.getText(), self.methodDic.keys())
            if expr.getText() in self.methodDic.keys():
                if self.methodDic[expr.getText()][0] in self.klassInher.keys():
                    if self.MethDeclType != "Object":
                        if self.MethDeclType not in self.klassInher[self.methodDic[expr.getText()][0]]:
                            raise lubtest()
            else:
                print('NopeIF')
    
    def printObj(self):
        print("***From Listener two, print obj_________________________________")
        print("FINAL klass Dic",            self.klassDic)
        print("FINAL method Dic",           self.methodDic)
        print("FINAL klass inher",          self.klassInher)
        print("FINAL klass Method Calls",   self.methodCalls)
        print("FINAL klass Method Formal",  self.methodFormal)
        print("INIT LAST",                  self.tempFormalID)
        print("***From Listener two, print obj_________________________________")


