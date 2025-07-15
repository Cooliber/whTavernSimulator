import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Users, RefreshCw, Save, Copy, Download, Dice6, Crown, Sword, Shield } from 'lucide-react'
import toast from 'react-hot-toast'

// WFRP Species with authentic data
const WFRPSpecies = {
  human: {
    name: 'Człowiek',
    icon: '👤',
    stats: { WS: 20, BS: 20, S: 20, T: 20, I: 20, Ag: 20, Dex: 20, Int: 20, WP: 20, Fel: 20 },
    skills: ['Język (Reikspiel)', 'Plotkowanie', 'Targowanie'],
    talents: ['Dodatkowy Punkt Losu', 'Spryt', 'Surowość'],
    trappings: ['Ubranie', 'Nóż', '2d10 monet miedzianych'],
    careers: ['Żołnierz', 'Kupiec', 'Rzemieślnik', 'Uczony', 'Złodziej', 'Rozrywkarz']
  },
  dwarf: {
    name: 'Krasnolud',
    icon: '🧔',
    stats: { WS: 30, BS: 20, S: 20, T: 30, I: 20, Ag: 10, Dex: 30, Int: 20, WP: 40, Fel: 10 },
    skills: ['Język (Khazalid)', 'Język (Reikspiel)', 'Wytrzymałość', 'Rzemiosło'],
    talents: ['Widzenie w Ciemności', 'Odporność na Magię', 'Rozwiązywanie'],
    trappings: ['Skórzana Zbroja', 'Topór lub Młot', 'Tarcza', '2d10 koron złotych'],
    careers: ['Kowal', 'Górnik', 'Wojownik', 'Inżynier', 'Strażnik', 'Rzemieślnik']
  },
  halfling: {
    name: 'Niziołek',
    icon: '🍃',
    stats: { WS: 10, BS: 30, S: 10, T: 20, I: 20, Ag: 30, Dex: 30, Int: 20, WP: 30, Fel: 30 },
    skills: ['Język (Halfling)', 'Język (Reikspiel)', 'Unik', 'Intuicja', 'Gotowanie'],
    talents: ['Odporność na Chaos', 'Szczęście', 'Mały'],
    trappings: ['Skórzana Kurtka', 'Proca', 'Worek Kamieni', 'Jedzenie na tydzień'],
    careers: ['Kucharz', 'Złodziej', 'Łowca', 'Kupiec', 'Rozrywkarz', 'Strażnik']
  },
  elf: {
    name: 'Elf',
    icon: '🧝',
    stats: { WS: 30, BS: 30, S: 20, T: 20, I: 40, Ag: 30, Dex: 30, Int: 30, WP: 30, Fel: 20 },
    skills: ['Język (Eltharin)', 'Język (Reikspiel)', 'Percepcja', 'Sztuka'],
    talents: ['Widzenie w Ciemności', 'Druga Wzrok', 'Elegancja'],
    trappings: ['Elficka Zbroja Skórzana', 'Elficki Łuk', 'Kołczan ze Strzałami', 'Elficki Płaszcz'],
    careers: ['Łowca', 'Uczony', 'Mag', 'Rozrywkarz', 'Strażnik', 'Rzemieślnik']
  }
}

// WFRP Careers with progression
const WFRPCareers = {
  soldier: {
    name: 'Żołnierz',
    class: 'Wojownik',
    tier: 'Brązowy',
    skills: ['Atletyka', 'Wspinaczka', 'Unik', 'Zastraszanie', 'Dowodzenie', 'Broń Biała'],
    talents: ['Broń Specjalistyczna', 'Szarża', 'Odporność Psychiczna'],
    trappings: ['Zbroja Skórzana', 'Miecz', 'Tarcza', 'Mundur'],
    income: '2d10 szylingów srebrnych'
  },
  merchant: {
    name: 'Kupiec',
    class: 'Mieszczanin',
    tier: 'Srebrny',
    skills: ['Targowanie', 'Ocena', 'Plotkowanie', 'Język', 'Sekretne Znaki', 'Jeździectwo'],
    talents: ['Surowość', 'Spryt', 'Czytanie/Pisanie'],
    trappings: ['Dobra Odzież', 'Koń', 'Wóz', 'Towary'],
    income: '1d10 koron złotych'
  },
  scholar: {
    name: 'Uczony',
    class: 'Akademik',
    tier: 'Srebrny',
    skills: ['Język (Klasyczny)', 'Badanie', 'Czytanie/Pisanie', 'Wiedza'],
    talents: ['Czytanie/Pisanie', 'Spryt', 'Surowość'],
    trappings: ['Księgi', 'Pergaminy', 'Atrament', 'Pióro'],
    income: '2d10 szylingów srebrnych'
  },
  thief: {
    name: 'Złodziej',
    class: 'Łotrzyk',
    tier: 'Miedziany',
    skills: ['Wspinaczka', 'Skradanie', 'Otwieranie Zamków', 'Zręczność', 'Percepcja', 'Sekretne Znaki'],
    talents: ['Alley Cat', 'Fleet Footed', 'Luck'],
    trappings: ['Skórzana Kurtka', 'Narzędzia Złodziejskie', 'Worek', 'Lina'],
    income: '1d10 szylingów srebrnych'
  }
}

// Random name generators by species
const NameGenerators = {
  human: {
    male: ['Heinrich', 'Wilhelm', 'Friedrich', 'Johann', 'Klaus', 'Otto', 'Rudolf', 'Gustav'],
    female: ['Gretchen', 'Brunhilde', 'Ingrid', 'Helga', 'Ursula', 'Astrid', 'Sigrid', 'Mathilde'],
    surnames: ['Schmidt', 'Müller', 'Weber', 'Wagner', 'Becker', 'Schulz', 'Hoffmann', 'Schäfer']
  },
  dwarf: {
    male: ['Thorek', 'Grimm', 'Borin', 'Dain', 'Balin', 'Gloin', 'Oin', 'Nain'],
    female: ['Vera', 'Nala', 'Disa', 'Hilda', 'Magna', 'Runa', 'Thora', 'Freya'],
    surnames: ['Ironbeard', 'Stonebreaker', 'Goldseeker', 'Axebreaker', 'Oathkeeper', 'Grudgebearer']
  },
  halfling: {
    male: ['Bilbo', 'Frodo', 'Samwise', 'Peregrin', 'Meriadoc', 'Bandobras', 'Bungo', 'Drogo'],
    female: ['Belladonna', 'Primula', 'Esmeralda', 'Pearl', 'Poppy', 'Daisy', 'Rose', 'Lily'],
    surnames: ['Baggins', 'Took', 'Brandybuck', 'Gamgee', 'Proudfoot', 'Bracegirdle', 'Greenhill']
  },
  elf: {
    male: ['Eltharion', 'Tyrion', 'Teclis', 'Alith', 'Caelir', 'Eldain', 'Korhil', 'Belannaer'],
    female: ['Alarielle', 'Morathi', 'Ariel', 'Naestra', 'Arahan', 'Tullaris', 'Hellebron', 'Crone'],
    surnames: ['Moonwhisper', 'Starweaver', 'Dawnbringer', 'Nightsong', 'Silverleaf', 'Goldmane']
  }
}

// Personality traits
const PersonalityTraits = [
  'Honorowy', 'Chciwy', 'Odważny', 'Tchórzliwy', 'Mądry', 'Głupi', 'Życzliwy', 'Wrogi',
  'Cierpliwy', 'Niecierpliwy', 'Lojalny', 'Zdradziecki', 'Spokojny', 'Nerwowy', 'Wesoły', 'Ponury',
  'Dumny', 'Pokorny', 'Ciekawski', 'Obojętny', 'Szczery', 'Kłamliwy', 'Pracowity', 'Leniwy'
]

// Physical descriptions
const PhysicalTraits = [
  'Wysoki', 'Niski', 'Gruby', 'Chudy', 'Muskularny', 'Słaby', 'Przystojny', 'Brzydki',
  'Blada cera', 'Opalona skóra', 'Blizny na twarzy', 'Tatuaże', 'Brakuje zęba', 'Kuleje',
  'Siwe włosy', 'Łysy', 'Długa broda', 'Wąsy', 'Przenikliwe oczy', 'Ślepe oko'
]

export const NPCGenerator = ({ gmMode, sessionData, onSessionDataUpdate }) => {
  const [generatedNPC, setGeneratedNPC] = useState(null)
  const [selectedSpecies, setSelectedSpecies] = useState('human')
  const [selectedCareer, setSelectedCareer] = useState('random')
  const [isGenerating, setIsGenerating] = useState(false)
  const [savedNPCs, setSavedNPCs] = useState([])

  // Load saved NPCs
  useEffect(() => {
    const saved = localStorage.getItem('wfrp_saved_npcs')
    if (saved) {
      try {
        setSavedNPCs(JSON.parse(saved))
      } catch (error) {
        console.error('Error loading saved NPCs:', error)
      }
    }
  }, [])

  // Generate random NPC
  const generateNPC = () => {
    setIsGenerating(true)
    
    setTimeout(() => {
      const species = WFRPSpecies[selectedSpecies]
      const careers = Object.values(WFRPCareers)
      const career = selectedCareer === 'random' 
        ? careers[Math.floor(Math.random() * careers.length)]
        : WFRPCareers[selectedCareer]

      // Generate name
      const names = NameGenerators[selectedSpecies]
      const gender = Math.random() > 0.5 ? 'male' : 'female'
      const firstName = names[gender][Math.floor(Math.random() * names[gender].length)]
      const surname = names.surnames[Math.floor(Math.random() * names.surnames.length)]

      // Generate stats
      const stats = {}
      Object.entries(species.stats).forEach(([stat, base]) => {
        stats[stat] = base + Math.floor(Math.random() * 21) - 10 // ±10 variation
      })

      // Generate characteristics
      const personality = PersonalityTraits[Math.floor(Math.random() * PersonalityTraits.length)]
      const physical = PhysicalTraits[Math.floor(Math.random() * PhysicalTraits.length)]

      const npc = {
        id: Date.now(),
        name: `${firstName} ${surname}`,
        species: species.name,
        career: career.name,
        class: career.class,
        tier: career.tier,
        gender,
        stats,
        skills: [...species.skills, ...career.skills],
        talents: [...species.talents, ...career.talents],
        trappings: [...species.trappings, ...career.trappings],
        personality,
        physical,
        income: career.income,
        background: generateBackground(species, career),
        hooks: generateHooks(),
        timestamp: Date.now()
      }

      setGeneratedNPC(npc)
      setIsGenerating(false)
      
      toast.success(`Wygenerowano ${npc.name}!`)
    }, 1000)
  }

  // Generate background story
  const generateBackground = (species, career) => {
    const backgrounds = {
      human: [
        'Pochodzący z małej wioski w Reiklandzie',
        'Wychowany w Altdorfie wśród miejskiego zgiełku',
        'Syn kupca z Marienburgiem',
        'Były żołnierz armii imperialnej'
      ],
      dwarf: [
        'Pochodzący z Karak Kadrin, twierdzy Zabójców Trolli',
        'Wygnany z klanu za złamanie tradycji',
        'Młody krasnolud szukający swojego miejsca w świecie',
        'Potomek słynnej linii kowali'
      ],
      halfling: [
        'Pochodzący z Moot, krainy niziołków',
        'Podróżnik z dalekiej wioski',
        'Kucharz szukający nowych przepisów',
        'Uciekinier przed rodzinnymi obowiązkami'
      ],
      elf: [
        'Wysłannik z Ulthuan w sprawach dyplomatycznych',
        'Wygnany elf szukający odkupienia',
        'Strażnik starożytnych sekretów',
        'Podróżnik badający ludzkie zwyczaje'
      ]
    }

    const speciesBackgrounds = backgrounds[selectedSpecies] || backgrounds.human
    return speciesBackgrounds[Math.floor(Math.random() * speciesBackgrounds.length)]
  }

  // Generate adventure hooks
  const generateHooks = () => {
    const hooks = [
      'Posiada informacje o zaginionym skarbie',
      'Jest świadkiem tajemniczego przestępstwa',
      'Szuka kogoś do wykonania niebezpiecznego zadania',
      'Ma długi u wpływowej osoby',
      'Ukrywa mroczną tajemnicę z przeszłości',
      'Jest poszukiwany przez prawo',
      'Posiada mapę do starożytnych ruin',
      'Zna lokalizację kultystów Chaosu'
    ]
    
    return hooks[Math.floor(Math.random() * hooks.length)]
  }

  // Save NPC
  const saveNPC = () => {
    if (!generatedNPC) return

    const newSavedNPCs = [...savedNPCs, generatedNPC]
    setSavedNPCs(newSavedNPCs)
    localStorage.setItem('wfrp_saved_npcs', JSON.stringify(newSavedNPCs))
    
    toast.success('NPC zapisany!')
  }

  // Copy NPC to clipboard
  const copyNPC = () => {
    if (!generatedNPC) return

    const npcText = `
${generatedNPC.name}
${generatedNPC.species} ${generatedNPC.career}

STATYSTYKI:
${Object.entries(generatedNPC.stats).map(([stat, value]) => `${stat}: ${value}`).join(', ')}

UMIEJĘTNOŚCI: ${generatedNPC.skills.join(', ')}
TALENTY: ${generatedNPC.talents.join(', ')}
WYPOSAŻENIE: ${generatedNPC.trappings.join(', ')}

OSOBOWOŚĆ: ${generatedNPC.personality}
WYGLĄD: ${generatedNPC.physical}
POCHODZENIE: ${generatedNPC.background}
ZACZYN PRZYGODY: ${generatedNPC.hooks}
    `.trim()

    navigator.clipboard.writeText(npcText)
    toast.success('NPC skopiowany do schowka!')
  }

  // Export NPC
  const exportNPC = () => {
    if (!generatedNPC) return

    const dataStr = JSON.stringify(generatedNPC, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    
    const link = document.createElement('a')
    link.href = url
    link.download = `${generatedNPC.name.replace(/\s+/g, '_')}.json`
    link.click()
    
    URL.revokeObjectURL(url)
    toast.success('NPC wyeksportowany!')
  }

  return (
    <div className="h-full flex flex-col p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-medieval text-white mb-2">Generator NPC</h3>
          <p className="text-secondary-300">
            Generuj postacie niezależne z pełnymi statystykami WFRP
          </p>
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={generateNPC}
            disabled={isGenerating}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-secondary-600 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            {isGenerating ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <Dice6 className="w-4 h-4" />
            )}
            {isGenerating ? 'Generowanie...' : 'Generuj NPC'}
          </button>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration Panel */}
        <div className="space-y-6">
          <div className="bg-secondary-700/50 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-3">Konfiguracja</h4>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-secondary-300 mb-2">
                  Rasa
                </label>
                <select
                  value={selectedSpecies}
                  onChange={(e) => setSelectedSpecies(e.target.value)}
                  className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                >
                  {Object.entries(WFRPSpecies).map(([key, species]) => (
                    <option key={key} value={key}>
                      {species.icon} {species.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-secondary-300 mb-2">
                  Kariera
                </label>
                <select
                  value={selectedCareer}
                  onChange={(e) => setSelectedCareer(e.target.value)}
                  className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                >
                  <option value="random">🎲 Losowa</option>
                  {Object.entries(WFRPCareers).map(([key, career]) => (
                    <option key={key} value={key}>
                      {career.name} ({career.tier})
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Saved NPCs */}
          <div className="bg-secondary-700/50 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-3">Zapisane NPC ({savedNPCs.length})</h4>
            
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {savedNPCs.map((npc) => (
                <div
                  key={npc.id}
                  className="p-2 bg-secondary-600/50 rounded text-sm"
                >
                  <div className="font-medium text-white">{npc.name}</div>
                  <div className="text-secondary-300">
                    {npc.species} {npc.career}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Generated NPC Display */}
        <div className="lg:col-span-2">
          <AnimatePresence mode="wait">
            {generatedNPC ? (
              <motion.div
                key={generatedNPC.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-secondary-700/50 rounded-lg p-6"
              >
                {/* NPC Header */}
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-2xl font-medieval text-white mb-1">
                      {generatedNPC.name}
                    </h3>
                    <p className="text-secondary-300">
                      {generatedNPC.species} • {generatedNPC.career} ({generatedNPC.tier})
                    </p>
                  </div>
                  
                  <div className="flex gap-2">
                    <button
                      onClick={saveNPC}
                      className="p-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
                      title="Zapisz NPC"
                    >
                      <Save className="w-4 h-4 text-white" />
                    </button>
                    <button
                      onClick={copyNPC}
                      className="p-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                      title="Kopiuj do schowka"
                    >
                      <Copy className="w-4 h-4 text-white" />
                    </button>
                    <button
                      onClick={exportNPC}
                      className="p-2 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
                      title="Eksportuj"
                    >
                      <Download className="w-4 h-4 text-white" />
                    </button>
                  </div>
                </div>

                {/* NPC Stats */}
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
                  {Object.entries(generatedNPC.stats).map(([stat, value]) => (
                    <div key={stat} className="text-center">
                      <div className="text-xs text-secondary-400 uppercase tracking-wide">
                        {stat}
                      </div>
                      <div className="text-lg font-bold text-white">
                        {value}
                      </div>
                    </div>
                  ))}
                </div>

                {/* NPC Details */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-white mb-2">Umiejętności</h4>
                    <div className="flex flex-wrap gap-1">
                      {generatedNPC.skills.map((skill, index) => (
                        <span
                          key={index}
                          className="text-xs px-2 py-1 bg-blue-400/20 text-blue-100 rounded border border-blue-400/50"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Talenty</h4>
                    <div className="flex flex-wrap gap-1">
                      {generatedNPC.talents.map((talent, index) => (
                        <span
                          key={index}
                          className="text-xs px-2 py-1 bg-amber-400/20 text-amber-100 rounded border border-amber-400/50"
                        >
                          {talent}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Wyposażenie</h4>
                    <div className="text-sm text-secondary-300">
                      {generatedNPC.trappings.join(', ')}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Dochód</h4>
                    <div className="text-sm text-secondary-300">
                      {generatedNPC.income}
                    </div>
                  </div>
                </div>

                {/* Character Details */}
                <div className="mt-6 space-y-4">
                  <div>
                    <h4 className="font-semibold text-white mb-2">Osobowość</h4>
                    <p className="text-secondary-300">{generatedNPC.personality}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Wygląd</h4>
                    <p className="text-secondary-300">{generatedNPC.physical}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Pochodzenie</h4>
                    <p className="text-secondary-300">{generatedNPC.background}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Zaczyn Przygody</h4>
                    <p className="text-secondary-300">{generatedNPC.hooks}</p>
                  </div>
                </div>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="h-full flex items-center justify-center"
              >
                <div className="text-center">
                  <Users className="w-24 h-24 text-secondary-400 mx-auto mb-4 opacity-50" />
                  <h3 className="text-xl font-medieval text-white mb-2">
                    Brak Wygenerowanego NPC
                  </h3>
                  <p className="text-secondary-400 mb-4">
                    Kliknij "Generuj NPC" aby stworzyć nową postać
                  </p>
                  <button
                    onClick={generateNPC}
                    className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors flex items-center gap-2 mx-auto"
                  >
                    <Dice6 className="w-5 h-5" />
                    Generuj Pierwszego NPC
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
