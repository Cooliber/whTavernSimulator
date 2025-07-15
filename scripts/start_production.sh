#!/bin/bash
set -e

echo "🏰 Starting Warhammer Fantasy Tavern Simulator - Production Edition"
echo "=================================================================="

# Function to handle cleanup on exit
cleanup() {
    echo "🛑 Shutting down services..."
    if [ ! -z "$HEALTH_PID" ]; then
        kill $HEALTH_PID 2>/dev/null || true
    fi
    if [ ! -z "$STREAMLIT_PID" ]; then
        kill $STREAMLIT_PID 2>/dev/null || true
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

echo "📊 Environment check:"
echo "  - Python: $(python --version)"
echo "  - Streamlit: $(streamlit --version)"
echo "  - Working directory: $(pwd)"
echo "  - User: $(whoami)"
echo "  - Available memory: $(free -h | grep '^Mem:' | awk '{print $7}')"
echo "  - CPU cores: $(nproc)"

# Validate environment variables
echo "🔑 API Configuration:"
if [ -z "$GROQ_API_KEY" ] && [ -z "$CEREBRAS_API_KEY" ]; then
    echo "  ⚠️  Warning: No API keys configured. Some features may not work."
else
    echo "  ✅ API keys configured"
fi

# Test import capabilities
echo "🔧 Testing imports..."
python -c "
import sys
sys.path.append('.')
try:
    import streamlit as st
    from services.tavern_economy import TavernEconomySystem
    from services.narrative_engine import NarrativeEngine
    from components.gsap_renderer import GSAPRenderer
    from services.health_monitor import health_monitor
    print('✅ All core imports successful')
except ImportError as e:
    print(f'❌ Import failed: {e}')
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Import test failed. Exiting."
    exit 1
fi

# Create necessary directories
echo "📁 Setting up directories..."
mkdir -p data/agent_memory logs
chmod 755 data logs
echo "✅ Directories ready"

# Start health check server in background
echo "🏥 Starting health check server..."
python health_endpoints.py &
HEALTH_PID=$!

# Wait for health server to start
sleep 2

# Test health server
echo "🧪 Testing health endpoints..."
if curl -f http://localhost:8502/health/live >/dev/null 2>&1; then
    echo "✅ Health server responding"
else
    echo "⚠️  Health server not responding, continuing anyway..."
fi

# Start Streamlit application
echo "🚀 Starting Streamlit application..."
echo "📱 Application will be available at:"
echo "  - Main app: http://localhost:8501"
echo "  - Health checks: http://localhost:8502"
echo "  - Metrics: http://localhost:8502/metrics"

# Use production app if available, fallback to regular app
if [ -f "app_production.py" ]; then
    echo "🎯 Using production application"
    streamlit run app_production.py \
        --server.port=8501 \
        --server.address=0.0.0.0 \
        --server.headless=true \
        --browser.gatherUsageStats=false \
        --logger.level=info &
else
    echo "🎯 Using standard application"
    streamlit run app.py \
        --server.port=8501 \
        --server.address=0.0.0.0 \
        --server.headless=true \
        --browser.gatherUsageStats=false \
        --logger.level=info &
fi

STREAMLIT_PID=$!

echo "✅ Streamlit started with PID: $STREAMLIT_PID"
echo "✅ Health server running with PID: $HEALTH_PID"

# Wait for Streamlit to be ready
echo "⏳ Waiting for application to be ready..."
for i in {1..30}; do
    if curl -f http://localhost:8502/health/ready >/dev/null 2>&1; then
        echo "✅ Application is ready!"
        break
    fi
    echo "  Attempt $i/30..."
    sleep 2
done

# Final status check
echo "📊 Final status check:"
if curl -f http://localhost:8502/health >/dev/null 2>&1; then
    echo "✅ All systems operational"
    echo "🎉 Warhammer Fantasy Tavern Simulator is running!"
    echo ""
    echo "📱 Access points:"
    echo "  🏰 Main Application: http://localhost:8501"
    echo "  🏥 Health Dashboard: http://localhost:8502/health"
    echo "  📊 Metrics: http://localhost:8502/metrics"
    echo "  💓 Liveness: http://localhost:8502/health/live"
    echo "  🎯 Readiness: http://localhost:8502/health/ready"
    echo ""
    echo "🔧 Monitoring:"
    echo "  - 18-agent system with 5 factions"
    echo "  - Real-time GSAP visualizations"
    echo "  - Economy and narrative integration"
    echo "  - Performance monitoring and health checks"
    echo ""
else
    echo "⚠️  Application may not be fully ready"
fi

# Keep the script running and monitor processes
echo "🔄 Monitoring services..."
while true; do
    # Check if Streamlit is still running
    if ! kill -0 $STREAMLIT_PID 2>/dev/null; then
        echo "❌ Streamlit process died, restarting..."
        if [ -f "app_production.py" ]; then
            streamlit run app_production.py \
                --server.port=8501 \
                --server.address=0.0.0.0 \
                --server.headless=true \
                --browser.gatherUsageStats=false \
                --logger.level=info &
        else
            streamlit run app.py \
                --server.port=8501 \
                --server.address=0.0.0.0 \
                --server.headless=true \
                --browser.gatherUsageStats=false \
                --logger.level=info &
        fi
        STREAMLIT_PID=$!
    fi
    
    # Check if health server is still running
    if ! kill -0 $HEALTH_PID 2>/dev/null; then
        echo "❌ Health server died, restarting..."
        python health_endpoints.py &
        HEALTH_PID=$!
    fi
    
    sleep 30
done
