import os
import sys

print("🔥 TBFPUMBA-SckanerOp v1.0 🔥")
print("⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡")
print("========================================")

SUSPICIOUS_PATTERNS = [
    "rm -rf",
    "format",
    "delete_all",
    "malware",
    "virus"
]

def scan_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in content:
                    return True, pattern
    except Exception:
        pass
    return False, None

def scan_folder(path):
    suspicious_files = []
    print(f"🔍 Сканування папки: {path}")
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith(('.txt', '.sh', '.py', '.js')):
                is_suspicious, pattern = scan_file(filepath)
                if is_suspicious:
                    suspicious_files.append((filepath, pattern))
                    print(f"⚠️ ПІДОЗРІЛИЙ ФАЙЛ: {filepath} (знайдено: '{pattern}')")
    return suspicious_files

if __name__ == "__main__":
    target_path = os.path.expanduser("~")
    results = scan_folder(target_path)

    if results:
        print("\n🚨 Список підозрілих файлів:")
        for file, pattern in results:
            print(f"  - {file} (патерн: {pattern})")
    else:
        print("\n✅ Підозрілих файлів не знайдено.")
