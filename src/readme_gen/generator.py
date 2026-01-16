# README generation logic
from pathlib import Path
from typing import Dict, Any
import datetime

# Simple templating - could be replaced with Jinja2 later
def _populate_template(template_content: str, data: Dict[str, Any]) -> str:
    """Populates a string template with data."""
    populated = template_content
    for key, value in data.items():
        placeholder = f"{{{{ {key} }}}}" # Using {{ key }} format
        populated = populated.replace(placeholder, str(value) if value is not None else "")
    return populated

def _format_list(items: list, item_format: str = "- {name} ({path})") -> str:
    """Formats a list of items (like apps or packages) into a markdown list."""
    if not items:
        return "N/A"
    return "\n".join([item_format.format(**item) for item in items])

def _generate_tech_stack_table(tech_stack: list) -> str:
    """Generates a 4x4 markdown table for the tech stack."""
    if not tech_stack:
        return "N/A"

    # Assume tech_stack is a list of badge markdown strings
    rows = []
    header = "| Tech | Tech | Tech | Tech |"
    separator = "| :---: | :---: | :---: | :---: |"
    rows.append(header)
    rows.append(separator)

    for i in range(0, len(tech_stack), 4):
        row_items = tech_stack[i:i+4]
        row_items += [''] * (4 - len(row_items)) # Pad with empty strings if needed
        rows.append(f"| {' | '.join(row_items)} |")

    return "\n".join(rows)


def generate_readme(
    config: Dict[str, Any],
    structure: Dict[str, Any],
    template_path: Path
) -> str:
    """
    Generates the README content based on config, structure, and template.

    Args:
        config: The loaded configuration dictionary.
        structure: The detected monorepo structure dictionary.
        template_path: Path to the README template file.

    Returns:
        The generated README content as a string.
    """
    if not template_path.exists():
        raise FileNotFoundError(f"README template not found at {template_path}")

    with open(template_path, 'r') as f:
        template_content = f.read()

    # Prepare data for the template
    template_data = {
        "repo_title": config.get("project", {}).get("title", "Project Title"),
        "repo_description": config.get("project", {}).get("description", "Project description."),
        "logo_url": config.get("project", {}).get("logo_url", "https://picsum.photos/80"), # Default placeholder
        "banner_url": config.get("project", {}).get("banner_url", "https://picsum.photos/1200/300"), # Default placeholder
        "repobeats_analytics_url": config.get("project", {}).get("repobeats_url", ""), # Optional analytics
        "about_description": config.get("about", {}).get("description", "More details about the project."),
        "tech_stack_table": _generate_tech_stack_table(config.get("tech_stack", [])),
        "apps_list": _format_list(structure.get("apps", []), item_format="#### {name}\n\n- Path: `{path}`\n- Description: Add description..."),
        "packages_list": _format_list(structure.get("packages", []), item_format="#### {name}\n\n- Path: `{path}`\n- Description: Add description..."),
        "config_files_list": _format_list(structure.get("config_files", []), item_format="#### {name}\n\n- Path: `{path}`\n- Description: Add description..."),
        "prerequisites": "\n".join([f"- {req}" for req in config.get("quickstart", {}).get("prerequisites", [])]) or "N/A",
        "installation_steps": "\n".join([f"{i+1}. {step}" for i, step in enumerate(config.get("quickstart", {}).get("installation", []))]) or "N/A",
        "usage_description": config.get("usage", {}).get("description", "How to use the project."),
        "usage_examples": "\n".join([f"- {ex}" for ex in config.get("usage", {}).get("examples", [])]) or "_Add usage examples here._",
        "roadmap_items": "\n".join([f"- [ ] {item}" for item in config.get("roadmap", [])]) or "N/A", # Basic unchecked list
        "contributing_steps": "\n".join([f"{i+1}. {step}" for i, step in enumerate(config.get("contributing", {}).get("steps", []))]) or "Follow standard fork and pull request workflow.",
        "license_text": config.get("license", {}).get("text", "MIT License"),
        "contact_name": config.get("contact", {}).get("name", "Your Name"),
        "contact_email": config.get("contact", {}).get("email", "your.email@example.com"),
        "project_link": config.get("contact", {}).get("project_link", "https://github.com/your_username/repo_name"),
        "acknowledgements": "\n".join([f"- [{ack.split('/')[-1]}]({ack})" for ack in config.get("acknowledgements", [])]) or "N/A",
        "current_year": datetime.datetime.now().year,
        # Add more fields as needed based on the template
    }

    generated_content = _populate_template(template_content, template_data)

    return generated_content

# Example usage (optional, can be removed)
if __name__ == "__main__":
    # Dummy data for testing
    dummy_config = {
        "project": {"title": "Test Repo", "description": "A test project."},
        "tech_stack": ["![JS](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)", "[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)]"],
        "roadmap": ["Feature A", "Feature B"],
        # ... other config sections
    }
    dummy_structure = {
        "apps": [{"name": "web", "path": "apps/web"}],
        "packages": [{"name": "ui", "path": "packages/ui"}],
        "config_files": [{"name": ".gitignore", "path": ".gitignore"}]
    }
    dummy_template_path = Path("dummy_template.md")
    with open(dummy_template_path, "w") as f:
        f.write("## {{ repo_title }}\n\n{{ repo_description }}\n\n### Tech Stack\n{{ tech_stack_table }}\n\n### Apps\n{{ apps_list }}")

    try:
        readme = generate_readme(dummy_config, dummy_structure, dummy_template_path)
        print("\nGenerated README Preview:")
        print(readme)
    except FileNotFoundError as e:
        print(e)
    finally:
        if dummy_template_path.exists():
             dummy_template_path.unlink() # Clean up dummy file