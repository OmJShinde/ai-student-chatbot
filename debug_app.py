import sys
import asyncio
import traceback
from app.core.config import settings
from app.core.database import get_db

async def test_startup():
    print("Testing imports...")
    try:
        from app.main import app
        print("Imports successful.")
    except Exception:
        traceback.print_exc()
        return

    print("Testing Database...")
    try:
        db = get_db()
        await db.connect()
        print(f"DB Connected: {db}")
        faqs = await db.get_all_faqs()
        print(f"FAQs: {len(faqs)}")
    except Exception:
        traceback.print_exc()
        return

    print("Testing NLP Engine...")
    try:
        from app.services.nlp_engine import nlp_engine
        print("NLP Engine loaded.")
        match = nlp_engine.find_best_match("hello", ["hello world", "goodbye"])
        print(f"Match result: {match}")
    except Exception:
        traceback.print_exc()
        return

    print("Diagnostics complete.")

if __name__ == "__main__":
    asyncio.run(test_startup())
