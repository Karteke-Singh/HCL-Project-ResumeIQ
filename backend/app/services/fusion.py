from typing import Dict, Any
from backend.app.schemas import ScoringWeights, ScoreBreakdown


class FusionEngine:
    """
    Tier 4 Fusion Layer:
    - Combines rule score, semantic similarity, experience ratio, and LLM fit rating.
    - Applies hard gate capping: If hard requirements fail, score is capped.
    - Yields transparent component-by-component breakdown.
    """

    def fuse(
        self,
        rule_score: float,
        semantic_score: float,
        experience_score: float,
        llm_fit_score: float,
        passed_hard_requirements: bool,
        weights: ScoringWeights
    ) -> ScoreBreakdown:
        # Normalize weights to sum to 1.0
        total_w = weights.rule + weights.semantic + weights.experience + weights.llm_fit
        if total_w <= 0:
            total_w = 1.0
        w_rule = weights.rule / total_w
        w_sem = weights.semantic / total_w
        w_exp = weights.experience / total_w
        w_llm = weights.llm_fit / total_w

        raw_total = (
            w_rule * rule_score +
            w_sem * semantic_score +
            w_exp * experience_score +
            w_llm * llm_fit_score
        )

        # Hard Gate Capping Rule:
        # If candidate fails mandatory requirements, cap total score so they cannot leapfrog passing candidates
        if not passed_hard_requirements:
            total_score = min(round(raw_total * 100, 1), 55.0)
        else:
            total_score = round(raw_total * 100, 1)

        return ScoreBreakdown(
            rule_score=round(rule_score, 3),
            semantic_score=round(semantic_score, 3),
            experience_score=round(experience_score, 3),
            llm_fit_score=round(llm_fit_score, 3),
            total_score=total_score,
            passed_hard_requirements=passed_hard_requirements
        )


fusion_engine = FusionEngine()
