# General Info about this Repo

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the CPython repository - the reference implementation of the Python programming language written in C. Python 3.15 alpha is currently under development.

## Build System and Development Commands

### Basic Build Process
```bash
./configure
make
make test
sudo make install  # or 'make altinstall' to avoid overwriting existing Python
```

### Common Development Tasks
- `make test` - Run the full test suite
- `make buildbottest` - Run resource-intensive tests (disk space, memory)
- `make quicktest` - Run basic test suite quickly
- `make clean` - Clean build artifacts
- `make profile-opt` - Build with Profile Guided Optimization
- `./configure --with-pydebug` - Configure debug build
- `./configure --enable-optimizations` - Configure optimized build with PGO/LTO

### Testing Individual Components
- `make test TESTOPTS="-v test_os test_gdb"` - Run specific tests in verbose mode
- `make clinic-tests` - Test Argument Clinic
- `make multissltest` - Test SSL configurations

## Repository Structure

### Core Directories
- **Python/** - Core interpreter implementation (AST, compiler, bytecode interpreter)
- **Objects/** - Python object implementations (int, str, list, dict, etc.)
- **Modules/** - Built-in modules and extension modules in C
- **Include/** - Header files for the Python C API
- **Lib/** - Python standard library implemented in Python
- **Parser/** - Python grammar and parser implementation
- **Programs/** - Main Python executable and utility programs
- **Grammar/** - Python language grammar files

### Build and Configuration
- **Makefile.pre.in** - Template for the main Makefile (processed by configure)
- **configure.ac** - Autotools configuration script source
- **pyconfig.h.in** - Configuration header template

### Platform-Specific
- **PC/** - Windows-specific build files
- **PCbuild/** - Windows build system
- **Mac/** - macOS-specific files
- **iOS/** - iOS platform support
- **Android/** - Android platform support

### Development Tools
- **Tools/** - Various development and build tools
  - **Tools/clinic/** - Argument Clinic for C API generation
  - **Tools/cases_generator/** - Bytecode interpreter case generation
  - **Tools/jit/** - Just-In-Time compiler
  - **Tools/peg_generator/** - PEG parser generator
  - **Tools/build/** - Build-related utilities

### Documentation
- **Doc/** - Official Python documentation (Sphinx)
- **InternalDocs/** - CPython internals documentation for maintainers
- **Misc/** - Release notes, acknowledgments, and miscellaneous docs

## Code Quality and Linting

### Primary Linting Tool
- **Ruff** is used for Python code linting and formatting
- Configuration in `.ruff.toml` (line-length: 79, target Python 3.10+)
- Different configs for different subdirectories (Tools/build/, Tools/clinic/, etc.)

### Pre-commit Hooks
Configured in `.pre-commit-config.yaml`:
- Ruff linting and formatting for various directories
- Black formatting for Tools/jit/
- Various file format checks (YAML, TOML, trailing whitespace)
- GitHub workflow validation
- Sphinx documentation linting

### Manual Linting Commands
```bash
ruff check .                    # Lint Python code
ruff format .                   # Format Python code
ruff check --fix .              # Auto-fix linting issues
```

## Architecture Overview

### Compilation Pipeline
1. **Parser** (Parser/) - Converts source to Parse Tree
2. **AST** (Python/ast.c) - Parse Tree to Abstract Syntax Tree
3. **Compiler** (Python/compile.c) - AST to bytecode
4. **Interpreter** (Python/ceval.c) - Executes bytecode

### Key Components
- **Object System** (Objects/) - All Python values are PyObject* with reference counting
- **Memory Management** - Reference counting + cycle detection garbage collector
- **Import System** (Python/import.c) - Module loading and caching
- **Built-in Types** - Implemented in Objects/ (dictobject.c, listobject.c, etc.)
- **Extension Modules** - C modules in Modules/, Python modules in Lib/

### C API
- **Include/Python.h** - Main header for embedding/extending Python
- **Include/cpython/** - CPython-specific APIs
- **Include/internal/** - Internal APIs not for public use

## Development Guidelines

### Contributing Process
- Follow the Python Developer's Guide: https://devguide.python.org/
- All pull requests require GitHub issue discussion first
- Add yourself to Misc/ACKS for non-trivial contributions
- Use the established code style and conventions

### Testing Requirements
- All changes must pass the test suite (`make test`)
- Add tests for new functionality in Lib/test/
- Consider both positive and negative test cases
- Test cross-platform compatibility when relevant

### Code Style
- Follow PEP 7 for C code
- Follow PEP 8 for Python code (enforced by Ruff)
- 79 character line limit
- Use existing patterns and conventions in the codebase
- Give each new function a docstring explaining its arguments and what the function does overall

### Interacting with Me
- I am navigating this code base as an educator, to help students understand how Python is implemented and what makes it special.
- Anytime you are answering a question about the implementation of python, include reference points for comparing that implementation choice to one or two other languages such as Ruby or Java.
