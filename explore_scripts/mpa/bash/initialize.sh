#!/bin/sh

TO_INSTALL=""

for pkg in python3 python3-pip python-is-python3; do
    if ! dpkg -s "$pkg" >/dev/null 2>&1; then
        TO_INSTALL="$TO_INSTALL $pkg"
    fi
done

if [ -n "$TO_INSTALL" ]; then
    echo "Installing missing packages:$TO_INSTALL"
    sudo apt update && sudo apt install -y $TO_INSTALL
else
    echo "All required Python packages are already installed."
fi
