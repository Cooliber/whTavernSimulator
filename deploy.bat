@echo off
echo 🏰 Warhammer Tavern Simulator - Vercel Deployment
echo ================================================

echo.
echo 📋 Step 1: Installing Vercel CLI...
call npm install -g vercel

echo.
echo 🔑 Step 2: Setting up environment variables...
echo Setting GROQ_API_KEY...
call vercel env add GROQ_API_KEY production
echo [ENTER_YOUR_GROQ_API_KEY]

echo.
echo Setting CEREBRAS_API_KEY...
call vercel env add CEREBRAS_API_KEY production
echo [ENTER_YOUR_CEREBRAS_API_KEY]

echo.
echo Setting NODE_ENV...
call vercel env add NODE_ENV production
echo production

echo.
echo Setting PYTHON_ENV...
call vercel env add PYTHON_ENV production
echo production

echo.
echo Setting MAX_AGENTS...
call vercel env add MAX_AGENTS production
echo 17

echo.
echo Setting CACHE_ENABLED...
call vercel env add CACHE_ENABLED production
echo true

echo.
echo Setting VITE_ENABLE_3D...
call vercel env add VITE_ENABLE_3D production
echo true

echo.
echo Setting VITE_GSAP_UTILIZATION...
call vercel env add VITE_GSAP_UTILIZATION production
echo 138

echo.
echo Setting VITE_MAX_AGENTS...
call vercel env add VITE_MAX_AGENTS production
echo 17

echo.
echo Setting VITE_ANIMATION_QUALITY...
call vercel env add VITE_ANIMATION_QUALITY production
echo high

echo.
echo 🚀 Step 3: Deploying to Vercel...
call vercel --prod

echo.
echo ✅ Deployment completed!
echo.
echo 🎯 Next steps:
echo 1. Check deployment URL
echo 2. Test all functionality
echo 3. Run Lighthouse audit
echo 4. Monitor performance
echo.
echo 🏰 Your Warhammer Tavern is now live! 🍺

pause