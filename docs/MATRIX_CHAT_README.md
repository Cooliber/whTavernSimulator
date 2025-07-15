# 🔋 Matrix Chat Interface - Warhammer Tavern Simulator

## Przegląd

**Matrix Chat Interface** to zaawansowany system wizualizacji rozmów dla Warhammer Tavern Simulator, który oferuje immersyjne doświadczenie czatu z efektami inspirowanymi filmem Matrix. System zapewnia płynne animacje, wielowymiarowe rozmowy i dynamiczne efekty wizualne.

## ✨ Kluczowe Funkcje

### 🎭 Efekty Matrix
- **Matrix Rain**: Animowany deszcz znaków w tle
- **Typewriter Effect**: Tekst pojawiający się znak po znaku
- **Matrix Text Reveal**: Tekst odkrywający się przez losowe znaki
- **Glow Effects**: Świecące obramowania i cienie
- **Shake Effects**: Animacje trzęsienia dla pilnych wiadomości

### 💬 Zaawansowane Rozmowy
- **Multi-dimensional Chat**: Różne typy wiadomości (szept, krzyk, myśl, akcja, magia)
- **Floating Bubbles**: Unoszące się dymki dla ważnych wiadomości
- **Emotion-based Styling**: Kolory i efekty bazowane na emocjach
- **Priority System**: Wizualne oznaczenia ważności wiadomości
- **Conversation Flow Tracking**: Śledzenie przepływu rozmów między agentami

### 🎨 Wizualne Ulepszenia
- **Responsive Design**: Dostosowuje się do różnych rozmiarów ekranu
- **Smooth Animations**: 60+ FPS animacje z GSAP
- **Custom Fonts**: Futurystyczna czcionka Orbitron
- **Dynamic Colors**: Kolory dostosowane do typu wiadomości i emocji
- **Performance Monitoring**: Monitorowanie FPS i użycia pamięci

## 🚀 Instalacja i Uruchomienie

### Wymagania
- Python 3.8+
- Streamlit
- GSAP (ładowane z CDN)
- Particles.js (ładowane z CDN)

### Uruchomienie Demo Streamlit
```bash
cd warhammer_tavern_simulator
streamlit run matrix_chat_demo.py
```

### Uruchomienie Standalone Demo
Otwórz plik `matrix_chat_standalone.html` w przeglądarce.

## 📁 Struktura Plików

```
components/
├── matrix_chat_interface.py    # Główny komponent interfejsu
matrix_chat_demo.py             # Demo aplikacja Streamlit
matrix_chat_standalone.html     # Standalone HTML demo
matrix_chat_standalone.js       # JavaScript dla standalone demo
MATRIX_CHAT_README.md          # Ta dokumentacja
```

## 🎮 Użycie

### Podstawowe Użycie w Streamlit

```python
from components.matrix_chat_interface import MatrixChatInterface, ChatMessage
from datetime import datetime

# Inicjalizacja interfejsu
chat_interface = MatrixChatInterface()

# Tworzenie wiadomości
message = ChatMessage(
    id="msg_1",
    sender="Karczmarz",
    receiver="Skrytobójca",
    content="Witaj w mojej karczmie!",
    message_type="whisper",
    emotion="happy",
    priority=5,
    timestamp=datetime.now(),
    effects=["glow", "typewriter"],
    color_theme="gold",
    duration=4.0
)

# Dodanie wiadomości
chat_interface.add_message(message)

# Renderowanie interfejsu
chat_interface.render_matrix_chat(height=600)
```

### Typy Wiadomości

| Typ | Opis | Efekty |
|-----|------|--------|
| `whisper` | Szept, prywatna wiadomość | Kursywa, przezroczystość |
| `shout` | Krzyk, ważna wiadomość | Wielkie litery, pulsowanie |
| `thought` | Myśl, wewnętrzny monolog | Kursywa, przerywana ramka |
| `action` | Akcja, czynność | Pogrubienie, pomarańczowa ramka |
| `magic` | Magia, zaklęcie | Fioletowe tło, migotanie |

### Emocje i Kolory

| Emocja | Kolor | Efekt |
|--------|-------|-------|
| `angry` | Czerwony | Intensywny blask |
| `happy` | Zielony | Łagodny blask |
| `mysterious` | Fioletowy | Migotanie |
| `urgent` | Pomarańczowy | Pulsowanie |
| `calm` | Niebieski | Spokojny blask |

### Efekty Wizualne

| Efekt | Opis |
|-------|------|
| `matrix` | Tekst odkrywający się przez Matrix znaki |
| `glow` | Świecące obramowanie |
| `shake` | Trzęsienie elementu |
| `typewriter` | Tekst pojawiający się znak po znaku |
| `fade` | Płynne pojawianie się |

## ⚙️ Konfiguracja

### Ustawienia Czatu

```python
chat_interface.set_chat_settings(
    matrix_mode=True,           # Włącz efekt Matrix rain
    auto_scroll=True,           # Automatyczne przewijanie
    sound_enabled=True,         # Efekty dźwiękowe
    effect_intensity=0.8,       # Intensywność efektów (0.0-1.0)
    max_messages=100            # Maksymalna liczba wiadomości
)
```

### Ustawienia Wydajności

```python
# W session state
st.session_state.matrix_chat_state['performance'] = {
    'fps': 60,                  # Docelowe FPS
    'particles': 500,           # Liczba cząsteczek Matrix
    'effects_quality': 'high'   # Jakość efektów: 'low', 'medium', 'high'
}
```

## 🎯 Funkcje Demo

### Kontrolki Demo
- **📨 Random Message**: Dodaje losową wiadomość
- **💥 Urgent Alert**: Dodaje pilny alarm
- **🔮 Magic Message**: Dodaje magiczną wiadomość
- **🤖 Auto Demo**: Automatyczne generowanie wiadomości
- **🗑️ Clear Chat**: Czyszczenie czatu

### Auto Demo
Auto demo automatycznie generuje wiadomości w określonych odstępach czasu, symulując żywą rozmowę w karczmie.

## 📊 Monitorowanie Wydajności

Interface automatycznie monitoruje:
- **FPS**: Klatki na sekundę
- **Message Count**: Liczba wiadomości
- **Effect Count**: Liczba aktywnych efektów
- **Memory Usage**: Użycie pamięci (jeśli dostępne)

## 🔧 Integracja z Istniejącym Systemem

### Integracja z Agent Manager

```python
from services.agent_manager import AgentManager, AgentCommunication

def convert_agent_communication_to_chat_message(comm: AgentCommunication) -> ChatMessage:
    """Konwertuje komunikację agenta na wiadomość czatu"""
    return ChatMessage(
        id=f"agent_comm_{int(time.time())}",
        sender=comm.sender,
        receiver=comm.receiver,
        content=comm.message,
        message_type=comm.message_type,
        emotion="calm" if comm.priority < 5 else "urgent",
        priority=comm.priority,
        timestamp=comm.timestamp,
        effects=["glow"] if comm.priority > 7 else ["fade"],
        color_theme="gold",
        duration=3.0 + comm.priority * 0.5
    )
```

### Integracja z Tavern Simulator

```python
def process_tavern_events_to_chat(simulator, chat_interface):
    """Przetwarza wydarzenia z symulatora na wiadomości czatu"""
    events = simulator.get_recent_events()
    
    for event in events:
        if event.type == "character_interaction":
            message = ChatMessage(
                id=f"event_{event.id}",
                sender=event.character1.name,
                receiver=event.character2.name,
                content=event.description,
                message_type="action",
                emotion=event.mood,
                priority=event.importance,
                timestamp=event.timestamp,
                effects=["typewriter"],
                color_theme="blue",
                duration=4.0
            )
            chat_interface.add_message(message)
```

## 🎨 Customizacja

### Dodawanie Nowych Efektów

1. Dodaj efekt do CSS w `_get_matrix_chat_css()`
2. Implementuj logikę w JavaScript w `_get_matrix_chat_javascript()`
3. Dodaj efekt do listy dostępnych efektów

### Nowe Typy Wiadomości

1. Dodaj styl CSS dla nowego typu
2. Dodaj obsługę w `getMessageAlignment()`
3. Dodaj do dokumentacji

## 🐛 Rozwiązywanie Problemów

### Problemy z Wydajnością
- Zmniejsz `effect_intensity`
- Ogranicz `max_messages`
- Wyłącz `matrix_mode` dla słabszych urządzeń

### Problemy z Animacjami
- Sprawdź czy GSAP jest poprawnie załadowany
- Sprawdź konsolę przeglądarki pod kątem błędów JavaScript
- Upewnij się, że `force3D` jest włączone

### Problemy z Particles.js
- Sprawdź czy particles.js jest załadowany
- Zmniejsz liczbę cząsteczek w konfiguracji
- Sprawdź czy element `matrix-rain` istnieje

## 🚀 Przyszłe Ulepszenia

- [ ] Integracja z WebRTC dla czatu głosowego
- [ ] Wsparcie dla emoji i reakcji
- [ ] Zaawansowane filtry rozmów
- [ ] Eksport historii czatu
- [ ] Integracja z AI dla automatycznych odpowiedzi
- [ ] Wsparcie dla załączników
- [ ] Tryb ciemny/jasny
- [ ] Personalizowane awatary

## 📝 Licencja

Ten komponent jest częścią Warhammer Tavern Simulator i podlega tym samym warunkom licencyjnym.

---

**Stworzony z pasją dla najlepszych interfejsów użytkownika! 🔋✨**
