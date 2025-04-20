# MinLang

A minimal, modern interpreted language with unique syntax and powerful features.

## Features

- **Modern Syntax**: Clean, readable syntax with unique features
- **Type Safety**: Optional types and type hints
- **Functional Features**: Pattern matching, pipes, and guards
- **Immutable by Default**: Variables are immutable unless explicitly marked as mutable
- **Object-Oriented**: Classes with methods and properties
- **Error Handling**: Try-catch blocks with pattern matching
- **Standard Library**: Built-in functions for common operations
- **REPL**: Interactive shell for quick testing
- **File Execution**: Run MinLang scripts with `.gkg` extension

## Installation

```bash
pip install minlang
```

## Usage

### REPL (Interactive Shell)

```bash
minlang
```

### Run a Script

```bash
minlang script.gkg
```

## Language Features

### Basic Syntax

```minlang
# Variables are declared with @
@x = 10
@name = "MinLang"

# Functions use fn
fn greet name
    return 'Hello, ' + name
end

# Classes use indentation
class Person
    fn new name
        @name = name
    end

    fn greet
        return 'Hello, my name is ' + @name
    end
end
```

### Control Flow

```minlang
# If-Then-Otherwise
if x > 10 then
    print 'Greater'
otherwise
    print 'Less or equal'
end

# While Loop
while x > 0 do
    print x
    x = x - 1
end

# For Loop
for i in 1..10 do
    print i
end
```

### Pattern Matching

```minlang
fn process data
    match data
        case [x, y] then
            return x + y
        case {name: n} then
            return 'Hello ' + n
    end
end
```

### Pipes

```minlang
@result = 10 |> square |> add 5 |> to_str
```

## Examples

### Hello World

```minlang
print 'Hello, World!'
```

### Fibonacci Sequence

```minlang
fn fib n
    if n <= 1 then
        return n
    otherwise
        return fib(n - 1) + fib(n - 2)
    end
end

for i in 0..10 do
    print fib(i)
end
```

### Class Example

```minlang
class Counter
    fn new
        @count = 0
    end

    fn increment
        @count = @count + 1
    end

    fn get_count
        return @count
    end
end

@counter = Counter.new
counter.increment
print counter.get_count
```

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 