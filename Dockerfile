# Warhammer Fantasy Tavern Simulator - Production Edition
# Multi-stage Docker build for optimized production deployment

# Build stage
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash tavern

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/tavern/.local

# Copy application code
COPY --chown=tavern:tavern . .

# Create necessary directories with proper permissions
RUN mkdir -p data/agent_memory logs \
    && chown -R tavern:tavern /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PATH=/home/tavern/.local/bin:$PATH
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Switch to non-root user
USER tavern

# Expose port
EXPOSE 8501

# Health check with better error handling
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || \
        (echo "Health check failed" && ps aux | grep streamlit && exit 1)

# Copy the enhanced startup script
COPY --chown=tavern:tavern start_production.sh /app/start.sh
RUN chmod +x /app/start.sh

# Run the application with enhanced startup script
CMD ["/app/start.sh"]
