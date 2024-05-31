import re
import tkinter as tk
from tkinter import ttk

# Diccionarios de tokens y sus categorías
operators = {
    '=': 'Operador de Asignación', '+': 'Operador de Suma', '-': 'Operador de Resta',
    '/': 'Operador de División', '*': 'Operador de Multiplicación', '<': 'Operador Menor que',
    '>': 'Operador Mayor que', '==': 'Operador de Igualdad', '!=': 'Operador de Desigualdad',
    '<=': 'Operador Menor o Igual', '>=': 'Operador Mayor o Igual'
}
reservwords = {
    'if': 'Condición', 'then': 'Entonces', 'else': 'Sino', 'case': 'Caso',
    'switch': 'Alterna', 'while': 'Mientras', 'for': 'Para', 'int': 'Entero',
    'float': 'Flotante', 'char': 'Carácter', 'long': 'Entero Largo', 'return': 'Retornar'
}
punctuation_symbol = {
    ':': 'Dos Puntos', ';': 'Punto y Coma', '.': 'Punto', ',': 'Coma', '(': 'Paréntesis Izquierdo',
    ')': 'Paréntesis Derecho', '{': 'Llave Izquierda', '}': 'Llave Derecha'
}
variables = {chr(i): 'Variable' for i in range(ord('a'), ord('z') + 1)}

# Función para el análisis léxico
def lexico(code):
    tokens = []
    line_count = 0

    program = code.split("\n")
    for line in program:
        if line.strip() == "":
            continue
        line_count += 1
        line_tokens = re.findall(r'\b\w+\b|[=+\-*/<>!;:.,(){}]', line)

        for token in line_tokens:
            if token in operators:
                tokens.append((line_count, 'Operador', token))
            elif token in reservwords:
                tokens.append((line_count, 'Palabra Reservada', token))
            elif token in punctuation_symbol:
                tokens.append((line_count, 'Símbolo de Puntuación', token))
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token):
                tokens.append((line_count, 'Identificador', token))
            elif re.match(r'^\d+$', token):
                tokens.append((line_count, 'Número Entero', token))
            elif re.match(r'^\d+\.\d+$', token):
                tokens.append((line_count, 'Número Flotante', token))
            else:
                tokens.append((line_count, 'No se encontró patrón', token))

    return tokens

# Función para el análisis sintáctico
def sintactico(tokens):
    errors = []
    index = 0

    # Función para analizar declaraciones
    def parse_declaration():
        nonlocal index
        line, token_type, token = tokens[index]

        if token_type == 'Palabra Reservada' and token in {'int', 'float', 'char', 'long'}:
            index += 1
            if index < len(tokens) and tokens[index][1] == 'Identificador':
                index += 1
                if index < len(tokens) and tokens[index][2] == '=':
                    index += 1
                    if index < len(tokens) and (tokens[index][1] == 'Número Entero' or tokens[index][1] == 'Número Flotante'):
                        index += 1
                        if index < len(tokens) and tokens[index][2] == ';':
                            index += 1
                        else:
                            errors.append((line, 'Error: Se esperaba un ";" al final de la declaración'))
                    else:
                        errors.append((line, 'Error: Se esperaba un valor numérico después de "="'))
                elif index < len(tokens) and tokens[index][2] == ';':
                    index += 1
                else:
                    errors.append((line, 'Error: Se esperaba un "=" o ";" después del nombre de la variable'))
            else:
                errors.append((line, 'Error: Se esperaba un nombre de variable después del tipo de dato'))

    # Función para analizar declaraciones "if"
    def parse_if_statement():
        nonlocal index
        line, token_type, token = tokens[index]
        if token == 'if':
            index += 1
            if index < len(tokens) and tokens[index][2] == '(':
                index += 1
                parse_expression()
                if index < len(tokens) and tokens[index][2] == ')':
                    index += 1
                    parse_block()
                    if index < len(tokens) and tokens[index][2] == 'else':
                        index += 1
                        parse_block()
                else:
                    errors.append((line, 'Error: Se esperaba un ")" después de la condición'))
            else:
                errors.append((line, 'Error: Se esperaba un "(" después de "if"'))

    # Función para analizar declaraciones "while"
    def parse_while_statement():
        nonlocal index
        line, token_type, token = tokens[index]
        if token == 'while':
            index += 1
            if index < len(tokens) and tokens[index][2] == '(':
                index += 1
                parse_expression()
                if index < len(tokens) and tokens[index][2] == ')':
                    index += 1
                    parse_block()
                else:
                    errors.append((line, 'Error: Se esperaba un ")" después de la condición'))
            else:
                errors.append((line, 'Error: Se esperaba un "(" después de "while"'))

    # Función para analizar declaraciones "for"
    def parse_for_statement():
        nonlocal index
        line, token_type, token = tokens[index]
        if token == 'for':
            index += 1
            if index < len(tokens) and tokens[index][2] == '(':
                index += 1
                parse_declaration()
                parse_expression()
                if index < len(tokens) and tokens[index][2] == ';':
                    index += 1
                    parse_expression()
                    if index < len(tokens) and tokens[index][2] == ')':
                        index += 1
                        parse_block()
                    else:
                        errors.append((line, 'Error: Se esperaba un ")" después de la condición'))
                else:
                    errors.append((line, 'Error: Se esperaba un ";" después de la condición'))
            else:
                errors.append((line, 'Error: Se esperaba un "(" después de "for"'))

    # Función para analizar expresiones
    def parse_expression():
        nonlocal index
        if index < len(tokens):
            current_line = tokens[index][0]
            current_token = tokens[index][2]
            prev_token_type = tokens[index - 1][1] if index > 0 else None
            if prev_token_type == 'Operador' and current_token in operators:
                errors.append((current_line, f'Error: No se permiten dos operadores "{tokens[index - 1][2]}{current_token}" seguidos'))
                index += 1
                return
            if current_token in operators:
                index += 1
                parse_expression()
            elif tokens[index][1] in {'Identificador', 'Número Entero', 'Número Flotante'}:
                index += 1
                if index < len(tokens) and tokens[index][1] == 'Operador':
                    index += 1
                    parse_expression()

    # Función para analizar bloques de código
    def parse_block():
        nonlocal index
        if index < len(tokens) and tokens[index][2] == '{':
            index += 1
            while index < len(tokens) and tokens[index][2] != '}':
                parse_statement()
            if index < len(tokens) and tokens[index][2] == '}':
                index += 1
            else:
                errors.append((tokens[index][0], 'Error: Se esperaba una "}" al final del bloque'))
        else:
            errors.append((tokens[index][0], 'Error: Se esperaba una "{" al inicio del bloque'))

    # Función para analizar declaraciones
    def parse_statement():
        nonlocal index
        if index < len(tokens):
            line, token_type, token = tokens[index]
            if token in {'int', 'float', 'char', 'long'}:
                parse_declaration()
            elif token == 'if':
                parse_if_statement()
            elif token == 'while':
                parse_while_statement()
            elif token == 'for':
                parse_for_statement()
            else:
                parse_expression()
                if index < len(tokens) and tokens[index][2] == ';':
                    index += 1
                else:
                    errors.append((line, 'Error: Se esperaba un ";" al final de la expresión'))

    # Analizar todas las declaraciones en el código
    while index < len(tokens):
        parse_statement()

    return errors

# Actualizar la tabla léxica
def update_lexical_table(code, table):
    table.delete(*table.get_children())
    code = code.strip()
    tokens = lexico(code)
    for token in tokens:
        table.insert('', tk.END, values=token)
    return tokens

# Actualizar la tabla de errores sintácticos
def update_syntax_table(tokens, table):
    table.delete(*table.get_children())
    errors = sintactico(tokens)
    if errors:
        for error in errors:
            table.insert('', tk.END, values=error)
    else:
        table.insert('', tk.END, values=(1, 'Sin errores sintácticos'))

# Crear la interfaz gráfica
def create_gui():
    app = tk.Tk()
    app.title("Analizador Léxico y Sintáctico")
    app.geometry('1200x700')
    app.configure(bg='#860e4e')

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#dedede", fieldbackground="#dedede", foreground="black", font=('Century Gothic', 12))

    title_label = tk.Label(app, text="Analizador Léxico y Sintáctico", font=('Century Gothic', 24), bg='#860e4e', fg='white')
    title_label.pack(pady=20)

    text_frame = tk.Frame(app, bg='#860e4e')
    text_frame.pack(pady=5)

    input_label = tk.Label(text_frame, text='Expresión:', font=('Century Gothic', 14), bg='#860e4e', fg='white')
    input_label.pack()

    text_input = tk.Text(text_frame, width=80, height=10, font=('Century Gothic', 12))
    text_input.pack()

    # Insertar el texto especificado
    text_input.insert(tk.END, "int = 4\nif x = 5\ny == 4")

    # Crear un marco contenedor común
    results_frame = tk.Frame(app, bg='#860e4e')
    results_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Análisis Léxico
    lexical_frame = tk.Frame(results_frame, bg='#860e4e')
    lexical_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    lexical_label = tk.Label(lexical_frame, text='Resultado del Análisis Léxico:', font=('Century Gothic', 14), bg='#860e4e', fg='white')
    lexical_label.pack(pady=5)

    lexical_table_frame = tk.Frame(lexical_frame, bg='#dedede')
    lexical_table_frame.pack(fill=tk.BOTH, expand=True)

    columns = ('Línea', 'Tipo', 'Token')
    token_table = ttk.Treeview(lexical_table_frame, columns=columns, show='headings', height=6)
    token_table.heading('Línea', text='Línea')
    token_table.column('Línea', width=5)
    token_table.heading('Tipo', text='Tipo')
    token_table.column('Tipo', width=150)
    token_table.heading('Token', text='Token')
    token_table.column('Token', width=200)

    token_table.pack(fill=tk.BOTH, expand=True)

    # Análisis Sintáctico
    syntax_frame = tk.Frame(results_frame, bg='#860e4e')
    syntax_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    syntax_label = tk.Label(syntax_frame, text='Resultado del Análisis Sintáctico:', font=('Century Gothic', 14), bg='#860e4e', fg='white')
    syntax_label.pack(pady=5)

    syntax_table_frame = tk.Frame(syntax_frame, bg='#dedede')
    syntax_table_frame.pack(fill=tk.BOTH, expand=True)

    syntax_columns = ('Línea', 'Descripción')
    syntax_table = ttk.Treeview(syntax_table_frame, columns=syntax_columns, show='headings', height=6)
    syntax_table.heading('Línea', text='Línea')
    syntax_table.column('Línea', width=5)
    syntax_table.heading('Descripción', text='Descripción')
    syntax_table.column('Descripción', width=300)

    syntax_table.pack(fill=tk.BOTH, expand=True)

    analyze_button = tk.Button(app, text='Analizar', font=('Century Gothic', 14), bg='#ff5f89', fg='white', command=lambda: analyze_code(text_input, token_table, syntax_table))
    analyze_button.pack(pady=10)

    app.mainloop()

# Función que realiza el análisis de código al presionar el botón
def analyze_code(text_widget, token_table, syntax_table):
    code = text_widget.get("1.0", tk.END)
    tokens = update_lexical_table(code, token_table)
    update_syntax_table(tokens, syntax_table)

# Llamar a la función de prueba después de crear la GUI
create_gui()