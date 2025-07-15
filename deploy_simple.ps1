# Warhammer Tavern Simulator - Simple Vercel Deployment
# Run with: powershell -ExecutionPolicy Bypass -File deploy_simple.ps1

Write-Host "Warhammer Tavern Simulator - Vercel Deployment" -ForegroundColor Magenta
Write-Host "=============================================" -ForegroundColor Magenta

# Check if we're in the right directory
if (-not (Test-Path "vercel.json")) {
    Write-Host "ERROR: vercel.json not found. Please run from project root." -ForegroundColor Red
    exit 1
}

Write-Host "Found vercel.json - we're in the right directory" -ForegroundColor Green

# Try to install Vercel CLI
Write-Host ""
Write-Host "Installing Vercel CLI..." -ForegroundColor Cyan
try {
    npm install -g vercel
    Write-Host "Vercel CLI installed successfully" -ForegroundColor Green
} catch {
    Write-Host "Warning: Could not install Vercel CLI globally" -ForegroundColor Yellow
}

# Environment variables info
Write-Host ""
Write-Host "IMPORTANT: Configure these environment variables in Vercel Dashboard:" -ForegroundColor Yellow
Write-Host "1. GROQ_API_KEY = [YOUR_GROQ_API_KEY_FROM_LOCAL_ENV]" -ForegroundColor White
Write-Host "2. CEREBRAS_API_KEY = [YOUR_CEREBRAS_API_KEY_FROM_LOCAL_ENV]" -ForegroundColor White
Write-Host "3. NODE_ENV = production" -ForegroundColor White
Write-Host "4. VITE_GSAP_UTILIZATION = 138" -ForegroundColor White
Write-Host "5. VITE_ENABLE_3D = true" -ForegroundColor White
Write-Host "6. MAX_AGENTS = 17" -ForegroundColor White

Write-Host ""
Write-Host "Go to: https://vercel.com/dashboard" -ForegroundColor Cyan
Write-Host "Then: Settings > Environment Variables" -ForegroundColor Cyan

Write-Host ""
Write-Host "Press any key to continue with deployment..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Try deployment
Write-Host ""
Write-Host "Attempting deployment..." -ForegroundColor Green

try {
    # Try npx first
    npx vercel --prod --yes
    Write-Host "Deployment completed successfully!" -ForegroundColor Green
} catch {
    try {
        # Try global vercel
        vercel --prod --yes
        Write-Host "Deployment completed successfully!" -ForegroundColor Green
    } catch {
        Write-Host "Deployment failed. Please deploy manually:" -ForegroundColor Red
        Write-Host "1. Run: vercel login" -ForegroundColor White
        Write-Host "2. Run: vercel --prod" -ForegroundColor White
        Write-Host "Or use Vercel Dashboard to import from GitHub" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "Deployment process completed!" -ForegroundColor Magenta
Write-Host "Check your Vercel dashboard for the deployment URL" -ForegroundColor Cyan

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")