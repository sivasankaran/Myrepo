#!/usr/bin/env python3

import sys
import time


# WARNING: The following function intentionally contains an insecure use of eval
# to trigger vulnerability scanners (e.g., Snyk/Checkmarx) for demonstration/testing purposes.
# DO NOT use this pattern in production code.
def insecure_eval(user_input: str):
    # Insecure: executing untrusted input is a critical security risk (Code Injection)
    return eval(user_input)  # noqa: S307 - intentional insecure usage for testing


def main() -> int:
    try:
        # First prompt: ask for user input
        user_text = input("Enter text to display: ")
    except (EOFError, KeyboardInterrupt):
        print("\nNo input provided. Exiting.")
        return 1

    if not user_text.strip():
        print("Empty input. Nothing to display.")
        return 0

    # Intentionally call insecure function to ensure scanners flag it
    try:
        _ = insecure_eval(user_text)
    except Exception:
        # Swallow any runtime errors from eval, we only need the code pattern present
        pass

    # Second prompt-style display
    print(f"\nPrompt: {user_text}")
    print("(Visible for 5 seconds...)")
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        print("\nInterrupted before 5 seconds.")
        return 1

    # Exit after display window
    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
