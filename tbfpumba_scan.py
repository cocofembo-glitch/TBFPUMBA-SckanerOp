#!/data/data/com.termux/files/usr/bin/bash
import os
import sys
import time

# ============================================
#   TBFPUMBA-SckanerOp v2.0
#   by TBFPUMBA — Technology. Security. Efficiency.
# ============================================

def loading_animation():
    print("\n🔍 Ініціалізація сканера TBFPUMBA...")
    for i in range(101):
        time.sleep(0.02)
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
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in content:
                    return True, pattern
    except Exception:
        pass
    return False, None

def scan_folder(path):
    suspicious_files = []
    print(f"\n📂 Сканування папки: {path}\n")
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            if filepath == os.path.realpath(__file__):
                continue
            if file.endswith(('.txt', '.sh', '.py', '.js', '.c', '.cpp')):
                is_suspicious, pattern = scan_file(filepath)
                if is_suspicious:
                    suspicious_files.append((filepath, pattern))
                    print(f"⚠️ ПІДОЗРІЛИЙ ФАЙЛ: {filepath} (знайдено: '{pattern}')")
    return suspicious_files

if __name__ == "__main__":
    os.system('clear')
    print("🔥 TBFPUMBA-SckanerOp v2.0 🔥")
    print("⚡ by TBFPUMBA — Technology. Security. Efficiency. ⚡")
    print("========================================")
    
    loading_animation()
    if not ask_user():
        sys.exit()
    
    target_path = os.path.expanduser("~")
    results = scan_folder(target_path)
    
    if results:
        print("\n🚨 Список підозрілих файлів:")
        for file, pattern in results:
            print(f"  - {file} (патерн: {pattern})")
        print("\n⚠️ Рекомендується перевірити ці файли вручну.")
    else:
        print("\n✅ Підозрілих файлів не знайдено. Ваша система чиста!")
    
    print("\n🔒 Сканування завершено. Дякуємо, що використовуєте TBFPUMBA-SckanerOp!")
