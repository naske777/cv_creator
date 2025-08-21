# CV Generator & Upload Service: Complete Guide

This comprehensive guide combines both the CV Creator (generates professional PDF résumés) and the PDF Upload Service (hosts and serves your CV). Follow this step-by-step to create, automate, and host your CV with HTTPS security.

## Public Repositories
- **PDF Upload Service**: [https://github.com/naske777/PDF-Upload-Service](https://github.com/naske777/PDF-Upload-Service)
- **CV Creator**: [https://github.com/naske777/cv_creator](https://github.com/naske777/cv_creator)

## Table of Contents
1. [System Overview](#system-overview)
2. [Prerequisites](#prerequisites)
3. [Setting Up CV Creator](#setting-up-cv-creator)
4. [Setting Up PDF Upload Service](#setting-up-pdf-upload-service)
5. [Integration: Automate CV Generation & Upload](#integration-automate-cv-generation--upload)
6. [Securing with HTTPS (Let's Encrypt)](#securing-with-https-lets-encrypt)
7. [Troubleshooting](#troubleshooting)

## System Overview

This combined system works in two parts:
- **CV Creator**: Generates a professional PDF résumé from structured YAML/Markdown files ([GitHub Repository](https://github.com/naske777/cv_creator))
- **PDF Upload Service**: Hosts your CV with secure Bearer token authentication ([GitHub Repository](https://github.com/naske777/PDF-Upload-Service))

The workflow:
1. You edit your CV content in YAML/Markdown format
2. CV Creator compiles it to a PDF
3. The PDF is automatically uploaded to your secure service
4. Your CV is available at `https://yourdomain.com/cv/latest.pdf`

## Prerequisites

### For CV Creator (PDF Generation)
- Python 3.8 or newer
- TeX Live with required LaTeX packages:
  ```bash
  sudo apt-get update
  sudo apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-recommended
  ```

### For PDF Upload Service
- Docker and Docker Compose
- OpenSSL (for token generation)
- Command line access to your server
- An HTTP site already running on port 80 (for Let's Encrypt)
- SSH access to your server
- Sudo privileges

### For HTTPS Setup (Let's Encrypt)
- A domain name pointing to your server
- Ports 80 and 443 open on your server
- DNS credentials for your domain (if using DNS validation)

## Setting Up CV Creator

### 1. Clone the repository
```bash
git clone https://github.com/naske777/cv_creator.git
cd cv_creator
```

### 2. Set up the virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Structure your CV content
Place your section files in `cv_data/sections/` with numbered prefixes for ordering:

```
cv_data/sections/
├── 01_personal_info.yaml
├── 02_summary.md
├── 03_experience.md
├── 04_education.md
├── 05_certifications.txt
├── 06_awards.md
├── 07_projects.md
└── 08_skills.yaml
```

### 4. Format your personal information (critical for header)
Example (`cv_data/sections/01_personal_info.yaml`):
```yaml
personal_information:
  name: Camila Torres
  location: Miami, FL
  contacts:
    email: camila.torres@email.com
    phone: "+1-786-555-0198"
    github: "https://github.com/camitorres"
```

### 5. Build your CV manually
```bash
python src/main.py
```
Output will be at `output/cv.pdf`

## Setting Up PDF Upload Service

### 1. Clone the repository
```bash
git clone https://github.com/naske777/PDF-Upload-Service.git
cd PDF-Upload-Service
```

### 2. Create a secure token
```bash
openssl rand -hex 32
```
Copy the output and save it in `.env`:
```env
UPLOAD_TOKEN=your_generated_token_here
```

### 3. Create the Docker network
```bash
docker network create pdf-service-network
```

### 4. Start the service
```bash
docker compose up -d --build
```

### 5. Verify the service is running
```bash
curl -I http://localhost:3000/cv/latest.pdf
```

## Integration: Automate CV Generation & Upload

### 1. Set up GitHub Actions automation
1. Fork the [CV Creator repository](https://github.com/naske777/cv_creator) to your GitHub account
2. Prepare an API endpoint (your PDF Upload Service):
   - URL: `http://your-server-ip:3000/cv/upload`
   - Path: `/cv/upload`
3. Set up repository secrets:
   - `API_URL`: Full URL to your upload endpoint (e.g., `http://your-server-ip:3000/cv/upload`)
   - `API_TOKEN`: Your secure token from `.env` file

### 2. Test the integration
1. Make changes to your CV section files
2. Commit and push to `main`
3. Check GitHub Actions logs for successful build and upload
4. Access your CV at `http://your-server-ip:6789/cv/latest.pdf`

## Securing with HTTPS (Let's Encrypt)

### 1. Ensure your server meets requirements
- Your domain points to your server IP
- Ports 80 and 443 are open
- You have an HTTP site running on port 80 (temporary for validation)

### 2. Generate SSL certificates
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

### 3. Configure Docker Compose for SSL
Update your `docker-compose.yml`:
```yaml
services:
  nginx:
    volumes:
      - /etc/letsencrypt:/etc/letsencrypt:ro
```

### 4. Reload Nginx
```bash
sudo systemctl reload nginx
```

### 5. Cloudflare Setup 
1. Add your domain to Cloudflare
2. Create A record pointing to your server IP
3. Set SSL/TLS mode to "Full (strict)"
4. Disable proxy (set to DNS only) when renewing certificates

## Troubleshooting

### CV Generation Issues
| Issue | Solution |
|-------|----------|
| PDF not generated | Check TeX Live installation and required packages |
| "pdflatex not found" | Install TeX Live as shown in Prerequisites |
| Encoding errors | Ensure all files are UTF-8 encoded |
| Personal info not formatted | Verify section is named `personal_information` with correct fields |

### Upload Service Issues
| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Verify token matches `.env` and is sent in `Authorization: Bearer` header |
| 413 Payload Too Large | File exceeds 25MB limit - reduce PDF size |
| PDF not accessible | Check `public/` directory has correct permissions |
| Docker network issues | Verify `pdf-service-network` exists with `docker network ls` |

### HTTPS/SSL Issues
| Issue | Solution |
|-------|----------|
| Certbot fails to validate | Temporarily disable Cloudflare proxy during certificate generation |
| "Port 80 not accessible" | Check firewall settings and ensure port 80 is open |
| Certificate not found in container | Verify volume mapping `- /etc/letsencrypt:/etc/letsencrypt:ro` |
| Mixed content warnings | Ensure all resources are loaded via HTTPS |

## Final Notes

- **Security**: Always use HTTPS in production and keep your `UPLOAD_TOKEN` secret
- **Updates**: Certbot certificates auto-renew, but verify with `sudo certbot renew --dry-run`
- **Maintenance**: Monitor disk space as versioned PDFs accumulate in `public/`
- **Backup**: Consider backing up your CV source files and generated PDFs

Your professional CV is now automatically generated, securely hosted, and available at `https://yourdomain.com/cv/latest.pdf` with proper HTTPS encryption!