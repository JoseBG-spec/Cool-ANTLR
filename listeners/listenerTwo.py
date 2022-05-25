from asyncio.windows_events import NULL
from xmlrpc.client import Boolean

from pyparsing import empty
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class listenerTwo(coolListener):

    def __str__(self):
        return "foo"

    def __init__(self):
        self.predefined = ['Object','Int','String','Boolean','SELF_TYPE','IO','Bool']
        self.klassName  =             ""
        self.klassDic = {}
        self.methodDic              = {}
        self.klassInher             = {}
        self.methodCalls            = {}
        self.methodFormal           = {}
        self.tempFormal             = []
        self.tempFormalID           = []

    def enterKlass(self, ctx:coolParser.KlassContext):
        if ctx.TYPE(0).getText() in self.klassDic.keys():
            raise redefinedclass()
        self.klassName = ctx.TYPE(0).getText()
        self.klassDic[self.klassName] = ""
        self.klassInher[self.klassName]=''
        
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

    def enterMethodDecl2(self, ctx: coolParser.MethodDecl2Context):
        self.methodDic[ctx.ID().getText()] = ""
        self.MethDeclType = ctx.TYPE().getText()
        self.klassDic[self.klassName] += ctx.ID().getText() + ","
        self.methodDic[ctx.ID().getText()] += ctx.TYPE().getText() + ","
        self.methDeclY = True

    def enterMethodDecl(self, ctx: coolParser.MethodDeclContext):
        self.methodFormal[ctx.ID().getText()] = ""
        for x in ctx.formal():
            self.methodFormal[ctx.ID().getText()] += x.getText() + '|'
        self.klassDic[self.klassName] += ctx.ID().getText() + ","
        self.methodDic[ctx.ID().getText()] = ""
        self.methodDic[ctx.ID().getText()] += ctx.TYPE().getText() + ","

    

    def printObj(self):
        print("***From Listener two, print obj")
        print("FINAL klass Dic",            self.klassDic)
        print("FINAL method Dic",           self.methodDic)
        print("FINAL klass inher",          self.klassInher)
        print("FINAL klass Method Calls",   self.methodCalls)
        print("FINAL klass Method Formal",  self.methodFormal)
        print("INIT tempFormalID",                  self.tempFormalID)
        print("INIT tempFormal",                  self.tempFormal)
        print("***From Listener two, print obj")
