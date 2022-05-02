from asyncio.windows_events import NULL
from types import NoneType
from xmlrpc.client import Boolean

from pyparsing import empty
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class dummyListener(coolListener):

    def __init__(self):
        self.predefined = ['Object','Int','String','Boolean','SELF_TYPE']
        self.main = False
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
                else:
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
        
        print("Buenas3",self.klassName,"Classes:", self.klassDic[self.klassName])
        print("Buenas4",self.klassName,"Inherits:", self.klassInher[self.klassName])
        #print("Buenas4", self.klassDic.keys())
        #self.methodNo = 0


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
        

    def enterExpr(self, ctx: coolParser.ExprContext): 
        print("buenas",ctx.getText())
        
        
        #if 'in' in ctx.getText():
        #    self.inCh = ctx.let_decl().getText()
        #if self.inCh is not empty:
        #    print(self.inCh)
        #print('buenas2',ctx.primary().getText())
        #if '=' in ctx.getText():
        #    if 'false' in ctx.expr().getText():
        #        if self.formalCh == "Int":
        #            self.badEqualityTest1 = True
        #    if 'true' in ctx.expr(1).getText():
        #        if self.formalCh == "Int":
        #            self.badEqualityTest2 = True

            

    
    def exitExpr(self, ctx: coolParser.ExprContext):
        if (self.selfAssignment):
            raise selfassignment()
        #if self.badEqualityTest1:
            #raise badequalitytest()
    
    def enterFormal(self, ctx: coolParser.FormalContext):
        print('gg', ctx.ID().getText(),ctx.TYPE().getText())
        self.formalCh = ctx.TYPE().getText()
        self.formalID = ctx.ID().getText()
        if (ctx.ID().getText()=='self'):
            self.selfInformalParameter = True
            #print(ctx.ID().getText())
        if (ctx.TYPE().getText()=='SELF_TYPE'):
            self.selfTypeParameterPosition = True
    
    def exitFormal(self, ctx: coolParser.FormalContext):
        if(self.selfInformalParameter):
            raise selfinformalparameter()
        if(self.selfTypeParameterPosition):
            raise selftypeparameterposition()

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        if ctx.ID() is not None:
            print('Buenas8',ctx.ID().getText());
            if self.methDeclY:
                if ctx.ID().getText() == "self":
                    raise selfassignment()
                if ctx.ID().getText() not in self.klassDic[self.klassName].split(","):
                    raise attrbadinit()
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
                if ctx.INTEGER() is None:
                    self.operation = ''
                    self.badArith = True

                
    
    def exitPrimary(self, ctx: coolParser.PrimaryContext):
        if(self.badArith):
            raise badarith()
            
    
    def enterMethodCall(self, ctx: coolParser.MethodCallContext):
        self.methodCalls[ctx.ID().getText()] = ''
        for parms in ctx.params:
            if parms.getText() == "self":
                self.methodCalls[ctx.ID().getText()] += self.klassName + ','
            elif parms.getText().isnumeric():
                self.methodCalls[ctx.ID().getText()] += "Int" + ','
            else:
                self.methodCalls[ctx.ID().getText()] += parms.getText() + ','
        print("Method Call",self.methodCalls.keys(),self.methodCalls[ctx.ID().getText()])
        if self.letCall in self.klassDic.keys():
            if ctx.ID().getText() not in self.klassDic[self.letCall].split(","):
                self.badDispatch = True
        if self.formalCh == 'Int':
            if ctx.ID().getText() == "length":
                raise badwhilebody()
        

    def exitMethodCall(self, ctx: coolParser.MethodCallContext):
        if self.badDispatch:
            raise baddispatch()        
    
    def enterMethodDecl(self, ctx: coolParser.MethodDeclContext):
        print('EnterMethDecl',ctx.getText())
        #if self.klassInher[self.klassName] is not empty:
        #for methods in self.klassInher[self.klassName].split(',')[1:]:
        #OverridingMethod4
        print('EnterMethDeclMethsForm',self.methodFormal.keys())
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
        
        self.MethDeclType = ctx.TYPE().getText()        
        #DupFormals
        if len(self.tempFormalID) != len(set(self.tempFormalID)):
            print("Duplicates",len(self.tempFormalID), len(set(self.tempFormalID)))
            raise dupformals()
        #raise badargs1()---------------------------------------
        if ctx.ID().getText() in self.methodCalls.keys():
            print('OJO',len(ctx.formal()),len(self.methodCalls[ctx.ID().getText()].split(',')))
            if len(ctx.formal()) == len(self.methodCalls[ctx.ID().getText()].split(','))-1:
                for x in range(len(ctx.formal())):                    
                    if ctx.formal()[x].getText().split(':')[1] != self.methodCalls[ctx.ID().getText()].split(',')[x]:
                        raise badargs1()
                
        
             
    
    def exitMethodDecl(self, ctx: coolParser.MethodDeclContext):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()
        print('MethodDecl',ctx.TYPE().getText(),',',self.klassDic.keys(),',',self.predefined)
        if ctx.TYPE().getText() not in self.klassDic.keys() and ctx.TYPE().getText() not in self.predefined:
            raise returntypenoexist()
        self.MethDeclType = ctx.TYPE().getText()
        self.tempFormal = []
        self.tempFormalID = []

        
        
    
    def enterMethodDecl2(self, ctx: coolParser.MethodDecl2Context):
        print('Buenas7',ctx.ID().getText())
        self.methodDic[ctx.ID().getText()] = ""
        if self.klassInher[self.klassName] is not empty:
            for methods in self.klassInher[self.klassName].split(','):
                if methods != '':
                    if ctx.ID().getText() in self.klassDic[methods]:
                        raise attroverride()
        if ctx.ID().getText() == "self":
            self.anAttributeNamedSelf = True
        self.MethDeclType = ctx.TYPE().getText()
        self.klassDic[self.klassName] += ctx.ID().getText() + ","
        self.methodDic[ctx.ID().getText()] += ctx.TYPE().getText() + ","
        self.methDeclY = True
    
    def exitMethodDecl2(self, ctx: coolParser.MethodDecl2Context):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()
        

    def enterAssoc(self, ctx: coolParser.AssocContext):
        print('Assoc',ctx.getText(),self.methodDic.keys())
        if (ctx.ID() is not None):
            if (ctx.ID().getText() =='self'):
                self.selfAssignment = True
            if ctx.ID().getText() in self.methodDic.keys():
                raise assignnoconform()
                #if self.methodDic[ctx.ID().getText()] in self.klassInher.keys():
                 #   if self.klassInher[self.methodDic[ctx.ID().getText()]] == '':
                        
            

    def exitAssoc(self, ctx: coolParser.AssocContext):
        if (self.selfAssignment):
            raise selfassignment()

    def enterSum(self, ctx: coolParser.SumContext):
        self.operation = 'sum'
    
    def enterEqu(self, ctx: coolParser.EquContext):
        #print('bb',ctx.expr(1).getText())
        self.operation = 'equ'
        

    def exitEqu(self, ctx: coolParser.EquContext):
        if self.strs == 'String':
            if self.formalCh == "Int":
                raise badequalitytest()
        if self.strs == 'Boolean':
            if self.formalCh == "Int":
                raise badequalitytest2()
    
    #def enterCase(self, ctx: coolParser.CaseContext):
        #print('oo', )
        

    def exitCase(self, ctx: coolParser.CaseContext):
        print(self.caseSt.count(self.formalCh))
        if self.caseSt.count(self.formalCh) > 1:
                raise caseidenticalbranch()
        self.caseSt = []


    def enterCase_stat(self, ctx: coolParser.Case_statContext):
        self.caseSt.append(ctx.TYPE().getText())
    
    def exitLet(self, ctx: coolParser.LetContext):
        print('letExit')
        self.letExit = True
    
    def enterNewType(self, ctx: coolParser.NewTypeContext):
        if self.MethDeclType is not None:
            print('MethDeclType',self.MethDeclType)
            if self.MethDeclType == 'Int':
                if ctx.TYPE().getText() == 0 or ctx.TYPE().getText() == 1:
                    print('Ok')
            if self.MethDeclType == 'String':
                print('String')
            if self.MethDeclType == 'Object':
                print('Object')
            else:
                print('SELF',ctx.TYPE().getText(),self.MethDeclType)
                if ctx.TYPE().getText() != self.MethDeclType:
                    raise selftypebadreturn()

    def enterWhileLoop(self, ctx: coolParser.WhileLoopContext):
        if ctx.expr(0).getText() == self.formalID:
            if self.formalCh != 'Int':
                raise badwhilecond()
    
    def enterMethod(self, ctx: coolParser.MethodContext):
        print('Methodddddd',ctx.params[0].getText(),self.tempFormal)
        if self.tempFormal[0] == "Int":
            if not ctx.params[0].getText().isnumeric():
                raise badmethodcallsitself()
    
    def enterMethodCall2(self, ctx: coolParser.MethodCall2Context):
        print('enterMethodCall2',ctx.getText(),ctx.expr()[0].getText())
        if "new" in ctx.expr()[0].getText():
            if ctx.expr()[0].getText().split('new')[1].split(')')[0] not in self.klassInher[ctx.TYPE().getText()].split(','):
                raise trickyatdispatch2()
        else:
            if ctx.ID().getText() not in self.klassInher[self.klassName].split(','):
                raise badstaticdispatch()
                

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

        
        





   

    

