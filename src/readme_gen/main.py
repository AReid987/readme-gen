# Main entry point for the readme-gen TUI application
from .app import ReadmeGenApp

def run():
    """Runs the Textual application."""
    app = ReadmeGenApp()
    app.run()

if __name__ == "__main__":
    run()