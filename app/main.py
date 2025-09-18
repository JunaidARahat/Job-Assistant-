from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.responses import JSONResponse
from uuid import uuid4
from typing import Optional
import os
import tempfile

from app.scraper.provider import get_provider
from app.cv.processor import extract_text_from_pdf, load_text_file, chunk_text
from app.embeddings.model import EmbeddingModel
from app.vectorstore.store import VectorStore
from app.match.matcher import extract_skills_from_cv, compute_fit_score, compare_skills
from app.interview.generator import generate_questions

app = FastAPI(title='Job Scraper & Interview Assistant')

TENANT_JOB_DB = {}
TENANT_CV_DB = {}
TENANT_VS = {}

EMBED_MODEL = EmbeddingModel()


@app.post('/scrape/{provider_name}')
def scrape(provider_name: str, x_tenant: Optional[str] = Header('default')):
    prov = get_provider(provider_name)
    jobs = prov.fetch()
    TENANT_JOB_DB.setdefault(x_tenant, []).extend(jobs)
    return {'count': len(jobs), 'jobs': jobs}


@app.post('/upload_cv')
def upload_cv(file: UploadFile = File(...), x_tenant: Optional[str] = Header('default')):
    content = file.filename.lower()
    cv_id = str(uuid4())
    text = ''

    # Cross-platform safe temp directory
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"{cv_id}_{file.filename}")

    # Save file
    with open(temp_path, 'wb') as f:
        f.write(file.file.read())

    # Extract text depending on file type
    if content.endswith('.pdf'):
        text = extract_text_from_pdf(temp_path)
    else:
        text = load_text_file(temp_path)

    if not text:
        text = ' '

    # Extract skills
    skills = extract_skills_from_cv(text)

    # Chunk text & add to vector store
    chunks = chunk_text(text)
    vs = TENANT_VS.get(x_tenant)
    if vs is None:
        vs = VectorStore(EMBED_MODEL)
        TENANT_VS[x_tenant] = vs
    ids = [f"{cv_id}-{i}" for i in range(len(chunks))]
    vs.add_documents(ids, chunks)

    TENANT_CV_DB.setdefault(x_tenant, {})[cv_id] = {
        'filename': file.filename,
        'text': text,
        'skills': skills
    }
    return {'cv_id': cv_id, 'skills': skills, 'chunks': len(chunks)}


@app.post('/match')
def match(job_index: Optional[int] = None, cv_id: Optional[str] = None, x_tenant: Optional[str] = Header('default')):
    jobs = TENANT_JOB_DB.get(x_tenant, [])
    if job_index is None:
        raise HTTPException(status_code=400, detail='job_index is required')
    if job_index < 0 or job_index >= len(jobs):
        raise HTTPException(status_code=404, detail='job not found')
    job = jobs[job_index]
    cv = TENANT_CV_DB.get(x_tenant, {}).get(cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail='cv not found')

    skills = cv.get('skills', [])
    fit = compute_fit_score(job.get('requirements', []), skills)
    comp = compare_skills(job.get('requirements', []), skills)
    return {'fit_score': fit, 'comparison': comp}


@app.post('/interview')
def interview(job_index: Optional[int] = None, cv_id: Optional[str] = None, x_tenant: Optional[str] = Header('default')):
    jobs = TENANT_JOB_DB.get(x_tenant, [])
    if job_index is None:
        raise HTTPException(status_code=400, detail='job_index is required')
    if job_index < 0 or job_index >= len(jobs):
        raise HTTPException(status_code=404, detail='job not found')
    job = jobs[job_index]
    cv = TENANT_CV_DB.get(x_tenant, {}).get(cv_id)
    if not cv:
        raise HTTPException(status_code=404, detail='cv not found')

    skills = cv.get('skills', [])
    fit = compute_fit_score(job.get('requirements', []), skills)
    result = generate_questions(job, cv.get('text', ''), skills, fit)
    return JSONResponse(result)


@app.get('/health')
def health():
    return {'status': 'ok'}
