#!/usr/bin/env python3
"""Document versioning system for automatic document version management."""
import json
import sys
import shutil
from pathlib import Path
from datetime import datetime
from shared_state import get_project_root

def load_config():
    """Load document governance configuration."""
    project_root = get_project_root()
    config_file = project_root / "sessions" / "sessions-config.json"

    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get("document_governance", {})
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    return {
        "enabled": False,
        "auto_versioning": True,
        "documents_path": "sessions/documents",
        "version_history_limit": 10
    }

def get_document_version(doc_path):
    """Extract version number from document content."""
    try:
        content = doc_path.read_text()
        lines = content.split('\n')

        for line in lines:
            if line.strip().startswith('**Document Version:**'):
                version_str = line.split(':', 1)[1].strip()
                try:
                    return float(version_str)
                except ValueError:
                    return 1.0
        return 1.0
    except Exception:
        return 1.0

def increment_version(current_version):
    """Increment document version number."""
    if current_version == int(current_version):
        return current_version + 1.0
    else:
        # Increment minor version
        major = int(current_version)
        minor = round((current_version - major) * 10)
        minor += 1
        if minor >= 10:
            major += 1
            minor = 0
        return major + (minor / 10)

def update_document_version(doc_path, new_version):
    """Update the version number in document content."""
    try:
        content = doc_path.read_text()
        lines = content.split('\n')

        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith('**Document Version:**'):
                lines[i] = f"**Document Version:** {new_version}"
                updated = True
                break
            elif line.strip().startswith('**Last Updated:**'):
                lines[i] = f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}"

        if not updated:
            # Add version info if not present
            lines.insert(2, f"**Document Version:** {new_version}")
            lines.insert(3, f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}")

        doc_path.write_text('\n'.join(lines))
        return True
    except Exception as e:
        print(f"Error updating document version: {e}", file=sys.stderr)
        return False

def archive_document_version(doc_path, version):
    """Archive the current version of a document."""
    try:
        project_root = get_project_root()
        config = load_config()

        # Create archive path
        relative_path = doc_path.relative_to(project_root)
        archive_dir = project_root / config["documents_path"] / "versions" / relative_path.parent
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Create versioned filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{doc_path.stem}_v{version}_{timestamp}{doc_path.suffix}"
        archive_path = archive_dir / archive_name

        # Copy current version to archive
        shutil.copy2(doc_path, archive_path)

        # Maintain version history limit
        cleanup_old_versions(archive_dir, doc_path.stem, config.get("version_history_limit", 10))

        return archive_path
    except Exception as e:
        print(f"Error archiving document version: {e}", file=sys.stderr)
        return None

def cleanup_old_versions(archive_dir, doc_stem, limit):
    """Clean up old versions beyond the history limit."""
    try:
        # Find all versions of this document
        pattern = f"{doc_stem}_v*"
        version_files = list(archive_dir.glob(pattern))

        # Sort by modification time (newest first)
        version_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # Remove excess versions
        for old_file in version_files[limit:]:
            old_file.unlink()
            print(f"Cleaned up old version: {old_file.name}", file=sys.stderr)
    except Exception as e:
        print(f"Error cleaning up old versions: {e}", file=sys.stderr)

def create_new_document_version(doc_path, changes_description=""):
    """Create a new version of a document with changes."""
    try:
        config = load_config()

        if not config.get("enabled", False) or not config.get("auto_versioning", True):
            return False

        # Get current version
        current_version = get_document_version(doc_path)

        # Archive current version
        archive_path = archive_document_version(doc_path, current_version)
        if not archive_path:
            return False

        # Create new version
        new_version = increment_version(current_version)

        # Update document with new version
        if update_document_version(doc_path, new_version):
            # Add change log entry if changes description provided
            if changes_description:
                add_change_log_entry(doc_path, new_version, changes_description)

            print(f"Document versioned: {doc_path.name} v{current_version} → v{new_version}", file=sys.stderr)
            return True

        return False
    except Exception as e:
        print(f"Error creating new document version: {e}", file=sys.stderr)
        return False

def add_change_log_entry(doc_path, version, description):
    """Add an entry to the document's change log."""
    try:
        content = doc_path.read_text()
        lines = content.split('\n')

        # Find change log section
        changelog_start = -1
        for i, line in enumerate(lines):
            if "## Change Log" in line or "## Changelog" in line:
                changelog_start = i
                break

        if changelog_start == -1:
            return False

        # Find the table header and insert new entry
        for i in range(changelog_start, len(lines)):
            if lines[i].strip().startswith('|') and 'Version' in lines[i]:
                # Found table header, insert new entry after it
                new_entry = f"| {version} | {datetime.now().strftime('%Y-%m-%d')} | System | {description} |"
                lines.insert(i + 2, new_entry)  # Insert after header and separator
                break

        doc_path.write_text('\n'.join(lines))
        return True
    except Exception as e:
        print(f"Error adding change log entry: {e}", file=sys.stderr)
        return False

def get_document_history(doc_path):
    """Get version history for a document."""
    try:
        project_root = get_project_root()
        config = load_config()

        relative_path = doc_path.relative_to(project_root)
        archive_dir = project_root / config["documents_path"] / "versions" / relative_path.parent

        if not archive_dir.exists():
            return []

        # Find all versions
        pattern = f"{doc_path.stem}_v*"
        version_files = list(archive_dir.glob(pattern))

        # Sort by modification time (newest first)
        version_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        history = []
        for version_file in version_files:
            # Extract version and timestamp from filename
            parts = version_file.stem.split('_')
            if len(parts) >= 3:
                version = parts[1][1:]  # Remove 'v' prefix
                timestamp = parts[2]
                history.append({
                    "version": version,
                    "timestamp": timestamp,
                    "file_path": str(version_file),
                    "size": version_file.stat().st_size
                })

        return history
    except Exception as e:
        print(f"Error getting document history: {e}", file=sys.stderr)
        return []

def restore_document_version(doc_path, target_version):
    """Restore a document to a specific version."""
    try:
        project_root = get_project_root()
        config = load_config()

        relative_path = doc_path.relative_to(project_root)
        archive_dir = project_root / config["documents_path"] / "versions" / relative_path.parent

        # Find the target version file
        pattern = f"{doc_path.stem}_v{target_version}_*"
        version_files = list(archive_dir.glob(pattern))

        if not version_files:
            print(f"Version {target_version} not found for {doc_path.name}", file=sys.stderr)
            return False

        # Use the most recent file if multiple matches
        version_file = sorted(version_files, key=lambda x: x.stat().st_mtime)[-1]

        # Archive current version before restoring
        current_version = get_document_version(doc_path)
        archive_document_version(doc_path, current_version)

        # Restore the target version
        shutil.copy2(version_file, doc_path)

        print(f"Restored {doc_path.name} to version {target_version}", file=sys.stderr)
        return True
    except Exception as e:
        print(f"Error restoring document version: {e}", file=sys.stderr)
        return False

def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: document-versioning.py <command> [args...]")
        print("Commands:")
        print("  version <file> [description] - Create new version")
        print("  history <file> - Show version history")
        print("  restore <file> <version> - Restore to specific version")
        return

    command = sys.argv[1]

    if command == "version" and len(sys.argv) >= 3:
        doc_path = Path(sys.argv[2])
        description = sys.argv[3] if len(sys.argv) > 3 else "Manual version update"
        create_new_document_version(doc_path, description)

    elif command == "history" and len(sys.argv) >= 3:
        doc_path = Path(sys.argv[2])
        history = get_document_history(doc_path)
        print(f"Version history for {doc_path.name}:")
        for entry in history:
            print(f"  v{entry['version']} - {entry['timestamp']} ({entry['size']} bytes)")

    elif command == "restore" and len(sys.argv) >= 4:
        doc_path = Path(sys.argv[2])
        target_version = sys.argv[3]
        restore_document_version(doc_path, target_version)

    else:
        print("Invalid command or arguments")

if __name__ == "__main__":
    main()