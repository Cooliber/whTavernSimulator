# 🚀 Manual Deployment Instructions - Warhammer Tavern Simulator

## ✅ Status: READY FOR DEPLOYMENT

Wszystkie pliki są przygotowane i zoptymalizowane. Vercel CLI zostało zainstalowane.

## 🔑 Krok 1: Konfiguracja Environment Variables

### Metoda A: Vercel Dashboard (ZALECANA)

1. **Idź do Vercel Dashboard**: https://vercel.com/dashboard
2. **Zaloguj się** do swojego konta Vercel
3. **Kliknij "Add New..." → Project**
4. **Import z GitHub** lub **Deploy z lokalnego folderu**
5. **Wybierz folder**: `j:\warhammer_tavern_simulator`
6. **Przejdź do Settings → Environment Variables**
7. **Dodaj następujące zmienne**:

#### 🔐 API Keys (WYMAGANE)
```
Name: GROQ_API_KEY
Value: [YOUR_GROQ_API_KEY_FROM_LOCAL_ENV]
Environment: Production

Name: CEREBRAS_API_KEY  
Value: [YOUR_CEREBRAS_API_KEY_FROM_LOCAL_ENV]
Environment: Production
```

#### ⚙️ Core Settings
```
NODE_ENV = production
PYTHON_ENV = production
MAX_AGENTS = 17
CACHE_ENABLED = true
```

#### 🎮 Frontend Settings
```
VITE_GSAP_UTILIZATION = 138
VITE_ENABLE_3D = true
VITE_MAX_AGENTS = 17
VITE_ANIMATION_QUALITY = high
VITE_ENABLE_PERFORMANCE_MONITORING = true
```

#### 🎯 Lighthouse Targets
```
VITE_TARGET_PERFORMANCE_SCORE = 90
VITE_TARGET_ACCESSIBILITY_SCORE = 95
VITE_TARGET_BEST_PRACTICES_SCORE = 90
```

### Metoda B: Command Line (jeśli PowerShell działa)

1. **Otwórz Command Prompt jako Administrator**
2. **Przejdź do folderu projektu**:
   ```cmd
   cd j:\warhammer_tavern_simulator
   ```
3. **Zaloguj się do Vercel**:
   ```cmd
   npx vercel login
   ```
4. **Dodaj zmienne środowiskowe**:
   ```cmd
   npx vercel env add GROQ_API_KEY production
   npx vercel env add CEREBRAS_API_KEY production
   npx vercel env add NODE_ENV production
   npx vercel env add VITE_GSAP_UTILIZATION production
   ```

## 🚀 Krok 2: Deployment

### Metoda A: Vercel Dashboard
1. **W Vercel Dashboard** kliknij **"Deploy"**
2. **Poczekaj na build** (około 2-5 minut)
3. **Sprawdź deployment URL**

### Metoda B: Command Line
1. **Otwórz Command Prompt jako Administrator**
2. **Przejdź do folderu**:
   ```cmd
   cd j:\warhammer_tavern_simulator
   ```
3. **Deploy**:
   ```cmd
   npx vercel --prod
   ```

### Metoda C: GitHub Integration (NAJLEPSZA)
1. **Push kod do GitHub** (jeśli jeszcze nie)
2. **W Vercel Dashboard** → **Add New Project**
3. **Import from GitHub**
4. **Wybierz repository**: `whTavernSimulator`
5. **Konfiguruj environment variables**
6. **Deploy**

## ✅ Krok 3: Weryfikacja po deployment

Po udanym deployment sprawdź:

### 🌐 Podstawowa funkcjonalność
- [ ] Strona główna ładuje się poprawnie
- [ ] Brak błędów w konsoli przeglądarki
- [ ] API endpoints odpowiadają (sprawdź `/api/health`)

### 🤖 AI i NPCs
- [ ] 17+ NPCs inicjalizuje się poprawnie
- [ ] CrewAI agents odpowiadają
- [ ] Rozmowy z postaciami działają

### 🎮 Game Master Tools
- [ ] Generator NPC działa
- [ ] Tabele losowe ładują się
- [ ] Session management funkcjonalny

### 🎨 Performance i Animacje
- [ ] GSAP animacje działają na 138% utilization
- [ ] Three.js 3D tavern renderuje się
- [ ] Strona ładuje się w <3 sekundy
- [ ] Brak problemów z responsywnością

### 🔍 Lighthouse Audit
Uruchom audit na deployment URL:
- **Performance**: >90
- **Accessibility**: >95  
- **Best Practices**: >90

## 🚨 Troubleshooting

### Problem: "Build failed"
**Rozwiązanie**: 
1. Sprawdź logi build w Vercel Dashboard
2. Upewnij się, że wszystkie environment variables są ustawione
3. Sprawdź czy `warhammer-tavern-web/dist` istnieje

### Problem: "API endpoints not working"
**Rozwiązanie**:
1. Sprawdź czy `GROQ_API_KEY` i `CEREBRAS_API_KEY` są ustawione
2. Sprawdź logi funkcji serverless w Vercel
3. Sprawdź czy `api/index.py` jest poprawny

### Problem: "NPCs not loading"
**Rozwiązanie**:
1. Sprawdź czy `MAX_AGENTS=17` jest ustawione
2. Sprawdź logi API w Vercel Dashboard
3. Sprawdź czy CrewAI dependencies są zainstalowane

### Problem: "Performance issues"
**Rozwiązanie**:
1. Sprawdź czy `VITE_GSAP_UTILIZATION=138` jest ustawione
2. Sprawdź czy `VITE_ENABLE_3D=true` jest ustawione
3. Uruchom Lighthouse audit i sprawdź bottlenecks

## 📊 Expected Results

Po udanym deployment powinieneś zobaczyć:

### 🎯 Performance Metrics
- **Page Load Time**: <3 seconds
- **API Response Time**: <2 seconds  
- **First Contentful Paint**: <2 seconds
- **Time to Interactive**: <5 seconds

### 🏆 Lighthouse Scores
- **Performance**: 90+ (Target: 90)
- **Accessibility**: 95+ (Target: 95)
- **Best Practices**: 90+ (Target: 90)
- **SEO**: 80+

### 🎮 Functionality
- **17+ AI NPCs**: Fully functional
- **GSAP Animations**: 138% utilization
- **Three.js 3D**: Smooth rendering
- **WebSocket**: Real-time communication
- **Game Master Tools**: Complete functionality

## 🎉 Success!

Jeśli wszystko działa poprawnie, powinieneś mieć:

🏰 **Fully functional Warhammer Fantasy Tavern Simulator**
🤖 **17+ AI-powered NPCs with unique personalities**  
🎨 **GSAP animations running at 138% utilization**
🎮 **Complete Game Master toolkit**
⚡ **Lighthouse scores meeting all targets**
🌐 **Production-ready deployment on Vercel**

---

## 📞 Support

Jeśli napotkasz problemy:
1. Sprawdź logi w Vercel Dashboard
2. Sprawdź environment variables
3. Sprawdź czy wszystkie pliki są na miejscu
4. Uruchom lokalny test: `npm run build && npm run preview`

**🏰 Niech rozpocznie się przygoda w tawernie! 🍺**