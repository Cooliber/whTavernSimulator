# 🏰 Warhammer Tavern Simulator - Web Interface

**Advanced Web Interface for Warhammer Fantasy Tavern Simulator with CrewAI Integration**

[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com)
[![React](https://img.shields.io/badge/React-18.2.0-blue?style=for-the-badge&logo=react)](https://reactjs.org)
[![Three.js](https://img.shields.io/badge/Three.js-0.158.0-green?style=for-the-badge&logo=three.js)](https://threejs.org)
[![GSAP](https://img.shields.io/badge/GSAP-3.12.5-brightgreen?style=for-the-badge)](https://greensock.com/gsap)
[![CrewAI](https://img.shields.io/badge/CrewAI-Integrated-purple?style=for-the-badge)](https://crewai.com)

> **Najzaawansowany symulator tawerny Warhammer Fantasy z integracją AI i narzędziami dla Mistrzów Gry**

## 🎯 Funkcjonalności

### 🤖 Integracja CrewAI
- **17+ Agentów AI** z unikalnymi osobowościami i frakcjami
- **Autonomiczne rozmowy** między postaciami
- **Dynamiczne wydarzenia** generowane przez AI
- **System ekonomii** z automatycznym handlem
- **Zarządzanie relacjami** między postaciami

### 🎮 Narzędzia Game Master
- **Generator NPC** z pełnymi statystykami WFRP
- **System losowych spotkań** na drogach Starego Świata
- **Zaczyny przygód** z kontekstem lore
- **Zarządzanie kampanią** z zapisem postępów
- **Tabele losowe** dla wszystkich aspektów gry
- **Tracker inicjatywy** i notatki sesji

### 🎨 Zaawansowane Animacje
- **GSAP 138% Utilization** - najwyższa wydajność animacji
- **Three.js Integration** - renderowanie 3D w czasie rzeczywistym
- **Framer Motion** - płynne przejścia UI
- **Particle Systems** - efekty atmosferyczne
- **Real-time Performance Monitoring** - 60+ FPS

### 🌐 Architektura Produkcyjna
- **Modular Design** - komponenty/services/agents/core
- **WebSocket Real-time** - synchronizacja w czasie rzeczywistym
- **Progressive Web App** - instalacja na urządzeniach
- **Responsive Design** - desktop, tablet, mobile
- **Error Boundaries** - graceful error handling

## 🚀 Quick Start

### Wymagania
- Node.js 18.0.0+
- npm 9.0.0+
- Python 3.9+ (dla backend CrewAI)

### Instalacja

```bash
# Klonuj repozytorium
git clone https://github.com/Cooliber/whTavernSimulator.git
cd whTavernSimulator/warhammer-tavern-web

# Zainstaluj zależności
npm install

# Skopiuj zmienne środowiskowe
cp .env.example .env

# Uruchom w trybie deweloperskim
npm run dev
```

### Zmienne Środowiskowe

```env
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws

# Feature Flags
VITE_ENABLE_DEBUG=true
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_PERFORMANCE_MONITORING=true

# Performance Settings
VITE_MAX_AGENTS=17
VITE_ANIMATION_QUALITY=high
VITE_ENABLE_3D=true
```

## 📦 Deployment na Vercel

### Automatyczne Deployment

1. **Fork repozytorium** na GitHub
2. **Połącz z Vercel** - import projektu z GitHub
3. **Skonfiguruj zmienne środowiskowe** w Vercel Dashboard
4. **Deploy** - automatyczne deployment przy każdym push

### Manualne Deployment

```bash
# Build produkcyjny
npm run build

# Test lokalny
npm run preview

# Deploy na Vercel
npx vercel --prod
```

### Konfiguracja Vercel

```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": { "distDir": "dist" }
    },
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" },
    { "src": "/(.*)", "dest": "/dist/$1" }
  ]
}
```

## 🏗️ Architektura

### Frontend Structure
```
src/
├── components/          # React komponenty
│   ├── animations/      # GSAP & Three.js
│   ├── characters/      # Karty postaci
│   ├── conversations/   # System rozmów
│   ├── gamemaster/      # Narzędzia GM
│   ├── tavern/          # Główny interfejs
│   └── ui/              # Komponenty UI
├── stores/              # Zustand state management
├── utils/               # Utilities i API client
└── tests/               # Testy jednostkowe
```

### Backend Integration
```
api/
├── index.py             # Vercel serverless function
├── fastapi_server.py    # Local development server
├── crewai_integration.py # CrewAI wrapper
└── websocket_manager.py  # Real-time communication
```

## 🧪 Testowanie

```bash
# Uruchom testy
npm test

# Testy z coverage
npm run test:coverage

# Testy UI
npm run test:ui

# Build test
npm run build
npm run preview
```

## 📊 Performance Benchmarks

### Lighthouse Scores (Target)
- **Performance**: >90
- **Accessibility**: >95
- **Best Practices**: >90
- **SEO**: >85

### Bundle Analysis
- **Main Bundle**: ~238KB (gzipped: ~78KB)
- **Vendor Bundle**: ~158KB (gzipped: ~45KB)
- **Animation Bundle**: ~172KB (gzipped: ~60KB)
- **Total**: ~568KB (gzipped: ~183KB)

### Runtime Performance
- **Initial Load**: <3 seconds
- **FPS**: 60+ (desktop), 30+ (mobile)
- **Memory Usage**: <100MB
- **GSAP Utilization**: 138%

## 🔧 Development

### Available Scripts

```bash
npm run dev          # Development server
npm run build        # Production build
npm run preview      # Preview production build
npm run test         # Run tests
npm run lint         # ESLint
npm run format       # Prettier
```

### Code Style
- **ESLint** - kod quality
- **Prettier** - formatowanie
- **Husky** - pre-commit hooks
- **TypeScript** - type safety (opcjonalnie)

## 🐛 Troubleshooting

### Częste Problemy

**Build Errors**
```bash
# Clear cache
rm -rf node_modules dist
npm install
npm run build
```

**WebSocket Connection Issues**
```bash
# Check backend status
curl http://localhost:8000/health

# Verify environment variables
echo $VITE_WS_URL
```

**Performance Issues**
```bash
# Enable performance monitoring
VITE_ENABLE_PERFORMANCE_MONITORING=true npm run dev

# Check bundle size
npm run build
npx vite-bundle-analyzer dist
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Games Workshop** - Warhammer Fantasy universe
- **CrewAI Team** - AI agent framework
- **GSAP Team** - Animation library
- **Three.js Team** - 3D graphics library
- **React Team** - UI framework

---

**Made with ⚔️ for the Old World**
