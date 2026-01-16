# README Generator Plan

This document outlines the plan for creating a monorepo-aware README generator using Textual.

**Goal:** Build a TUI application that reads a configuration file, automatically detects the structure of a monorepo, and generates a `README.md` file based on a predefined template and the detected structure. Future enhancements include integrating AI (Gemma3 via Ollama) for content generation.

**Revised Plan:**

**Phase 1: Core Functionality - Configuration, Structure Detection, TUI, and Basic Generation**

1.  **Project Setup:**
    *   Ensure `pyproject.toml` is configured correctly.
    *   Add `textual` and `pyyaml` as dependencies in `pyproject.toml`.
    *   Create `src/readme_gen` directory.
    *   Create necessary Python files: `main.py`, `app.py`, `config.py`, `structure.py`, `generator.py`.
    *   Create `readme-config.yaml` (in the project root).
    *   Create `templates/readme_template.md`.

2.  **Configuration File Handling (`readme-config.yaml` and `src/readme_gen/config.py`):**
    *   **Define YAML Structure:** Design the configuration structure (project metadata, sections, monorepo settings).
    *   **Implement Configuration Loading:** Create functions in `src/readme_gen/config.py` to read and parse `readme-config.yaml`.

3.  **Monorepo Structure Detection (`src/readme_gen/structure.py`):**
    *   **Detection Logic:** Implement functions to automatically detect apps, packages, and config files based on configurable criteria.
    *   **Output Structure:** Return a structured representation of the detected monorepo layout.

4.  **README Template and Generation (`src/readme_gen/generator.py` and `templates/readme_template.md`):**
    *   **Create README Template:** Design `templates/readme_template.md` with placeholders following the specified format.
    *   **Generation Logic:** Create a function in `src/readme_gen/generator.py` to load the template, populate it with configuration and structure data, and generate the final `README.md` string.

5.  **Textual User Interface (TUI) (`src/readme_gen/app.py`):**
    *   **Create App Class:** Define the main Textual `App` class in `src/readme_gen/app.py`.
    *   **Design TUI Layout:** Use Textual widgets (Tree, Markdown, RichLog, Buttons) to display config, structure, preview, and provide generation controls.
    *   **Implement TUI Logic:** Integrate calls to config, structure, and generation functions. Handle user input and update the UI.
    *   **Entry Point (`src/readme_gen/main.py`):** Create a script to run the Textual app.

**Phase 2: Gemma3/Ollama Integration (Future Enhancement)**

*   Set up Ollama and Gemma3.
*   Install a Python Ollama client.
*   Identify integration points (descriptions, roadmap, about section).
*   Modify `src/readme_gen/generator.py` to call Ollama/Gemma3.
*   Add configuration options for AI integration.

**Phase 3: Testing and Refinement**

*   Write basic unit tests (config, structure, generation).
*   Perform manual testing on various monorepos.
*   Gather feedback and iterate on logic, templates, and UI.

**Mermaid Diagram**

```mermaid
graph LR
    subgraph Phase 1: Core Functionality
        A[Project Setup + Deps] --> B(Config File Handling);
        B --> C(Monorepo Structure Detection);
        C --> D(README Template & Generation);
        D --> E(Textual User Interface (TUI));
    end
    E --> F[Phase 2: Gemma3 Integration (Future)];
    F --> G[Phase 3: Testing & Refinement];
    G --> H[End];

    style F fill:#f9f,stroke:#333,stroke-width:2px