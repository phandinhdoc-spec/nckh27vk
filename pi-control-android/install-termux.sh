#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
command -v python >/dev/null || { echo 'Trong Termux chạy: pkg install python openssh curl'; exit 1; }
command -v ssh >/dev/null
command -v curl >/dev/null
# Set PI_CONTROL_REVISION to a reviewed commit SHA to pin a release.
revision="${PI_CONTROL_REVISION:-main}"
base="https://raw.githubusercontent.com/phandinhdoc-spec/nckh27vk/$revision"
mkdir -p "$HOME/pi-control-android-releases"
staging=$(mktemp -d "$HOME/pi-control-android-releases/release.XXXXXX")
complete=0
trap 'if [[ $complete -eq 0 ]]; then rm -rf -- "$staging"; fi' EXIT
for path in pi-control/core.py pi-control/remote_probe.py pi-control-android/server.py pi-control-android/static/index.html pi-control-android/static/style.css pi-control-android/static/app.js pi-control-android/README.md; do
    mkdir -p "$staging/$(dirname "$path")"
    curl --fail --location --retry 2 "$base/$path" -o "$staging/$path"
done
python -m py_compile "$staging/pi-control/core.py" "$staging/pi-control/remote_probe.py" "$staging/pi-control-android/server.py"
launcher="$HOME/pi-control-android-start.sh"
printf '#!/data/data/com.termux/files/usr/bin/bash\nexec python %q "$@"\n' "$staging/pi-control-android/server.py" > "$staging/start.sh"
chmod 700 "$staging/start.sh"
mv "$staging/start.sh" "$launcher"
complete=1
printf '\nDa cai. Chay: bash ~/pi-control-android-start.sh\nDemo: bash ~/pi-control-android-start.sh --demo\n'
