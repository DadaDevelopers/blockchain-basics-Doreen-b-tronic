import hashlib

# -------------------------------
# Step 1: Transaction Hashes
# -------------------------------
tx_hashes = [
    "75dd9121f42c14e4ce80e6bcb595519b493e370eafc1c7f2ab7337e483d153ea",
    "53d3260bab208080c43de4b5b12f0a4bfe9f72ce5425fac985ae154659bb8bd9",
    "90ffb5696bcaab70eee7fc53f3e8ed23972adfadaad1b291c1bbf78bd253798c",
    "ba6673df7938b93da81579eb6e0412a9120b64fe6861421d4775a22be7eb9f08"
]

# -------------------------------
# Step 2: Double SHA256 Function
# -------------------------------
def double_sha256(data: bytes) -> bytes:
    """Perform Bitcoin-style double SHA256 hashing"""
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

# -------------------------------
# Step 3: Build the Merkle Tree
# -------------------------------
def build_merkle_root(txids):
    """Builds the Merkle tree and returns the root + intermediate hashes"""
    level0 = [bytes.fromhex(txid) for txid in txids]
    hash_ab = double_sha256(level0[0] + level0[1])
    hash_cd = double_sha256(level0[2] + level0[3])
    merkle_root = double_sha256(hash_ab + hash_cd)
    return {
        "level0": [h.hex() for h in level0],
        "hash_ab": hash_ab.hex(),
        "hash_cd": hash_cd.hex(),
        "merkle_root": merkle_root.hex(),
    }

# -------------------------------
# Step 4: Run and Save Documentation
# -------------------------------
result = build_merkle_root(tx_hashes)

steps = f"""
Merkle Root Calculation - Step by Step
======================================

Transaction Hashes (Leaves):
1. {result['level0'][0]}
2. {result['level0'][1]}
3. {result['level0'][2]}
4. {result['level0'][3]}

Step 1: Pair Transactions
- Pair AB = Tx1 + Tx2
- Pair CD = Tx3 + Tx4

Step 2: Double SHA256 of Each Pair
- Hash(AB) = double_sha256(Tx1 || Tx2)
  => {result['hash_ab']}
- Hash(CD) = double_sha256(Tx3 || Tx4)
  => {result['hash_cd']}

Step 3: Combine and Double SHA256 for Root
- Concatenate: Hash(AB) + Hash(CD)
- Merkle Root = double_sha256(Hash(AB) || Hash(CD))
  => {result['merkle_root']}
"""

with open("merkle_steps.txt", "w") as f:
    f.write(steps)

# -------------------------------
# Step 5: Summary Output
# -------------------------------
print("✅ Merkle root calculation complete!")
print("🧾 Detailed steps saved to: merkle_steps.txt")
print(f"🔗 Merkle Root: {result['merkle_root']}")

