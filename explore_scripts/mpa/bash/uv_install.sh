#!/bin/sh

echo "Removing existing .venv..."
rm -rf "$DEFAULT_PROJ_ROOT/.venv"

echo "Syncing dependencies with uv..."
cd "$DEFAULT_PROJ_ROOT" && uv sync
