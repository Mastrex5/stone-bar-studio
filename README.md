# Stone Bar Studio

A custom business management app for Stone Bar Studio, a high-end masonry and outdoor living start-up in San Antonio, TX.

## Features
- **Material Prep & Planning Studio**: Calculate Bill of Materials (BOM) for custom stone bars.
- **Receipt Generator**: Create professional invoices and export to PDF.
- **Financial Dashboard**: Track costs, profits, and splits.

## Quick Start

### Option 1: Streamlit Community Cloud (Easiest)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select the `Mastrex5/stone-bar-studio` repository
4. Set main file path to `main.py`
5. Deploy!

### Option 2: Docker (Most Flexible)
```bash
# Clone and run with Docker
git clone https://github.com/Mastrex5/stone-bar-studio.git
cd stone-bar-studio
docker-compose up --build
```
Then visit `http://localhost:8501`

### Option 3: Local Development
```bash
git clone https://github.com/Mastrex5/stone-bar-studio.git
cd stone-bar-studio
pip install -r requirements.txt
streamlit run main.py
```

## Deployment Options

### 🌐 Streamlit Community Cloud
- **Pros**: Free, instant deployment, no server management
- **Best for**: Quick sharing, demos, public access
- **URL**: `https://stone-bar-studio-rzixijeq9usopjypkjfn8h.streamlit.app`

### 🐳 Docker
- **Pros**: Portable, runs anywhere, full control
- **Best for**: Production deployment, custom environments
- **Platforms**: AWS, Google Cloud, Azure, local servers
- **See**: `DOCKER_README.md` for detailed instructions

### ☁️ Other Cloud Platforms
- **Heroku**: Add `gunicorn` to requirements.txt
- **Railway**: Automatic Docker deployment
- **Render**: Free tier available

## Tech Stack
- Python 3.11+
- Streamlit (Web UI)
- ReportLab (PDF Generation)
- Plotly (Charts)
- JSON/SQLite (Data Storage)