import subprocess

DANGEROUS_PATTERNS = ["rm -rf /", "mkfs", "dd if=", ":(){:|:&};:", "> /dev/sd"]
SHELL_STATE_COMMANDS = ["cd", "export", "source", "alias", "unset"]

def is_dangerous(command):
    return any(pattern in command for pattern in DANGEROUS_PATTERNS)

def affects_shell_state(command):
    first_word = command.strip().split()[0] if command.strip() else ""
    return first_word in SHELL_STATE_COMMANDS

def confirm_and_run(command, explanation):
    if affects_shell_state(command):
        print("\nThis command changes your current shell's state (directory, "
              "environment variable, etc.) and can't be run automatically — "
              "it would only affect a temporary subprocess, not your terminal.")
        print(f"Run it yourself: {command}")
        return  

    if is_dangerous(command):

        print("\n⚠️  This command matches a known destructive pattern and will NOT be auto-run.")
        print("Review it yourself if you still want to run it.")
        return
    
    choice = input("\nRun this command? [y/N]: ").strip().lower()
    if choice == "y":
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"Command exited with error:\n{result.stderr}")
    else:
        print("Skipped.")