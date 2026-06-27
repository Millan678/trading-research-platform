"""Storage — SQLite + JSON mirror with PG graceful fallback."""
import hashlib, json, os, sqlite3
from datetime import datetime
from typing import Any, Dict, List, Optional


class Storage:
    def __init__(self, base_dir: str, pg_url: Optional[str] = None):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)
        self.db_path = os.path.join(base_dir, "verification.db")
        self.json_dir = os.path.join(base_dir, "json_mirror")
        os.makedirs(self.json_dir, exist_ok=True)
        self.pg_url = pg_url
        self._pg_available = False
        self._init_sqlite()

    def _init_sqlite(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS records "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "category TEXT, record_type TEXT, data TEXT, "
                "sha256 TEXT, created_at TEXT)"
            )

    def append(self, category: str, record_type: str, data: dict) -> dict:
        serialized = json.dumps(data, sort_keys=True, default=str)
        sha = hashlib.sha256(serialized.encode()).hexdigest()
        ts = datetime.utcnow().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO records (category, record_type, data, sha256, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (category, record_type, serialized, sha, ts),
            )
        cat_dir = os.path.join(self.json_dir, category)
        os.makedirs(cat_dir, exist_ok=True)
        existing = []
        if os.path.isfile(os.path.join(cat_dir, f"{record_type}.json")):
            with open(os.path.join(cat_dir, f"{record_type}.json")) as f:
                existing = json.load(f)
        entry = {"data": data, "sha256": sha, "created_at": ts}
        existing.append(entry)
        with open(os.path.join(cat_dir, f"{record_type}.json"), "w") as f:
            json.dump(existing, f, indent=2, default=str)
        return {"sha256": sha, "appended": True}

    def read(self, category: str) -> list:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT data FROM records WHERE category = ? ORDER BY id",
                (category,),
            ).fetchall()
        return [json.loads(r[0]) for r in rows]

    def try_postgresql(self) -> dict:
        if not self.pg_url:
            return {"status": "graceful_fallback", "reason": "no_pg_url"}
        try:
            import psycopg2
            conn = psycopg2.connect(self.pg_url)
            conn.close()
            self._pg_available = True
            return {"status": "available"}
        except Exception as e:
            return {"status": "graceful_fallback", "reason": str(e)}
