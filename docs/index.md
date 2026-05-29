# Excel MCP Server

MCP-сервер для работы с Excel-файлами через AI-агентов (Claude и др.).  
Форк [haris-musa/excel-mcp-server](https://github.com/haris-musa/excel-mcp-server) с поддержкой Docker и инструментом автопоиска файлов по дате.

---

## Быстрый старт

```bash
git clone https://github.com/neo37/excel-mcp-server.git
cd excel-mcp-server
mkdir excel-files
docker compose up -d
```

MCP-эндпоинт: `http://localhost:8080/mcp`  
Файлы: `http://localhost:8080/files/`

---

## Подключение к Claude Code

Добавьте в `.claude/settings.json` проекта и закоммитьте — вся команда получит доступ автоматически:

```json
{
  "mcpServers": {
    "excel": {
      "url": "http://YOUR_SERVER_IP:8080/mcp",
      "type": "http"
    }
  }
}
```

---

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `EXCEL_FILES_PATH` | `/data` | Путь к папке с Excel-файлами внутри контейнера |
| `FASTMCP_PORT` | `8017` | Внутренний порт MCP-сервера |
| `EXCEL_SERVER_URL` | — | Внешний URL сервера для генерации ссылок на файлы |

---

## Инструменты

### `get_latest_excel_file` ✨ новый

Находит Excel-файл с наиболее поздней датой в имени и возвращает имя файла и ссылку для скачивания.

**Параметры:**
- `pattern` *(опционально)* — подстрока для фильтрации, например `"report"` или `"export"`

**Пример ответа:**
```
Latest Excel file: sales_report_2025-05-29_14-30.xlsx
Download URL: http://your-server:8080/files/sales_report_2025-05-29_14-30.xlsx
Use filepath 'sales_report_2025-05-29_14-30.xlsx' with other Excel tools.
```

**Поддерживаемые форматы дат в имени файла:**

| Пример имени | Формат |
|---|---|
| `report_2025-05-29.xlsx` | ISO дата |
| `export_2025-05-29_14-30.xlsx` | ISO дата + время |
| `data_20250529.xlsx` | Компактная дата |
| `file_20250529_143000.xlsx` | Компактная дата + время |
| `doc_2025.05.29.xlsx` | Дата с точками |

После получения имени файла используйте его напрямую в других инструментах:
`read_data_from_excel`, `write_data_to_excel`, `get_workbook_metadata` и др.

---

## Системный промт для Claude

Чтобы Claude автоматически использовал сервер при работе с таблицами, добавьте в системный промт:

```
Для любых задач с Excel-файлами используй MCP-инструменты excel-сервера.
Перед работой с файлом вызови get_latest_excel_file (с нужным pattern если известен),
чтобы получить актуальное имя файла — оно содержит дату и может меняться.
```

---

## Структура

```
excel-mcp-server/
├── Dockerfile
├── docker-compose.yml
├── nginx.conf                  # проксирует /mcp и раздаёт /files/
└── src/excel_mcp/
    ├── server.py               # все MCP-инструменты
    ├── file_link.py            # парсинг datetime из имён файлов
    └── ...
```

---

## Полный список инструментов

| Инструмент | Описание |
|---|---|
| `get_latest_excel_file` | Найти файл с последней датой в имени |
| `read_data_from_excel` | Прочитать данные из диапазона |
| `write_data_to_excel` | Записать данные |
| `create_workbook` | Создать новый файл |
| `create_worksheet` | Создать лист |
| `apply_formula` | Применить формулу |
| `format_range` | Форматирование ячеек |
| `create_chart` | Создать график |
| `create_pivot_table` | Сводная таблица |
| `create_table` | Таблица Excel |
| `get_workbook_metadata` | Метаданные файла |
| `insert_rows` / `delete_rows` | Вставка/удаление строк |
| `insert_columns` / `delete_columns` | Вставка/удаление столбцов |
| `merge_cells` / `unmerge_cells` | Объединение ячеек |
| `copy_worksheet` / `delete_worksheet` | Операции с листами |
