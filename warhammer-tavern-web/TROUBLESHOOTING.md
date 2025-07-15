# 🔧 Troubleshooting Guide - Warhammer Tavern Simulator

## 🚨 Częste Problemy i Rozwiązania

### 1. Build Errors

#### Problem: "Module not found" podczas build
```bash
Error: Cannot resolve module '@components/...'
```

**Rozwiązanie:**
```bash
# Sprawdź ścieżki w vite.config.js
# Wyczyść cache i reinstaluj
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Problem: "terser not found"
```bash
[vite:terser] terser not found
```

**Rozwiązanie:**
```bash
npm install terser --save-dev
```

#### Problem: "immer not found" z Zustand
```bash
"produce" is not exported by "immer"
```

**Rozwiązanie:**
```bash
npm install immer
```

### 2. WebSocket Connection Issues

#### Problem: WebSocket nie łączy się
```bash
WebSocket connection failed
```

**Diagnostyka:**
```bash
# Sprawdź status backend
curl http://localhost:8000/health

# Sprawdź zmienne środowiskowe
echo $VITE_WS_URL

# Sprawdź czy port jest wolny
netstat -an | grep 8000
```

**Rozwiązanie:**
```bash
# Uruchom backend
cd ../
python api/fastapi_server.py

# Lub użyj Docker
docker-compose up backend
```

### 3. CrewAI Integration Issues

#### Problem: CrewAI agents nie odpowiadają
```bash
CrewAI integration not available
```

**Diagnostyka:**
```bash
# Sprawdź status CrewAI
curl http://localhost:8000/api/crew/status

# Sprawdź logi backend
tail -f logs/crewai.log
```

**Rozwiązanie:**
```bash
# Zrestartuj backend z pełną inicjalizacją
python -c "
from crewai_app import WarhamerTavernCrew
crew = WarhamerTavernCrew()
crew.initialize_mvp_crew()
"
```

### 4. Performance Issues

#### Problem: Niska wydajność animacji
```bash
FPS < 30, stuttering animations
```

**Diagnostyka:**
```bash
# Włącz monitoring wydajności
VITE_ENABLE_PERFORMANCE_MONITORING=true npm run dev

# Sprawdź wykorzystanie GPU
# W DevTools: Performance tab
```

**Rozwiązanie:**
```bash
# Zmniejsz jakość animacji
VITE_ANIMATION_QUALITY=medium

# Wyłącz 3D jeśli potrzeba
VITE_ENABLE_3D=false

# Zmniejsz liczbę agentów
VITE_MAX_AGENTS=10
```

#### Problem: Duży rozmiar bundle
```bash
Bundle size > 1MB
```

**Rozwiązanie:**
```bash
# Analiza bundle
npm run build
npx vite-bundle-analyzer dist

# Optymalizacja w vite.config.js
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        // Lepsze dzielenie chunków
      }
    }
  }
}
```

### 5. Deployment Issues

#### Problem: Vercel deployment fails
```bash
Build failed on Vercel
```

**Diagnostyka:**
```bash
# Test lokalny production build
npm run build
npm run preview

# Sprawdź logi Vercel
vercel logs
```

**Rozwiązanie:**
```bash
# Sprawdź Node.js version w package.json
"engines": {
  "node": ">=18.0.0"
}

# Sprawdź zmienne środowiskowe w Vercel Dashboard
# Upewnij się że wszystkie VITE_ zmienne są ustawione
```

#### Problem: API endpoints nie działają na Vercel
```bash
404 on /api/* routes
```

**Rozwiązanie:**
```bash
# Sprawdź vercel.json routing
{
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" }
  ]
}

# Sprawdź czy api/index.py eksportuje handler
```

### 6. Three.js Issues

#### Problem: WebGL context lost
```bash
WebGL context lost, cannot render 3D
```

**Rozwiązanie:**
```bash
# Dodaj error handling w Three.js setup
renderer.domElement.addEventListener('webglcontextlost', (event) => {
  event.preventDefault()
  // Reinitialize renderer
})
```

#### Problem: Three.js performance na mobile
```bash
Low FPS on mobile devices
```

**Rozwiązanie:**
```bash
# Zmniejsz pixel ratio
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))

# Użyj LOD (Level of Detail)
# Zmniejsz liczbę polygonów na mobile
```

### 7. GSAP Animation Issues

#### Problem: GSAP animations nie działają
```bash
GSAP animations not playing
```

**Rozwiązanie:**
```bash
# Sprawdź czy GSAP jest załadowany
console.log(gsap.version)

# Sprawdź czy elementy istnieją
gsap.set(".element", { opacity: 0 }) // Test

# Sprawdź timeline
const tl = gsap.timeline()
console.log(tl.duration()) // Should be > 0
```

### 8. State Management Issues

#### Problem: Zustand state nie persists
```bash
State resets on page reload
```

**Rozwiązanie:**
```bash
# Sprawdź persist middleware
import { persist } from 'zustand/middleware'

export const useAppStore = create()(
  persist(
    (set, get) => ({
      // state
    }),
    {
      name: 'warhammer-tavern-app',
      // Sprawdź czy localStorage działa
    }
  )
)
```

### 9. Testing Issues

#### Problem: Tests fail z "jsdom not found"
```bash
Environment "jsdom" not found
```

**Rozwiązanie:**
```bash
npm install jsdom --save-dev

# W vite.config.js
test: {
  environment: 'jsdom'
}
```

### 10. Environment Variables

#### Problem: Zmienne środowiskowe nie działają
```bash
import.meta.env.VITE_API_URL is undefined
```

**Rozwiązanie:**
```bash
# Sprawdź prefix VITE_
VITE_API_URL=http://localhost:8000

# Sprawdź czy .env jest w root directory
ls -la .env

# Restart dev server po zmianie .env
npm run dev
```

## 🔍 Debugging Tools

### 1. Browser DevTools
```javascript
// Performance monitoring
window.__TAVERN_DEBUG__ = {
  performance: true,
  verbose: true
}

// GSAP debugging
gsap.globalTimeline.getChildren(true, true, true)

// Three.js debugging
window.scene = scene
window.renderer = renderer
```

### 2. Network Debugging
```bash
# Monitor WebSocket
# W DevTools: Network tab → WS filter

# Monitor API calls
# W DevTools: Network tab → XHR filter

# Check CORS
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     http://localhost:8000/api/health
```

### 3. Performance Profiling
```bash
# Lighthouse audit
npx lighthouse http://localhost:4173 --view

# Bundle analyzer
npx vite-bundle-analyzer dist

# Memory profiling
# DevTools: Memory tab → Heap snapshot
```

## 📞 Wsparcie

### Gdzie szukać pomocy:
1. **GitHub Issues** - zgłoś bug lub feature request
2. **Discord Community** - szybka pomoc od społeczności
3. **Documentation** - sprawdź docs/ folder
4. **Stack Overflow** - tag: warhammer-tavern-simulator

### Informacje do zgłoszenia:
- Wersja Node.js: `node --version`
- Wersja npm: `npm --version`
- System operacyjny
- Przeglądarka i wersja
- Kroki do reprodukcji problemu
- Logi błędów (console, network, backend)

---

**Pamiętaj: Większość problemów można rozwiązać przez restart dev server i wyczyścenie cache! 🔄**
