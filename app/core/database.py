import json
import os
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.models.faq import FAQ, QueryLog
import asyncio

class DatabaseInterface:
    async def connect(self): pass
    async def disconnect(self): pass
    async def get_all_faqs(self) -> List[FAQ]: pass
    async def get_faq(self, id: str) -> Optional[FAQ]: pass
    async def add_faq(self, faq: FAQ) -> FAQ: pass
    async def update_faq(self, id: str, faq_data: dict) -> Optional[FAQ]: pass
    async def delete_faq(self, id: str) -> bool: pass
    async def log_query(self, log: QueryLog): pass

class MongoDatabase(DatabaseInterface):
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URL)
        self.db = self.client[settings.DATABASE_NAME]
        print(f"Connected to MongoDB at {settings.MONGO_URL}")

    async def disconnect(self):
        if self.client:
            self.client.close()

    async def get_all_faqs(self) -> List[FAQ]:
        faqs = []
        async for doc in self.db.faqs.find():
            faqs.append(FAQ(**doc))
        return faqs

    async def get_faq(self, id: str) -> Optional[FAQ]:
        doc = await self.db.faqs.find_one({"id": id})
        if doc:
            return FAQ(**doc)
        return None

    async def add_faq(self, faq: FAQ) -> FAQ:
        await self.db.faqs.insert_one(faq.model_dump())
        return faq

    async def update_faq(self, id: str, faq_data: dict) -> Optional[FAQ]:
        result = await self.db.faqs.update_one({"id": id}, {"$set": faq_data})
        if result.modified_count > 0:
            return await self.get_faq(id)
        return None

    async def delete_faq(self, id: str) -> bool:
        result = await self.db.faqs.delete_one({"id": id})
        return result.deleted_count > 0

    async def log_query(self, log: QueryLog):
        await self.db.logs.insert_one(log.model_dump())

class JsonDatabase(DatabaseInterface):
    def __init__(self):
        self.file_path = settings.Json_DB_PATH
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({"faqs": [], "logs": []}, f)

    def _read_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _write_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f, default=str, indent=2)

    async def connect(self):
        print(f"Using JSON Database at {self.file_path}")

    async def disconnect(self):
        pass

    async def get_all_faqs(self) -> List[FAQ]:
        data = self._read_data()
        return [FAQ(**item) for item in data.get("faqs", [])]

    async def get_faq(self, id: str) -> Optional[FAQ]:
        data = self._read_data()
        for item in data.get("faqs", []):
            if item["id"] == id:
                return FAQ(**item)
        return None

    async def add_faq(self, faq: FAQ) -> FAQ:
        data = self._read_data()
        data.setdefault("faqs", []).append(faq.model_dump())
        self._write_data(data)
        return faq

    async def update_faq(self, id: str, faq_data: dict) -> Optional[FAQ]:
        data = self._read_data()
        faqs = data.get("faqs", [])
        for i, item in enumerate(faqs):
            if item["id"] == id:
                item.update(faq_data)
                faqs[i] = item
                self._write_data(data)
                return FAQ(**item)
        return None

    async def delete_faq(self, id: str) -> bool:
        data = self._read_data()
        faqs = data.get("faqs", [])
        new_faqs = [item for item in faqs if item["id"] != id]
        if len(new_faqs) < len(faqs):
            data["faqs"] = new_faqs
            self._write_data(data)
            return True
        return False

    async def log_query(self, log: QueryLog):
        data = self._read_data()
        data.setdefault("logs", []).append(log.model_dump())
        self._write_data(data)

db: DatabaseInterface = JsonDatabase() if settings.USE_JSON_DB else MongoDatabase()

def get_db() -> DatabaseInterface:
    return db
