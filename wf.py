from __future__ import annotations

"""waterfall_manager.py

Utility for managing *waterfall*‑style reporting inside a project directory.

Phase 1 (initial commit) implemented:
• directory / database bootstrap
• metadata table ``available_reports``
• :py:meth:`WaterfallManager.add_report` – ingest new report tables

Phase 2 (this revision) adds:
• :py:meth:`WaterfallManager.generate_report` – build a row‑aligned Excel
  comparison between the most‑recent report and a historical report closest to
  *N* days in the past.
"""

from pathlib import Path
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any, List, Tuple

import pandas as pd

__all__ = ["WaterfallManager", "ColumnValidationError", "NoReportsError"]


class ColumnValidationError(ValueError):
    """Raised when the source table does not match the required schema."""


class NoReportsError(RuntimeError):
    """Raised when *generate_report* is invoked but no reports exist."""


class WaterfallManager:
    """Manage a local *waterfall* SQLite database and its reports."""

    REQUIRED_COLUMNS: set[str] = {"sortbad", "cntr"}

    # ---------------------------------------------------------------------
    # constructor / bootstrap
    # ---------------------------------------------------------------------
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir).expanduser().resolve()
        self.waterfall_dir = self.project_dir / "waterfall"
        self.waterfall_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = self.waterfall_dir / "waterfall.db"
        self._init_db()

    # ------------------------------------------------------------------
    # PUBLIC API – PHASE 1
    # ------------------------------------------------------------------
    def add_report(
        self,
        src_conn: "sqlite3.Connection | Any",
        schema_table: str,
        offer_code: str,
    ) -> str:
        """Ingest a source table and register it as a new report."""
        df = self._fetch_source(src_conn, schema_table)
        self._validate_dataframe(df)
        df = self._coerce_types(df)

        target_name = self._generate_table_name(offer_code)
        self._write_report_table(df, target_name)
        self._register_report(target_name)
        return target_name

    # ------------------------------------------------------------------
    # PUBLIC API – PHASE 2
    # ------------------------------------------------------------------
    def generate_report(
        self,
        days: int,
        output_path: str | Path | None = None,
    ) -> Path:
        """Create an Excel comparison report.

        Parameters
        ----------
        days
            Number of *days* to look back when selecting the historical report
            (closest absolute difference to *now − days*).
        output_path, optional
            Target filename for the XLSX file; defaults to something like
            ``waterfall_report_3d_20250520_193700.xlsx`` under the *waterfall*
            directory.

        Returns
        -------
        Path
            The path to the XLSX file written.
        """
        reports = self._list_reports_with_dt()
        if not reports:
            raise NoReportsError("No reports are available in the database.")

        # Sort newest → oldest
        reports.sort(key=lambda r: r[2], reverse=True)
        most_recent = reports[0]

        if len(reports) == 1:
            historic = None
        else:
            target_dt = datetime.now(timezone.utc) - timedelta(days=days)
            # pick report (not necessarily distinct yet) with smallest |Δt|
            historic = min(
                reports,
                key=lambda r: abs(r[2] - target_dt),
            )
            # Ensure historic differs from most_recent if possible
            if historic[0] == most_recent[0] and len(reports) >= 2:
                historic = reports[1]
            if historic[0] == most_recent[0]:
                historic = None  # still only one unique report

        # Load dataframes from SQLite
        with sqlite3.connect(self.db_path) as conn:
            recent_df = pd.read_sql(f"SELECT * FROM {most_recent[1]}", conn)
            historic_df = (
                pd.read_sql(f"SELECT * FROM {historic[1]}", conn)
                if historic is not None
                else None
            )

        # Build comparison DataFrame
        report_df = self._build_aligned_dataframe(historic_df, recent_df)

        # Write Excel
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        default_name = f"waterfall_report_{days}d_{ts}.xlsx"
        dest = Path(output_path) if output_path else self.waterfall_dir / default_name

        dest.parent.mkdir(parents=True, exist_ok=True)
        with pd.ExcelWriter(dest, engine="xlsxwriter") as writer:
            report_df.to_excel(writer, index=False, sheet_name="report")
        return dest

    # ------------------------------------------------------------------
    # INTERNAL HELPERS (phase 2)
    # ------------------------------------------------------------------
    def _list_reports_with_dt(self) -> List[Tuple[int, str, datetime]]:
        """Return [(id, table_name, created_timestamp as dt), …]."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, table_name, created_timestamp FROM available_reports"
            ).fetchall()
        result: List[Tuple[int, str, datetime]] = []
        for rid, tname, ts in rows:
            try:
                result.append((rid, tname, datetime.fromisoformat(ts).astimezone(timezone.utc)))
            except ValueError:
                continue  # skip bad rows silently
        return result

    # .................................................................
    def _build_aligned_dataframe(
        self,
        hist_df: pd.DataFrame | None,
        recent_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Align two datasets row‑by‑row per spec and return a combined DF."""

        # Guarantee sortbad/cntr order is preserved as in original ingest.
        rec_vals = recent_df["sortbad"].tolist()
        rec_cntr = recent_df["cntr"].tolist()

        if hist_df is not None:
            hist_vals = hist_df["sortbad"].tolist()
            hist_cntr = hist_df["cntr"].tolist()
        else:
            hist_vals, hist_cntr = [], []

        out_records: list[list[Any]] = []

        max_len = max(len(hist_vals), len(rec_vals))
        for idx in range(max_len):
            h_val = hist_vals[idx] if idx < len(hist_vals) else None
            r_val = rec_vals[idx] if idx < len(rec_vals) else None
            h_cntr = hist_cntr[idx] if idx < len(hist_cntr) else None
            r_cntr = rec_cntr[idx] if idx < len(rec_cntr) else None

            # Case 1: both present and equal – join same row
            if h_val is not None and r_val is not None and h_val == r_val:
                out_records.append([h_val, r_val, h_cntr, r_cntr])
            else:
                # If historic row exists – write it on its own
                if h_val is not None:
                    out_records.append([h_val, None, h_cntr, None])
                # If recent row exists – write it on a new row
                if r_val is not None:
                    out_records.append([None, r_val, None, r_cntr])

        col1_header = hist_df.attrs.get("table_name") if hist_df is not None else "historic"
        col2_header = recent_df.attrs.get("table_name", "recent")

        df_out = pd.DataFrame(out_records, columns=[col1_header, col2_header, "cntr_hist", "cntr_recent"])
        return df_out

    # ------------------------------------------------------------------
    # INTERNAL HELPERS – PHASE 1 (unchanged)
    # ------------------------------------------------------------------
    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS available_reports (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_name       TEXT    NOT NULL UNIQUE,
                    created_timestamp TEXT   NOT NULL
                )
                """
            )
            conn.commit()

    # .................................................................
    def _fetch_source(self, src_conn: Any, schema_table: str) -> pd.DataFrame:
        query = f"SELECT * FROM {schema_table}"
        return pd.read_sql(query, src_conn)

    # .................................................................
    def _validate_dataframe(self, df: pd.DataFrame) -> None:
        if set(df.columns) != self.REQUIRED_COLUMNS:
            raise ColumnValidationError(
                "Source table must contain only the columns "
                f"{sorted(self.REQUIRED_COLUMNS)}; received {sorted(df.columns)}."
            )

    # .................................................................
    def _coerce_types(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["sortbad"] = df["sortbad"].astype(str)

        def _to_int(val):
            if pd.isna(val):
                return None
            if isinstance(val, int):
                return val
            if isinstance(val, float):
                iv = int(val)
                if iv == val:
                    return iv
            raise ValueError(f"Cannot coerce value '{val}' to int.")

        df["cntr"] = df["cntr"].apply(_to_int)
        return df

    # .................................................................
    def _generate_table_name(self, offer_code: str) -> str:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        safe_offer = offer_code.strip().upper().replace(" ", "_")
        return f"{safe_offer}_{ts}"

    # .................................................................
    def _write_report_table(self, df: pd.DataFrame, table_name: str) -> None:
        # Store originating table name for downstream metadata (attrs)
        df = df.copy()
        df.attrs["table_name"] = table_name
        with sqlite3.connect(self.db_path) as conn:
            df.to_sql(table_name, conn, index=False, if_exists="fail")

    # .................................................................
    def _register_report(self, table_name: str) -> None:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO available_reports (table_name, created_timestamp) "
                "VALUES (?, ?)",
                (table_name, ts),
            )
            conn.commit()

    # ------------------------------------------------------------------
    # Utility – list reports (unchanged signature)
    # ------------------------------------------------------------------
    def list_reports(self) -> list[tuple[int, str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute(
                "SELECT id, table_name, created_timestamp FROM available_reports"
            ).fetchall()
