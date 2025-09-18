from typing import List, Dict

COMMON_SKILLS = ['python','django','flask','fastapi','docker','kubernetes','ci/cd','aws','gcp','sql','postgres','react','pandas','numpy','torch','tensorflow','rest','graphql']

def extract_skills_from_cv(cv_text: str, candidate_skill_list: List[str] = None) -> List[str]:
    candidate_skill_list = candidate_skill_list or COMMON_SKILLS
    lower = (cv_text or '').lower()
    found = []
    for s in candidate_skill_list:
        if s.lower() in lower:
            found.append(s)
    return found

def compute_fit_score(job_requirements: List[str], cv_skills: List[str]) -> int:
    if not job_requirements:
        return 0
    jr = [j.lower() for j in job_requirements]
    cs = [c.lower() for c in cv_skills]
    matched = sum(1 for r in jr if any(r in c or c in r for c in cs))
    score = int(round(100 * matched / len(jr)))
    if score < 0:
        score = 0
    if score > 100:
        score = 100
    return score

def compare_skills(job_reqs: List[str], cv_skills: List[str]) -> Dict:
    jr = [j for j in job_reqs]
    cs = [c.lower() for c in cv_skills]
    matched = [j for j in jr if any(j.lower() in c or c in j.lower() for c in cs)]
    missing = [j for j in jr if j not in matched]
    return {'matched': matched, 'missing': missing}
