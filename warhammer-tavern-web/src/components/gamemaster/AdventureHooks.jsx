import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Scroll, RefreshCw, Save, Copy, Star, Clock, Users, Crown } from 'lucide-react'
import toast from 'react-hot-toast'

// WFRP Adventure Hook Categories
const AdventureCategories = {
  investigation: {
    name: 'Śledztwo',
    icon: '🔍',
    color: 'text-blue-400',
    hooks: [
      {
        title: 'Zaginięcie w Altdorfie',
        description: 'Syn wpływowego kupca zaginął w dzielnicach nędzy. Rodzina oferuje sowite wynagrodzenie za jego odnalezienie.',
        patron: 'Kupiec Wilhelm Steinberg',
        reward: '50 koron złotych',
        complications: ['Syn przyłączył się do kultu Chaosu', 'Jest więziony przez rywalizujący dom handlowy', 'Ukrywa się dobrowolnie z powodu długów'],
        locations: ['Altdorf - dzielnice nędzy', 'Doki', 'Podziemne tunele'],
        duration: '2-4 sesje'
      },
      {
        title: 'Morderca z Mgły',
        description: 'Seria tajemniczych morderstw w małym miasteczku. Ofiary są znajdowane bez krwi, z dziwnymi symbolami.',
        patron: 'Burmistrz miasteczka',
        reward: '30 koron złotych + mieszkanie',
        complications: ['Morderca to wampir', 'Kultysci Chaosu przeprowadzają rytuały', 'Nekromanta eksperymentuje na mieszkańcach'],
        locations: ['Miasteczko Graustadt', 'Cmentarz', 'Stary młyn'],
        duration: '3-5 sesji'
      },
      {
        title: 'Skradziony Artefakt',
        description: 'Z świątyni Sigmara skradziono święty relikwiar. Kapłani podejrzewają wewnętrzną zdradę.',
        patron: 'Arcykapłan Sigmara',
        reward: 'Błogosławieństwo + 40 koron',
        complications: ['Złodziej to kapłan świątyni', 'Artefakt został sprzedany kultystom', 'Relikwiar ma mroczną przeszłość'],
        locations: ['Świątynia Sigmara', 'Czarny rynek', 'Ruiny starego klasztoru'],
        duration: '2-3 sesje'
      }
    ]
  },
  
  combat: {
    name: 'Walka',
    icon: '⚔️',
    color: 'text-red-400',
    hooks: [
      {
        title: 'Obrona Wioski',
        description: 'Wioska jest terroryzowana przez bandę orków. Mieszkańcy desperacko szukają obrońców.',
        patron: 'Sołtys wioski',
        reward: '20 koron + ziemia',
        complications: ['Orki mają ludzkiego przywódcę', 'W wiosce ukrywa się zdrajca', 'Orki szukają starożytnego artefaktu'],
        locations: ['Wioska Kleinsdorf', 'Okoliczne lasy', 'Orkowy obóz'],
        duration: '1-2 sesje'
      },
      {
        title: 'Turniej Rycerski',
        description: 'Wielki turniej w Bretonnii. Zwycięzca otrzyma tytuł i ziemie, ale coś złowrogiego się dzieje.',
        patron: 'Lord Bretonnii',
        reward: 'Tytuł szlachecki + 100 koron',
        complications: ['Jeden z rycerzy to kultysca Chaosu', 'Turniej to pułapka na bohaterów', 'Magiczne oszustwa'],
        locations: ['Zamek w Bretonnii', 'Pole turniejowe', 'Tajne komnaty'],
        duration: '3-4 sesje'
      },
      {
        title: 'Ostatni Bastion',
        description: 'Twierdza graniczna jest oblężona przez hordy Chaosu. Obrońcy potrzebują wsparcia.',
        patron: 'Kapitan Twierdzy',
        reward: 'Honory wojskowe + 60 koron',
        complications: ['Zdrajca w twierdzy', 'Demon dowodzi atakiem', 'Zapasy się kończą'],
        locations: ['Twierdza Sigmarsheim', 'Mury obronne', 'Podziemne tunele'],
        duration: '2-3 sesje'
      }
    ]
  },
  
  exploration: {
    name: 'Eksploracja',
    icon: '🗺️',
    color: 'text-green-400',
    hooks: [
      {
        title: 'Zaginiona Ekspedycja',
        description: 'Ekspedycja badawcza zaginęła w Drakwaldzie. Uniwersytet w Altdorfie szuka ratowników.',
        patron: 'Profesor Uniwersytetu',
        reward: '40 koron + artefakty',
        complications: ['Ekspedycja odkryła ruiny Chaosu', 'Członkowie zostali opętani', 'Las jest przeklęty'],
        locations: ['Drakwald', 'Ruiny elfickie', 'Obóz ekspedycji'],
        duration: '4-6 sesji'
      },
      {
        title: 'Mapa Skarbów',
        description: 'Stara mapa prowadzi do skarbu ukrytego w Szarych Górach. Ale inni też ją szukają.',
        patron: 'Umierający poszukiwacz przygód',
        reward: 'Skarb (200+ koron)',
        complications: ['Mapa jest fałszywa', 'Skarb strzeże demon', 'Rywalizujący poszukiwacze'],
        locations: ['Szare Góry', 'Stara kopalnia', 'Krasnoludzkie ruiny'],
        duration: '3-5 sesji'
      },
      {
        title: 'Wyspa Tajemnic',
        description: 'Nowa wyspa pojawiła się na morzu. Marynarz oferuje transport w zamian za ochronę.',
        patron: 'Kapitan statku',
        reward: 'Część znalezionych skarbów',
        complications: ['Wyspa to iluzja Chaosu', 'Zamieszkują ją mutanci', 'Wyspa znika o świcie'],
        locations: ['Tajemnicza wyspa', 'Statek', 'Podwodne jaskinie'],
        duration: '2-4 sesje'
      }
    ]
  },
  
  intrigue: {
    name: 'Intryga',
    icon: '🎭',
    color: 'text-purple-400',
    hooks: [
      {
        title: 'Spisek Dworski',
        description: 'Na dworze Elektora planowany jest zamach. Lojalny sługa potrzebuje dyskretnych agentów.',
        patron: 'Dworzanin (tajny)',
        reward: '80 koron + protekcja',
        complications: ['Spiskowcy to kultysci', 'Elektor jest już opętany', 'Bohaterowie są podstawieni'],
        locations: ['Pałac Elektora', 'Dwór', 'Tajne przejścia'],
        duration: '4-6 sesji'
      },
      {
        title: 'Wojna Gildii',
        description: 'Dwie potężne gildie walczą o kontrolę nad handlem. Obie strony szukają najemników.',
        patron: 'Przedstawiciele gildii',
        reward: '50 koron + przywileje handlowe',
        complications: ['Jedna gildia służy Chaosowi', 'To pułapka na bohaterów', 'Trzecia strona manipuluje konfliktem'],
        locations: ['Domy gildii', 'Magazyny', 'Czarny rynek'],
        duration: '3-5 sesji'
      },
      {
        title: 'Szpieg w Szeregach',
        description: 'W armii imperialnej działa szpieg Chaosu. Wywiad potrzebuje agentów do jego wykrycia.',
        patron: 'Oficer wywiadu',
        reward: '60 koron + stopnie wojskowe',
        complications: ['Szpieg to wysokiej rangi oficer', 'Bohaterowie są podejrzani', 'Cała jednostka jest skorumpowana'],
        locations: ['Koszary', 'Sztab generalny', 'Tajne spotkania'],
        duration: '3-4 sesje'
      }
    ]
  },
  
  horror: {
    name: 'Horror',
    icon: '💀',
    color: 'text-gray-400',
    hooks: [
      {
        title: 'Dom Przeklęty',
        description: 'Stary dwór jest nawiedzany. Nowi właściciele oferują fortunę za oczyszczenie go.',
        patron: 'Nowi właściciele',
        reward: '70 koron + część majątku',
        complications: ['Dom żyje własnym życiem', 'Poprzedni właściciele byli kultystami', 'Duchy chcą zemsty'],
        locations: ['Nawiedzony dwór', 'Podziemia', 'Rodzinny cmentarz'],
        duration: '2-3 sesje'
      },
      {
        title: 'Plaga Nieumarłych',
        description: 'W miasteczku zmarli powstają z grobów. Mieszkańcy w panice szukają pomocy.',
        patron: 'Burmistrz i mieszkańcy',
        reward: '45 koron + wdzięczność',
        complications: ['Nekromanta ukrywa się w mieście', 'Plaga się rozprzestrzenia', 'Niektórzy mieszkańcy są już nieumarli'],
        locations: ['Miasteczko Morrslieb', 'Cmentarz', 'Stara krypta'],
        duration: '2-4 sesje'
      },
      {
        title: 'Kult Mrocznego Boga',
        description: 'Tajny kult planuje wielki rytuał. Tylko bohaterowie mogą ich powstrzymać.',
        patron: 'Kapłan Sigmara (tajny)',
        reward: 'Błogosławieństwa + 55 koron',
        complications: ['Rytuał już się rozpoczął', 'Kultysci infiltrowali władze', 'Demon już został przywołany'],
        locations: ['Podziemne świątynie', 'Opuszczone ruiny', 'Miejsce rytuału'],
        duration: '4-7 sesji'
      }
    ]
  }
}

// Adventure complexity levels
const ComplexityLevels = [
  { name: 'Prosta', sessions: '1-2', description: 'Szybka przygoda na jedną sesję' },
  { name: 'Średnia', sessions: '3-4', description: 'Standardowa przygoda z kilkoma wątkami' },
  { name: 'Złożona', sessions: '5-7', description: 'Długa przygoda z wieloma lokacjami' },
  { name: 'Kampania', sessions: '8+', description: 'Wielka przygoda na całą kampanię' }
]

export const AdventureHooks = ({ gmMode, sessionData, onSessionDataUpdate }) => {
  const [generatedHook, setGeneratedHook] = useState(null)
  const [selectedCategory, setSelectedCategory] = useState('investigation')
  const [selectedComplexity, setSelectedComplexity] = useState(1)
  const [isGenerating, setIsGenerating] = useState(false)
  const [savedHooks, setSavedHooks] = useState([])
  const [customNotes, setCustomNotes] = useState('')

  // Load saved hooks
  useEffect(() => {
    const saved = localStorage.getItem('wfrp_saved_hooks')
    if (saved) {
      try {
        setSavedHooks(JSON.parse(saved))
      } catch (error) {
        console.error('Error loading saved hooks:', error)
      }
    }
  }, [])

  // Generate adventure hook
  const generateHook = () => {
    setIsGenerating(true)
    
    setTimeout(() => {
      const category = AdventureCategories[selectedCategory]
      const hooks = category.hooks
      const baseHook = hooks[Math.floor(Math.random() * hooks.length)]
      const complexity = ComplexityLevels[selectedComplexity]
      
      // Add random complications based on complexity
      const numComplications = selectedComplexity + 1
      const selectedComplications = baseHook.complications
        .sort(() => 0.5 - Math.random())
        .slice(0, numComplications)

      // Generate additional details
      const urgency = ['Natychmiastowa', 'Pilna', 'Normalna', 'Można odłożyć'][Math.floor(Math.random() * 4)]
      const secrecy = ['Tajne', 'Dyskretne', 'Publiczne'][Math.floor(Math.random() * 3)]
      
      const hook = {
        id: Date.now(),
        category: category.name,
        complexity: complexity.name,
        title: baseHook.title,
        description: baseHook.description,
        patron: baseHook.patron,
        reward: baseHook.reward,
        complications: selectedComplications,
        locations: baseHook.locations,
        duration: baseHook.duration,
        urgency: urgency,
        secrecy: secrecy,
        notes: '',
        timestamp: Date.now()
      }

      setGeneratedHook(hook)
      setIsGenerating(false)
      toast.success('Wygenerowano zaczyn przygody!')
    }, 1000)
  }

  // Save hook
  const saveHook = () => {
    if (!generatedHook) return

    const hookToSave = { ...generatedHook, notes: customNotes }
    const newSavedHooks = [...savedHooks, hookToSave]
    setSavedHooks(newSavedHooks)
    localStorage.setItem('wfrp_saved_hooks', JSON.stringify(newSavedHooks))
    
    toast.success('Zaczyn przygody zapisany!')
  }

  // Copy hook to clipboard
  const copyHook = () => {
    if (!generatedHook) return

    const hookText = `
ZACZYN PRZYGODY: ${generatedHook.title}
Kategoria: ${generatedHook.category}
Złożoność: ${generatedHook.complexity}

OPIS:
${generatedHook.description}

ZLECENIODAWCA: ${generatedHook.patron}
NAGRODA: ${generatedHook.reward}
PILNOŚĆ: ${generatedHook.urgency}
TAJNOŚĆ: ${generatedHook.secrecy}

LOKACJE:
${generatedHook.locations.map(loc => `• ${loc}`).join('\n')}

KOMPLIKACJE:
${generatedHook.complications.map(comp => `• ${comp}`).join('\n')}

SZACOWANY CZAS: ${generatedHook.duration}

NOTATKI MG:
${customNotes}
    `.trim()

    navigator.clipboard.writeText(hookText)
    toast.success('Zaczyn przygody skopiowany!')
  }

  const getCategoryColor = (category) => {
    const colors = {
      'Śledztwo': 'text-blue-400 bg-blue-400/20 border-blue-400/50',
      'Walka': 'text-red-400 bg-red-400/20 border-red-400/50',
      'Eksploracja': 'text-green-400 bg-green-400/20 border-green-400/50',
      'Intryga': 'text-purple-400 bg-purple-400/20 border-purple-400/50',
      'Horror': 'text-gray-400 bg-gray-400/20 border-gray-400/50'
    }
    return colors[category] || 'text-gray-400 bg-gray-400/20 border-gray-400/50'
  }

  const getUrgencyColor = (urgency) => {
    switch (urgency) {
      case 'Natychmiastowa': return 'text-red-400'
      case 'Pilna': return 'text-orange-400'
      case 'Normalna': return 'text-yellow-400'
      case 'Można odłożyć': return 'text-green-400'
      default: return 'text-gray-400'
    }
  }

  return (
    <div className="h-full flex flex-col p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-medieval text-white mb-2">Zaczyny Przygód</h3>
          <p className="text-secondary-300">
            Generuj pomysły na przygody dla kampanii WFRP
          </p>
        </div>
        
        <button
          onClick={generateHook}
          disabled={isGenerating}
          className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-secondary-600 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          {isGenerating ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <Scroll className="w-4 h-4" />
          )}
          {isGenerating ? 'Generowanie...' : 'Generuj Zaczyn'}
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
                  Kategoria
                </label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                >
                  {Object.entries(AdventureCategories).map(([key, category]) => (
                    <option key={key} value={key}>
                      {category.icon} {category.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-secondary-300 mb-2">
                  Złożoność
                </label>
                <select
                  value={selectedComplexity}
                  onChange={(e) => setSelectedComplexity(parseInt(e.target.value))}
                  className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                >
                  {ComplexityLevels.map((level, index) => (
                    <option key={index} value={index}>
                      {level.name} ({level.sessions})
                    </option>
                  ))}
                </select>
                <p className="text-xs text-secondary-400 mt-1">
                  {ComplexityLevels[selectedComplexity].description}
                </p>
              </div>
            </div>
          </div>

          {/* Saved Hooks */}
          <div className="bg-secondary-700/50 rounded-lg p-4">
            <h4 className="font-semibold text-white mb-3">Zapisane Zaczyny ({savedHooks.length})</h4>
            
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {savedHooks.map((hook) => (
                <div
                  key={hook.id}
                  className="p-2 bg-secondary-600/50 rounded text-sm cursor-pointer hover:bg-secondary-600"
                  onClick={() => setGeneratedHook(hook)}
                >
                  <div className="font-medium text-white">{hook.title}</div>
                  <div className="text-secondary-300 text-xs">
                    {hook.category} • {hook.complexity}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Generated Hook Display */}
        <div className="lg:col-span-3">
          <AnimatePresence mode="wait">
            {generatedHook ? (
              <motion.div
                key={generatedHook.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="bg-secondary-700/50 rounded-lg p-6"
              >
                {/* Hook Header */}
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h3 className="text-2xl font-medieval text-white mb-1">
                      {generatedHook.title}
                    </h3>
                    <div className="flex items-center gap-4 text-sm">
                      <span className={`px-2 py-1 rounded text-xs border ${getCategoryColor(generatedHook.category)}`}>
                        {generatedHook.category}
                      </span>
                      <span className="text-secondary-300">
                        Złożoność: {generatedHook.complexity}
                      </span>
                      <span className={`${getUrgencyColor(generatedHook.urgency)}`}>
                        {generatedHook.urgency}
                      </span>
                    </div>
                  </div>
                  
                  <div className="flex gap-2">
                    <button
                      onClick={saveHook}
                      className="p-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
                      title="Zapisz zaczyn"
                    >
                      <Save className="w-4 h-4 text-white" />
                    </button>
                    <button
                      onClick={copyHook}
                      className="p-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                      title="Kopiuj do schowka"
                    >
                      <Copy className="w-4 h-4 text-white" />
                    </button>
                  </div>
                </div>

                {/* Hook Description */}
                <div className="mb-6">
                  <h4 className="font-semibold text-white mb-2">Opis Przygody</h4>
                  <p className="text-secondary-300 leading-relaxed">
                    {generatedHook.description}
                  </p>
                </div>

                {/* Hook Details */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <div>
                    <h4 className="font-semibold text-white mb-2">Szczegóły</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Zleceniodawca:</span>
                        <span className="text-white">{generatedHook.patron}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Nagroda:</span>
                        <span className="text-amber-400">{generatedHook.reward}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Tajność:</span>
                        <span className="text-white">{generatedHook.secrecy}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-secondary-400">Czas trwania:</span>
                        <span className="text-white">{generatedHook.duration}</span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Lokacje</h4>
                    <div className="space-y-1">
                      {generatedHook.locations.map((location, index) => (
                        <div key={index} className="flex items-center gap-2 text-sm">
                          <span className="text-secondary-400">•</span>
                          <span className="text-secondary-300">{location}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Complications */}
                <div className="mb-6">
                  <h4 className="font-semibold text-white mb-2">Możliwe Komplikacje</h4>
                  <div className="space-y-2">
                    {generatedHook.complications.map((complication, index) => (
                      <div key={index} className="flex items-start gap-2 text-sm">
                        <span className="text-red-400 mt-1">⚠️</span>
                        <span className="text-secondary-300">{complication}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* GM Notes */}
                <div>
                  <h4 className="font-semibold text-white mb-2">Notatki MG</h4>
                  <textarea
                    value={customNotes}
                    onChange={(e) => setCustomNotes(e.target.value)}
                    placeholder="Dodaj swoje pomysły i modyfikacje do tego zaczynu przygody..."
                    className="w-full h-32 bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white placeholder-secondary-400 resize-none"
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
                  <Scroll className="w-24 h-24 text-secondary-400 mx-auto mb-4 opacity-50" />
                  <h3 className="text-xl font-medieval text-white mb-2">
                    Brak Wygenerowanego Zaczynu
                  </h3>
                  <p className="text-secondary-400 mb-4">
                    Kliknij "Generuj Zaczyn" aby stworzyć pomysł na przygodę
                  </p>
                  <button
                    onClick={generateHook}
                    className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors flex items-center gap-2 mx-auto"
                  >
                    <Scroll className="w-5 h-5" />
                    Generuj Pierwszy Zaczyn
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
