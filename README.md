```markdown
# 🧮 Калькулятор чаевых  

Простое графическое приложение на Python для расчета чаевых с сохранением истории, экспортом данных и пересчетом в реальном времени.  

## 📋 Возможности  

✅ **Расчет чаевых и общей суммы**  
- Поддержка разных процентов чаевых (от 0% до 100%)  
- Мгновенный пересчет при изменении значений  

✅ **Разделение счета**  
- Можно указать количество человек, и приложение посчитает сумму с чаевыми на каждого  

✅ **Поддержка валют**  
- Рубли (руб.), доллары (USD), евро (EUR)  
- Учет курса обмена  

✅ **История расчетов**  
- Сохранение в **JSON**  
- Просмотр истории в отдельном окне  
- Экспорт в **CSV**  

✅ **Дополнительные функции**  
- Очистка формы  
- Переключение между светлой и темной темами  

## ⚙️ Установка и запуск  

1. **Убедитесь, что у вас установлен Python 3.8+**  
   ```bash
   python --version
   ```
   Если Python не установлен, скачайте его с [официального сайта](https://www.python.org/downloads/).  

2. **Установите зависимости**  
   ```bash
   pip install -r requirements.txt
   ```
   *(На самом деле, `tkinter` обычно уже установлен, но если возникают ошибки, см. раздел "Проблемы")*  

3. **Запустите приложение**  
   ```bash
   python tip_calc.py
   ```

## 📌 Пример использования  

1. Введите сумму счета, например, `1000`.  
2. Выберите процент чаевых (по умолчанию 10%).  
3. Если нужно разделить счет, поставьте галочку и укажите количество человек.  
4. Выберите валюту и курс (если считаете не в рублях).  
5. Нажмите **"Рассчитать"** — результат появится автоматически.  

## 📂 Файлы данных  

- **`tip_calc_history.json`** — история расчетов в JSON.  
- **`tip_calc_history.csv`** — создается после экспорта.  
- **`app.log`** — логи работы программы.  

## 🔧 Возможные проблемы  

### ❌ `ModuleNotFoundError: No module named 'tkinter'`  
- **Linux (Debian/Ubuntu):**  
  ```bash
  sudo apt-get install python3-tk
  ```  
- **Fedora:**  
  ```bash
  sudo dnf install python3-tkinter
  ```  
- **Windows/macOS:**  
  Должен быть установлен по умолчанию. Если нет — переустановите Python с галочкой **"Install Tkinter"**.  

### ❌ Приложение не запускается  
- Убедитесь, что файл `tip_calc.py` в той же папке, где вы запускаете программу.  
- Попробуйте переустановить зависимости:  
  ```bash
  pip install --force-reinstall -r requirements.txt
  ```  

## 📜 Лицензия  
MIT License — свободное использование и модификация.  
```


