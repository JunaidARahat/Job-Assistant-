from typing import Dict, List

TEMPLATES = {
    'python': "Explain Python generators and when you'd use them.",
    'django': "Explain the Django request/response lifecycle and ORM patterns you use.",
    'flask': "How do you structure a Flask project for production?",
    'fastapi': "Explain FastAPI dependency injection and async endpoints.",
    'docker': "How would you dockerize a Python web application?",
    'kubernetes': "How do you deploy and scale a microservice on Kubernetes?",
    'ci/cd': "How would you design a CI/CD pipeline for this project? Include testing and rollbacks."
}

def generate_questions(job: Dict, cv_text: str, cv_skills: List[str], fit_score: int, min_accept: int = 50) -> Dict:
    if fit_score < min_accept:
        return {
            'fit_score': fit_score,
            'message': f'Candidate fit score below threshold ({min_accept}). Not recommending interview questions.'
        }

    top_skills = cv_skills[:3]
    questions: List[str] = []
    for s in top_skills:
        key = s.lower()
        q = TEMPLATES.get(key, f'Discuss your experience with {s} and a significant challenge you solved using it.')
        questions.append(q)

    while len(questions) < 3:
        questions.append('Describe a challenging production bug you fixed and the steps you took to resolve it.')

    scenario = f"Scenario: The {job.get('title','role')} at {job.get('company','company')} experiences a performance regression after a deploy. How do you triage and fix it?"
    questions.append(scenario)

    return {'fit_score': fit_score, 'questions': questions}
