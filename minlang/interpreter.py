from typing import Dict, List, Optional, Any
from minlang.lexer import Token, TokenType
from minlang.parser import *

class Environment:
    def __init__(self, enclosing: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token) -> Any:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

    def get_at(self, distance: int, name: str) -> Any:
        return self.ancestor(distance).values[name]

    def assign_at(self, distance: int, name: Token, value: Any):
        self.ancestor(distance).values[name.lexeme] = value

    def ancestor(self, distance: int) -> 'Environment':
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

class MinLangClass:
    def __init__(self, name: str, superclass: Optional['MinLangClass'], methods: Dict[str, 'MinLangFunction']):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def find_method(self, name: str) -> Optional['MinLangFunction']:
        if name in self.methods:
            return self.methods[name]
        
        if self.superclass is not None:
            return self.superclass.find_method(name)
        
        return None

    def __str__(self):
        return self.name

class MinLangInstance:
    def __init__(self, klass: MinLangClass):
        self.klass = klass
        self.fields: Dict[str, Any] = {}

    def get(self, name: Token) -> Any:
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]
        
        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)
        
        raise RuntimeError(f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.klass.name} instance"

class MinLangFunction:
    def __init__(self, declaration: Function, closure: Environment, is_initializer: bool = False):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def bind(self, instance: MinLangInstance) -> 'MinLangFunction':
        environment = Environment(self.closure)
        environment.define("this", instance)
        return MinLangFunction(self.declaration, environment, self.is_initializer)

    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value
        
        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

class ReturnException(Exception):
    def __init__(self, value: Any):
        self.value = value

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals: Dict[Expr, int] = {}

        # Define native functions
        self.globals.define("clock", ClockFunction())
        self.globals.define("print", PrintFunction())

    def interpret(self, statements: List[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            print(f"Runtime error: {error}")

    def execute(self, stmt: Stmt):
        if isinstance(stmt, Expression):
            self.evaluate(stmt.expression)
        elif isinstance(stmt, Print):
            value = self.evaluate(stmt.expression)
            print(self.stringify(value))
        elif isinstance(stmt, Var):
            value = None
            if stmt.initializer is not None:
                value = self.evaluate(stmt.initializer)
            self.environment.define(stmt.name.lexeme, value)
        elif isinstance(stmt, Block):
            self.execute_block(stmt.statements, Environment(self.environment))
        elif isinstance(stmt, If):
            if self.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.then_branch)
            elif stmt.else_branch is not None:
                self.execute(stmt.else_branch)
        elif isinstance(stmt, While):
            while self.is_truthy(self.evaluate(stmt.condition)):
                self.execute(stmt.body)
        elif isinstance(stmt, Function):
            function = MinLangFunction(stmt, self.environment)
            self.environment.define(stmt.name.lexeme, function)
        elif isinstance(stmt, Return):
            value = None
            if stmt.value is not None:
                value = self.evaluate(stmt.value)
            raise ReturnException(value)
        elif isinstance(stmt, Class):
            superclass = None
            if stmt.superclass is not None:
                superclass = self.evaluate(stmt.superclass)
                if not isinstance(superclass, MinLangClass):
                    raise RuntimeError("Superclass must be a class.")
            
            self.environment.define(stmt.name.lexeme, None)
            
            if stmt.superclass is not None:
                self.environment = Environment(self.environment)
                self.environment.define("super", superclass)
            
            methods = {}
            for method in stmt.methods:
                function = MinLangFunction(method, self.environment, method.name.lexeme == "init")
                methods[method.name.lexeme] = function
            
            klass = MinLangClass(stmt.name.lexeme, superclass, methods)
            
            if stmt.superclass is not None:
                self.environment = self.environment.enclosing
            
            self.environment.assign(stmt.name, klass)

    def execute_block(self, statements: List[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def evaluate(self, expr: Expr) -> Any:
        if isinstance(expr, Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)
            
            if expr.operator.type == TokenType.PLUS:
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                raise RuntimeError("Operands must be two numbers or two strings.")
            elif expr.operator.type == TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            elif expr.operator.type == TokenType.MULTIPLY:
                self.check_number_operands(expr.operator, left, right)
                return left * right
            elif expr.operator.type == TokenType.DIVIDE:
                self.check_number_operands(expr.operator, left, right)
                return left / right
            elif expr.operator.type == TokenType.EQUALS:
                return self.is_equal(left, right)
            elif expr.operator.type == TokenType.NOT_EQUALS:
                return not self.is_equal(left, right)
            elif expr.operator.type == TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            elif expr.operator.type == TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            elif expr.operator.type == TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            elif expr.operator.type == TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
        elif isinstance(expr, Unary):
            right = self.evaluate(expr.right)
            
            if expr.operator.type == TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            elif expr.operator.type == TokenType.BANG:
                return not self.is_truthy(right)
        elif isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Grouping):
            return self.evaluate(expr.expression)
        elif isinstance(expr, Variable):
            return self.look_up_variable(expr.name, expr)
        elif isinstance(expr, Call):
            callee = self.evaluate(expr.callee)
            
            arguments = []
            for argument in expr.arguments:
                arguments.append(self.evaluate(argument))
            
            if not isinstance(callee, MinLangFunction):
                raise RuntimeError("Can only call functions and classes.")
            
            if len(arguments) != callee.arity():
                raise RuntimeError(f"Expected {callee.arity()} arguments but got {len(arguments)}.")
            
            return callee.call(self, arguments)
        elif isinstance(expr, Get):
            obj = self.evaluate(expr.obj)
            if isinstance(obj, MinLangInstance):
                return obj.get(expr.name)
            raise RuntimeError("Only instances have properties.")
        elif isinstance(expr, Set):
            obj = self.evaluate(expr.obj)
            if not isinstance(obj, MinLangInstance):
                raise RuntimeError("Only instances have fields.")
            value = self.evaluate(expr.value)
            obj.set(expr.name, value)
            return value

    def look_up_variable(self, name: Token, expr: Expr) -> Any:
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def is_truthy(self, obj: Any) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def is_equal(self, a: Any, b: Any) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def check_number_operand(self, operator: Token, operand: Any):
        if isinstance(operand, (int, float)):
            return
        raise RuntimeError(f"Operand must be a number.")

    def check_number_operands(self, operator: Token, left: Any, right: Any):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeError(f"Operands must be numbers.")

    def stringify(self, obj: Any) -> str:
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(obj)

class ClockFunction:
    def __init__(self):
        pass

    def call(self, interpreter: Interpreter, arguments: List[Any]) -> float:
        import time
        return time.time()

    def arity(self) -> int:
        return 0

    def __str__(self):
        return "<native fn>"

class PrintFunction:
    def __init__(self):
        pass

    def call(self, interpreter: Interpreter, arguments: List[Any]) -> None:
        print(*arguments)

    def arity(self) -> int:
        return -1  # Variable number of arguments

    def __str__(self):
        return "<native fn>" 