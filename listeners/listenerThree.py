from asyncio.windows_events import NULL
from xmlrpc.client import Boolean

from pyparsing import empty
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class listenerThree(coolListener):
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

    ##!!!
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
                ##!!!
                raise signaturechange()