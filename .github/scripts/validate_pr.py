import os
import re
import subprocess
import sys


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

ALLOWED_DIRECTORIES = {
    "Java": {".java"},
    "Python": {".py"},
    "JS": {".js"},
    "C++": {".cpp", ".cc", ".cxx", ".hpp", ".h"},
}

ALLOWED_ROOT_FILES = {
    "README.md",
}

LEETCODE_URL_PATTERN = re.compile(
    r"https?://(?:www\.)?leetcode\.com/problems/[a-z0-9-]+/?",
    re.IGNORECASE,
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def fail(message):
    print(f"❌ {message}")


def success(message):
    print(f"✅ {message}")


def get_changed_files():
    base_sha = os.environ["BASE_SHA"]
    head_sha = os.environ["HEAD_SHA"]

    result = subprocess.run(
        [
            "git",
            "diff",
            "--name-status",
            f"{base_sha}...{head_sha}",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    changed_files = []

    for line in result.stdout.splitlines():
        if not line.strip():
            continue

        parts = line.split("\t")

        # Format:
        # M    README.md
        # A    Java/two-sum.java
        status = parts[0]
        path = parts[-1]

        changed_files.append((status, path))

    return changed_files


# ---------------------------------------------------------
# PR validation
# ---------------------------------------------------------

def validate_pr_description():
    body = os.environ.get("PR_BODY", "") or ""

    if not body.strip():
        fail("PR description is empty.")
        return False

    if not LEETCODE_URL_PATTERN.search(body):
        fail(
            "PR description must contain a LeetCode problem URL."
        )
        return False

    success("LeetCode URL found in PR description.")
    return True


def validate_changed_files(changed_files):
    valid = True
    solution_files = []

    for status, path in changed_files:

        # Ignore deleted files for directory validation.
        if status == "D":
            continue

        # README is allowed.
        if path == "README.md":
            success("README.md change is allowed.")
            continue

        # Anything else must be inside a supported language directory.
        parts = path.split("/")

        if len(parts) < 2:
            fail(
                f"Invalid file changed: {path}. "
                "Only README.md or solution files inside "
                "language directories are allowed."
            )
            valid = False
            continue

        language = parts[0]

        if language not in ALLOWED_DIRECTORIES:
            fail(
                f"Invalid directory: {language}/ "
                f"in file {path}"
            )
            valid = False
            continue

        extension = os.path.splitext(path)[1].lower()

        if extension not in ALLOWED_DIRECTORIES[language]:
            allowed = ", ".join(
                sorted(ALLOWED_DIRECTORIES[language])
            )

            fail(
                f"Invalid file extension for {language}: "
                f"{path}. Allowed: {allowed}"
            )

            valid = False
            continue

        solution_files.append(path)

        success(f"Valid solution file: {path}")

    if not solution_files:
        fail(
            "No solution file was changed. "
            "A PR must contain at least one solution file."
        )
        valid = False

    return valid


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("")
    print("=" * 60)
    print("PR Guidelines Validation")
    print("=" * 60)
    print("")

    validation_passed = True

    # 1. Validate PR description
    print("Checking PR description...")
    print("")

    if not validate_pr_description():
        validation_passed = False

    print("")
    print("Checking changed files...")
    print("")

    # 2. Get changed files
    try:
        changed_files = get_changed_files()
    except subprocess.CalledProcessError as error:
        fail("Unable to determine changed files.")
        print(error)
        sys.exit(1)

    # 3. Validate changed files
    if not validate_changed_files(changed_files):
        validation_passed = False

    print("")
    print("=" * 60)

    if validation_passed:
        print("✅ PR GUIDELINES VALIDATION PASSED")
        print("=" * 60)
        sys.exit(0)

    print("❌ PR GUIDELINES VALIDATION FAILED")
    print("=" * 60)
    print("")
    print("Please fix the issues above and push a new commit.")
    print("The validation will run automatically again.")

    sys.exit(1)


if __name__ == "__main__":
    main()
