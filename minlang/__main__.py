import sys
import os
from minlang.lexer import Lexer
from minlang.parser import Parser
from minlang.interpreter import Interpreter

class MinLang:
    def __init__(self):
        self.interpreter = Interpreter()
        self.had_error = False

    def run_file(self, path: str):
        if not path.endswith('.gkg'):
            print(f"Error: File must have .gkg extension")
            sys.exit(74)
            
        try:
            with open(path, 'r') as file:
                source = file.read()
                self.run(source)
                if self.had_error:
                    sys.exit(65)
        except FileNotFoundError:
            print(f"Error: Could not open file '{path}'")
            sys.exit(74)

    def run_prompt(self):
        print("MinLang REPL (type 'exit' to quit)")
        while True:
            try:
                line = input("> ")
                if line.lower() == 'exit':
                    break
                self.run(line)
                self.had_error = False
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                print("\nExiting...")
                break

    def run(self, source: str):
        lexer = Lexer(source)
        tokens = lexer.scan_tokens()
        
        parser = Parser(tokens)
        statements = parser.parse()
        
        if self.had_error:
            return
        
        self.interpreter.interpret(statements)

def main():
    minlang = MinLang()
    if len(sys.argv) > 2:
        print("Usage: python -m minlang [script.gkg]")
        sys.exit(64)
    elif len(sys.argv) == 2:
        minlang.run_file(sys.argv[1])
    else:
        minlang.run_prompt()

if __name__ == "__main__":
    main() 