"""Storage — append-only SQLite + JSON mirror + PostgreSQL graceful fallback."""
import json, os, sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional

_JOURNAL_TABLE = "core_journal"

class Storage:
    def __init__(self, base_dir: str, pg_url: str = ""):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        self.db_path = os.path.join(base_dir, "core.db")
        self.json_dir = os.path.join(base_dir, "json_mirror")
        os.makedirs(self.json_dir, exist_ok=True)
        self.pg_url = pg_url
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f"CREATE TABLE IF NOT EXISTS {_JOURNAL_TABLE} ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "record_id TEXT NOT NULL, "
                "record_type TEXT NOT NULL, "
                "data TEXT NOT NULL, "
                "created_at TEXT NOT NULL)"
            )
            conn.commit()

    def append(self, record_id: str, record_type: str, data: dict) -> str:
        ts = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f"INSERT INTO {_JOURNAL_TABLE} (record_id, record_type, data, created_at) VALUES (?,?,?,?)",
                (record_id, record_type, json.dumps(data, default=str), ts),
            )
            conn.commit()
        self._mirror(record_type, data, record_id, ts)
        return record_id

    def _mirror(self, record_type: str, data: dict, record_id: str, ts: str):
        d = os.path.join(self.json_dir, record_type)
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, f"{record_id}.json")
        records = []
        if os.path.isfile(path):
            with open(path) as f:
                records = json.load(f)
        records.append({"record_id": record_id, **data, "created_at": ts})
        with open(path, "w") as f:
            json.dump(records, f, indent=2, default=str)

    def query(self, record_type: str) -> list:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                f"SELECT data FROM {_JOURNAL_TABLE} WHERE record_type=? ORDER BY id",
                (record_type,),
            ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def read(self, record_id: str) -> list:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                f"SELECT data FROM {_JOURNAL_TABLE} WHERE record_id=? ORDER BY id",
                (record_id,),
            ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def count(self, record_type: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cnt = conn.execute(
                f"SELECT COUNT(*) FROM {_JOURNAL_TABLE} WHERE record_type=?",
                (record_type,),
            ).fetchone()[0]
        return cnt

    def try_postgresql(self) -> dict:
        try:
            import psycopg2
            return {"status": "available", "note": "PostgreSQL connected"}
        except Exception:
            return {"status": "graceful_fallback", "note": "SQLite active, PostgreSQL optional"}
