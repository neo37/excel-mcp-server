import os
import re
from datetime import datetime
from typing import Optional

# Ordered from most specific to least specific
_PATTERNS = [
    # 2025-05-29_14-30-00 or 2025-05-29T14-30-00
    (r'(\d{4}-\d{2}-\d{2})[_T](\d{2}-\d{2}-\d{2})\b', lambda m: f"{m.group(1)} {m.group(2)}", "%Y-%m-%d %H-%M-%S"),
    # 2025-05-29_14-30
    (r'(\d{4}-\d{2}-\d{2})[_T](\d{2}-\d{2})\b', lambda m: f"{m.group(1)} {m.group(2)}", "%Y-%m-%d %H-%M"),
    # 2025-05-29
    (r'(\d{4}-\d{2}-\d{2})\b', lambda m: m.group(1), "%Y-%m-%d"),
    # 2025.05.29
    (r'(\d{4})\.(\d{2})\.(\d{2})\b', lambda m: f"{m.group(1)}-{m.group(2)}-{m.group(3)}", "%Y-%m-%d"),
    # 20250529_143000 or 20250529-143000
    (r'(\d{8})[_-](\d{6})\b', lambda m: f"{m.group(1)} {m.group(2)}", "%Y%m%d %H%M%S"),
    # 20250529_1430 or 20250529-1430
    (r'(\d{8})[_-](\d{4})\b', lambda m: f"{m.group(1)} {m.group(2)}", "%Y%m%d %H%M"),
    # 20250529
    (r'\b(\d{8})\b', lambda m: m.group(1), "%Y%m%d"),
]


def parse_datetime_from_filename(filename: str) -> Optional[datetime]:
    stem = os.path.splitext(os.path.basename(filename))[0]
    for pattern, extractor, fmt in _PATTERNS:
        m = re.search(pattern, stem)
        if m:
            try:
                return datetime.strptime(extractor(m), fmt)
            except ValueError:
                continue
    return None


def find_latest_excel_file(directory: str, pattern: Optional[str] = None) -> Optional[str]:
    """Return the filename (not full path) of the Excel file with the latest datetime in its name."""
    try:
        entries = os.listdir(directory)
    except OSError:
        return None

    candidates = []
    for name in entries:
        if not name.lower().endswith((".xlsx", ".xlsm", ".xls")):
            continue
        if pattern and pattern.lower() not in name.lower():
            continue
        dt = parse_datetime_from_filename(name)
        if dt:
            candidates.append((dt, name))

    if not candidates:
        return None

    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]
