import asyncio
from app.core.database import get_db
from app.models.faq import FAQ

async def seed_bulk_data():
    db = get_db()
    await db.connect()
    
    # Raw data string from user
    raw_data = """
How do I connect to the campus Wi-Fi? | Connect to the "Student-WiFi" network and log in using your student ID and password.
Is the campus Wi-Fi free? | Yes, Wi-Fi is free for all registered students.
I forgot my Wi-Fi password. What should I do? | Reset your Wi-Fi password through the IT Helpdesk portal.
The Wi-Fi is not working. Who should I contact? | Contact the IT Support Desk at helpdesk@college.edu or visit the IT office.
How do I reset my student portal password? | Click “Forgot Password” on the student portal login page.
I can't log in to the student portal. What should I do? | Check your credentials. If it still fails, contact IT Support.
Where can I find my student ID number? | It is printed on your student ID card and included in your admission email.
When do classes start? | Classes begin on the first Monday of the semester.
Where can I view my class timetable? | Your timetable is available in the Student Portal under Academics > Timetable.
Are Saturday classes mandatory? | Saturday classes are held only for labs or special sessions.
How much attendance is required? | Minimum 75% attendance is required to appear for exams.
Where can I find the exam schedule? | Check the Examination section in the Student Portal.
What documents do I need for exams? | You need your student ID card and exam hall ticket.
When will exam results be declared? | Results are typically released 3–4 weeks after exams.
I missed an exam. Can I get a re-exam? | Re-exams are allowed only for valid reasons with department approval.
How can I pay my fees online? | Go to the Student Portal → Finance → Pay Fees.
My fee payment failed. What should I do? | Wait 24 hours. If unresolved, contact Accounts with your transaction ID.
Are scholarships available? | Yes, scholarships are available based on merit and financial need.
How do I apply for a scholarship? | Apply through the Scholarships section in the Student Portal.
Where is the library located? | The library is on the 2nd floor of the Academic Block.
What are the library hours? | Monday–Friday: 9 AM–6 PM, Saturday: 9 AM–2 PM.
How many books can I borrow? | Students may borrow 2 books for 14 days.
How do I renew a library book? | Renew it through the library portal using your login.
Is there a fine for late book returns? | Yes, ₹5 per day per book.
How do I apply for hostel accommodation? | Submit an application through the Hostel Module in the Student Portal.
Is hostel Wi-Fi available? | Yes, Wi-Fi is available in all hostel blocks.
What is the hostel curfew time? | The hostel curfew is 9:30 PM.
Is college bus service available? | Yes, transport service is available on major routes.
How do I register for bus service? | Register through the Transport section in the Student Portal.
Where can I check bus timings? | Bus timings are listed in the Transport section.
How do I get a new student ID card? | Visit the Admin Office and submit an ID card request.
I lost my student ID card. What should I do? | Report it to the Admin Office and request a duplicate card.
Where can I download a bonafide certificate? | Download it from Certificates in the Student Portal.
What are cafeteria timings? | The cafeteria is open from 8 AM to 7 PM.
Is there a medical room on campus? | Yes, it is located near the main entrance.
How do I contact the administration office? | Email admin@college.edu or visit during working hours.
How do I update my phone number? | Update it in Profile Settings on the Student Portal.
Can I change my registered email ID? | Yes, but it requires admin approval.
My portal is showing an error. What should I do? | Clear your browser cache. If the issue persists, contact IT Support.
"""
    
    # Parse and insert
    lines = raw_data.strip().split('\n')
    count = 0
    for line in lines:
        if '|' in line:
            parts = line.split('|')
            q = parts[0].strip()
            a = parts[1].strip()
            
            # Check for duplicates (simple check)
            # ideally we check DB, but to go fast we just insert. 
            # The user might have older data, this adds more or duplicates. 
            # For a proper seed we might want to plain clear or check existence.
            # Let's check existence by question string match
            
            existing = await db.get_all_faqs()
            exists = any(faq.question == q for faq in existing)
            
            if not exists:
                await db.add_faq(FAQ(question=q, answer=a))
                print(f"Added: {q}")
                count += 1
            else:
                print(f"Skipped (exists): {q}")

    print(f"Done! Added {count} new FAQs.")

if __name__ == "__main__":
    asyncio.run(seed_bulk_data())
