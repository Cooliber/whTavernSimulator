# Warhammer Tavern Simulator - Vercel Deployment Script
# Run with: powershell -ExecutionPolicy Bypass -File deploy_vercel.ps1

Write-Host "🏰 Warhammer Tavern Simulator - Vercel Deployment" -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Magenta
Write-Host ""

# Function to run commands safely
function Run-Command {
    param([string]$Command)
    try {
        Write-Host "Running: $Command" -ForegroundColor Yellow
        Invoke-Expression $Command
        return $true
    }
    catch {
        Write-Host "Error running command: $_" -ForegroundColor Red
        return $false
    }
}

# Step 1: Check if we're in the right directory
if (-not (Test-Path "vercel.json")) {
    Write-Host "❌ vercel.json not found. Please run from project root." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Found vercel.json - we're in the right directory" -ForegroundColor Green

# Step 2: Install Vercel CLI
Write-Host ""
Write-Host "📦 Installing Vercel CLI..." -ForegroundColor Cyan
$result = Run-Command "npm install -g vercel"
if (-not $result) {
    Write-Host "⚠️  Global install failed, trying npx..." -ForegroundColor Yellow
}

# Step 3: Login to Vercel
Write-Host ""
Write-Host "🔐 Please login to Vercel..." -ForegroundColor Cyan
Write-Host "If this fails, please run manually: vercel login" -ForegroundColor Yellow

# Step 4: Set environment variables
Write-Host ""
Write-Host "🔑 Setting up environment variables..." -ForegroundColor Cyan

$envVars = @{
    "GROQ_API_KEY" = "[YOUR_GROQ_API_KEY_HERE]"
    "CEREBRAS_API_KEY" = "[YOUR_CEREBRAS_API_KEY_HERE]"
    "NODE_ENV" = "production"
    "PYTHON_ENV" = "production"
    "MAX_AGENTS" = "17"
    "CACHE_ENABLED" = "true"
    "RETRY_ATTEMPTS" = "2"
    "REQUEST_TIMEOUT" = "25"
    "COLD_START_OPTIMIZATION" = "true"
    "LAZY_LOADING" = "true"
    "CACHE_TIMEOUT" = "900"
    "VITE_ENABLE_DEBUG" = "false"
    "VITE_ENABLE_ANALYTICS" = "true"
    "VITE_ENABLE_PERFORMANCE_MONITORING" = "true"
    "VITE_MAX_AGENTS" = "17"
    "VITE_ANIMATION_QUALITY" = "high"
    "VITE_ENABLE_3D" = "true"
    "VITE_GSAP_UTILIZATION" = "138"
    "VITE_OPTIMIZE_LIGHTHOUSE" = "true"
    "VITE_TARGET_PERFORMANCE_SCORE" = "90"
    "VITE_TARGET_ACCESSIBILITY_SCORE" = "95"
    "VITE_TARGET_BEST_PRACTICES_SCORE" = "90"
    "VITE_THREE_RENDERER_PRECISION" = "highp"
    "VITE_THREE_ANTIALIAS" = "true"
    "VITE_THREE_POWER_PREFERENCE" = "high-performance"
    "VITE_GSAP_FORCE3D" = "true"
    "VITE_GSAP_AUTOALPHA" = "true"
    "VITE_GSAP_LAZY_LOADING" = "true"
}

Write-Host ""
Write-Host "Environment variables to be set:" -ForegroundColor Yellow
foreach ($key in $envVars.Keys) {
    if ($key -like "*API_KEY*") {
        Write-Host "  $key = [HIDDEN]" -ForegroundColor Gray
    } else {
        Write-Host "  $key = $($envVars[$key])" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "⚠️  IMPORTANT: You need to set these manually in Vercel Dashboard:" -ForegroundColor Yellow
Write-Host "1. Go to https://vercel.com/dashboard" -ForegroundColor White
Write-Host "2. Select your project" -ForegroundColor White
Write-Host "3. Go to Settings > Environment Variables" -ForegroundColor White
Write-Host "4. Add the variables listed above" -ForegroundColor White

# Step 5: Deploy
Write-Host ""
Write-Host "🚀 Ready to deploy to Vercel..." -ForegroundColor Cyan
Write-Host "Press any key to continue with deployment, or Ctrl+C to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Deploying to Vercel..." -ForegroundColor Green

# Try different ways to run vercel
$deploySuccess = $false

# Try npx first
Write-Host "Trying npx vercel..." -ForegroundColor Yellow
$result = Run-Command "npx vercel --prod --yes"
if ($result) {
    $deploySuccess = $true
} else {
    # Try global vercel
    Write-Host "Trying global vercel..." -ForegroundColor Yellow
    $result = Run-Command "vercel --prod --yes"
    if ($result) {
        $deploySuccess = $true
    }
}

# Final status
Write-Host ""
if ($deploySuccess) {
    Write-Host "🎉 Deployment completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎯 Next steps:" -ForegroundColor Cyan
    Write-Host "1. ✅ Check deployment URL" -ForegroundColor White
    Write-Host "2. ✅ Test all Game Master tools" -ForegroundColor White
    Write-Host "3. ✅ Verify 17+ NPCs are working" -ForegroundColor White
    Write-Host "4. ✅ Test GSAP 138% utilization" -ForegroundColor White
    Write-Host "5. ✅ Run Lighthouse audit" -ForegroundColor White
    Write-Host "6. ✅ Monitor performance metrics" -ForegroundColor White
    Write-Host ""
    Write-Host "🏰 Your Warhammer Fantasy Tavern is now LIVE! 🍺" -ForegroundColor Magenta
} else {
    Write-Host "❌ Deployment failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Manual deployment options:" -ForegroundColor Yellow
    Write-Host "1. Install Vercel CLI: npm install -g vercel" -ForegroundColor White
    Write-Host "2. Login: vercel login" -ForegroundColor White
    Write-Host "3. Deploy: vercel --prod" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use Vercel Dashboard:" -ForegroundColor Yellow
    Write-Host "1. Go to https://vercel.com/new" -ForegroundColor White
    Write-Host "2. Import from GitHub" -ForegroundColor White
    Write-Host "3. Configure environment variables" -ForegroundColor White
    Write-Host "4. Deploy" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")