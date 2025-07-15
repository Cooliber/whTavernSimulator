import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sword, RefreshCw, Save, Copy, MapPin, Clock, Users, Skull } from 'lucide-react'
import toast from 'react-hot-toast'

// WFRP Encounter Types by Location
const EncounterTypes = {
  road: {
    name: 'Drogi',
    icon: '🛤️',
    color: 'text-amber-400',
    encounters: [
      {
        type: 'Bandyci',
        description: 'Grupa {1d4+2} bandytów atakuje podróżników',
        threat: 'Średnie',
        loot: '2d10 szylingów srebrnych, broń',
        tactics: 'Zasadzka z ukrycia, żądają okupu'
      },
      {
        type: 'Patrol Straży Drogowej',
        description: 'Patrol {1d6+2} strażników sprawdza dokumenty',
        threat: 'Niskie',
        loot: 'Informacje, ewentualnie pomoc',
        tactics: 'Rutynowa kontrola, podejrzliwi wobec obcych'
      },
      {
        type: 'Kupiecka Karawana',
        description: 'Karawana {2d4} kupców z {1d6+4} strażnikami',
        threat: 'Niskie',
        loot: 'Towary handlowe, informacje o cenach',
        tactics: 'Ostrożni, ale chętni do handlu'
      },
      {
        type: 'Mutanci Chaosu',
        description: 'Grupa {1d4+1} mutantów Chaosu',
        threat: 'Wysokie',
        loot: 'Artefakty Chaosu (niebezpieczne)',
        tactics: 'Szaleńczy atak, nieprzewidywalni'
      },
      {
        type: 'Pielgrzymi',
        description: '{2d6+4} pielgrzymów w drodze do świątyni',
        threat: 'Niskie',
        loot: 'Błogosławieństwa, informacje religijne',
        tactics: 'Pokojowi, proszą o ochronę'
      },
      {
        type: 'Łowcy Nagród',
        description: '{1d3+1} łowców nagród szuka przestępcy',
        threat: 'Średnie',
        loot: 'Listy gończe, informacje o przestępcach',
        tactics: 'Profesjonalni, pytają o poszukiwanego'
      }
    ]
  },
  
  forest: {
    name: 'Las',
    icon: '🌲',
    color: 'text-green-400',
    encounters: [
      {
        type: 'Orki',
        description: 'Grupa {1d6+2} orków poluje w lesie',
        threat: 'Wysokie',
        loot: 'Prymitywne bronie, zdobyczne przedmioty',
        tactics: 'Brutalny atak, walczą do śmierci'
      },
      {
        type: 'Elfy Leśne',
        description: '{1d4+1} elfów leśnych strzeże swojego terytorium',
        threat: 'Średnie',
        loot: 'Elfickie strzały, zioła lecznicze',
        tactics: 'Ostrzegają przed wejściem, atakują z ukrycia'
      },
      {
        type: 'Niedźwiedź',
        description: 'Wielki niedźwiedź broni swojego terytorium',
        threat: 'Wysokie',
        loot: 'Skóra niedźwiedzia, mięso',
        tactics: 'Agresywny jeśli zagrożony, można go odstraszyć'
      },
      {
        type: 'Drwale',
        description: 'Grupa {1d4+2} drwali pracuje w lesie',
        threat: 'Niskie',
        loot: 'Drewno, narzędzia, informacje lokalne',
        tactics: 'Przyjazni, znają okolicę'
      },
      {
        type: 'Wilki',
        description: 'Wataha {2d4} wilków poluje',
        threat: 'Średnie',
        loot: 'Skóry wilków',
        tactics: 'Atakują grupowo, uciekają gdy przegrywają'
      },
      {
        type: 'Pustelnik',
        description: 'Stary pustelnik mieszka w leśnej chacie',
        threat: 'Niskie',
        loot: 'Mądrość, mikstury lecznicze',
        tactics: 'Pokojowy, oferuje schronienie'
      }
    ]
  },
  
  city: {
    name: 'Miasto',
    icon: '🏘️',
    color: 'text-blue-400',
    encounters: [
      {
        type: 'Kieszonkowcy',
        description: '{1d3} młodych złodziei próbuje okraść',
        threat: 'Niskie',
        loot: 'Skradzione przedmioty',
        tactics: 'Szybki atak i ucieczka'
      },
      {
        type: 'Patrol Straży',
        description: '{1d4+2} strażników miejskich patroluje',
        threat: 'Niskie',
        loot: 'Informacje, pomoc prawna',
        tactics: 'Rutynowy patrol, reagują na przestępstwa'
      },
      {
        type: 'Kultysci Chaosu',
        description: '{1d4+1} ukrytych kultystów planuje rytuał',
        threat: 'Wysokie',
        loot: 'Zakazane księgi, symbole Chaosu',
        tactics: 'Działają w ukryciu, desperacko bronią tajemnicy'
      },
      {
        type: 'Kupcy',
        description: 'Grupa {1d6} kupców handluje na targu',
        threat: 'Niskie',
        loot: 'Różnorodne towary',
        tactics: 'Chcą sprzedać, targują się'
      },
      {
        type: 'Szlachcic',
        description: 'Arrogancki szlachcic z {1d4+1} strażnikami',
        threat: 'Średnie',
        loot: 'Cenne przedmioty, dokumenty',
        tactics: 'Wyniosły, używa wpływów'
      },
      {
        type: 'Żebracy',
        description: 'Grupa {2d4} żebraków prosi o jałmużnę',
        threat: 'Niskie',
        loot: 'Plotki, informacje z ulicy',
        tactics: 'Natarczywie proszą, mogą być informatami'
      }
    ]
  },
  
  dungeon: {
    name: 'Podziemia',
    icon: '🕳️',
    color: 'text-purple-400',
    encounters: [
      {
        type: 'Szkielety',
        description: '{1d6+2} szkieletów strzeże komnaty',
        threat: 'Średnie',
        loot: 'Starożytne bronie, monety',
        tactics: 'Atakują bez strachu, walczą do zniszczenia'
      },
      {
        type: 'Szczury Olbrzymie',
        description: 'Wataha {2d6} olbrzymich szczurów',
        threat: 'Średnie',
        loot: 'Nic wartościowego',
        tactics: 'Atakują grupowo, przenoszą choroby'
      },
      {
        type: 'Goblin Patrol',
        description: '{1d4+3} goblinów patroluje korytarze',
        threat: 'Średnie',
        loot: 'Prymitywne bronie, błyszczące przedmioty',
        tactics: 'Tchórzliwi, uciekają gdy przegrywają'
      },
      {
        type: 'Pułapka',
        description: 'Mechaniczna pułapka w korytarzu',
        threat: 'Różne',
        loot: 'Mechanizmy, czasem skarby',
        tactics: 'Wymaga wykrycia i rozbrojenia'
      },
      {
        type: 'Duch',
        description: 'Niespokojny duch dawnego mieszkańca',
        threat: 'Wysokie',
        loot: 'Informacje o przeszłości',
        tactics: 'Ataki psychiczne, może być uspokojony'
      },
      {
        type: 'Skarb',
        description: 'Ukryta skrytka ze skarbem',
        threat: 'Niskie',
        loot: '{2d6} koron złotych, klejnoty',
        tactics: 'Może być chroniona pułapkami'
      }
    ]
  }
}

// Weather conditions affecting encounters
const WeatherConditions = [
  { name: 'Słonecznie', modifier: 'Normalna widoczność', effect: 'Brak modyfikatorów' },
  { name: 'Deszcz', modifier: '-10 do Percepcji', effect: 'Trudniejsze śledzenie' },
  { name: 'Mgła', modifier: '-20 do Percepcji', effect: 'Ograniczona widoczność' },
  { name: 'Śnieg', modifier: '-10 do Zręczności', effect: 'Śliska powierzchnia' },
  { name: 'Wiatr', modifier: '-10 do BS', effect: 'Utrudnione strzelanie' },
  { name: 'Burza', modifier: '-20 do wszystkich testów', effect: 'Ekstremalne warunki' }
]

// Time of day modifiers
const TimeOfDay = [
  { name: 'Świt', modifier: 'Zmęczenie po nocy', effect: '-10 do Inicjatywy' },
  { name: 'Rano', modifier: 'Świeżość', effect: '+5 do testów Percepcji' },
  { name: 'Południe', modifier: 'Pełna aktywność', effect: 'Brak modyfikatorów' },
  { name: 'Popołudnie', modifier: 'Lekkie zmęczenie', effect: '-5 do testów Wytrzymałości' },
  { name: 'Wieczór', modifier: 'Słabe światło', effect: '-10 do testów wzroku' },
  { name: 'Noc', modifier: 'Ciemność', effect: '-20 do testów bez źródła światła' }
]

export const RandomEncounters = ({ gmMode, sessionData, onSessionDataUpdate }) => {
  const [generatedEncounter, setGeneratedEncounter] = useState(null)
  const [selectedLocation, setSelectedLocation] = useState('road')
  const [selectedWeather, setSelectedWeather] = useState(0)
  const [selectedTime, setSelectedTime] = useState(2)
  const [isGenerating, setIsGenerating] = useState(false)
  const [encounterHistory, setEncounterHistory] = useState([])

  // Load encounter history
  useEffect(() => {
    const saved = localStorage.getItem('wfrp_encounter_history')
    if (saved) {
      try {
        setEncounterHistory(JSON.parse(saved))
      } catch (error) {
        console.error('Error loading encounter history:', error)
      }
    }
  }, [])

  // Generate random encounter
  const generateEncounter = () => {
    setIsGenerating(true)
    
    setTimeout(() => {
      const location = EncounterTypes[selectedLocation]
      const encounters = location.encounters
      const encounter = encounters[Math.floor(Math.random() * encounters.length)]
      const weather = WeatherConditions[selectedWeather]
      const time = TimeOfDay[selectedTime]

      // Generate additional details
      const distance = Math.floor(Math.random() * 200) + 50 // 50-250 meters
      const surprise = Math.random() < 0.3 // 30% chance of surprise
      const mood = ['Hostile', 'Neutral', 'Friendly'][Math.floor(Math.random() * 3)]

      const generatedEncounter = {
        id: Date.now(),
        location: location.name,
        encounter: encounter,
        weather: weather,
        time: time,
        distance: `${distance}m`,
        surprise: surprise,
        mood: mood,
        timestamp: Date.now(),
        notes: ''
      }

      setGeneratedEncounter(generatedEncounter)
      
      // Add to history
      const newHistory = [generatedEncounter, ...encounterHistory.slice(0, 19)] // Keep last 20
      setEncounterHistory(newHistory)
      localStorage.setItem('wfrp_encounter_history', JSON.stringify(newHistory))
      
      setIsGenerating(false)
      toast.success('Wygenerowano spotkanie!')
    }, 800)
  }

  // Copy encounter to clipboard
  const copyEncounter = () => {
    if (!generatedEncounter) return

    const encounterText = `
SPOTKANIE: ${generatedEncounter.encounter.type}
Lokacja: ${generatedEncounter.location}
Czas: ${generatedEncounter.time.name}
Pogoda: ${generatedEncounter.weather.name}

OPIS: ${generatedEncounter.encounter.description}
Zagrożenie: ${generatedEncounter.encounter.threat}
Dystans: ${generatedEncounter.distance}
Zaskoczenie: ${generatedEncounter.surprise ? 'Tak' : 'Nie'}
Nastawienie: ${generatedEncounter.mood}

TAKTYKA: ${generatedEncounter.encounter.tactics}
ŁUPY: ${generatedEncounter.encounter.loot}

MODYFIKATORY:
${generatedEncounter.weather.name}: ${generatedEncounter.weather.modifier}
${generatedEncounter.time.name}: ${generatedEncounter.time.modifier}
    `.trim()

    navigator.clipboard.writeText(encounterText)
    toast.success('Spotkanie skopiowane do schowka!')
  }

  // Save encounter notes
  const saveEncounterNotes = (notes) => {
    if (!generatedEncounter) return

    const updatedEncounter = { ...generatedEncounter, notes }
    setGeneratedEncounter(updatedEncounter)

    // Update in history
    const updatedHistory = encounterHistory.map(enc => 
      enc.id === generatedEncounter.id ? updatedEncounter : enc
    )
    setEncounterHistory(updatedHistory)
    localStorage.setItem('wfrp_encounter_history', JSON.stringify(updatedHistory))
  }

  const getThreatColor = (threat) => {
    switch (threat) {
      case 'Niskie': return 'text-green-400 bg-green-400/20 border-green-400/50'
      case 'Średnie': return 'text-yellow-400 bg-yellow-400/20 border-yellow-400/50'
      case 'Wysokie': return 'text-red-400 bg-red-400/20 border-red-400/50'
      default: return 'text-gray-400 bg-gray-400/20 border-gray-400/50'
    }
  }

  const getMoodColor = (mood) => {
    switch (mood) {
      case 'Friendly': return 'text-green-400'
      case 'Neutral': return 'text-yellow-400'
      case 'Hostile': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  return (
    <div className="h-full flex flex-col p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-medieval text-white mb-2">Losowe Spotkania</h3>
          <p className="text-secondary-300">
            Generuj spotkania dla różnych lokacji w Starym Świecie
          </p>
        </div>
        
        <button
          onClick={generateEncounter}
          disabled={isGenerating}
          className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-secondary-600 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          {isGenerating ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <Sword className="w-4 h-4" />
          )}
          {isGenerating ? 'Generowanie...' : 'Generuj Spotkanie'}
        </button>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Configuration Panel */}
        <div className="space-y-6">
          <div className="bg-secondary-700/50 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-3">Konfiguracja</h4>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-secondary-300 mb-2">
                  Lokacja
                </label>
                <select
                  value={selectedLocation}
                  onChange={(e) => setSelectedLocation(e.target.value)}
                  className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                >
                  {Object.entries(EncounterTypes).map(([key, location]) => (
                    <option key={key} value={key}>
                      {location.icon} {location.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-secondary-300 mb-2">
                  Pogoda
                </label>
                <select
                  value={selectedWeather}
                  onChange={(e) => setSelectedWeather(parseInt(e.target.value))}
                  className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                >
                  {WeatherConditions.map((weather, index) => (
                    <option key={index} value={index}>
                      {weather.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-secondary-300 mb-2">
                  Pora Dnia
                </label>
                <select
                  value={selectedTime}
                  onChange={(e) => setSelectedTime(parseInt(e.target.value))}
                  className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                >
                  {TimeOfDay.map((time, index) => (
                    <option key={index} value={index}>
                      {time.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Encounter History */}
          <div className="bg-secondary-700/50 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-3">Historia Spotkań</h4>
            
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {encounterHistory.slice(0, 10).map((encounter) => (
                <div
                  key={encounter.id}
                  className="p-2 bg-secondary-600/50 rounded text-sm cursor-pointer hover:bg-secondary-600"
                  onClick={() => setGeneratedEncounter(encounter)}
                >
                  <div className="font-medium text-white">{encounter.encounter.type}</div>
                  <div className="text-secondary-300 text-xs">
                    {encounter.location} • {new Date(encounter.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Generated Encounter Display */}
        <div className="lg:col-span-3">
          <AnimatePresence mode="wait">
            {generatedEncounter ? (
              <motion.div
                key={generatedEncounter.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-secondary-700/50 rounded-lg p-6"
              >
                {/* Encounter Header */}
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-2xl font-medieval text-white mb-1">
                      {generatedEncounter.encounter.type}
                    </h3>
                    <div className="flex items-center gap-4 text-sm text-secondary-300">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-4 h-4" />
                        {generatedEncounter.location}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {generatedEncounter.time.name}
                      </span>
                      <span>🌤️ {generatedEncounter.weather.name}</span>
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <button
                      onClick={copyEncounter}
                      className="p-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                      title="Kopiuj do schowka"
                    >
                      <Copy className="w-4 h-4 text-white" />
                    </button>
                  </div>
                </div>

                {/* Encounter Details */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div>
                    <h4 className="font-semibold text-white mb-2">Opis Spotkania</h4>
                    <p className="text-secondary-300 mb-4">
                      {generatedEncounter.encounter.description}
                    </p>
                    
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <span className="text-secondary-400">Zagrożenie:</span>
                        <span className={`px-2 py-1 rounded text-xs border ${getThreatColor(generatedEncounter.encounter.threat)}`}>
                          {generatedEncounter.encounter.threat}
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <span className="text-secondary-400">Dystans:</span>
                        <span className="text-white">{generatedEncounter.distance}</span>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <span className="text-secondary-400">Zaskoczenie:</span>
                        <span className={generatedEncounter.surprise ? 'text-red-400' : 'text-green-400'}>
                          {generatedEncounter.surprise ? 'Tak' : 'Nie'}
                        </span>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <span className="text-secondary-400">Nastawienie:</span>
                        <span className={getMoodColor(generatedEncounter.mood)}>
                          {generatedEncounter.mood}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Taktyka</h4>
                    <p className="text-secondary-300 mb-4">
                      {generatedEncounter.encounter.tactics}
                    </p>
                    
                    <h4 className="font-semibold text-white mb-2">Potencjalne Łupy</h4>
                    <p className="text-secondary-300">
                      {generatedEncounter.encounter.loot}
                    </p>
                  </div>
                </div>

                {/* Environmental Modifiers */}
                <div className="bg-secondary-600/30 rounded-lg p-4 mb-6">
                  <h4 className="font-semibold text-white mb-3">Modyfikatory Środowiskowe</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="text-secondary-400">Pogoda ({generatedEncounter.weather.name}):</span>
                      <p className="text-secondary-300">{generatedEncounter.weather.modifier}</p>
                      <p className="text-xs text-secondary-400">{generatedEncounter.weather.effect}</p>
                    </div>
                    <div>
                      <span className="text-secondary-400">Pora dnia ({generatedEncounter.time.name}):</span>
                      <p className="text-secondary-300">{generatedEncounter.time.modifier}</p>
                      <p className="text-xs text-secondary-400">{generatedEncounter.time.effect}</p>
                    </div>
                  </div>
                </div>

                {/* GM Notes */}
                <div>
                  <h4 className="font-semibold text-white mb-2">Notatki MG</h4>
                  <textarea
                    value={generatedEncounter.notes}
                    onChange={(e) => saveEncounterNotes(e.target.value)}
                    placeholder="Dodaj swoje notatki o tym spotkaniu..."
                    className="w-full h-24 bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white placeholder-secondary-400 resize-none"
                  />
                </div>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="h-full flex items-center justify-center"
              >
                <div className="text-center">
                  <Sword className="w-24 h-24 text-secondary-400 mx-auto mb-4 opacity-50" />
                  <h3 className="text-xl font-medieval text-white mb-2">
                    Brak Wygenerowanego Spotkania
                  </h3>
                  <p className="text-secondary-400 mb-4">
                    Kliknij "Generuj Spotkanie" aby stworzyć nowe wyzwanie
                  </p>
                  <button
                    onClick={generateEncounter}
                    className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors flex items-center gap-2 mx-auto"
                  >
                    <Sword className="w-5 h-5" />
                    Generuj Pierwsze Spotkanie
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}
