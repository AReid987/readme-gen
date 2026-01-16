# Monorepo structure detection logic
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Default directories often containing apps/packages in monorepos
DEFAULT_APP_DIRS = ["apps", "examples", "services"]
DEFAULT_PACKAGE_DIRS = ["packages", "libs", "modules"]

# Default criteria for identifying apps/packages (can be expanded)
# Example: presence of certain files
APP_MARKERS = ["app.py", "main.py", "index.html", "app.js", "package.json"] # Simplified example
PACKAGE_MARKERS = ["pyproject.toml", "package.json", "setup.py"] # Simplified example

# Files/Dirs to generally ignore
IGNORE_PATTERNS = [".git", "__pycache__", ".venv", "node_modules", "build", "dist", ".DS_Store"]

def _is_ignored(path: Path, ignore_patterns: List[str]) -> bool:
    """Check if a path matches any ignore patterns."""
    return any(part in ignore_patterns for part in path.parts) or path.name in ignore_patterns


def detect_monorepo_structure(
    root_dir: Path = Path("."),
    app_dirs: List[str] = DEFAULT_APP_DIRS,
    package_dirs: List[str] = DEFAULT_PACKAGE_DIRS,
    app_markers: List[str] = APP_MARKERS,
    package_markers: List[str] = PACKAGE_MARKERS,
    ignore_patterns: List[str] = IGNORE_PATTERNS
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Detects the structure of a monorepo by looking for apps and packages.

    Args:
        root_dir: The root directory of the monorepo.
        app_dirs: List of directory names likely containing apps.
        package_dirs: List of directory names likely containing packages.
        app_markers: List of filenames indicating an app directory.
        package_markers: List of filenames indicating a package directory.
        ignore_patterns: List of directory/file names to ignore.

    Returns:
        A dictionary with 'apps', 'packages', and 'config_files'.
    """
    structure = {"apps": [], "packages": [], "config_files": []}
    visited_dirs = set()

    # 1. Look in specific app/package directories first
    potential_roots = [root_dir / d for d in app_dirs + package_dirs if (root_dir / d).is_dir()]

    for potential_root in potential_roots:
        for item in potential_root.iterdir():
            if item.is_dir() and not _is_ignored(item, ignore_patterns):
                if potential_root.name in app_dirs:
                    # Basic check: assume dirs inside app_dirs are apps
                    structure["apps"].append({"name": item.name, "path": str(item.relative_to(root_dir))})
                    visited_dirs.add(item)
                elif potential_root.name in package_dirs:
                     # Basic check: assume dirs inside package_dirs are packages
                    structure["packages"].append({"name": item.name, "path": str(item.relative_to(root_dir))})
                    visited_dirs.add(item)

    # 2. Scan root directory for other potential items and config files
    for item in root_dir.iterdir():
        if _is_ignored(item, ignore_patterns) or item in visited_dirs:
            continue

        if item.is_dir():
            # Check if it qualifies as an app or package based on markers (simple check)
            is_package = any((item / marker).exists() for marker in package_markers)
            is_app = any((item / marker).exists() for marker in app_markers)

            if is_package and item not in [pkg["path"] for pkg in structure["packages"]]:
                 structure["packages"].append({"name": item.name, "path": str(item.relative_to(root_dir))})
            elif is_app and item not in [app["path"] for app in structure["apps"]]:
                 structure["apps"].append({"name": item.name, "path": str(item.relative_to(root_dir))})
            # Else: Could be a config dir, tests, etc. - currently ignored unless explicitly configured

        elif item.is_file():
            # Consider root-level files as config files (can be refined)
            structure["config_files"].append({"name": item.name, "path": str(item.relative_to(root_dir))})

    # TODO: Add more sophisticated detection logic, read package manifests for names/descriptions
    # TODO: Allow config overrides from readme-config.yaml

    return structure


# Example usage (optional, can be removed)
if __name__ == "__main__":
    detected = detect_monorepo_structure()
    print("Detected Monorepo Structure:")
    import json
    print(json.dumps(detected, indent=2))