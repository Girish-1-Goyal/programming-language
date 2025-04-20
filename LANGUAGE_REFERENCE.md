# MinLang Language Reference

## Table of Contents
1. [Basic Syntax](#basic-syntax)
2. [Data Types](#data-types)
3. [Control Flow](#control-flow)
4. [Functions](#functions)
5. [Classes](#classes)
6. [Pattern Matching](#pattern-matching)
7. [Pipes](#pipes)
8. [Error Handling](#error-handling)
9. [Comments](#comments)
10. [File Extension](#file-extension)

## Basic Syntax

### Statement Terminator
```minlang
# All statements end with @
@x = 10 @
```

### Variable Declaration
```minlang
# Variables are declared with @
@x = 10
@name = "MinLang"

# Mutable variables require mut keyword
mut @counter = 0
```

## Data Types

### Numbers
```minlang
@integer = 42
@float = 3.14
@hex = 0xFF
@binary = 0b1010
```

### Strings
```minlang
@str = 'Hello, World!'
@raw = r'Raw string \n not escaped'
@template = f'Hello {name}!'
```

### Booleans
```minlang
@yes = yes
@no = no
```

### Null
```minlang
@empty = null
```

### Lists
```minlang
@empty_list = []
@numbers = [1, 2, 3]
@nested = [[1, 2], [3, 4]]
```

### Maps
```minlang
@empty_map = {}
@person = {
    name: 'Alice'
    age: 25
    is_student: yes
}
```

### Optional Types
```minlang
@maybe_name: str? = null
@maybe_age: num? = 25
```

## Control Flow

### If-Then-Otherwise
```minlang
if x > 10 then
    print 'Greater'
otherwise if x < 5 then
    print 'Less'
otherwise
    print 'Equal'
end
```

### Loops

#### While Loop
```minlang
while x > 0 do
    print x
    x = x - 1
end
```

#### For Loop
```minlang
# Range-based loop
for i in 1..10 do
    print i
end

# List-based loop
for item in [1, 2, 3] do
    print item
end

# Map-based loop
for key value in {a: 1, b: 2} do
    print key + ': ' + value
end
```

## Functions

### Function Definition
```minlang
# Basic function
fn add a b
    return a + b
end

# Function with type hints
fn greet name: str -> str
    return 'Hello, ' + name
end

# Function with guards
fn process x
    guard x > 0 then
        return 'Positive'
    guard x < 0 then
        return 'Negative'
    otherwise
        return 'Zero'
    end
end
```

### Function Types
```minlang
# Void function
fn print_hello
    print 'Hello'
end

# Number function
fn square x: num -> num
    return x * x
end

# String function
fn get_greeting name: str -> str
    return 'Hello, ' + name
end

# Boolean function
fn is_even n: num -> bool
    return n % 2 == 0
end
```

### Function Overloading
```minlang
fn add a: num b: num -> num
    return a + b
end

fn add a: str b: str -> str
    return a + b
end
```

## Classes

### Class Definition
```minlang
class Person
    # Constructor
    fn new name: str age: num
        @name = name
        @age = age
    end

    # Method
    fn greet -> str
        return 'Hello, my name is ' + @name
    end

    # Property
    fn is_adult -> bool
        return @age >= 18
    end
end
```

## Pattern Matching

### Basic Pattern Matching
```minlang
fn process data
    match data
        case [x, y] then
            return x + y
        case {name: n, age: a} then
            return 'Name: ' + n + ', Age: ' + a
        case null then
            return 'No data'
    end
end
```

### Pattern Matching with Guards
```minlang
fn process data
    match data
        case [x, y] when x > y then
            return 'First is greater'
        case [x, y] when x < y then
            return 'Second is greater'
        case [x, y] then
            return 'Equal'
    end
end
```

## Pipes

### Basic Pipes
```minlang
@result = 10 |> square |> add 5 |> to_str
```

### Pipes with Multiple Arguments
```minlang
@result = [1, 2, 3] |> map square |> filter is_even |> sum
```

## Error Handling

### Try-Catch
```minlang
try
    # code that might throw an error
catch error
    # handle the error
    print 'Error: ' + error
end
```

### Pattern Matching in Error Handling
```minlang
try
    # code that might throw an error
catch
    case DivisionByZero then
        print 'Cannot divide by zero'
    case InvalidInput then
        print 'Invalid input provided'
    case error then
        print 'Unknown error: ' + error
end
```

## Comments

```minlang
# Single line comment

#*
Multi-line
comment
*#

#**
 * Documentation comment
 * @param x First number
 * @param y Second number
 * @return Sum of x and y
 *#
fn add x y
    return x + y
end
```

## File Extension

All MinLang source files use the `.gkg` extension:
- `program.gkg`
- `module.gkg`
- `script.gkg`

## Best Practices

1. **Immutability**: Use immutable variables by default, only use `mut` when necessary
2. **Type Safety**: Use type hints for function parameters and return values
3. **Pattern Matching**: Prefer pattern matching over if-else chains
4. **Pipes**: Use pipes for function composition when it improves readability
5. **Error Handling**: Always handle errors appropriately using try-catch
6. **Documentation**: Document public functions and classes with documentation comments 