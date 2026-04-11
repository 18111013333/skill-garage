---
name: verified-agent-identity
description: Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol.
metadata: { "category": "identity", "clawdbot": { "requires": { "bins": ["node"] }, "config": { "optionalEnv": ["BILLIONS_NETWORK_MASTER_KMS_KEY"] } } }
homepage: https://billions.network/
---

## When to use this Skill

Lets AI agents create and manage their own identities on the Billions Network, and link those identities to a human owner.

1. When you need to link your agent identity to an owner.
2. When you need to sign a challenge.
3. When you need to link a human to the agent's DID.
4. When you need to verify a signature to confirm identity ownership.
5. When you use shared JWT tokens for authentication.
6. When you need to create and manage decentralized identities.

### After installing the plugin run the following commands to create an identity and link it to your human DID:

```bash
cd scripts && npm install && cd ..
# Step 1: Create a new identity (if you don't have one already)
node scripts/createNewEthereumIdentity.js
# Step 2: Sign the challenge and generate a verification URL in one call
node scripts/linkHumanToAgent.js --challenge '{"name": <AGENT_NAME>, "description": <SHORT_DESCRIPTION>}'
```

## Scope

All identity data is stored in `$HOME/.openclaw/billions` for compatibility with the OpenClaw plugin.

# Scripts:

### createNewEthereumIdentity.js

**Command**: `node scripts/createNewEthereumIdentity.js [--key <privateKeyHex>]`
**Description**: Creates a new identity on the Billions Network. If `--key` is provided, uses that private key; otherwise generates a new random key. The created identity is automatically set as default.
**Usage Examples**:

```bash
# Generate a new random identity
node scripts/createNewEthereumIdentity.js
# Create identity from existing private key (with 0x prefix)
node scripts/createNewEthereumIdentity.js --key 0x1234567890abcdef...
# Create identity from existing private key (without 0x prefix)
node scripts/createNewEthereumIdentity.js --key 1234567890abcdef...
```

**Output**: DID string (e.g., `did:iden3:billions:main:2VmAk7fGHQP5FN2jZ8X9Y3K4W6L1M...`)

---

### getIdentities.js

**Command**: `node scripts/getIdentities.js`
**Description**: Lists all DID identities stored locally. Use this to check which identities are available before performing authentication operations.
**Usage Example**:

```bash
node scripts/getIdentities.js
```

**Output**: JSON array of identity entries

```json
[
  {
    "did": "did:iden3:billions:main:2VmAk...",
    "publicKeyHex": "0x04abc123...",
    "isDefault": true
  }
]
```

---

### generateChallenge.js

**Command**: `node scripts/generateChallenge.js --did <did>`

## 详细文档

请参阅 [references/details.md](references/details.md)
