#!/bin/sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPOS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
FIRST_NO_CODE_DIR="$REPOS_DIR/first_no_code"
REPO_URL="https://github.com/jfharney77/first_no_code.git"
BRANCH="mp"

# Check if first_no_code repo exists, clone if not
if [ ! -d "$FIRST_NO_CODE_DIR" ]; then
    echo "first_no_code not found. Cloning into $REPOS_DIR..."
    git clone "$REPO_URL" "$FIRST_NO_CODE_DIR"
fi

# Checkout the mp branch and pull latest changes
cd "$FIRST_NO_CODE_DIR"
echo "Checking out branch '$BRANCH'..."
git fetch origin
git checkout "$BRANCH" 2>/dev/null || git checkout -b "$BRANCH" "origin/$BRANCH"
git pull origin "$BRANCH"

# Run install_and_run.sh samewindow
echo "Starting services..."
sh "$FIRST_NO_CODE_DIR/explore_scripts/mpa/bash/install_and_run.sh" samewindow
