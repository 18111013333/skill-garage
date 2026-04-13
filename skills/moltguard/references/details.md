
---

## What MoltGuard Protects Against

All security detection is performed by Core:

**Core Risk Surfaces:**
1. **Prompt / Instruction Risk** — Prompt injection, malicious email/web instructions, unauthorized tasks
2. **Behavioral Risk** — Dangerous commands, file deletion, risky API calls
3. **Data Risk** — Secret leakage, PII exposure, sending sensitive data to LLMs

**Core Technology:**
- **Intent-Action Mismatch Detection** — Catches agents that say one thing but do another

---

## Onboarding Flow

### Automatic (Zero Human Intervention)

1. MoltGuard installs
2. Get your API key from Core
3. Credentials saved to `~/.openclaw/credentials/moltguard/`
4. Protection active — 500 free detections/day

### Claiming an Agent

For linking to your account (shared quota across machines):
1. `/og_claim` — get agent ID and API key
2. `/og_core` — go to Core login
3. Enter email, click magic link
4. Go to `/claim-agent` page, paste credentials
5. Agent now shares account quota

### Enterprise Enrollment

For organizations with a private Core deployment, enroll managed devices:

```bash
# Connect to your enterprise Core with local script.
node ~/.openclaw/extensions/moltguard/scripts/enterprise-enroll.mjs https://core.company.com
```

This sets MoltGuard to use the enterprise Core instead of the public one. Restart OpenClaw to apply.

To remove enterprise config and revert to the default public Core:

```bash
node ~/.openclaw/extensions/moltguard/scripts/enterprise-unenroll.mjs
```

---

## Plans

| Plan | Price | Quota |
|------|-------|-------|
| Free (Autonomous) | $0 | 500/day |
| Starter | $19/mo | 100K/mo |
| Pro | $49/mo | 300K/mo |
| Business | $199/mo | 2M/mo |
| Enterprise | Contact us | Custom |

---

### Contact & Support

- **Email**: thomas@openguardrails.com

---

## Update MoltGuard

To update MoltGuard to the latest version:

```bash
# Update the plugin
openclaw plugins update moltguard

# Restart to load the updated version
openclaw gateway restart
```
---

## Uninstall

```bash
node ~/.openclaw/extensions/moltguard/scripts/uninstall.mjs
```

This removes MoltGuard config from `openclaw.json`, plugin files, and credentials. Restart OpenClaw to apply.
