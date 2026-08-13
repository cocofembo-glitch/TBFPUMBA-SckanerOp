# 🔥 TBFPUMBA-SckanerOp v7.0 PRO

<p align="center">
  <img src="https://img.shields.io/badge/License-GPLv3-brightgreen.svg" alt="GPLv3 License">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Platform-Termux%20%7C%20Linux-orange.svg" alt="Platform">
  <img src="https://img.shields.io/badge/UI-Rich%20%2F%20Cyberpunk-magenta.svg" alt="UI Style">
</p>

> **Technology. Security. Efficiency.**  
> Мощный CLI-сканер безопасности и антивирус для **Termux** и **Linux**, предназначенный для глубокого анализа файлов, APK-пакетов, опасных скриптов и мгновенного удаления угроз.

---

## ✨ Основные возможности (Features)

- 🌍 **Мультиязычность (i18n):** Встроенная поддержка Украинского, Русского и Английского языков с переключением через `TBF++`.
- 📦 **Глубокий APK-анализ:** Инспекция Android-приложений (подозрительные разрешения, размеры файлов и имена пакетов через `aapt`).
- 🔍 **Эвристический & Сигнатурный движок:** Детект опасных команд (`rm -rf`, `eval`, `exec`, reverse shell, exploit payloads и др.).
- 🛡️ **Проверка исполняемых прав:** Поиск подозрительных исполняемых файлов без стандартных расширений.
- 🗑️ **Безопасная очистка (Threat Remover):** Мгновенное удаление обнаруженных угроз по команде `-TBF`.
- 🎨 **Rich Cyberpunk UI:** Интерактивные таблицы, прогресс-бары в реальном времени и неоновая стилизация.

---

## 🚀 Быстрый запуск (Quick Start)

Запусти одну команду в **Termux / Linux**, чтобы установить зависимости и сразу запустить сканер:

```bash
git clone [https://github.com/cocofembo-glitch/TBFPUMBA-SckanerOp.git](https://github.com/cocofembo-glitch/TBFPUMBA-SckanerOp.git) && cd TBFPUMBA-SckanerOp && pip install -r requirements.txt && python tbfpumba_scan.py

