#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
#
# Phase -1.0 baseline detection.
#
# Read-only probe of the current dev stack. Emits a KEY=VALUE report on stdout
# that Phase -1.1 parses into the gap report card. Never installs, never writes
# outside stdout, never prompts the user. Must complete in <5 s on a typical
# machine.
#
# Exit codes:
#   0  probe ran (regardless of what was found)
#   2  fundamental shell environment unusable (extremely unlikely)
#
# Output format: one `KEY=VALUE` per line, sorted by key. VALUE is one of:
#   present    installed and on PATH
#   missing    not installed or not on PATH
#   unknown    detection not supported on this OS or probe failed
# Free-form metadata uses KEY_VERSION or KEY_PATH suffixes where useful.

set -u

emit() { printf '%s=%s\n' "$1" "$2"; }

# ---------- OS family ----------
uname_s=$(uname -s 2>/dev/null || echo unknown)
case "$uname_s" in
  Linux*)                       os_family=linux ;;
  Darwin*)                      os_family=macos ;;
  MINGW*|MSYS*|CYGWIN*|Windows*) os_family=windows ;;
  *)                            os_family=unknown ;;
esac
emit OS_FAMILY "$os_family"
emit OS_UNAME  "$uname_s"

# ---------- package manager ----------
pkg_mgr=missing
case "$os_family" in
  windows)
    if command -v winget >/dev/null 2>&1; then pkg_mgr=winget; fi
    ;;
  macos)
    if command -v brew >/dev/null 2>&1; then pkg_mgr=brew; fi
    ;;
  linux)
    if   command -v apt     >/dev/null 2>&1; then pkg_mgr=apt
    elif command -v dnf     >/dev/null 2>&1; then pkg_mgr=dnf
    elif command -v pacman  >/dev/null 2>&1; then pkg_mgr=pacman
    elif command -v zypper  >/dev/null 2>&1; then pkg_mgr=zypper
    fi
    ;;
esac
emit PKG_MANAGER "$pkg_mgr"

# ---------- Layer 3 dev essentials ----------
probe_cmd() {
  local key=$1 cmd=$2 version_flag=${3:---version}
  if command -v "$cmd" >/dev/null 2>&1; then
    emit "${key}" present
    local v
    v=$("$cmd" "$version_flag" 2>&1 | head -n 1 | tr -d '\r' || echo "")
    emit "${key}_VERSION" "${v:-unknown}"
  else
    emit "${key}" missing
  fi
}

probe_cmd NODE     node
probe_cmd NPM      npm
probe_cmd GIT      git
probe_cmd GH_CLI   gh
probe_cmd CODE     code    --version
probe_cmd CLAUDE   claude  --version

# ---------- Chrome / Edge ----------
chrome=missing
chrome_path=""
case "$os_family" in
  windows)
    for p in \
        "/c/Program Files/Google/Chrome/Application/chrome.exe" \
        "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
        "$LOCALAPPDATA/Google/Chrome/Application/chrome.exe"; do
      [ -n "${p:-}" ] && [ -e "$p" ] && { chrome=present; chrome_path="$p"; break; }
    done
    ;;
  macos)
    for p in \
        "/Applications/Google Chrome.app" \
        "$HOME/Applications/Google Chrome.app"; do
      [ -e "$p" ] && { chrome=present; chrome_path="$p"; break; }
    done
    ;;
  linux)
    if command -v google-chrome >/dev/null 2>&1 \
    || command -v google-chrome-stable >/dev/null 2>&1 \
    || command -v chromium >/dev/null 2>&1; then
      chrome=present
    fi
    ;;
esac
emit CHROME "$chrome"
[ -n "$chrome_path" ] && emit CHROME_PATH "$chrome_path"

# ---------- Claude Code VS Code extension (also the `ide` MCP server) ----------
code_ext=unknown
if command -v code >/dev/null 2>&1; then
  if code --list-extensions 2>/dev/null | grep -iq '^anthropic\.claude-code$'; then
    code_ext=present
  else
    code_ext=missing
  fi
fi
emit CLAUDE_CODE_VSCODE_EXTENSION "$code_ext"

# ---------- MCPs registered with Claude Code ----------
mcp_list=unknown
playwright_mcp=unknown
ide_mcp=unknown
if command -v claude >/dev/null 2>&1; then
  mcp_output=$(claude mcp list 2>/dev/null || true)
  if [ -n "$mcp_output" ]; then
    mcp_list=present
    if printf '%s' "$mcp_output" | grep -iq 'playwright'; then
      playwright_mcp=present
    else
      playwright_mcp=missing
    fi
    if printf '%s' "$mcp_output" | grep -iq '^ide'; then
      ide_mcp=present
    else
      ide_mcp=missing
    fi
  else
    mcp_list=missing
    playwright_mcp=missing
    ide_mcp=missing
  fi
fi
emit MCP_LIST        "$mcp_list"
emit MCP_PLAYWRIGHT  "$playwright_mcp"
emit MCP_IDE         "$ide_mcp"

# ---------- Claude in Chrome extension (via native messaging host file) ----------
# Claude in Chrome registers a native messaging host; its config file lives in
# a well-known per-OS directory when installed. Presence of the file is a
# reliable proxy for "extension installed at least once".
cic=unknown
case "$os_family" in
  windows)
    # Native messaging hosts on Windows are registered in the registry under
    # HKCU\Software\Google\Chrome\NativeMessagingHosts; from a bash probe we
    # cannot read the registry reliably, so report unknown and let Phase -1.1
    # fall back to asking the user.
    cic=unknown
    ;;
  macos)
    cic_dir="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
    if [ -d "$cic_dir" ] && ls "$cic_dir" 2>/dev/null | grep -iq 'claude'; then
      cic=present
    else
      cic=missing
    fi
    ;;
  linux)
    cic_dir="$HOME/.config/google-chrome/NativeMessagingHosts"
    if [ -d "$cic_dir" ] && ls "$cic_dir" 2>/dev/null | grep -iq 'claude'; then
      cic=present
    else
      cic=missing
    fi
    ;;
esac
emit CLAUDE_IN_CHROME "$cic"

# ---------- SSH keys under ~/.ssh/ ----------
ssh_keys=missing
if [ -d "$HOME/.ssh" ]; then
  if ls "$HOME/.ssh"/id_* 2>/dev/null | grep -qv '\.pub$'; then
    ssh_keys=present
  fi
fi
emit SSH_KEYS "$ssh_keys"

# ---------- Shell / env baseline ----------
emit SHELL_NAME "${SHELL:-unknown}"
emit HOME_DIR   "${HOME:-unknown}"

exit 0
