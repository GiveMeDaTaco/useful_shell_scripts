# Waterfall Manager

A lightweight utility for **versioning small data extracts** as *waterfall* reports and comparing them over time.  Each extract is stored in a local SQLite database under your project directory, and the library can automatically build an **Excel comparison** between the most‑recent snapshot and an historic snapshot *N* days in the past.

---

## Features

|                           | Capability                                                                                                                                       |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 📁 **Self‑contained**     | Creates a `waterfall/` sub‑folder inside your project with both the database (`waterfall.db`) and generated Excel files.                         |
| 📊 **Snapshot ingest**    | `add_report()` pulls data from any SQL source (via an existing DB‑API connection), validates its two‑column schema, and saves it as a new table. |
| 🗓️ **Report catalogue**  | All snapshots are registered in an `available_reports` table with timestamp metadata for easy lookup.                                            |
| 📈 **Time‑based compare** | `generate_report(days=N)` selects the latest snapshot + the snapshot closest to *N* days ago and creates a row‑aligned Excel file.               |
| 📥 **Simple API**         | One class — `WaterfallManager` — covers directory bootstrap, ingest, listing, and report generation.                                             |

---

## Installation

```bash
python -m pip install pandas xlsxwriter
```

*Python 3.9 + is recommended.*

There are **no external system dependencies** – SQLite is part of Python’s standard library.

---

## Quick‑start

```python
from waterfall_manager import WaterfallManager
import sqlite3

# 1 – point the manager at your project directory
wm = WaterfallManager("/path/to/my/project")

# 2 – ingest a new snapshot from a source database
src = sqlite3.connect("/path/to/source.db")  # any DB‑API connection works
wm.add_report(src_conn=src,
              schema_table="myschema.mytable",  # must have sortbad / cntr cols
              offer_code="OFFER123")

# 3 – create an Excel comparison between the newest snapshot and the snapshot
#     closest to 3 days ago (if available)
report_path = wm.generate_report(days=3)
print("Excel saved to", report_path)
```

> **Note** – If only one snapshot exists the comparison report will contain that snapshot alone.

---

## Data requirements

Each source table **must** contain exactly two columns:

| Column    | Type     | Notes                                                              |
| --------- | -------- | ------------------------------------------------------------------ |
| `sortbad` | *string* | Treated as a free‑form identifier; stored as TEXT.                 |
| `cntr`    | *int*    | Counts / metric; floats that are whole numbers are coerced to int. |

No additional columns are allowed – validation will raise `ColumnValidationError`.

---

## Output format

The Excel sheet (`report` tab) has four columns:

1. **Historic `sortbad`**   (snapshot closest to *N* days ago)
2. **Recent `sortbad`**     (latest snapshot)
3. **Historic `cntr`**
4. **Recent `cntr`**

Row‑alignment rules:

* If the same `sortbad` value occurs in the **same row index** in both snapshots → data share one row.
* Otherwise each unmatched row is written on its own line, preserving original order.

The column headers are automatically labelled with the originating table names so you can trace the provenance of each column.

---

## API reference

```python
class WaterfallManager(project_dir: str | Path):
    add_report(src_conn, schema_table: str, offer_code: str) -> str
        """Snapshot ingest and registration."""

    generate_report(days: int, output_path: str | Path | None = None) -> Path
        """Build Excel comparison; returns file path."""

    list_reports() -> list[tuple[id, table_name, created_ts]]
        """Utility for introspection / debugging."""
```

### Exceptions

* **`ColumnValidationError`** – source table schema is incorrect.
* **`NoReportsError`** – `generate_report()` called before any snapshots exist.

---

## Development

1. Clone the repo & create a virtual environment.
2. `pip install -r requirements-dev.txt` (flake8, mypy, pytest, etc.).
3. Run tests with `pytest`.

A basic *pytest* suite lives in `tests/` and uses temporary directories + SQLite in‑memory connections.

---

## Roadmap

* **CLI wrapper** (`python -m waterfall_manager …`)
* **Automatic diff metrics** (added / removed / changed counts)
* **Custom join keys** (support multi‑column primary keys)
* **Parquet + CSV export** in addition to Excel

---
