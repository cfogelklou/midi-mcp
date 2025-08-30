# AI Agent Instructions

This document provides guidelines for all AI agents contributing to this codebase. Adhering to these instructions will ensure consistency, readability, and maintainability of the code.

## General Principles

*   **Clarity and Simplicity:** Write code that is easy to understand. Avoid unnecessary complexity.
*   **Modularity:** Keep functions and classes focused on a single responsibility.
*   **DRY (Don't Repeat Yourself):** Avoid duplicating code. Use functions, classes, and modules to promote reuse.
*   **Readability:** Follow the PEP 8 style guide for Python code. Use meaningful names for variables, functions, and classes.

## Python Best Practices

*   **Style Guide:** All Python code must adhere to the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/).
*   **Docstrings:** All modules, functions, classes, and methods should have docstrings as described in [PEP 257](https://www.python.org/dev/peps/pep-0257/).
*   **Typing:** Use type hints for all function signatures as described in [PEP 484](https://www.python.org/dev/peps/pep-0484/).
*   **Imports:** Import modules at the top of the file, one per line.
*   **Error Handling:** Use exceptions for error handling. Avoid returning error codes.

## Development Environment

*   **Virtual Environment:** This project uses a Python virtual environment located in the `venv` directory.
*   **Activating the Environment:** Before running any Python or pip commands, you must activate the virtual environment. This should be the first step in any new terminal session.
    ```bash
    source venv/bin/activate
    ```
*   **Command Failures:** If you encounter an error with a `python` or `pip` command, your first step should be to ensure the virtual environment is active by running `source venv/bin/activate` and then retrying the command.

## File Structure

*   **One Feature Per File:** Each distinct piece of functionality should reside in its own Python file. Do not combine multiple features into a single monolithic file.
*   **Descriptive File Names:** The name of each file should clearly indicate the feature it contains. For example, a file for handling MIDI note on/off messages could be named `midi_note_handler.py`.

## File Header

Every Python file must begin with a header that includes the following information:

```python
# -*- coding: utf-8 -*-
"""
<A brief one-sentence description of the file's purpose.>

<A more detailed description of the file's contents and functionality.>
"""
#
#   __author__ = "Chris Fogelklou"
#   __email__ = "chris.fogelklou@gmail.com"
#   __copyright__ = "Copyright 2025"
#   __license__ = "MIT"
#
#   (with lots of help from AI agents)
#
```

## Commits

*   **Atomic Commits:** Each commit should represent a single logical change.
*   **Clear Commit Messages:** Write clear and concise commit messages that explain the "what" and "why" of the change.

By following these guidelines, we can create a high-quality, maintainable, and collaborative codebase.