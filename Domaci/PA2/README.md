# PA2 — Cool Parser (bison)

The second phase of the Cool compiler. It reads a Cool source file, parses it
with a **bison** grammar, builds an **abstract syntax tree (AST)** using the
tree package, and prints the tree. This is the input to PA3 (semantic analysis).

## The file you actually write
- **`cool.y`** — the bison grammar + semantic actions that build the AST. This
  is the graded deliverable. Everything else is supporting infrastructure.

## How it's wired (self-contained, macOS-friendly)
Stanford's original setup runs `lexer | parser` as two programs connected by a
pipe, relying on Linux reference binaries. Those don't run on Apple Silicon, so
here the **flex scanner feeds the bison parser directly** inside one executable:

```
cool.flex --(flex)--> lex.yy.cc  ┐
cool.y    --(bison)-> cool-parse.cc ├─(g++)─> parser ──> AST dump
parser-main.cc + tree package ----┘
```

- `cool.flex`     — the scanner (adapted from PA1) that returns tokens to bison
- `cool.y`        — the grammar (writes the AST)
- `parser-main.cc`— driver: opens the `.cl` file, calls `yyparse()`, dumps the AST
- `cool-tree.*`, `tree.*`, `stringtab.*`, `utilities.*`, `dumptype.cc` — the
  standard CS143 tree package / support code (do not edit)

## Build & run

### Terminal / VS Code
```bash
make            # bison + flex + g++  ->  ./parser
./parser good.cl   # parse a file, print its AST
make test          # build, then parse good.cl
make clean
```
In VS Code: **Cmd+Shift+B** to build, or run task "Run parser on good.cl".

### CodeBlocks
Open `cool_parser.cbp` and press **Build** (Ctrl-F9). A Terminal window opens
and runs the parser on `good.cl` and `bad.cl`. (Same mechanism as PA1 — the
build is driven by `run_build.sh`.)

## Test files
- **`good.cl`** — exercises every legal construct (classes, inheritance,
  methods, attributes, dispatch, static dispatch, let, case, if, while, blocks,
  arithmetic, comparisons, new, isvoid, not, neg, self).
- **`bad.cl`** — exercises parser error **recovery** at the four required
  points: class, feature, block expression, and let binding.

## Notes
- The AST dump shows `_no_type` for every expression — types are filled in later
  by PA3 (the semantic analyzer).
- Line numbers attached to nodes come from the lexer via bison locations; per the
  assignment, they need not match the reference compiler exactly.
