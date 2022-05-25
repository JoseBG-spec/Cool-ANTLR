from string import Template

tpl_start_text = """
    .text
main: 
"""

tpl_start_data = """
    .data
"""

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
