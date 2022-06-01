from string import Template

tpl_start_text = """
    .text
main: 
"""

tpl_start_data = """
    .data"""

tpl_var_decl = Template("""
$varname: .word 0
""")

tpl_end = """
    li	    $v0     10                  # 10 para terminar la emulación
    syscall
"""

tpl_immediate = Template("""
    li      $$a0    $immediate
""")

tpl_suma = Template("""
$left
    sw      $$a0    0($$sp)             # Salvar en el stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)             # Recuperar resultado parcial anterior
    addiu   $$sp    $$sp        4       # Pop
    add     $$a0    $$a0        $$t1
""")

tpl_resta = Template("""
$left
    sw      $$a0    0($$sp)             # Salvar en el stack
    addiu   $$sp    $$sp        -4
$right
    lw      $$t1    4($$sp)             # Recuperar resultado parcial anterior
    addiu   $$sp    $$sp        4       # Pop
    sub     $$a0    $$t1        $$a0
""")

tpl_print_int = Template("""
$prev
	li	    $$v0     1              # para imprimir enteros
	syscall			                # imprimir
""")

tpl_print_str = Template("""
$prev
	li	    $$v0     4              # para imprimir cadenas
	syscall			                # imprimir
""")

tpl_var = Template("""
    lw      $$a0        $name       # Usar variable
""")

tpl_asignacion = Template("""
$prev
    sw      $$a0        $name       # Guardar valor
""")

tpl_string_const_decl = Template("""
$name: .asciiz $content
""")

tpl_string_const = Template("""
    la      $$a0        $name
""")

tpl_if = Template("""
$prev
    beqz    $$a0        label$n
$stmt_true
label$n:
""")

tpl_if_else = Template("""
$prev
    beqz      $$a0        label$n
$stmt_true
    j       labelexit$n
label$n:
$stmt_false
labelexit$n:
""")

tpl_while = Template("""
label_test$n:
$test
    beqz        $$a0        label_exit$n
$stmt
    j           label_test$n
label_exit$n:
""")

tpl_procedure = Template("""
$name:
    sw      $$ra    0($$sp)             # Salvar en el stack el RA
    addiu   $$sp    $$sp        -4
    sw      $$fp    0($$sp)             # Ahora el fp
    addiu   $$sp    $$sp        -4
    addiu   $$fp    $$fp        8
$code
    lw      $$fp    4($$sp)
    addiu   $$sp    $$sp        4
    lw      $$ra    4($$sp)
    addiu   $$sp    $$sp        4
    jr      $$ra
""")

tpl_push_arg = """
    sw      $$a0    0($$sp)             # Salvar en el stack
    addiu   $$sp    $$sp        -4
"""

tpl_call = Template("""
$push_arguments
    jal     $name
""")

#DEFAULT VALUES AT THE START OF FILE

# GLOBAL TAGS
tpl_global_tags_start = Template("""
    .align  2
    .globl  class_nameTab$prototype_tags
    .globl  bool_const0
    .globl  bool_const1$class_tags""")

tpl_global_class_tag = Template(("""
    .globl  _${name}_tag"""))  # lowercase

# CLASS TAGS
tpl_class_tag = Template("""
_${name}_tag:
    .word   $n"""
)

# PROTOTYPE
tpl_prototype_tag = Template(("""
    .globl  ${name}_protObj"""))


#MemMgr

tpl_MemMgr = """
    .globl  _MemMgr_INITIALIZER
_MemMgr_INITIALIZER:
    .word NoGC Init
    .globl _MemMgr_COLLECTOR
_MemMgr_COLLECTOR:
    .word _NoGC_Collect
    .globl _MemMgr_TEST
_MemMgr_TEST:
    .word   0
    .word   -1"""

#MemMgr

tpl_mOne = """
    .word   -1"""

tpl_bool= """
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
	.word	1"""

tpl_str_obj= Template(("""
	.word	-1
str_const${const_no}:
	.word	4
	.word	5
	.word	String_dispTab
	.word	${str_value}
	.byte	0	
	.align	2"""))

tpl_int_obj= Template(("""
	.word	-1
int_const${int_no}:
	.word	2
	.word	4
	.word	Int_dispTab
	.word	${int_value}"""))

tpl_str_disTab= """
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
	.word	1"""