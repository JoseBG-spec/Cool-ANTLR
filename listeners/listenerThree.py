from asyncio.windows_events import NULL
from xmlrpc.client import Boolean

from pyparsing import empty
from util.exceptions import *
from antlr.coolListener import coolListener
from antlr.coolParser import coolParser

class listenerThree(coolListener):
    def __init__(self):
        self.predefined = ['Object','Int','String','Boolean','SELF_TYPE','IO','Bool']
        self.main                   = True
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