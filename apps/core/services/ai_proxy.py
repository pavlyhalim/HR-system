"""AI Proxy Service - Interface for external AI/ML services.

All AI operations are proxied through this service. Currently returns
mock responses. Replace with actual AI service calls when ready.
"""

import uuid


class AIProxyService:
    """Stub proxy to external AI/ML services."""

    @staticmethod
    def parse_cv(cv_file_path: str) -> dict:
        return {
            "name": "Parsed Candidate",
            "email": "candidate@example.com",
            "skills": ["Python", "Django", "REST APIs"],
            "experience_years": 5,
            "education": [{"degree": "BSc Computer Science", "institution": "University"}],
        }

    @staticmethod
    def score_candidate(candidate_data: dict, jd_data: dict) -> dict:
        return {
            "overall_score": 78.5,
            "competency_scores": {"Technical": 80, "Communication": 75, "Leadership": 70},
            "match_percentage": 78.5,
            "reasoning": "Strong technical match with relevant experience.",
        }

    @staticmethod
    def generate_interview_questions(jd_data: dict, difficulty: str = "Mid") -> list:
        return [
            {"question": "Describe your experience with the key technologies in this role.", "competency": "Technical", "difficulty": difficulty, "type": "Behavioral"},
            {"question": "How do you handle conflicting priorities?", "competency": "Communication", "difficulty": difficulty, "type": "Situational"},
            {"question": "Walk us through a complex project you led.", "competency": "Leadership", "difficulty": difficulty, "type": "Behavioral"},
        ]

    @staticmethod
    def analyze_interview(interview_data: dict) -> dict:
        return {
            "overall_score": 75.0,
            "competency_breakdown": {"Technical": 80, "Communication": 70, "Problem-Solving": 75},
            "sentiment": "Positive",
            "red_flags": [],
            "recommendation": "Proceed to next stage",
        }

    @staticmethod
    def generate_jd(job_analysis_data: dict) -> dict:
        return {
            "job_purpose": "Placeholder job purpose based on analysis inputs.",
            "responsibilities": ["Responsibility 1", "Responsibility 2"],
            "competencies": [{"name": "Technical Skill", "proficiency": "Senior", "weight": 40}],
            "kpis": ["KPI 1", "KPI 2"],
        }

    @staticmethod
    def calculate_promotion_score(employee_data: dict, target_jd: dict) -> dict:
        return {
            "promotion_score": 82.0,
            "competency_delta": {"Leadership": +10, "Technical": +5},
            "justification": "Employee meets most criteria for promotion.",
        }

    @staticmethod
    def match_mobility(employee_data: dict, role_data: dict) -> dict:
        return {
            "role_fit_score": 71.0,
            "skill_gaps": ["Cloud Architecture", "Team Management"],
            "recommendation": "Suitable with targeted development.",
        }

    @staticmethod
    def identify_successors(role_data: dict, candidates: list) -> list:
        return [
            {"employee_id": str(uuid.uuid4()), "readiness": "Ready", "gap_percentage": 10},
            {"employee_id": str(uuid.uuid4()), "readiness": "6-12mo", "gap_percentage": 30},
        ]

    @staticmethod
    def analyze_maturity(survey_data: dict) -> dict:
        return {
            "domain_scores": {"Governance": 3.2, "Culture": 2.8, "Technology": 3.5, "Talent": 3.0},
            "overall_level": 3,
            "gaps": [{"domain": "Culture", "description": "Low employee engagement scores"}],
        }

    @staticmethod
    def generate_hr_strategy(company_data: dict, maturity_data: dict) -> dict:
        return {
            "pillars": [
                {"name": "Talent Acquisition", "priority": 1, "description": "Strengthen recruitment pipeline"},
                {"name": "Employee Development", "priority": 2, "description": "Invest in capability building"},
            ],
            "kpis": ["Time-to-Hire", "Employee NPS", "Training Hours"],
            "roadmap": {"Q1": ["Launch new ATS"], "Q2": ["Implement TNA"]},
        }
