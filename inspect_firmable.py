import subprocess

ZSTD = r"C:\Users\hp\AppData\Local\Microsoft\WinGet\Packages\Meta.Zstandard_Microsoft.Winget.Source_8wekyb3d8bbwe\zstd-v1.5.7-win64\zstd.exe"
DATASET = r"C:\Users\hp\firmable_dataset.zst"

print("Starting dataset inspection...")
print("Reading first 64 KB only...\n")

process = subprocess.Popen(
    [ZSTD, "-dc", DATASET],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

sample = process.stdout.read(64 * 1024)

process.kill()

print("========== DATASET PREVIEW ==========\n")

try:
    print(sample.decode("utf-8", errors="replace"))
except Exception as e:
    print(f"Could not decode preview: {e}")

print("\n========== END PREVIEW ==========")
print(f"\nBytes inspected: {len(sample):,}")