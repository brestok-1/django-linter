from pathlib import Path

from pylint import epylint as lint

BASE_DIR = Path(__file__).resolve().parent.parent


def check_file_errors(file_path):
    (pylint_stdout, pylint_stderr) = lint.py_run(f"{file_path} --disable=import-error,missing-module-docstring,missing-function-docstring,missing-class-docstring",
                                                 return_std=True)

    output = pylint_stdout.getvalue()
    return output


file_path = 'test_celery_utils.py'
errors = check_file_errors(file_path)
print(errors)

import pycodestyle

# import subprocess
#
#
# def check_file_errors(file_path):
#     result = subprocess.run(['mypy', file_path], capture_output=True, text=True)
#     output = result.stdout
#     return output
#
#
# file_path = 'main.py'
# errors = check_file_errors(file_path)
# print(errors)

# import pyflakes.api
#
#
# def check_file_syntax_errors(file_path):
#     with open(file_path, 'r') as file:
#         tree = pyflakes.api.check(file.read(), file_path)
#         errors = pyflakes.api.Messages(tree)
#         output = '\n'.join(str(error) for error in errors)
#     return output
#
#
# file_path = 'main.py'
# syntax_errors = check_file_syntax_errors(file_path)
# print(syntax_errors)


# def check_python_file(file_path):
#     style_guide = pycodestyle.StyleGuide()
#     result = style_guide.check_files([file_path])
#     if result.total_errors == 0:
#         print("No errors found in the file.")
#     else:
#         print(f"Found {result.total_errors} error(s) in the file.")
#
# check_python_file("main.py")


# import pycodestyle
#
#
# def check_code_conformance(file_path, config_path):
#     style_guide = pycodestyle.StyleGuide(config_file=config_path)
#     result = style_guide.check_files([file_path])
#     if result.total_errors == 0:
#         print("Code conforms to the style guide.")
#         return []
#     else:
#         print(f"Code does not conform to the style guide. Found {result.total_errors} error(s).")
#
#
# check_code_conformance("main.py", '.pycodestyle')
