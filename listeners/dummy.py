from asyncio.windows_events import NULL
from types import NoneType

from pyparsing import empty
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class dummyListener(coolListener):

    def __init__(self):
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
        self.sum = False
        self.badArith = False
        #self.klassNo = 0
        #self.methodNo = 0
        #self.klass = [[]]
        #self.inherits = []
        #self.inCh = ''
        self.formalCh = ''
        self.badEqualityTest1 = False
        self.badEqualityTest2 = False


    def enterKlass(self, ctx:coolParser.KlassContext):
        #self.klassNo
        #self.klass[self.klassNo] = ctx.TYPE(0).getText()
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
            if ctx.TYPE(1).getText() == 'Bool':
                self.inheritsBool = True
            if ctx.TYPE(1).getText() == 'SELF_TYPE':
                self.inheritsSelfType = True
            if ctx.TYPE(1).getText() == 'String':
                self.inheritsString = True
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
        #self.klassNo+=1
        #self.methodNo = 0
    
    def enterFeature(self, ctx: coolParser.FeatureContext):
        #print(ctx.getText())
        if ctx.ID().getText() == "self":
            self.anAttributeNamedSelf = True
        #self.klass[self.klassNo][self.methodNo] = ctx.TYPE().getText()

    def exitFeature(self, ctx: coolParser.FeatureContext):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()
        #self.methodNo +=1
        

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        print('let',ctx.ID().getText())
        if (ctx.ID().getText() == 'self'):
            self.letSelf = True
    
    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        if (self.letSelf):
            raise letself()

    def enterExpr(self, ctx: coolParser.ExprContext): 
        #print("buenas",ctx.getText())
        if (ctx.ID() is not None):
            #print('exp',ctx.ID().getText())
            if (ctx.ID().getText() =='self'):
                self.selfAssignment = True
        if '+' in ctx.getText():
            self.sum = True
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
        self.formalCh = ctx.TYPE().getText()
        if (ctx.ID().getText()=='self'):
            self.selfInformalParameter = True
            print(ctx.ID().getText())
        if (ctx.TYPE().getText()=='SELF_TYPE'):
            self.selfTypeParameterPosition = True
    
    def exitFormal(self, ctx: coolParser.FormalContext):
        if(self.selfInformalParameter):
            raise selfinformalparameter()
        if(self.selfTypeParameterPosition):
            raise selftypeparameterposition()

    def enterPrimary(self, ctx: coolParser.PrimaryContext):
        print(ctx.getText())
        
        if self.sum:
            #print('Gamer',ctx.getText());
            if ctx.INTEGER() is None:
                self.sum = False
                self.badArith = True

                
    
    def exitPrimary(self, ctx: coolParser.PrimaryContext):
        if(self.badArith):
            raise badarith()


   

    

