import asyncio
from app.core.database import get_db
from app.models.faq import FAQ

async def seed():
    db = get_db()
    await db.connect()
    
    # Check if empty
    faqs = await db.get_all_faqs()
    if len(faqs) > 0:
        print(f"Database already has {len(faqs)} FAQs. Skipping seed.")
        return

    sample_data = [
        ("When do classes start?", "Classes for the Fall semester start on September 1st."),
        ("How do I reset my password?", "You can reset your portal password at https://portal.university.edu/reset"),
        ("Where is the library?", "The library is located in Building C, near the main quad."),
        ("What are the library hours?", "The library is open 24/7 during exam weeks, and 8am-10pm otherwise."),
        ("Is there free Wi-Fi?", "Yes, connect to 'Student-WiFi' using your student ID and password."),
        ("How do I apply for a scholarship?", "Scholarship applications are available at the Financial Aid office in Building A."),
        ("Can I change my major?", "Yes, you can change your major by meeting with your academic advisor before the third week of the semester."),
        ("Where is the cafeteria?", "The main cafeteria is on the first floor of the Student Union building."),
    ]

    print("Seeding database with sample data...")
    for q, a in sample_data:
        await db.add_faq(FAQ(question=q, answer=a))
        print(f"Added: {q}")
        
    print("Done! You can now chat with the bot.")

if __name__ == "__main__":
    asyncio.run(seed())
