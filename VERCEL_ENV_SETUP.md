# 🔑 Vercel Environment Variables Setup

## Klucze API z pliku .env

### 🔐 API Keys (WYMAGANE)
```
GROQ_API_KEY = [YOUR_GROQ_API_KEY_HERE]
CEREBRAS_API_KEY = [YOUR_CEREBRAS_API_KEY_HERE]
```

## 📋 Kompletna lista zmiennych środowiskowych dla Vercel

### Core Application Settings
```
NODE_ENV = production
PYTHON_ENV = production
DEBUG = false
LOG_LEVEL = INFO
```

### Performance & Caching
```
MAX_AGENTS = 17
CACHE_ENABLED = true
RETRY_ATTEMPTS = 2
REQUEST_TIMEOUT = 25
COLD_START_OPTIMIZATION = true
LAZY_LOADING = true
CACHE_TIMEOUT = 900
```

### Frontend Configuration (VITE_)
```
VITE_ENABLE_DEBUG = false
VITE_ENABLE_ANALYTICS = true
VITE_ENABLE_PERFORMANCE_MONITORING = true
VITE_MAX_AGENTS = 17
VITE_ANIMATION_QUALITY = high
VITE_ENABLE_3D = true
VITE_GSAP_UTILIZATION = 138
```

### Lighthouse Optimization
```
VITE_OPTIMIZE_LIGHTHOUSE = true
VITE_TARGET_PERFORMANCE_SCORE = 90
VITE_TARGET_ACCESSIBILITY_SCORE = 95
VITE_TARGET_BEST_PRACTICES_SCORE = 90
```

### Three.js Configuration
```
VITE_THREE_RENDERER_PRECISION = highp
VITE_THREE_ANTIALIAS = true
VITE_THREE_POWER_PREFERENCE = high-performance
```

### GSAP Configuration
```
VITE_GSAP_FORCE3D = true
VITE_GSAP_AUTOALPHA = true
VITE_GSAP_LAZY_LOADING = true
```

### Security Headers
```
VITE_ENABLE_SECURITY_HEADERS = true
```

## 🚀 Instrukcje konfiguracji w Vercel Dashboard

### Metoda 1: Vercel Dashboard (Zalecana)
1. Idź do https://vercel.com/dashboard
2. Wybierz swój projekt (lub stwórz nowy)
3. Przejdź do **Settings** → **Environment Variables**
4. Dodaj każdą zmienną z powyższej listy:
   - **Name**: Nazwa zmiennej (np. GROQ_API_KEY)
   - **Value**: Wartość zmiennej
   - **Environment**: Wybierz **Production** (i opcjonalnie Preview/Development)
5. Kliknij **Save**

### Metoda 2: Vercel CLI
```bash
# Zainstaluj Vercel CLI
npm install -g vercel

# Zaloguj się
vercel login

# Dodaj zmienne środowiskowe
vercel env add GROQ_API_KEY production
vercel env add CEREBRAS_API_KEY production
vercel env add NODE_ENV production
# ... itd. dla wszystkich zmiennych
```

### Metoda 3: Automatyczny skrypt
Uruchom jeden z przygotowanych skryptów:
```bash
# Windows PowerShell
powershell -ExecutionPolicy Bypass -File deploy_vercel.ps1

# Windows Command Prompt
deploy.bat
```

## ⚠️ Ważne uwagi

### Bezpieczeństwo
- **NIE** commituj kluczy API do repozytorium
- Klucze są już w `.env` - skopiuj je do Vercel Dashboard
- Użyj różnych kluczy dla development/production jeśli to możliwe

### Wymagane zmienne
Te zmienne są **WYMAGANE** do działania aplikacji:
- `GROQ_API_KEY` - Dla AI agents
- `CEREBRAS_API_KEY` - Dla AI agents
- `NODE_ENV` - Dla optymalizacji
- `VITE_GSAP_UTILIZATION` - Dla animacji

### Opcjonalne zmienne
Te zmienne poprawiają wydajność ale nie są krytyczne:
- Wszystkie `VITE_TARGET_*` - Dla Lighthouse
- Wszystkie `VITE_THREE_*` - Dla Three.js
- Wszystkie `VITE_GSAP_*` - Dla GSAP

## 🎯 Weryfikacja konfiguracji

Po dodaniu zmiennych sprawdź:
1. **Deployment logs** - czy nie ma błędów o brakujących zmiennych
2. **Application functionality** - czy NPCs się inicjalizują
3. **Performance metrics** - czy GSAP działa na 138%
4. **API responses** - czy endpoints odpowiadają

## 🔧 Troubleshooting

### Problem: "Environment variable not found"
**Rozwiązanie**: Sprawdź czy nazwa zmiennej jest dokładnie taka sama (case-sensitive)

### Problem: "API key invalid"
**Rozwiązanie**: Sprawdź czy klucz został skopiowany w całości bez spacji

### Problem: "Build failed"
**Rozwiązanie**: Sprawdź czy wszystkie wymagane zmienne są ustawione

### Problem: "Performance issues"
**Rozwiązanie**: Sprawdź czy `VITE_GSAP_UTILIZATION=138` jest ustawione

## ✅ Checklist przed deployment

- [ ] GROQ_API_KEY dodany
- [ ] CEREBRAS_API_KEY dodany  
- [ ] NODE_ENV=production ustawiony
- [ ] VITE_GSAP_UTILIZATION=138 ustawiony
- [ ] VITE_ENABLE_3D=true ustawiony
- [ ] MAX_AGENTS=17 ustawiony
- [ ] Wszystkie inne zmienne dodane
- [ ] Deployment test przeprowadzony

🏰 **Gotowe do deployment!** 🍺