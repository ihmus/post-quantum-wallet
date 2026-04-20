from mnemonic import Mnemonic

# ---------------------------
# 1️⃣ 12 Kelimelik Seed Üretimi
# ---------------------------
mnemo = Mnemonic("english")
seed_phrase = mnemo.generate(strength=128)  # 12 kelime
seed_bytes = mnemo.to_seed(seed_phrase)

print("Seed Phrase:", seed_phrase)
print("Seed (bytes):", seed_bytes.hex()[:64], "...")  # uzun, baştan 64 karakter göster
