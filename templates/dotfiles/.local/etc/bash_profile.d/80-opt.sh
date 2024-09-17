# shellcheck shell=sh

# Optional directory that may be used by packages to install "front-end"
# executables (by linking or copying)
# cf. https://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch03s13.html

OPT_BIN_DIR="${HOME}/.local/opt/bin"

if test -d "${OPT_BIN_DIR}"; then
    PATH="${OPT_BIN_DIR}:${PATH}"
fi
export PATH
