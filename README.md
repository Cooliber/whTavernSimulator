# 🏰 Warhammer Fantasy Tavern Simulator

**Zaawansowany symulator tawerny z uniwersum Warhammer Fantasy z AI-powered NPCs, systemem rozmów i narzędziami dla Mistrzów Gry.**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Cooliber/whTavernSimulator)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 🎯 Przegląd

Warhammer Fantasy Tavern Simulator to zaawansowana aplikacja łącząca backend Python z frontendem React, oferująca:

- **🤖 17+ AI-powered NPCs** z unikalnymi osobowościami z uniwersum Warhammer Fantasy
- **💬 Zaawansowany system rozmów** z uczestnictwem użytkownika
- **👑 Narzędzia dla Mistrzów Gry** - generator NPC, spotkań, przygód
- **🎨 Immersive 3D interface** z animacjami GSAP i Three.js
- **⚡ Real-time WebSocket** komunikacja
- **🎲 Authentic WFRP content** z oficjalnymi danymi

## 🚀 Quick Start

### Backend (Python)
```bash
# Klonuj repozytorium
git clone https://github.com/Cooliber/whTavernSimulator.git
cd whTavernSimulator

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom serwer API
python start_api_server.py
```

### Frontend (React)
```bash
# Przejdź do folderu frontend
cd warhammer-tavern-web

# Zainstaluj zależności
npm install

# Uruchom aplikację
npm run dev
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5173`

## 📁 Struktura Projektu

```
whTavernSimulator/
├── 🐍 Backend (Python)
│   ├── agents/          # AI agents (NPCs)
│   ├── api/             # FastAPI endpoints
│   ├── core/            # Logika gry
│   ├── services/        # Serwisy (LLM, pamięć)
│   └── components/      # Komponenty UI (Streamlit)
│
├── ⚛️ Frontend (React)
│   └── warhammer-tavern-web/
│       ├── src/
│       │   ├── components/  # React komponenty
│       │   ├── stores/      # Zustand stores
│       │   └── styles/      # CSS/Tailwind
│       └── public/
│
├── 📚 Documentation
│   └── docs/            # Pełna dokumentacja
│
├── 🧪 Testing
│   └── tests/           # Testy jednostkowe
│
├── 📝 Examples
│   └── examples/        # Przykłady użycia
│
└── 🔧 Scripts
    └── scripts/         # Skrypty deployment
```

## ✨ Główne Funkcje

### 🏰 Symulator Tawerny
- **Immersive 3D environment** z animacjami
- **Dynamic atmosphere** reagująca na wydarzenia
- **Real-time character interactions**
- **Faction-based behaviors** (Empire, Chaos, Elves, Dwarfs, Orcs)

### 🤖 AI-Powered NPCs
- **17+ unikalnych postaci** z Warhammer Fantasy
- **Authentic personalities** zgodne z lore
- **Dynamic conversations** z kontekstem
- **Memory system** pamiętający interakcje

### 💬 System Rozmów
- **User participation** w rozmowach NPC
- **Quick response system** z faction-specific odpowiedziami
- **Conversation bubbles** nad postaciami w 3D
- **Emotion-based animations** GSAP

### 👑 Game Master Tools
- **NPC Generator** z prawdziwymi statystykami WFRP
- **Random Encounters** dla różnych lokacji
- **Adventure Hooks** w 5 kategoriach
- **Campaign Manager** do długotrwałych kampanii
- **Random Tables** z oficjalnych źródeł

## 🛠️ Technologie

### Backend
- **Python 3.8+** - główny język
- **FastAPI** - REST API i WebSocket
- **CrewAI** - orkiestracja AI agents
- **Streamlit** - alternatywny UI
- **SQLite** - baza danych

### Frontend
- **React 18** - główny framework
- **Vite** - build tool
- **Tailwind CSS** - styling
- **Framer Motion** - animacje
- **GSAP** - zaawansowane animacje 3D
- **Three.js** - 3D graphics
- **Zustand** - state management

### AI & Services
- **OpenAI GPT** - główny model językowy
- **Groq** - szybkie inferowanie
- **Cerebras** - alternatywny provider
- **WebSocket** - real-time komunikacja

## 🚀 Deployment

### Vercel (Recommended)
```bash
# Automatyczne deployment
vercel --prod

# Lub użyj przycisku Deploy
```

### Docker
```bash
# Build i uruchom
docker-compose up --build
```

### Manual
```bash
# Backend
python start_api_server.py

# Frontend
cd warhammer-tavern-web
npm run build
npm run preview
```

## 📖 Dokumentacja

Pełna dokumentacja dostępna w folderze [`docs/`](docs/):

- 📋 [Features Overview](docs/FEATURES.md)
- 🏗️ [Architecture Guide](docs/MODULAR_ARCHITECTURE_COMPLETE.md)
- 🎮 [Game Master Tools](docs/GAME_MASTER_TOOLS_SUMMARY.md)
- 💬 [Conversation System](docs/CONVERSATION_SYSTEM_SUMMARY.md)
- 🚀 [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- 🎨 [UI Enhancement](docs/ENHANCED_UI_README.md)

## 🧪 Testing

```bash
# Uruchom wszystkie testy
python -m pytest tests/

# Testy konkretnego modułu
python -m pytest tests/test_agents.py

# Testy z coverage
python -m pytest --cov=. tests/
```

## 🤝 Contributing

1. Fork repozytorium
2. Stwórz branch dla feature (`git checkout -b feature/amazing-feature`)
3. Commit zmiany (`git commit -m 'Add amazing feature'`)
4. Push do branch (`git push origin feature/amazing-feature`)
5. Otwórz Pull Request

## 📄 License

Ten projekt jest licencjonowany na licencji MIT - zobacz plik [LICENSE](LICENSE) dla szczegółów.

## 🙏 Acknowledgments

- **Games Workshop** za uniwersum Warhammer Fantasy
- **Cubicle 7** za WFRP 4th Edition
- **OpenAI** za GPT models
- **Vercel** za hosting platform
- **Community** za feedback i wsparcie

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/Cooliber/whTavernSimulator/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Cooliber/whTavernSimulator/discussions)
- 📧 **Email**: support@whtavernsimulator.com

---

**Stworzony z ❤️ dla społeczności Warhammer Fantasy Roleplay**

*"W tawernie każdy ma swoją historię do opowiedzenia..."* 🍺⚔️