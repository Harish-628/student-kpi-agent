# Frontend Server Configuration

This file contains instructions for running the frontend locally during development and deployment.

## Quick Start

### Option 1: Python HTTP Server (Recommended for Development)

```bash
# Navigate to project root
cd d:\student-kpi-project

# Start the server on port 8080
python -m http.server 8080

# Open browser and go to:
# http://localhost:8080/frontend/
```

### Option 2: Python with Custom Port

```bash
# Run on a different port (e.g., 3000)
python -m http.server 3000

# Access at http://localhost:3000/frontend/
```

### Option 3: Node.js HTTP Server

```bash
# Install http-server globally (one-time)
npm install -g http-server

# Run from project root
http-server -p 8080 -o

# Or run from frontend folder
cd frontend
http-server -p 8080
```

### Option 4: PHP Built-in Server

```bash
# Run from project root
php -S localhost:8000

# Access at http://localhost:8000/frontend/
```

## Running Backend Alongside Frontend

To test full functionality with the backend:

### Terminal 1 - Backend (FastAPI)
```bash
cd d:\student-kpi-project
python backend/main.py
# Server runs on http://localhost:8000
```

### Terminal 2 - Frontend
```bash
cd d:\student-kpi-project
python -m http.server 8080
# Access frontend at http://localhost:8080/frontend/
```

### Terminal 3 (Optional) - Database
Ensure your database is running if using external DB.

## Browser Access

After starting the server:

| Component | URL |
|-----------|-----|
| Login Page | http://localhost:8080/frontend/index.html |
| Dashboard | http://localhost:8080/frontend/dashboard.html |
| Setup Guide | http://localhost:8080/frontend/setup.html |
| API Docs | http://localhost:8000/docs (Backend) |

## Development vs Production

### Development Settings
- Debug mode: ON
- CORS: Permissive (allow all origins)
- Cache: Minimal
- Logging: Verbose

### Production Settings
- Debug mode: OFF
- CORS: Restricted to specific domains
- Cache: Aggressive caching
- Logging: Error level only
- HTTPS: Required
- Minification: Enabled

## Troubleshooting Server Issues

### Port Already in Use
```bash
# Find process using port 8080
tasklist /fi "imagename eq python.exe"

# Or kill the port (Windows)
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### CORS Issues When Connecting to Backend
Add this to your backend (FastAPI):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Files Not Loading
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Check file paths are correct
- Ensure relative paths use correct notation

## Production Deployment

### Using Nginx
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /frontend/ {
        alias /path/to/frontend/;
        index index.html;
        try_files $uri $uri/ /frontend/index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
    }
}
```

### Using Apache
```apache
<Directory /var/www/html/frontend>
    RewriteEngine On
    RewriteBase /frontend/
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /frontend/index.html [L]
</Directory>
```

### Docker Deployment
```dockerfile
FROM nginx:latest

COPY frontend/ /usr/share/nginx/html/frontend/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Run with:
```bash
docker build -t kpi-frontend .
docker run -p 80:80 kpi-frontend
```

## Environment Configuration

Create a `.env` file for environment variables:
```
# API Configuration
API_BASE_URL=http://localhost:8000/api
AUTH_TOKEN_NAME=authToken
SESSION_TIMEOUT=1800

# Feature Flags
ENABLE_ANALYTICS=true
ENABLE_EXPORTS=true
DEBUG_MODE=false

# UI Settings
THEME_COLOR=#667eea
ITEMS_PER_PAGE=10
```

Load in JavaScript:
```javascript
const config = await fetch('.env').then(r => r.json());
```

## Monitoring & Logging

### Browser Console
- Press F12 to open Developer Tools
- Check Console tab for JavaScript errors
- Check Network tab for API call issues

### Server Logs
Monitor the HTTP server output for:
- 404 errors (missing files)
- 500 errors (server issues)
- Request patterns

## Performance Optimization

### Minification
```bash
# CSS minification
npm install -g csso-cli
csso css/styles.css -o css/styles.min.css

# JavaScript minification
npm install -g terser
terser js/dashboard.js -o js/dashboard.min.js
```

### Caching Strategy
Add cache headers in your web server configuration for:
- CSS and JavaScript files: 30 days
- HTML files: 1 day
- Images: 90 days

### CDN Integration
Use CDN for Chart.js and other external libraries:
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@latest"></script>
```

## Troubleshooting Checklist

- [ ] Server is running on correct port
- [ ] Browser can access the port (no firewall blocks)
- [ ] All file paths are correct
- [ ] No JavaScript errors in console (F12)
- [ ] Backend is running if API calls are needed
- [ ] CORS is configured if accessing different origin
- [ ] CSS and images are loading (check Network tab)
- [ ] Database is accessible (if using backend features)

## Common Commands

```bash
# Start frontend only
python -m http.server 8080

# Start both frontend and backend
start python -m http.server 8080
start python backend/main.py

# Run with custom config
python -m http.server 8080 --directory ./frontend/

# Test with curl
curl http://localhost:8080/frontend/index.html
```

## Version Info

- Tested on: Python 3.8+, Node.js 14+
- Server: HTTP/1.1 compatible
- Browser Support: Chrome, Firefox, Safari, Edge (latest versions)
- Mobile: Full responsive support

---

For more information, see:
- `frontend/README.md` - Frontend documentation
- `frontend/setup.html` - Setup guide (view in browser)
- `DATABASE_SETUP.md` - Infrastructure setup
