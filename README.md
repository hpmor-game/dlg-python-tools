# dlg-python-tools
Набор утилит на Python для работы с диалоговыми файлами.

## Требования
- `python`
- `rich`
## Список утилит
- `parser.py`
Реализует класс `Parser` с методом `parse()`, который превращает `.dlg`-файл в словарь

**Использование:**
```python
from parser import Parser

parser = Parser()
dialogue = parser.parse("dialogues/alice_bob_calse.dlg")

print("В этом диалоге", len(dialogue["marks"]), "бранчей")
```

- `printer.py`
Печатает диалог из `.dlg`-файла в консоль с оформлением

**Использование:**
```bash
$ python printer.py dialogues/alice_bob_case.dlg
Алиса, зевая, заходит в комнату Боба

🥱 Алиса
Привет, Боб!

😀 Алиса
Сегодня такой хороший день!
С самого утра я чувствую воодушение и
радость!
...
```

- `player.py`
Проигрывает диалог в консоли

- `dlg2json.py`
Конвертирует `.dlg` в `.json`

**Использование:**
```bash
$ python dlg2json.py dialogues/alice_bob_case.dlg test.json
File has been saved as test.json
```

- `dlg2ron.py`
Конвертирует `.dlg` в `.ron`

## Дополнительно
- `characters.csv` хранит информацию о персонажах для проигрывания (alias,name,color)
- `dialogues` — директория с `.dlg`-файлами для вывода


## Спецификации
Парсер использует спецификацию `.dlg` из [hpmor#8](https://github.com/hpmor-game/hpmor/issues/8). Также в выводе поддерживается BBCode.

### Синтаксис
Для написания диалога используются спецстмволы в начале строки.
- `@` — обьявление говорящего
**Использование:**
```js
@alias:emotion //Начало реплики персонажа alias с эмоцией
```
- `:` — начало команды
  - `:menu` — создаёт меню из последующих команд `opt`
  - `:opt(#mark)` — добавляет опцию, отправляющую в бранч `#mark`

- `#` — начало бранча

Также `//` делает весь последующий текст в строке комментарием

### BBCode

При использовании `printer.py` и `player.py` доступно форматирование BBCode, встроенное в модуль `rich`. Доступные теги:

- ``b`` жирный
- ``i`` курсив
- ``r`` инверсия с фоном
- ``s`` зачёркнутый
- ``u`` подчёркнутый
- ``#``-код или имя из [этого списка](https://rich.readthedocs.io/en/stable/appendix/colors.html?highlight=color) изменяет цвет
