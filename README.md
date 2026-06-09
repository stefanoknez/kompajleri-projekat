# Programski prevodioci (Kompajleri)

Repo za domaće zadatke i materijale s predmeta **Programski prevodioci**,
treća godina, drugi semestar.

> **Napomena:** Ovaj repozitorijum je privatan.

---

## Struktura foldera

```
.
├── Domaci/          # Postavke domaćih zadataka (PDF)
│   ├── WA1.pdf      # Written Assignment 1 (Stanford CS143)
│   ├── WA2.pdf      # Written Assignment 2 (Stanford CS143)
│   ├── PA1.pdf      # Programming Assignment 1 – Lexer
│   ├── PA2.pdf      # Programming Assignment 2 – Parser
│   ├── PA3.pdf      # Programming Assignment 3 – Semantička analiza
│   ├── WA1/         # Moje rješenje za WA1
│   ├── WA2/         # Moje rješenje za WA2
│   ├── PA1/         # Moj kod za PA1 (lekser, Flex)
│   ├── PA2/         # Moj kod za PA2 (parser, Bison)
│   └── PA3/         # Moj kod za PA3 (semantička analiza)
│
├── vjezbe/          # Vježbe po temama
│   ├── lex-flex/    # Leksička analiza (Flex)
│   ├── bison/       # Sintaksna analiza (Bison)
│   ├── mips/        # Generisanje koda (MIPS)
│   └── automati/    # Konačni automati
│
├── teorija/         # Markdown bilješke o konceptima
│                    # (regex, DFA, CFG, FIRST/FOLLOW, ...)
│
└── kolokvijum/      # Priprema za kolokvijum
    ├── stari-zadaci/
    └── moja-rjesenja/
```

---

## Cool kompajler — tri faze (PA1, PA2, PA3)

Programski zadaci grade prednji dio (front-end) kompajlera za jezik **Cool**.
Svaka faza koristi izlaz prethodne:

```
izvorni.cl ──▶ [PA1 Lekser] ──▶ tokeni ──▶ [PA2 Parser] ──▶ AST ──▶ [PA3 Semantika] ──▶ AST sa tipovima
               (Flex)                      (Bison)                  (semant.cc)
```

- **PA1 – Lekser:** čita karaktere i grupiše ih u tokene (Flex).
- **PA2 – Parser:** od tokena gradi apstraktno sintaksno stablo / AST (Bison).
- **PA3 – Semantička analiza:** provjerava nasljeđivanje, opsege i tipove, i
  upisuje tip svakom čvoru u stablu.

Svaka faza je **samostalna** (jedan izvršni fajl) i radi na macOS-u — nisu
potrebni Stanfordovi Linux binarni fajlovi ni pipe-ovi.

---

## Kako pokrenuti projekat

Potrebno je imati **flex** i **bison** (na macu preko Homebrew-a:
`brew install flex bison`).

### 1) Terminal (make) — najjednostavnije

Uđi u folder zadatka i kucaj `make`:

```bash
# PA1 – lekser
cd Domaci/PA1
make
./lexer test.cl          # ispisuje tokene
make test                # build + pokretanje
make clean

# PA2 – parser
cd Domaci/PA2
make
./parser good.cl         # ispisuje AST
bash tests/run_tests.sh  # svi testovi

# PA3 – semantička analiza
cd Domaci/PA3
make
./semant good.cl         # ispisuje AST sa tipovima (ili greške)
bash tests/run_tests.sh  # svi testovi
```

Možeš pokrenuti bilo koji `.cl` fajl: `./lexer fajl.cl`, `./parser fajl.cl`,
`./semant fajl.cl`.

### 2) VS Code

Otvori folder zadatka (npr. `Domaci/PA3`) i pritisni **Cmd+Shift+B** da se
build-uje. Za pokretanje: **Cmd+Shift+P → Tasks: Run Task → "Run ... on good.cl"**.
Izlaz se vidi u ugrađenom terminalu.

### 3) CodeBlocks

Otvori projekat (`cool_lexer.cbp` / `cool_parser.cbp` / `cool_semant.cbp`) i
pritisni **Build (Ctrl-F9)**. Otvara se Terminal prozor i pokreće program na
test fajlovima. (Koristi se dugme **Build**, ne Run.)

---

## Brza provjera (good.cl vs bad.cl)

- **`good.cl`** — ispravan program; prolazi i ispisuje rezultat.
- **`bad.cl`** — namjerne greške; ispisuju se poruke sa brojem linije.
- Razlika PA2 i PA3: PA2 pokazuje `: _no_type` na svakom izrazu, a PA3 popuni
  prave tipove (`: Int`, `: Bool`, `: SELF_TYPE`, ...).
