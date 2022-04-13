from asyncio.windows_events import NULL
from types import NoneType
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

    def enterKlass(self, ctx:coolParser.KlassContext):
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
    
    def enterFeature(self, ctx: coolParser.FeatureContext):
        #print(ctx.formal()[0].getText())
        if ctx.ID().getText() == "self":
            self.anAttributeNamedSelf = True

    def exitFeature(self, ctx: coolParser.FeatureContext):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()

    def enterLet_decl(self, ctx: coolParser.Let_declContext):
        #print('let',ctx.ID().getText())
        if (ctx.ID().getText() == 'self'):
            self.letSelf = True
    
    def exitLet_decl(self, ctx: coolParser.Let_declContext):
        if (self.letSelf):
            raise letself()

    def enterExpr(self, ctx: coolParser.ExprContext):
        if (ctx.ID() is not None):
            print('exp',ctx.ID().getText())
            if (ctx.ID().getText() =='self'):
                self.selfAssignment = True
    
    def exitExpr(self, ctx: coolParser.ExprContext):
        if (self.selfAssignment):
            raise selfassignment()
    
    def enterFormal(self, ctx: coolParser.FormalContext):
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


   

    

