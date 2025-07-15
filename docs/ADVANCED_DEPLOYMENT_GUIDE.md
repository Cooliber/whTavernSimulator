# 🚀 Advanced Deployment Guide - Warhammer Fantasy Tavern Simulator

## Overview

This guide covers deploying the advanced web interface for the Warhammer Fantasy Tavern Simulator, including both the FastAPI backend and React frontend.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.11+ with UV package manager
- **Node.js**: 18.0+ with npm 9.0+
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux

### Environment Variables
Create a `.env` file in the project root:

```env
# API Keys (required for full functionality)
groq_api_key=your_groq_api_key_here
Cerebras_api=your_cerebras_api_key_here

# Server Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FASTAPI_RELOAD=true

# Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws

# Production Settings
NODE_ENV=production
PYTHONPATH=/app
```

## 🔧 Local Development Setup

### 1. Backend Setup

```bash
# Clone the repository
git clone https://github.com/Cooliber/Tawerna.git
cd warhammer_tavern_simulator

# Install Python dependencies with UV
uv pip install -r requirements_crewai.txt

# Verify installation
python -c "import fastapi, crewai; print('✅ Dependencies installed')"

# Start the FastAPI server
python start_api_server.py
```

The backend will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd warhammer-tavern-web

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at:
- **Application**: http://localhost:3000
- **Hot Reload**: Enabled for development

### 3. Verify Integration

1. Open http://localhost:3000 in your browser
2. Check connection status indicator (top-right)
3. Verify WebSocket connection in browser DevTools
4. Test agent interactions and real-time updates

## 🐳 Docker Deployment

### Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - groq_api_key=${groq_api_key}
      - Cerebras_api=${Cerebras_api}
      - PYTHONPATH=/app
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./warhammer-tavern-web
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment

### Vercel (Frontend)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from frontend directory
cd warhammer-tavern-web
vercel --prod
```

### Railway (Backend)

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy automatically on git push

## 🔒 Production Configuration

### Security Settings

```python
# In fastapi_server.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Performance Optimization

```bash
# Backend optimizations
export PYTHONOPTIMIZE=1
export PYTHONDONTWRITEBYTECODE=1

# Frontend optimizations
npm run build  # Includes minification and tree-shaking
```

## 🔍 Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   
   # Verify WebSocket endpoint
   wscat -c ws://localhost:8000/ws
   ```

2. **API Key Issues**
   ```bash
   # Verify environment variables
   python -c "import os; print(os.getenv('groq_api_key'))"
   ```

3. **Frontend Build Errors**
   ```bash
   # Clear cache and reinstall
   rm -rf node_modules package-lock.json
   npm install
   ```

### Performance Issues

1. **High Memory Usage**
   - Reduce `MAX_AGENTS` in configuration
   - Enable garbage collection optimization
   - Monitor with `htop` or similar tools

2. **Slow Response Times**
   - Enable Redis caching
   - Optimize database queries
   - Use connection pooling

## 📊 Monitoring and Maintenance

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# WebSocket status
curl http://localhost:8000/api/websocket/stats

# System metrics
curl http://localhost:8000/metrics
```

### Performance Benchmarks

### Expected Performance
- **API Response Time**: < 100ms (95th percentile)
- **WebSocket Latency**: < 50ms
- **Frontend Load Time**: < 3 seconds
- **Memory Usage**: < 512MB per service
- **CPU Usage**: < 50% under normal load

This deployment guide ensures a smooth transition from development to production while maintaining the high performance and reliability expected from the advanced web interface.
