import re
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from backend.app.schemas import ParsedProfile, JobRequirements


class SemanticScorer:
    """
    Tier 2 ML/NLP Layer:
    - Computes TF-IDF and embedding semantic cosine similarity between resume and JD.
    - Evaluates nice-to-have skill bonus.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))

    def compute_similarity(self, resume_text: str, jd_text: str, profile: ParsedProfile, requirements: JobRequirements) -> float:
        try:
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, jd_text])
            cos_sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        except Exception:
            cos_sim = 0.3

        # Nice-to-have skill match bonus
        candidate_skills = set(s.lower() for s in profile.skills)
        nice_to_haves = [s for s in requirements.nice_to_have_skills if s.lower() in candidate_skills]
        nice_ratio = len(nice_to_haves) / len(requirements.nice_to_have_skills) if requirements.nice_to_have_skills else 0.0

        # Blended semantic score
        raw_semantic = 0.7 * cos_sim + 0.3 * nice_ratio
        # Normalize to 0.0 - 1.0 scale
        return round(min(1.0, max(0.0, raw_semantic * 1.5)), 3)


semantic_scorer = SemanticScorer()
