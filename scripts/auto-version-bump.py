#!/usr/bin/env python3
"""
Auto-version bump script for cc-sessions
Automatically increments patch version when significant files are modified
"""

import json
import re
import subprocess
import sys
from pathlib import Path

def get_git_diff_files():
    """Get list of staged files for commit"""
    try:
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'],
                              capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError:
        return []

def should_bump_version(changed_files):
    """Check if changes warrant a version bump"""
    significant_patterns = [
        'cc_sessions/install.py',
        'cc_sessions/uninstall.py',
        'install.js',
        'uninstall.js',
        'cc_sessions/hooks/',
        'cc_sessions/agents/',
        'cc_sessions/commands/',
        'cc_sessions/protocols/',
        'cc_sessions/templates/',
        'pyproject.toml',
        'package.json',
        'cc_sessions/__init__.py'
    ]

    for file in changed_files:
        for pattern in significant_patterns:
            if pattern in file:
                return True
    return False

def bump_version(version_str, bump_type='patch'):
    """Bump version string"""
    parts = version_str.split('.')
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == 'patch':
        patch += 1
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'major':
        major += 1
        minor = 0
        patch = 0

    return f"{major}.{minor}.{patch}"

def update_pyproject_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.exists():
        return False

    content = pyproject_path.read_text()
    updated_content = re.sub(
        r'version = "[^"]*"',
        f'version = "{new_version}"',
        content
    )

    if content != updated_content:
        pyproject_path.write_text(updated_content)
        return True
    return False

def update_package_json_version(new_version):
    """Update version in package.json"""
    package_path = Path('package.json')
    if not package_path.exists():
        return False

    with open(package_path) as f:
        data = json.load(f)

    old_version = data.get('version')
    if old_version != new_version:
        data['version'] = new_version
        with open(package_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    return False

def update_init_version(new_version):
    """Update version in cc_sessions/__init__.py"""
    init_path = Path('cc_sessions/__init__.py')
    if not init_path.exists():
        return False

    content = init_path.read_text()
    updated_content = re.sub(
        r'__version__ = "[^"]*"',
        f'__version__ = "{new_version}"',
        content
    )

    if content != updated_content:
        init_path.write_text(updated_content)
        return True
    return False

def main():
    # Get current staged files
    changed_files = get_git_diff_files()

    if not should_bump_version(changed_files):
        print("No significant changes detected, skipping version bump")
        return 0

    # Read current version from pyproject.toml
    pyproject_path = Path('pyproject.toml')
    if not pyproject_path.exists():
        print("pyproject.toml not found")
        return 1

    content = pyproject_path.read_text()
    version_match = re.search(r'version = "([^"]*)"', content)
    if not version_match:
        print("Could not find version in pyproject.toml")
        return 1

    current_version = version_match.group(1)
    new_version = bump_version(current_version)

    print(f"Auto-bumping version: {current_version} → {new_version}")

    # Update all version files
    updated_pyproject = update_pyproject_version(new_version)
    updated_package = update_package_json_version(new_version)
    updated_init = update_init_version(new_version)

    if updated_pyproject or updated_package or updated_init:
        # Stage the version files
        if updated_pyproject:
            subprocess.run(['git', 'add', 'pyproject.toml'])
        if updated_package:
            subprocess.run(['git', 'add', 'package.json'])
        if updated_init:
            subprocess.run(['git', 'add', 'cc_sessions/__init__.py'])

        print(f"Version bumped to {new_version}")

    return 0

if __name__ == '__main__':
    sys.exit(main())