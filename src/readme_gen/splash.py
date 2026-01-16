from time import time

from textual import on
from textual.app import App, ComposeResult, RenderableType
from textual.containers import Container, Horizontal, VerticalScroll
from textual.renderables.gradient import LinearGradient
from textual.widgets import Static, Button, Header, Footer
from textual.reactive import reactive

COLORS = [
    "#881177",
    "#aa3355",
    "#cc6666",
    "#ee9944",
    "#eedd00",
    "#99dd55",
    "#44dd88",
    "#22ccbb",
    "#00bbcc",
    "#0099cc",
    "#3366bb",
    "#663399",
]
STOPS = [(i / (len(COLORS) - 1), color) for i, color in enumerate(COLORS)]


class Splash(Container):
    """Custom widget that extends Container."""

    DEFAULT_CSS = """
    Splash {
        align: center middle;
    }
    Static {
        width: 50%;
        padding: 2 4;
    }
    """

    title_text = """
'########::'########::::'###::::'########::'##::::'##:'########:::::'######:::'########:'##::: ##
:##.... ##: ##.....::::'## ##::: ##.... ##: ###::'###: ##.....:::::'##... ##:: ##.....:: ###:: ##
:##:::: ##: ##::::::::'##:. ##:: ##:::: ##: ####'####: ##:::::::::: ##:::..::: ##::::::: ####: ##
:########:: ######:::'##:::. ##: ##:::: ##: ## ### ##: ######:::::: ##::'####: ######::: ## ## ##
:##.. ##::: ##...:::: #########: ##:::: ##: ##. #: ##: ##...::::::: ##::: ##:: ##...:::: ##. ####
:##::. ##:: ##::::::: ##.... ##: ##:::: ##: ##:.:: ##: ##:::::::::: ##::: ##:: ##::::::: ##:. ###
:##:::. ##: ########: ##:::: ##: ########:: ##:::: ##: ########::::  ######::: ########: ##::. ##
:..:::::..::........::..:::::..::........:::..:::::..::........::::::......::::........::..::::..::
    """
    
    def on_mount(self) -> None:
        self.text_title.styles.height = "auto"
        self.text_title.styles.width = "75%"
        self.text_title.styles.color = "white"
        self.text_title.styles.text_align = "center"
        self.text_title.styles.background = "darkblue"
        self.text_title.styles.border = ("heavy", "blue")   
        self.auto_refresh = 1 / 30

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        self.text_title = Static(self.title_text)
        yield Header()
        yield Footer()
        yield VerticalScroll(
            Horizontal(self.text_title, id="title-container"),
            Horizontal(
                Button("Generate README", id="generate_readme_button", variant="success", classes="button"),
                Button("View Config", id="view_config_button", variant="primary", classes="button"),
                Button("Quit", id="quit_button", variant="error", classes="button"),
                id="button-container"
            ),
            id="splash-container"
        )
            
    @on(Button.Pressed, ".button")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        print(f"Button ID: {button_id}")
    

    def render(self) -> RenderableType:
        return LinearGradient(time() * 90, STOPS)


class ReadmeGenApp(App):
    """Simple app to show our custom widget."""
    CSS_PATH = "README-Gen-Splash.tcss"
    
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Splash()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    app = ReadmeGenApp()
    app.run()