# Textual TUI application definition
import json # For pretty printing config
from pathlib import Path
from typing import Dict, Any

from textual.app import App, ComposeResult
# Import Vertical explicitly for layout
from textual.containers import Container, VerticalScroll, Vertical, Horizontal
from textual.widgets import Header, Footer, Static, RichLog, Button, Tree
from textual.reactive import reactive

# Import Splash Screen
from .splash import ReadmeGenApp

# Import our modules
from .config import load_config, DEFAULT_CONFIG_PATH
from .structure import detect_monorepo_structure
from .generator import generate_readme

DEFAULT_TEMPLATE_PATH = Path("templates/readme_template.md")
OUTPUT_README_PATH = Path("README_GENERATED.md") # Use a different name to avoid overwriting the project's README initially

class ReadmeGen(App):
    """The main Textual application for readme-gen."""

    CSS_PATH = "readme_gen.css"

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("g", "generate", "Generate README"),
        ("ctrl+s", "save_readme", "Save Generated README"),
    ]

    # Reactive variables to hold state
    config_data: reactive[Dict[str, Any] | None] = reactive(None)
    structure_data: reactive[Dict[str, Any] | None] = reactive(None)
    generated_readme: reactive[str | None] = reactive(None)
    status_message: reactive[str] = reactive("Load config and detect structure...")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="app-grid"):
            with Horizontal(id="horizontal-container"):
                # Left Column for Config and Structure using Vertical layout
                with Vertical(id="left-column"):
                    with Container(id="config-pane"):
                        
                        yield Static("Configuration", classes="pane-title")
                        yield RichLog(id="config-log", wrap=True, highlight=True)
                    with Container(id="structure-pane"):
                        yield Static("Detected Structure", classes="pane-title")
                        yield Tree(id="structure-tree", label=".") # Use Tree widget

                # Right Column for Preview - removed extra VerticalScroll
                with Container(id="preview-pane"):
                    yield Static("README Preview", classes="pane-title")
                    yield RichLog(id="readme-preview", wrap=False, highlight=True) # Use RichLog for preview
                    # Consider using Markdown widget later: from textual.widgets import Markdown
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.query_one(Footer).tooltip = self.status_message
        self.load_and_detect()

    def load_and_detect(self) -> None:
        """Load config and detect structure."""
        self.status_message = f"Loading config from {DEFAULT_CONFIG_PATH}..."
        self.config_data = load_config(DEFAULT_CONFIG_PATH)
        self.log(f"Config loaded: {self.config_data}")
        # Format config data for display
        config_display = json.dumps(self.config_data, indent=4)
        self.query_one("#config-log").write(config_display)

        self.status_message = "Detecting monorepo structure..."
        self.structure_data = detect_monorepo_structure()
        self.log(f"Structure detected: {self.structure_data}")
        self._populate_structure_tree() # Populate the tree view


        self.status_message = "Ready. Press 'G' to generate."

    def action_generate(self) -> None:
        """Generate the README content."""
        if not self.config_data or not self.structure_data:
            self.status_message = "Error: Config or structure not loaded."
            self.log("Attempted to generate README without config or structure data.")
            return

        self.status_message = f"Generating README using template {DEFAULT_TEMPLATE_PATH}..."
        try:
            self.generated_readme = generate_readme(
                self.config_data,
                self.structure_data,
                DEFAULT_TEMPLATE_PATH
            )
            preview_log = self.query_one("#readme-preview", RichLog)
            preview_log.clear()
            preview_log.write(self.generated_readme)
            self.status_message = f"README generated. Press Ctrl+S to save to {OUTPUT_README_PATH}."
            self.log("README generated successfully.")
        except FileNotFoundError as e:
            self.status_message = f"Error: Template file not found: {e}"
            self.log(f"Error generating README: {e}")
        except Exception as e:
            self.status_message = f"Error during generation: {e}"
            self.log(f"Error generating README: {e}")

    def action_save_readme(self) -> None:
        """Save the generated README to a file."""
        if not self.generated_readme:
            self.status_message = "Nothing to save. Generate README first (Press 'G')."
            self.log("Attempted to save README before generation.")
            return

        self.status_message = f"Saving README to {OUTPUT_README_PATH}..."
        try:
            with open(OUTPUT_README_PATH, "w") as f:
                f.write(self.generated_readme)
            self.status_message = f"README saved successfully to {OUTPUT_README_PATH}."
            self.log(f"README saved to {OUTPUT_README_PATH}.")
        except Exception as e:
            self.status_message = f"Error saving README: {e}"
            self.log(f"Error saving README to {OUTPUT_README_PATH}: {e}")

    def _populate_structure_tree(self) -> None:
        """Populates the structure tree widget with detected items."""
        tree = self.query_one("#structure-tree", Tree)
        tree.clear()
        tree.root.expand()

        if not self.structure_data:
            tree.root.set_label("[red]No structure data[/]")
            return

        apps_node = tree.root.add("Apps :package:", expand=True)
        for app in self.structure_data.get("apps", []):
            apps_node.add_leaf(f"{app.get('name', 'N/A')} [dim]({app.get('path', '')})[/]")

        packages_node = tree.root.add("Packages :toolbox:", expand=True)
        for pkg in self.structure_data.get("packages", []):
            packages_node.add_leaf(f"{pkg.get('name', 'N/A')} [dim]({pkg.get('path', '')})[/]")

        config_node = tree.root.add("Config Files :page_facing_up:", expand=False)
        for cfg in self.structure_data.get("config_files", []):
            config_node.add_leaf(f"{cfg.get('name', 'N/A')}")



    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        # Reverting to standard toggle method
        self.dark = not self.dark

    # Watch for status message changes and update the footer
    def watch_status_message(self, new_message: str) -> None:
        self.query_one(Footer).tooltip = new_message


if __name__ == "__main__":
    # This allows running the app directly for testing
    # In production, use the main.py entry point
    app = ReadmeGen()
    app.run()
