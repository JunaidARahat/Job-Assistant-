# Job Scraper & Interview Assistant (Complete Runnable Project)

# 📌 Job Scraper & Interview Assistant

A minimal **FastAPI-based platform** for:
- 🔍 Scraping LinkedIn job posts → clean JSON  
- 📄 Uploading & analyzing CVs (with RAG-like approach)  
- 🤝 Matching CVs with job requirements → Fit score + skills match  
- 🎤 Generating interview questions  
- 🐳 Dockerized with GitHub Actions CI/CD  

---

## 🚀 Features
- **LinkedIn Job Scraper** → Converts raw job HTML into structured JSON  
- **CV Analysis** → Extracts skills, stores embeddings, compares with job  
- **Fit Score** → 0–100 score with matched/missing skills  
- **Interview Assistant** → Generates 3 technical + 1 scenario question  
- **CI/CD** → GitHub Actions runs tests, validates JSON, builds Docker image  

---

## 🛠️ Installation

### 1️⃣ Clone repo
```bash
git clone https://github.com/your-username/job-assistant.git
cd job-assistant


2️⃣ Setup Python environment

Using conda:

conda create -n job python=3.11 -y
conda activate job

3️⃣ Install dependencies
pip install -r requirements.txt

Running the App
uvicorn app.main:app --reload

Now open Swagger UI in your browser:
👉 http://127.0.0.1:8000/docs


📡 API Endpoints
1. Scrape Jobs

POST /scrape/linkedin
Headers:

x-tenant: default

2. Upload CV

POST /upload_cv
Upload a .txt or .pdf file.

3. Match CV with Job

POST /match?job_index=0&cv_id=XXXXXXX

4. Generate Interview Questions

POST /interview?job_index=0&cv_id=XXXXX

🧪 Running Tests
pytest -q

🐳 Docker Support
Build image
docker build -t job-assistant .

Run container
docker run -p 8000:8000 job-assistant


Now access at: http://127.0.0.1:8000/docs

⚙️ CI/CD with GitHub Actions

Runs tests

Validates JSON outputs

Builds & pushes Docker image

Workflow file: .github/workflows/ci.yml

📂 Project Structure
job-assistant/
│── app/
│   ├── main.py            # FastAPI app entry
│   ├── scraper.py         # LinkedIn job scraper
│   ├── cv_processor.py    # CV embedding & analysis
│   ├── matcher.py         # Matching logic
│   ├── interview.py       # Question generator
│── data/
│   └── samples/
│       ├── linkedin/
│       │   └── sample1.html
│       └── cv_sample.txt
│── tests/                 # Unit tests
│── requirements.txt
│── Dockerfile
│── README.md
│── .github/workflows/ci.yml

✨ Future Improvements

Multi-tenant support (separate recruiter data)

Better job parsing (SerpAPI / ScrapingBee integration)

Real LangChain/OpenAI integration for advanced Q&A

Skills validation (prevent hallucinations)





