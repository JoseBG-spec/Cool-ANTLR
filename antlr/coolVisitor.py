# Generated from f:\pepot\Documents\8vo Semestre\CoolProject\Cool-ANTLR\antlr\cool.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .coolParser import coolParser
else:
    from coolParser import coolParser

# This class defines a complete generic visitor for a parse tree produced by coolParser.

class coolVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by coolParser#program.
    def visitProgram(self, ctx:coolParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#klass.
    def visitKlass(self, ctx:coolParser.KlassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#methodDecl.
    def visitMethodDecl(self, ctx:coolParser.MethodDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#methodDecl2.
    def visitMethodDecl2(self, ctx:coolParser.MethodDecl2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#formal.
    def visitFormal(self, ctx:coolParser.FormalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#greaterEqu.
    def visitGreaterEqu(self, ctx:coolParser.GreaterEquContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#newType.
    def visitNewType(self, ctx:coolParser.NewTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#rest.
    def visitRest(self, ctx:coolParser.RestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#whileLoop.
    def visitWhileLoop(self, ctx:coolParser.WhileLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#mult.
    def visitMult(self, ctx:coolParser.MultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#method.
    def visitMethod(self, ctx:coolParser.MethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#ifThenElse.
    def visitIfThenElse(self, ctx:coolParser.IfThenElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#Equ.
    def visitEqu(self, ctx:coolParser.EquContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#sum.
    def visitSum(self, ctx:coolParser.SumContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#isVoidExp.
    def visitIsVoidExp(self, ctx:coolParser.IsVoidExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#div.
    def visitDiv(self, ctx:coolParser.DivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#not.
    def visitNot(self, ctx:coolParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#primaryExp.
    def visitPrimaryExp(self, ctx:coolParser.PrimaryExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#assoc.
    def visitAssoc(self, ctx:coolParser.AssocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#let.
    def visitLet(self, ctx:coolParser.LetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#exp2.
    def visitExp2(self, ctx:coolParser.Exp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#exp.
    def visitExp(self, ctx:coolParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#greater.
    def visitGreater(self, ctx:coolParser.GreaterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#case.
    def visitCase(self, ctx:coolParser.CaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#methodCall.
    def visitMethodCall(self, ctx:coolParser.MethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#methodCall2.
    def visitMethodCall2(self, ctx:coolParser.MethodCall2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#case_stat.
    def visitCase_stat(self, ctx:coolParser.Case_statContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#let_decl.
    def visitLet_decl(self, ctx:coolParser.Let_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by coolParser#primary.
    def visitPrimary(self, ctx:coolParser.PrimaryContext):
        return self.visitChildren(ctx)



del coolParser