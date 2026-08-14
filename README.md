# Compilers (Programski prevodioci)

Repository for homework assignments and course materials from the **Compilers** course,
third year, second semester.

> **Note:** This repository is private.

---

## Folder structure

```
.
├── Domaci/          # Homework assignment PDFs and solutions
│   ├── WA1.pdf      # Written Assignment 1 (Stanford CS143)
│   ├── WA2.pdf      # Written Assignment 2 (Stanford CS143)
│   ├── PA1.pdf      # Programming Assignment 1 – Lexer
│   ├── PA2.pdf      # Programming Assignment 2 – Parser
│   ├── PA3.pdf      # Programming Assignment 3 – Semantic Analysis
│   ├── WA1/         # My solution for WA1
│   ├── WA2/         # My solution for WA2
│   ├── PA1/         # My code for PA1 (lexer, Flex)
│   ├── PA2/         # My code for PA2 (parser, Bison)
│   └── PA3/         # My code for PA3 (semantic analysis)
│
├── vjezbe/          # Practice exercises by topic
│   ├── lex-flex/    # Lexical analysis (Flex)
│   ├── bison/       # Syntax analysis (Bison)
│   ├── mips/        # Code generation (MIPS)
│   └── automati/    # Finite automata
│
├── teorija/         # Markdown notes on concepts
│                    # (regex, DFA, CFG, FIRST/FOLLOW, ...)
│
└── kolokvijum/      # Exam preparation
    ├── stari-zadaci/
    └── moja-rjesenja/
```

---

## Cool compiler — three phases (PA1, PA2, PA3)

The programming assignments build the front-end of a compiler for the **Cool** language.
Each phase feeds into the next:

```
source.cl ──▶ [PA1 Lexer] ──▶ tokens ──▶ [PA2 Parser] ──▶ AST ──▶ [PA3 Semantics] ──▶ typed AST
              (Flex)                      (Bison)                   (semant.cc)
```

- **PA1 – Lexer:** reads characters and groups them into tokens (Flex).
- **PA2 – Parser:** builds an abstract syntax tree / AST from tokens (Bison).
- **PA3 – Semantic analysis:** checks inheritance, scopes, and types, and
  annotates every AST node with its type.

Each phase is **self-contained** (a single executable) and runs on macOS — no
Stanford Linux binaries or pipes required.

---

## How to run

Requires **flex** and **bison** (on macOS via Homebrew: `brew install flex bison`).

### 1) Terminal (make) — simplest

Enter the assignment folder and run `make`:

```bash
# PA1 – lexer
cd Domaci/PA1
make
./lexer test.cl          # prints tokens
make test                # build + run
make clean

# PA2 – parser
cd Domaci/PA2
make
./parser good.cl         # prints AST
bash tests/run_tests.sh  # all tests

# PA3 – semantic analysis
cd Domaci/PA3
make
./semant good.cl         # prints typed AST (or errors)
bash tests/run_tests.sh  # all tests
```

Any `.cl` file can be passed directly: `./lexer file.cl`, `./parser file.cl`,
`./semant file.cl`.

### 2) VS Code

Open the assignment folder (e.g. `Domaci/PA3`) and press **Cmd+Shift+B** to build.
To run: **Cmd+Shift+P → Tasks: Run Task → "Run ... on good.cl"**.
Output appears in the integrated terminal.

### 3) CodeBlocks

Open the project (`cool_lexer.cbp` / `cool_parser.cbp` / `cool_semant.cbp`) and
press **Build (Ctrl-F9)**. A Terminal window opens and runs the program on the test
files. (Use the **Build** button, not Run.)

---

## Quick sanity check (good.cl vs bad.cl)

- **`good.cl`** — a valid program; passes and prints the result.
- **`bad.cl`** — intentional errors; error messages with line numbers are printed.
- Difference between PA2 and PA3: PA2 shows `: _no_type` on every expression,
  while PA3 fills in the real types (`: Int`, `: Bool`, `: SELF_TYPE`, ...).
