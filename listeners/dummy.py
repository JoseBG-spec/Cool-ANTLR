from asyncio.windows_events import NULL
from xmlrpc.client import Boolean

from pyparsing import empty
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class dummyListener(coolListener):

    def __init__(self, 
    predefined,
    main,
    redefineInt,
    anAttributeNamedSelf,
    inheritsBool,
    inheritsSelfType,
    inheritsString,
    letSelf,
    redefinedObject,
    selfAssignment,
    selfInformalParameter,
    selfTypeParameterPosition,
    selfTypeRedeclared,
    operation,
    badArith,

    klassDic,
    methodDic,
    klassInher,
    methodCalls,
    methodFormal,

    klassName,
    letCall,
    letID,
    letExit,
    strs,
    MethDeclType,
    caseSt,
    assocID,

    formalCh,
    badDispatch,
    badEqualityTest1,
    badEqualityTest2,
    missClass,
    methDeclY,
    tempFormal,
    tempFormalID
    ):

        self.predefined = ['Object','Int','String','Boolean','SELF_TYPE','IO','Bool']
        self.main                   = main
        self.redefineInt            = redefineInt
        self.anAttributeNamedSelf   = anAttributeNamedSelf
        self.inheritsBool           = inheritsBool
        self.inheritsSelfType       = inheritsSelfType
        self.inheritsString         = inheritsString
        self.letSelf                = letSelf
        self.redefinedObject        = redefinedObject
        self.selfAssignment         = selfAssignment
        self.selfInformalParameter  = selfInformalParameter
        self.selfTypeParameterPosition  = selfTypeParameterPosition
        self.selfTypeRedeclared     = selfTypeRedeclared
        self.operation              = operation
        self.badArith               = badArith

        self.klassDic               = klassDic
        self.methodDic              = methodDic
        self.klassInher             = klassInher
        self.methodCalls            = methodCalls
        self.methodFormal           = methodFormal

        self.klassName              = klassName
        self.letCall                = letCall
        self.letID                  = letID
        self.letExit                = letExit
        self.strs                   = strs
        self.MethDeclType           = MethDeclType
        self.caseSt                 = caseSt
        self.assocID                = assocID
        

        self.formalCh               = formalCh
        self.badDispatch            = badDispatch
        self.badEqualityTest1       = badEqualityTest1
        self.badEqualityTest2       = badEqualityTest2
        self.missClass              = missClass
        self.methDeclY              = methDeclY
        self.tempFormal             = tempFormal
        self.tempFormalID           = tempFormalID

        print("--INIT DUMMY_________________________________")
        print("INIT klass Dic",            self.klassDic)
        print("INIT method Dic",           self.methodDic)
        print("INIT klass inher",          self.klassInher)
        print("INIT klass Method Calls",   self.methodCalls)
        print("INIT klass Method Formal",  self.methodFormal)
        print("INIT LAST",                 self.tempFormalID)
        print("--INIT DUMMY_________________________________")

    """
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
    """
    def enterKlass(self, ctx:coolParser.KlassContext):     
        if ctx.TYPE(0).getText() == 'Main':
            self.main = True
        if ctx.TYPE(0).getText() == 'Int':
            self.redefineInt = True
        if ctx.TYPE(0).getText() == 'Object':
            self.redefinedObject = True
        if ctx.TYPE(0).getText() == 'SELF_TYPE':
            self.selfTypeRedeclared = True

        if (ctx.TYPE(1) is not None):
            if ctx.TYPE(1).getText() not in self.klassDic.keys():
                if ctx.TYPE(1).getText() == 'Bool':
                    self.inheritsBool = True
                if ctx.TYPE(1).getText() == 'SELF_TYPE':
                    self.inheritsSelfType = True
                if ctx.TYPE(1).getText() == 'String':
                    self.inheritsString = True
                elif(ctx.TYPE(1).getText() not in self.predefined):
                    self.missClass = True



        #Esto rompe todos los tests
        #if ctx.TYPE(0).getText() in self.klassDic.keys():
            #raise redefinedclass()

    def exitKlass(self, ctx:coolParser.KlassContext):
        if (not self.main):
            raise nomain()
        if (self.redefineInt):
            raise badredefineint()
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
        
        #print("Class Name",self.klassName,"Classes:", self.klassDic[self.klassName])
        #print("Class Name",self.klassName,"Inherits:", self.klassInher[self.klassName])
        #print("DicMethod",self.methodDic)
        self.methodDic = {}


        

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

        print(ctx.ID().getText())

        if (ctx.ID().getText()=='self'):
            self.selfInformalParameter = True
        if (ctx.TYPE().getText()=='SELF_TYPE'):
            self.selfTypeParameterPosition = True
    
    def exitFormal(self, ctx: coolParser.FormalContext):
        if(self.selfInformalParameter):
            raise selfinformalparameter()
        if(self.selfTypeParameterPosition):
            raise selftypeparameterposition()


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

    def exitPrimary(self, ctx: coolParser.PrimaryContext):
        if(self.badArith):
            raise badarith()


    def enterMethodCall(self, ctx: coolParser.MethodCallContext):
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

    def enterMethodCall2(self, ctx: coolParser.MethodCall2Context):
        print('enterMethodCall2',ctx.getText(),ctx.expr()[0].getText())
        if "new" in ctx.expr()[0].getText():
            if ctx.expr()[0].getText().split('new')[1].split(')')[0] not in self.klassInher[ctx.TYPE().getText()].split(','):
                raise trickyatdispatch2()
        else:
            print("badstaticdispatch?", ctx.ID().getText(), self.klassInher[self.klassName].split(','))
            if ctx.ID().getText() not in self.klassInher[self.klassName].split(','):
                raise badstaticdispatch()

  

    def exitMethodDecl(self, ctx: coolParser.MethodDeclContext):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()
        print('MethodDecl',ctx.TYPE().getText(),',',self.klassDic.keys(),',',self.predefined)
        if ctx.TYPE().getText() not in self.klassDic.keys() and ctx.TYPE().getText() not in self.predefined:
            raise returntypenoexist()
        
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
    
    def exitMethodDecl2(self, ctx: coolParser.MethodDecl2Context):
        if (self.anAttributeNamedSelf):
            raise anattributenamedself()     
    
    def enterAssoc(self, ctx: coolParser.AssocContext):
        print('Assoc',ctx.getText(),self.methodDic.keys())
        if (ctx.ID() is not None):
            self.assocID = ctx.ID().getText()
            #if (ctx.ID().getText() =='self'):
                #self.selfAssignment = True
            #if ctx.ID().getText() in self.methodDic.keys():
            #    print(self.methodDic[ctx.ID().getText()])
            #    if(ctx.expr().getText().isnumeric() and self.methodDic[ctx.ID().getText()] != "Int,"):
            #        raise assignnoconform()
            #    elif(not ctx.expr().getText().isnumeric()):
            #        if()

                
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
                print('New String')

            if self.MethDeclType == 'Object':
                print('New Object',self.MethDeclType,ctx.TYPE().getText(),self.assocID,self.methodDic.keys())
                if(self.assocID in self.methodDic.keys()):
                    if(self.methodDic[self.assocID].split(',')[0] != ctx.TYPE().getText()):
                        raise assignnoconform()

            if self.MethDeclType == 'SELF_TYPE':
                raise selftypebadreturn()

            elif ctx.TYPE().getText() != self.MethDeclType:
                print('SELF', ctx.TYPE().getText(), self.MethDeclType, self.klassDic.keys())
                # and ctx.TYPE().getText() not in self.klassDic.keys() and ctx.TYPE().getText() not in
                print(ctx.TYPE().getText(),self.MethDeclType,ctx.getText())
                #raise selftypebadreturn()

    def enterWhileLoop(self, ctx: coolParser.WhileLoopContext):
        if ctx.expr(0).getText() == self.tempFormalID:
            if self.formalCh != 'Int':
                raise badwhilecond()



    def printObj(self):
        print("***From Dummy, print obj_________________________________")
        print("FINAL klass Dic",            self.klassDic)
        print("FINAL method Dic",           self.methodDic)
        print("FINAL klass inher",          self.klassInher)
        print("FINAL klass Method Calls",   self.methodCalls)
        print("FINAL klass Method Formal",  self.methodFormal)
        print("INIT LAST",                  self.tempFormalID)
        print("***From Dummy, print obj_________________________________")


