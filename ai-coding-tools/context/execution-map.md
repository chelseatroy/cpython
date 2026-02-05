# CPython Execution Path Map

This document traces 5 key execution paths through the CPython interpreter, showing how source code flows from entry points through parsing, compilation, and execution.

## Entry Points

| Emoji | Entry Point | Description |
|-------|-------------|-------------|
| 🔵 | `python script.py` | File execution path through parser and compiler |
| 🟢 | `python` (no args) | Interactive REPL loop with prompt handling |
| 🟠 | `import module` | Import system via importlib bootstrap |
| 🔴 | `func()` | Function call dispatch and frame creation |
| 🟣 | `"hello".upper()` | Built-in method lookup and C implementation |

## ASCII Diagram

```
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                    CPython Execution Path Diagram                                                 ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║  ENTRY POINTS:  🔵 python script.py   🟢 python (REPL)   🟠 import module   🔴 func()   🟣 "hello".upper()       ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Programs/python.c:main()                     🔵🟢 Entry point for CPython executable. Parses argv and calls      │
│                                              Py_BytesMain() to initialize the runtime environment.               │
└──────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Modules/main.c:pymain_main()                 🔵🟢 Coordinates initialization and execution mode selection.       │
│                                              Calls pymain_init() then pymain_run_python().                       │
└──────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┘
                                               │
                         ┌─────────────────────┴─────────────────────┐
                         │                                           │
                         ▼                                           ▼
┌────────────────────────────────────────────────────┐  ┌────────────────────────────────────────────────────┐
│ Modules/main.c:pymain_run_file()                   │  │ Modules/main.c:pymain_run_stdin()                  │
│ 🔵 Opens file, checks encoding, creates file       │  │ 🟢 Detects if stdin is TTY. Starts _pyrepl         │
│ object. Dispatches to pythonrun.c for execution.   │  │ interactive console or basic readline loop.        │
└────────────────────────┬───────────────────────────┘  └────────────────────────┬───────────────────────────┘
                         │                                                       │
                         ▼                                                       ▼
┌────────────────────────────────────────────────────┐  ┌────────────────────────────────────────────────────┐
│ Python/pythonrun.c:_PyRun_SimpleFileObject()       │  │ Python/pythonrun.c:_PyRun_InteractiveLoopObject()  │
│ 🔵 Reads entire file content, sets up __main__     │  │ 🟢 Displays prompt (>>> or ...), reads one         │
│ module globals, then calls run compilation chain.  │  │ statement at a time, compiles and executes it.     │
└────────────────────────┬───────────────────────────┘  └────────────────────────┬───────────────────────────┘
                         │                                                       │
                         └───────────────────────┬───────────────────────────────┘
                                                 │
                                                 ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Parser/peg_api.c:_PyParser_ASTFromString()   🔵🟢 Tokenizes source code and runs PEG parser to produce an       │
│                                              Abstract Syntax Tree (mod_ty). Handles syntax errors here.          │
└──────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Python/compile.c:_PyAST_Compile()            🔵🟢 Walks AST to generate bytecode instructions. Creates          │
│                                              PyCodeObject with constants, names, and bytecode bytes.             │
└──────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Python/ceval.c:PyEval_EvalCode()             🔵🟢🟠🔴🟣 Creates execution frame from code object. Sets up       │
│                                              locals/globals dicts and dispatches to frame evaluator.             │
└──────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────┘
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Python/ceval.c:_PyEval_EvalFrameDefault()    🔵🟢🟠🔴🟣 THE BYTECODE INTERPRETER LOOP. Fetches opcodes,         │
│                                              dispatches via computed goto/switch. Heart of Python execution.     │
└────────────┬─────────────────────────────────┼────────────────────────────────────────────────────────────────┬──┘
             │                                 │                                                                │
             │ IMPORT_NAME opcode              │ CALL opcode                                                    │ LOAD_METHOD opcode
             ▼                                 ▼                                                                ▼
┌────────────────────────────────┐  ┌────────────────────────────────┐  ┌─────────────────────────────────────────┐
│ Python/import.c:               │  │ Objects/call.c:                │  │ Objects/typeobject.c:                   │
│   PyImport_ImportModule()      │  │   _PyObject_Call()             │  │   call_method()                         │
│ 🟠 Entry to import system.     │  │ 🔴 Main call dispatcher.       │  │ 🟣 Looks up method on type's MRO.       │
│ Checks sys.modules cache first.│  │ Checks for vectorcall support. │  │ Returns bound method or descriptor.     │
└────────────┬───────────────────┘  └────────────┬───────────────────┘  └────────────────────┬────────────────────┘
             │                                   │                                           │
             ▼                                   ▼                                           ▼
┌────────────────────────────────┐  ┌────────────────────────────────┐  ┌─────────────────────────────────────────┐
│ Python/import.c:               │  │ Objects/call.c:                │  │ Objects/typeobject.c:                   │
│   import_find_and_load()       │  │   _PyFunction_Vectorcall()     │  │   vectorcall_method()                   │
│ 🟠 Calls into importlib        │  │ 🔴 Fast path for Python funcs. │  │ 🟣 Calls C function directly via        │
│ (_bootstrap._find_and_load).   │  │ Creates frame, binds args.     │  │ vectorcall protocol (METH_O/NOARGS).    │
└────────────┬───────────────────┘  └────────────┬───────────────────┘  └────────────────────┬────────────────────┘
             │                                   │                                           │
             ▼                                   │                                           ▼
┌────────────────────────────────┐               │                      ┌─────────────────────────────────────────┐
│ Lib/importlib/_bootstrap.py:  │               │                      │ Objects/unicodeobject.c:                │
│   _find_and_load()            │               │                      │   unicode_upper()                       │
│ 🟠 Searches finders (file,    │               │                      │ 🟣 Actual implementation. Iterates      │
│ frozen, built-in). Loads code.│               │                      │ codepoints, applies Unicode case map.   │
└────────────┬───────────────────┘               │                      └─────────────────────────────────────────┘
             │                                   │
             │ [compile module source]           │
             └──────────────┬────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  ↑ RECURSE ↑  │
                    │ Back to ceval │
                    │ for execution │
                    └───────────────┘
```

## Legend

| Symbol | Meaning |
|--------|---------|
| 🔵 | Script execution (`python script.py`) - File read → Parse → Compile → Execute |
| 🟢 | REPL (interactive mode) - Read line → Parse → Compile → Execute → Loop |
| 🟠 | Import (`import module`) - Find → Load → Parse → Compile → Execute in module namespace |
| 🔴 | Function call (`func()`) - Push args → Call dispatcher → Create frame → Execute bytecode |
| 🟣 | Method call (`"hello".upper()`) - Lookup on type → Vectorcall → C implementation |

## Comparison to Other Languages

| Aspect | CPython | Java | Ruby |
|--------|---------|------|------|
| **Execution Model** | Bytecode interpreted | Bytecode JIT-compiled | Bytecode interpreted (YARV) |
| **Module Loading** | Dynamic importlib | Static classloader | Dynamic require |
| **Memory Management** | Reference counting + GC | Tracing GC | Tracing GC |
| **REPL** | _pyrepl (Python) | jshell (Java) | IRB (C) |
| **Method Dispatch** | MRO lookup + vectorcall | vtable | Method cache |

## Key Convergence Point

All execution paths converge at `Python/ceval.c:_PyEval_EvalFrameDefault()` - the bytecode interpreter loop. This is the heart of Python execution where opcodes are fetched and dispatched.

## File Reference

| File | Purpose |
|------|---------|
| `Programs/python.c` | Main entry point |
| `Modules/main.c` | Initialization and mode selection |
| `Python/pythonrun.c` | High-level execution APIs |
| `Parser/peg_api.c` | PEG parser interface |
| `Python/compile.c` | AST to bytecode compiler |
| `Python/ceval.c` | Bytecode interpreter |
| `Python/import.c` | Import system C code |
| `Lib/importlib/_bootstrap.py` | Import system Python code |
| `Objects/call.c` | Function call mechanics |
| `Objects/typeobject.c` | Type system and method lookup |
| `Objects/unicodeobject.c` | String implementation |
