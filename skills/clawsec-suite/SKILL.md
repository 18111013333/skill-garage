---
name: clawsec-suite
version: 0.1.4
description: ClawSec suite manager with embedded advisory-feed monitoring, cryptographic signature verification, approval-gated malicious-skill response, and guided setup for additional security skills.
homepage: https://clawsec.prompt.security
clawdis:
  emoji: "📦"
  requires:
    bins: [curl, jq, shasum, openssl]
---

# ClawSec Suite

This means `clawsec-suite` can:
- monitor the ClawSec advisory feed,
- track which advisories are new since last check,
- cross-reference advisories against locally installed skills,
- recommend removal for malicious-skill advisories and require explicit user approval first,
- and still act as the setup/management entrypoint for other ClawSec protections.

## Included vs Optional Protections

### Built into clawsec-suite
- Embedded feed seed file: `advisories/feed.json`
- Portable heartbeat workflow in `HEARTBEAT.md`
- Advisory polling + state tracking + affected-skill checks
- OpenClaw advisory guardian hook package: `hooks/clawsec-advisory-guardian/`
- Setup scripts for hook and optional cron scheduling: `scripts/`
- Guarded installer: `scripts/guarded_skill_install.mjs`
- Dynamic catalog discovery for installable skills: `scripts/discover_skill_catalog.mjs`

### Installed separately (dynamic catalog)
`clawsec-suite` does not hard-code add-on skill names in this document.

Discover the current catalog from the authoritative index (`https://clawsec.prompt.security/skills/index.json`) at runtime:

```bash
SUITE_DIR="${INSTALL_ROOT:-$HOME/.openclaw/skills}/clawsec-suite"
node "$SUITE_DIR/scripts/discover_skill_catalog.mjs"
```

Fallback behavior:
- If the remote catalog index is reachable and valid, the suite uses it.
- If the remote index is unavailable or malformed, the script falls back to suite-local catalog metadata in `skill.json`.

## Installation

### Cross-shell path note

- In `bash`/`zsh`, keep path variables expandable (for example, `INSTALL_ROOT="$HOME/.openclaw/skills"`).
- Do not single-quote home-variable paths (avoid `'$HOME/.openclaw/skills'`).
- In PowerShell, set an explicit path:
  - `$env:INSTALL_ROOT = Join-Path $HOME ".openclaw\\skills"`
- If a path is passed with unresolved tokens (like `\$HOME/...`), suite scripts now fail fast with a clear error.

### Option A: Via clawhub (recommended)

```bash
npx clawhub@latest install clawsec-suite
```

### Option B: Manual download with signature + checksum verification

```bash
set -euo pipefail

VERSION="${SKILL_VERSION:?Set SKILL_VERSION (e.g. 0.0.8)}"
INSTALL_ROOT="${INSTALL_ROOT:-$HOME/.openclaw/skills}"
DEST="$INSTALL_ROOT/clawsec-suite"
BASE="https://github.com/prompt-security/clawsec/releases/download/clawsec-suite-v${VERSION}"

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# Pinned release-signing public key (verify fingerprint out-of-band on first use)
# Fingerprint (SHA-256 of SPKI DER): 711424e4535f84093fefb024cd1ca4ec87439e53907b305b79a631d5befba9c8
RELEASE_PUBKEY_SHA256="711424e4535f84093fefb024cd1ca4ec87439e53907b305b79a631d5befba9c8"
cat > "$TEMP_DIR/release-signing-public.pem" <<'PEM'
-----BEGIN PUBLIC KEY-----
MCowBQYDK2VwAyEAS7nijfMcUoOBCj4yOXJX+GYGv2pFl2Yaha1P4v5Cm6A=
-----END PUBLIC KEY-----
PEM

ACTUAL_KEY_SHA256="$(openssl pkey -pubin -in "$TEMP_DIR/release-signing-public.pem" -outform DER | shasum -a 256 | awk '{print $1}')"
if [ "$ACTUAL_KEY_SHA256" != "$RELEASE_PUBKEY_SHA256" ]; then
  echo "ERROR: Release public key fingerprint mismatch" >&2
  exit 1
fi

ZIP_NAME="clawsec-suite-v${VERSION}.zip"

# 1) Download release archive + signed checksums manifest + signing public key
curl -fsSL "$BASE/$ZIP_NAME" -o "$TEMP_DIR/$ZIP_NAME"
curl -fsSL "$BASE/checksums.json" -o "$TEMP_DIR/checksums.json"
curl -fsSL "$BASE/checksums.sig" -o "$TEMP_DIR/checksums.sig"

# 2) Verify checksums manifest signature before trusting any hashes
openssl base64 -d -A -in "$TEMP_DIR/checksums.sig" -out "$TEMP_DIR/checksums.sig.bin"
if ! openssl pkeyutl -verify \
  -pubin \

## 详细文档

请参阅 [references/details.md](references/details.md)
