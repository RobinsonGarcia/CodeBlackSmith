import argparse
import sys
import subprocess
import codehammer  # Import CodeHammer CLI commands
from .assistant.cli import register_commands as register_assistant_commands

#######################
# Command Forwarding  #
#######################
def forward_to_codehammer():
    """Forward unknown commands to CodeHammer."""
    command = [sys.executable, "-m", "codehammer.cli"] + sys.argv[1:]
    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    sys.exit(result.returncode)

#######################
# Main CLI Entry Point#
#######################
def main():
    parser = argparse.ArgumentParser(description="CodeBlacksmith: AI & Code Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Register CodeHammer CLI commands
    try:
        import codehammer.cli
        codehammer.cli.register_core_commands(subparsers)
    except ImportError:
        print("⚠️ Warning: CodeHammer is not installed. CLI commands will be limited.")

    # Register Assistant Commands
    register_assistant_commands(subparsers)

    args, unknown_args = parser.parse_known_args()

    # If the command is from CodeHammer, forward it
    if args.command in ["tree", "file", "files", "files_recursive", "write", "combine", "clean_result"]:
        forward_to_codehammer()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()