from app.services.nlp_engine import nlp_engine
import sys

questions = [
    "Where is the library?",
    "What are the library hours?",
    "When do classes start?",
    "Is there free Wi-Fi?"
]

query = "Is the library open now?"

print("\n" * 5)
print("RESULTS_START")
results = nlp_engine.compute_similarity(query, questions)

for index, score in results:
    print(f"Score: {score:.4f} - Q: {questions[index]}")
print("RESULTS_END")
print("\n" * 5)
