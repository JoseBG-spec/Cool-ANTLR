
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
	.word	8
	.word	String_dispTab
	.word	Int_cons1
	.ascii	"Object"
	.byte	0	
	.align	2
	.word	-1
str_const1:
	.word	4
	.word	8
	.word	String_dispTab
	.word	Int_cons2
	.ascii	"IO"
	.byte	0	
	.align	2
	.word	-1
str_const2:
	.word	4
	.word	8
	.word	String_dispTab
	.word	Int_cons3
	.ascii	"Int"
	.byte	0	
	.align	2
	.word	-1
str_const3:
	.word	4
	.word	8
	.word	String_dispTab
	.word	Int_cons4
	.ascii	"String"
	.byte	0	
	.align	2
	.word	-1
str_const4:
	.word	4
	.word	8
	.word	String_dispTab
	.word	Int_cons5
	.ascii	"Boolean"
	.byte	0	
	.align	2
	.word	-1
str_const5:
	.word	4
	.word	8
	.word	String_dispTab
	.word	Int_cons6
	.ascii	""test""
	.byte	0	
	.align	2
	.word	-1
int_const0:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	5
	.word	-1
int_const1:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	6
	.word	-1
int_const2:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	2
	.word	-1
int_const3:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	3
	.word	-1
int_const4:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	6
	.word	-1
int_const5:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	7
	.word	-1
int_const6:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	6
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
class_nameTab:
    .word	str_const4
    .word	str_const5
    .word	str_const6
    .word	str_const7
    .word	str_const8
    .word	str_const9
class_objTab:
    .word	str_const4
Object_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
IO_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	IO.out_string
	.word	IO.out_int
	.word	IO.in_string
	.word	IO.in_int
Int_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
Bool_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
String_dispTab:
	.word	Object.abort
	.word	Object.type_name
	.word	Object.copy
	.word	String.length
	.word	String.concat
	.word	String.substr
obj_protObj:
	.word	0 
	.word	3 
	.word	0 
	.word	0
Object_protObj:
	.word	0 
	.word	3 
	.word	Object_dispTab 
	.word	-1 
IO_protObj:
	.word	1 
	.word	3 
	.word	IO_dispTab 
	.word	-1 
Int_protObj:
	.word	2 
	.word	4 
	.word	Int_dispTab 
	.word	0 
	.word	-1 
Bool_protObj:
	.word	3 
	.word	4 
	.word	Bool_dispTab 
	.word	0
	.word	-1 
String_protObj:
	.word	4 
	.word	5 
	.word	String_dispTab 
	.word	int_const1 
	.word	0 
	.word	-1 
Main_protObj:
	.word	5 
	.word	5 
	.word	Main_dispTab 
	.word	int_const1 
	.word	str_const10 
	.globl	heap_start 
heap_start:
	.word	0 
	.text	 
	.globl	Main_init 
	.globl	Int_init 
	.globl	String_init 
	.globl	Bool_init 
	.globl	Main.main 
 $$$$$$$$$$$$$$$$$$$$$$$$$$
    .text
main: 

    li	    $v0     10                  # 10 para terminar la emulación
    syscall
