# Mini Python

In this post we're implementing Python in Python. There will be a tokenizer,
a parser, an interpreter, a compiler, and a virtual machine.

The post is still in progress. At the moment, only the tokenizer is available.
It uses a indentation stack to deal with python identation rule. For example
the code

```python
def f():
    print(1)


print('done')
```

will produce the following list of tokens:

```
[   t: DEF, line: 1, column: 1,
    t: f, line: 1, column: 5,
    t: LPAREN, line: 1, column: 6,
    t: RPAREN, line: 1, column: 7,
    t: COLON, line: 1, column: 8,
    t: NEWLINE, line: 1, column: 9,
    t: INDENT, line: 2, column: 5,
    t: PRINT, line: 2, column: 6,
    t: LPAREN, line: 2, column: 11,
    t: 1, line: 2, column: 12,
    t: RPAREN, line: 2, column: 13,
    t: NEWLINE, line: 2, column: 14,
    t: NEWLINE, line: 3, column: 1,
    t: NEWLINE, line: 4, column: 1,
    t: DEDENT, line: 5, column: 0,
    t: PRINT, line: 5, column: 1,
    t: LPAREN, line: 5, column: 6,
    t: done, line: 5, column: 7,
    t: RPAREN, line: 5, column: 8,
    t: NEWLINE, line: 5, column: 9]
```
