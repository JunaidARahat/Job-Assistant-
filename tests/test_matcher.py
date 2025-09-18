from app.match.matcher import extract_skills_from_cv, compute_fit_score

def test_skills_and_score():
    cv = 'Experienced Python developer. Used Django and Docker in production. Familiar with CI/CD.'
    skills = extract_skills_from_cv(cv)
    assert 'python' in [s.lower() for s in skills]
    assert 'django' in [s.lower() for s in skills]

    job_reqs = ['Python', 'Django', 'CI/CD', 'Kubernetes']
    score = compute_fit_score(job_reqs, skills)
    assert isinstance(score, int)
    assert 0 <= score <= 100
