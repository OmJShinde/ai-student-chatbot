from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.core.database import get_db, DatabaseInterface
from app.models.faq import FAQ, FAQCreate, FAQUpdate, QueryLog
from app.services.nlp_engine import nlp_engine
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    confidence: float

class LoginRequest(BaseModel):
    username: str
    password: str

import traceback

from app.services.spell_checker import spell_corrector

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: DatabaseInterface = Depends(get_db)):
    try:
        # Pre-process: Spell Correction
        original_query = request.query
        corrected_query = spell_corrector.correct_text(original_query)
        
        # Log if correction happened (optional, for debug)
        if original_query != corrected_query:
            print(f"Corrected '{original_query}' to '{corrected_query}'")

        # Basic Greeting Logic
        greetings = {
            "hi": "Hello! How can I help you today?",
            "hello": "Hi there! What can I do for you?",
            "hey": "Hey! Need any help with campus info?",
            "good morning": "Good morning! How can I assist you?",
            "good afternoon": "Good afternoon! What's on your mind?",
            "good evening": "Good evening! How can I help?",
            "how are you": "I'm just a bot, but I'm functioning perfectly! How can I help you?",
            "who are you": "I am the Student Support Bot. specialized in answering queries about the campus, exams, and facilities."
        }
        
        clean_query = corrected_query.lower().strip("!?. ")
        if clean_query in greetings:
            return ChatResponse(answer=greetings[clean_query], confidence=1.0)

        # 1. Fetch all FAQs
        faqs = await db.get_all_faqs()
        if not faqs:
            return ChatResponse(answer="Sorry, I don't have enough knowledge to answer that yet.", confidence=0.0)

        # 2. Extract content for matching (Question + Answer for better context)
        corpus = [f"{faq.question} {faq.answer}" for faq in faqs]
        questions_only = [faq.question for faq in faqs] # For display in fallback

        # 3. Intelligent Match Logic
        THRESHOLD = 0.65
        
        # A. Semantic Search on Corrected Query
        match = nlp_engine.find_best_match(corrected_query, corpus, threshold=THRESHOLD)

        response_text = ""
        score = 0.0

        if match:
            # Direct hit
            index, score = match
            best_faq = faqs[index]
            response_text = best_faq.answer
        else:
            # B. Fallback: Get Top 3 suggestions
            suggestions = nlp_engine.find_closest_matches(corrected_query, corpus, k=3)
            
            # Filter out very bad matches (e.g. score < 0.1)
            valid_suggestions = [s for s in suggestions if s[1] > 0.1]
            
            if valid_suggestions:
                list_text = "\n".join([f"- {questions_only[idx]}" for idx, sc in valid_suggestions])
                response_text = f"I'm not 100% sure, but did you mean one of these?\n\n{list_text}"
                score = valid_suggestions[0][1] # set score to best guess
            else:
                response_text = "Sorry, I couldn't find any answer related to that. Can you try rephrasing?"

        # 4. Log the query
        await db.log_query(QueryLog(query=original_query, response=response_text, score=score))

        return ChatResponse(answer=response_text, confidence=score)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggested-questions", response_model=List[str])
async def get_suggested_questions(db: DatabaseInterface = Depends(get_db)):
    # Return a random sample or fixed list of common questions
    faqs = await db.get_all_faqs()
    if not faqs:
        return []
    # prioritizing checking existing faqs
    return [faq.question for faq in faqs[:5]] # Return top 5 for chips

from fastapi import Header

async def verify_token(authorization: str = Header(None)):
    if authorization != "Bearer fake-jwt-token-for-mvp":
        raise HTTPException(status_code=401, detail="Unauthorized")

# --- FAQ CRUD ---

@router.get("/faqs", response_model=List[FAQ])
async def get_faqs(db: DatabaseInterface = Depends(get_db)):
    return await db.get_all_faqs()

@router.post("/faqs", response_model=FAQ, dependencies=[Depends(verify_token)])
async def create_faq(faq: FAQCreate, db: DatabaseInterface = Depends(get_db)):
    new_faq = FAQ(question=faq.question, answer=faq.answer)
    return await db.add_faq(new_faq)

@router.put("/faqs/{faq_id}", response_model=FAQ, dependencies=[Depends(verify_token)])
async def update_faq(faq_id: str, faq_data: FAQUpdate, db: DatabaseInterface = Depends(get_db)):
    updated_faq = await db.update_faq(faq_id, faq_data.model_dump(exclude_unset=True))
    if not updated_faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return updated_faq

@router.delete("/faqs/{faq_id}", dependencies=[Depends(verify_token)])
async def delete_faq(faq_id: str, db: DatabaseInterface = Depends(get_db)):
    success = await db.delete_faq(faq_id)
    if not success:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return {"status": "success"}

# --- Admin ---

@router.post("/admin/login")
async def admin_login(creds: LoginRequest):
    # Simple hardcoded check for MVP
    if creds.username == "admin" and creds.password == "admin123":
        return {"token": "fake-jwt-token-for-mvp", "status": "success"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
