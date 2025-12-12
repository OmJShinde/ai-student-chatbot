from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple, Optional
import torch

class NLPEngine:
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-MiniLM-L6-v2"):
        print(f"Loading NLP model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("NLP model loaded.")

    def compute_similarity(self, query: str, corpus: List[str]) -> List[Tuple[int, float]]:
        """
        Computes similarity scores between a query and a list of corpus strings.
        Returns a list of (index, score) tuples, sorted by score descending.
        """
        if not corpus:
            return []

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        corpus_embeddings = self.model.encode(corpus, convert_to_tensor=True)

        # Compute cosine similarity
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]

        # Get sorted results
        # We prefer to return top k results or just all sorted
        results = []
        for i in range(len(corpus)):
            results.append((i, float(cos_scores[i])))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def find_best_match(self, query: str, questions: List[str], threshold: float = 0.5) -> Optional[Tuple[int, float]]:
        """
        Finds the single best match for a query among questions.
        Returns (index, score) if score > threshold, else None.
        """
        results = self.compute_similarity(query, questions)
        if results and results[0][1] >= threshold:
            return results[0]
        return None

    def find_closest_matches(self, query: str, questions: List[str], k: int = 3) -> List[Tuple[int, float]]:
        """
        Returns top k matches regardless of threshold, for fallback suggestions.
        """
        results = self.compute_similarity(query, questions)
        return results[:k]

# Global instance
nlp_engine = NLPEngine()
