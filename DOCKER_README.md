# Stone Bar Studio - Docker Deployment

This Docker setup allows you to run the Stone Bar Studio application in a containerized environment.

## Prerequisites
- Docker installed on your system
- Git (to clone the repository)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mastrex5/stone-bar-studio.git
   cd stone-bar-studio
   ```

2. **Build the Docker image:**
   ```bash
   docker build -t stone-bar-studio .
   ```

3. **Run the container:**
   ```bash
   docker run -p 8501:8501 stone-bar-studio
   ```

4. **Access the application:**
   Open your browser and go to `http://localhost:8501`

## Docker Commands

### Build the image
```bash
docker build -t stone-bar-studio .
```

### Run with volume mounting (for development)
```bash
docker run -p 8501:8501 -v $(pwd):/app stone-bar-studio
```

### Run in background
```bash
docker run -d -p 8501:8501 --name stone-bar-studio-app stone-bar-studio
```

### Stop the container
```bash
docker stop stone-bar-studio-app
```

### Remove the container
```bash
docker rm stone-bar-studio-app
```

## Deployment Options

### 1. Streamlit Community Cloud (Easiest)
- Push to GitHub
- Deploy via share.streamlit.io
- Free hosting with public URL

### 2. Docker (Most Flexible)
- Build and run anywhere Docker is supported
- Deploy to AWS, Google Cloud, Azure, etc.
- Run locally for development

### 3. Heroku (Alternative)
```bash
# Add to requirements.txt: gunicorn
heroku create your-app-name
git push heroku main
```

## File Structure
```
stone-bar-studio/
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup (optional)
├── requirements.txt        # Python dependencies
├── main.py                # Streamlit entry point
├── app/                   # Application code
├── data/                  # Data storage
└── static/                # Static assets (CSS, logo)
```