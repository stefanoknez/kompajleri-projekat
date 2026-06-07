# PA3 — Cool Semantic Analyzer

The third phase of the Cool compiler. It takes the AST produced by the parser
(PA2) and enforces Cool's **static semantics**: it builds the inheritance graph,
checks it is well formed, manages scopes, type-checks every expression, and
annotates the AST with the inferred types.

## The file you actually write
- **`semant.cc`** — the semantic analyzer (the graded deliverable).
- `semant.h` — its header.
- `cool-tree.h` / `cool-tree.handcode.h` — extended with the `semant()` /
  `checkType()` hooks the analyzer implements.

Everything else is the standard CS143 tree package / support code.

## What it checks (Cool Reference Manual)
1. **Inheritance graph** — classes not multiply defined; parents exist; no
   inheriting from `Int`/`Bool`/`String`/`SELF_TYPE`; no cycles.
2. **Program shape** — a `Main` class containing a `main()` method.
3. **Scoping** — attributes, method formals, `let` bindings and `case` branches,
   via a `SymbolTable` object environment; `self` / `SELF_TYPE` handled specially.
4. **Type checking** — every expression against the Cool typing rules
   (conformance, `LCA`/join for `if`/`case`, dispatch argument/return types,
   arithmetic/comparison operand types, overriding-method signature matching,
   etc.), assigning each node its type.

## How it's wired (self-contained, macOS-friendly)
Stanford's original pipes three programs (`lexer | parser | semant`) using Linux
reference binaries. Those don't run on Apple Silicon, so all three phases are
linked into **one executable**:

```
cool.flex --(flex)--> lex.yy.cc  ┐
cool.y    --(bison)-> cool-parse  ├─(g++)─> semant ──> type-annotated AST
semant.cc + tree package + driver ┘
```

The driver (`semant-main.cc`): lex+parse the file → `ast_root->semant()` →
`ast_root->dump_with_types()`.

## Build & run

### Terminal / VS Code
```bash
make               # bison + flex + g++  ->  ./semant
./semant good.cl   # analyze a file; prints the typed AST (or errors)
make test          # build, then analyze good.cl
make clean
```
In VS Code: **Cmd+Shift+B** to build, or run task "Run semant on good.cl".

### CodeBlocks
Open `cool_semant.cbp` and press **Build** (Ctrl-F9). A Terminal window opens and
runs the analyzer on `good.cl` and `bad.cl`. (Same mechanism as PA1/PA2.)

## Tests
- **`good.cl`** — a valid program (inheritance, SELF_TYPE, dispatch chains, let,
  case, if, while, arithmetic, overriding). Prints a fully type-annotated AST.
- **`bad.cl`** — a single file packed with ~12 distinct type errors, all reported
  with line numbers.
- **`tests/`** — focused error cases (inheritance cycle, undefined/illegal parent,
  missing `Main`, missing `main()`, class redefinition, SELF_TYPE misuse) plus a
  runner: `bash tests/run_tests.sh`.

Verified: all standalone Cool example programs from the distribution pass; every
error case is detected. The output format matches the reference (it uses
Stanford's verbatim `dumptype.cc`).

## Note on the type-annotated output
After analysis, the AST dump shows real types (`: Int`, `: Bool`, `: SELF_TYPE`,
…) on every expression — compare with PA2, which showed `_no_type` everywhere.
