
    .data
    .align  2
    .globl  class_nameTab
    .globl  Main_protObj
    .globl  Int_protObj
    .globl  String_protObj
    .globl  bool_const0
    .globl  bool_const1
    .globl  _int_tag
    .globl  _bool_tag
    .globl  _string_tag
_int_tag:
    .word   2
_bool_tag:
    .word   3
_string_tag:
    .word   4
    .globl  _MemMgr_INITIALIZER
_MemMgr_INITIALIZER:
    .word NoGC Init
    .globl _MemMgr_COLLECTOR
_MemMgr_COLLECTOR:
    .word _NoGC_Collect
    .globl _MemMgr_TEST
_MemMgr_TEST:
    .word   0
    .word   -1
	.word	-1
str_const0:
	.word	4
	.word	5
	.word	String_dispTab
	.word	Hello
	.byte	0	
	.align	2
	.word	-1
int_const0:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	5
	.word	-1
bool_const0:
	.word	3
	.word	4
	.word	Bool_dispTab
	.word	0
	.word	-1
bool_const1:
	.word	3
	.word	4
	.word	Bool_dispTab
	.word	1
 $$$$$$$$$$$$$$$$$$$$$$$$$$
    .text
main: 

    li	    $v0     10                  # 10 para terminar la emulación
    syscall
