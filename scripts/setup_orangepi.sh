#!/usr/bin/env bash
# Run manually on the Orange Pi after reviewing the commands.
# Does not configure USB gadget mode, networking, SSH, or startup services.
set -euo pipefail

echo "Kernel: $(uname -r)"
echo "USB device controllers:"
ls /sys/class/udc || true
echo
echo "Python:"
python3 --version
echo
echo "Pygame (if installed):"
python3 -c 'import pygame; print(pygame.version.ver)' || echo "Pygame not available to this Python interpreter"
echo
echo "This diagnostic script makes no system configuration changes."
