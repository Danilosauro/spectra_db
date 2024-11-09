#!/bin/bash

if [ ! -x "$0" ]; then
    chmod +x "$0"
fi

if command -v python3 &>/dev/null; then
    python3 scripts/initial_screen.py
elif command -v python &>/dev/null; then
    python scripts/initial_screen.py
else
    echo "Python não está instalado. Por favor, instale o Python para rodar este programa."
    exit 1
fi
