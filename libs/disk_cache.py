import os
from datetime import timedelta, datetime
from typing import Optional


class DiskCache:
    def __init__(self, base_path: str, age_limit: Optional[timedelta] = None):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        self.age_limit = age_limit

    def exists(self, path: str) -> bool:
        return os.path.exists(f"{self.base_path}/{path}")

    def put(self, path: str, buf: bytes):
        os.makedirs(f"{self.base_path}{os.path.dirname(path)}", exist_ok=True)
        with open(f"{self.base_path}{path}", "wb") as fp:
            fp.write(buf)

    def get(self, path: str) -> Optional[bytes]:
        if not os.path.exists(f"{self.base_path}{path}"):
            return None
        if (
            self.age_limit
            and datetime.fromtimestamp(
                os.path.getmtime(f"{self.base_path}{path}")
            )
            + self.age_limit
            < datetime.now()
        ):
            os.remove(f"{self.base_path}{path}")
            return None
        with open(f"{self.base_path}{path}", "rb") as fp:
            return fp.read()
