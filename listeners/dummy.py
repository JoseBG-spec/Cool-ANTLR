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


    def enterKlass(self, ctx:coolParser.KlassContext):
        if ctx.TYPE(0).getText() in self.klassDic.keys():
            raise redefinedclass()
        self.klassName = ctx.TYPE(0).getText()
        self.klassDic[self.klassName] = ''
        
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
        
        print("Buenas3", self.klassDic[self.klassName])
        #print("Buenas4", self.klassDic.keys())
        #self.methodNo = 0


    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        print('let',ctx.TYPE().getText())
        self.letCall = ctx.TYPE().getText()
        self.letID = ctx.ID().getText()
        if (ctx.ID().getText() == 'self'):
            self.letSelf = True
    
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
        self.klassDic[self.klassName] += ctx.ID().getText() + ","
        self.MethDeclType = ctx.TYPE().getText()
        
             
    
    def exitMethodDecl(self, ctx: coolParser.MethodDeclContext):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()
        print('MethodDecl',ctx.TYPE().getText(),',',self.klassDic.keys(),',',self.predefined)
        if ctx.TYPE().getText() not in self.klassDic.keys() and ctx.TYPE().getText() not in self.predefined:
            raise returntypenoexist()
        self.MethDeclType = ctx.TYPE().getText()
        
    
    def enterMethodDecl2(self, ctx: coolParser.MethodDecl2Context):
        if ctx.ID().getText() == "self":
            self.anAttributeNamedSelf = True
        self.MethDeclType = ctx.TYPE().getText()
    
    def exitMethodDecl2(self, ctx: coolParser.MethodDecl2Context):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()

    def enterAssoc(self, ctx: coolParser.AssocContext):
        if (ctx.ID() is not None):
            #print('exp',ctx.ID().getText())
            if (ctx.ID().getText() =='self'):
                self.selfAssignment = True

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
        





   

    

