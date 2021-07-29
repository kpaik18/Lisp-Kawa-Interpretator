Lisp Dialect - Kawa Interpretator in Python

Lisp Core functional, which is Implemented:
  - Symbols: +, -, *, / (division operator results in float numbers)
  - apply (+, -, *, /)
  - List operations (car, cdr, cons, list, append, length)
  - eval
  - boolean operators
    - >, >=, =, <, <=, null?, list?
    - if, cond, and, or
  - map (takes function as an argument or lambda function)

Little difference from kawa language: Lists doesn't need quode before evaluation
    - Standard Kawa Syntax - '(1 2 3) -> (1 2 3)
    - Implemented Kawa Syntax - (1 2 3) -> (1 2 3)
    
For Testing
  - To use kawa terminal, run kawa.py in python terminal
  - For automated testing, use auto_tester.py
  - Test cases are read from TestFiles folder
  - Test cases can be manually added in simple_tests file
    - input$correct_output
      - correct_output (elem1 elem2 elem3) with single space between each element
  - function_tests() method checks function define methods
  - Test cases can be added function_tests file
