import _ast
import re, sys, os
import ast


def file_opener():
    args = sys.argv
    file_path = args[1]
    # file_path = 'test.py'

    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
            line_checker(code, file_path)
        return

    py_files = []
    for filename in os.listdir(file_path):
        if filename.endswith('.py'):
            py_files.append(filename)
    py_files = sorted(py_files)
    for filename in py_files:
        with open(file_path + '/' + filename, 'r') as f:
            code = f.read()
            line_checker(code, file_path + '/' + filename)


def line_checker(code, file_path):
    faults = []
    faulty_var = []
    blank_lines_counter = 0
    lines = code.splitlines()
    for line in enumerate(lines, start=1):
        if len(line[1]) > 79:
            faults.append(f"Line {line[0]}: S001 Too long")

        if line[1].startswith(' ') and not bool(re.match(r"^(\s{4})*\S", str(line[1]))):
            faults.append(f"Line {line[0]}: S002 Indentation is not a multiple of four")

        if line[1].endswith(';') and "#" not in str(line[1]) or bool(re.search(r";\s*#", line[1])):
            faults.append(f"Line {line[0]}: S003 Unnecessary semicolon after a statement")

        if "#" in line[1] and not str(line[1]).startswith('#'):
            splited_line = str(line).split("#")
            if not splited_line[0].endswith(' ' * 2):
                faults.append(f"Line {line[0]}: S004 Less than two spaces before inline comments")

        # S005 TODO found
        if re.search(r"#\s*(todo)+", str(line[1]).lower()):
            faults.append(f"Line {line[0]}: S005 TODO found")

        # S006 More than two blank lines preceding a code line
        if line[1] == '':
            blank_lines_counter += 1
        if line[1] != '':
            if blank_lines_counter > 2:
                faults.append(f"Line {line[0]}: S006 More than two blank lines preceding a code line")
            blank_lines_counter = 0

        # S007 too many spaces after 'class' or 'def'
        if re.search(r"\s*class\s*\w*", line[1]):
            splitted = line[1].split('class')
            if not re.match(r"^\s{1}\w", splitted[1]):
                faults.append(f"Line {line[0]}: S007 Too many spaces after 'class'")
        if re.search(r"\s*def\s*\w*(.*)", line[1]):
            splitted = line[1].split('def')
            if not re.match(r"^\s{1}\w", splitted[1]):
                faults.append(f"Line {line[0]}: S007 Too many spaces after 'def'")

        # S008 Class name class_name should be written in CamelCase
        if re.search(r"\s*class\s*\w*", line[1]):
            splitted = line[1].split(' ')
            if not re.match(r"^[A-Z]\w*", splitted[-1]):
                class_name = ''.join([x for x in splitted[-1] if x != ":"])
                faults.append(f"Line {line[0]}: S008 Class name '{class_name}' should be written in CamelCase")

        # S009 snake_style
        if re.search(r"\s*def\s*\w*(.*)", line[1]):
            splitted = line[1].split('def')
            splitted = [x.strip() for x in splitted]
            if not re.match(r"^[a-z._]+[a-z,_]*", splitted[-1]):
                func_name = ''.join([x for x in splitted[-1] if x not in ":()"] )
                faults.append(f"Line {line[0]}: S009 Function name '{func_name}' should be written in snake_case.")

    # S010 Argument name arg_name should be written in snake_case
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for x in node.args.args:
                if not re.match(r"^[a-z._]+[a-z,_]*", x.arg):
                    faults.append(f"Line {node.lineno}: S010 Argument name '{x.arg}' should be written in snake_case.")
        if isinstance(node, ast.Name):
            if not re.match(r"^[a-z._]+[a-z,_]*", node.id):
                if node.id not in faulty_var:
                    faulty_var.append(node.id)
                    faults.append(f"Line {node.lineno}: S011 Variable name '{node.id}' should be written in snake_case.")
        if isinstance(node, ast.FunctionDef):
            for x in node.args.defaults:
                if isinstance(x, _ast.List):
                    faults.append(f"Line {node.lineno}: S012 Default argument value is mutable.")

    a = [print(f"{file_path}: {x}") for x in faults]


def main():
    file_opener()


if __name__ == '__main__':
    main()
