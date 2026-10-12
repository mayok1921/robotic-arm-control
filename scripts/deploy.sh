#!/usr/bin/env bash
# Run on the development computer after wired SSH is confirmed.
# Example: bash scripts/deploy.sh orangepi@192.168.7.2
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: bash scripts/deploy.sh user@verified-orange-pi-ip" >&2
  exit 2
fi

target="$1"
case "$target" in
  *@*) ;;
  *) echo "Expected SSH destination user@host" >&2; exit 2 ;;
esac

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ssh "$target" 'mkdir -p ~/robotic_arm'
scp "$repo_dir/controller_test.py" "$target:~/robotic_arm/controller_test.py"
echo "Transferred controller_test.py. To run: ssh $target 'python3 ~/robotic_arm/controller_test.py'"
