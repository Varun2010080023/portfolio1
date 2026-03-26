# Varun Chandra Cherukuri — Portfolio

Personal portfolio website with Flask backend, contact form API, and CV download endpoint.

## Project Structure

```
portfolio/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── Procfile               # Heroku / Railway process file
├── Dockerfile             # Docker container config
├── railway.json           # Railway deployment config
├── .env.example           # Environment variable template
├── .gitignore
├── static/
│   └── varun_cv.pdf       # ← Place your CV PDF here
└── templates/
    └── index.html         # Frontend (served by Flask)
```

## Local Development

```bash
# 1. Clone and enter the project
git clone https://github.com/Varun2010080023/portfolio
cd portfolio

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env with your SMTP credentials (optional)

# 5. Add your CV PDF
cp /path/to/your/cv.pdf static/varun_cv.pdf

# 6. Run dev server
FLASK_ENV=development python app.py
# → Open http://localhost:5000
```

## Deploy to Railway (Recommended — Free Tier)

1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repo
4. Railway auto-detects the Dockerfile and deploys
5. Add environment variables in Railway dashboard:
   - `SMTP_HOST` = smtp.gmail.com
   - `SMTP_USER` = your-gmail@gmail.com
   - `SMTP_PASS` = your-app-password (Google App Password)
   - `TO_EMAIL`  = varun.ch1405@gmail.com
6. Done — Railway gives you a free `.railway.app` URL

## Deploy to Render (Free Tier)

1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repo
4. Set:
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variables in Render dashboard
6. Deploy → get a free `.onrender.com` URL

## Deploy to Heroku

```bash
heroku create varun-portfolio
heroku config:set SMTP_HOST=smtp.gmail.com SMTP_USER=... SMTP_PASS=... TO_EMAIL=varun.ch1405@gmail.com
git push heroku main
```

## Deploy with Docker

```bash
docker build -t varun-portfolio .
docker run -p 5000:5000 --env-file .env varun-portfolio
# → Open http://localhost:5000
```

## Contact Form Email Setup (Gmail)

1. Go to Google Account → Security → 2-Step Verification → App Passwords
2. Generate an App Password for "Mail"
3. Add to `.env`:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_USER=varun.ch1405@gmail.com
   SMTP_PASS=xxxx-xxxx-xxxx-xxxx   # your 16-char app password
   TO_EMAIL=varun.ch1405@gmail.com
   ```

If SMTP is not configured, form submissions are logged to console — no emails sent, but the form still works.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Portfolio homepage |
| POST | `/api/contact` | Contact form submission (JSON) |
| GET | `/api/health` | Health check |
| GET | `/cv` | Download CV PDF |
