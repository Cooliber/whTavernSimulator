import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Dice6, Users, Map, Scroll, Crown, Sword, Shield, 
  BookOpen, Settings, RefreshCw, Save, Download, Upload,
  Eye, EyeOff, Plus, Minus, Star, Zap
} from 'lucide-react'
import { WarhammerGSAPController } from '../animations/WarhammerGSAPController'
import { NPCGenerator } from './NPCGenerator'
import { RandomEncounters } from './RandomEncounters'
import { AdventureHooks } from './AdventureHooks'
import { CampaignManager } from './CampaignManager'
import { RandomTablesComponent as RandomTables } from './RandomTables'
import { useAppStore } from '@stores/appStore'
import toast from 'react-hot-toast'

// GM Tool Categories with Warhammer Fantasy theme
const GMToolCategories = {
  npcs: {
    name: 'Generator NPC',
    icon: Users,
    color: 'text-blue-400',
    bgColor: 'bg-blue-400/20',
    borderColor: 'border-blue-400/50',
    description: 'Generuj postacie niezależne z pełnymi statystykami',
    component: NPCGenerator
  },
  encounters: {
    name: 'Losowe Spotkania',
    icon: Sword,
    color: 'text-red-400',
    bgColor: 'bg-red-400/20',
    borderColor: 'border-red-400/50',
    description: 'Generuj spotkania na drogach Starego Świata',
    component: RandomEncounters
  },
  hooks: {
    name: 'Zaczyny Przygód',
    icon: Scroll,
    color: 'text-amber-400',
    bgColor: 'bg-amber-400/20',
    borderColor: 'border-amber-400/50',
    description: 'Pomysły na przygody i zadania dla graczy',
    component: AdventureHooks
  },
  campaign: {
    name: 'Zarządzanie Kampanią',
    icon: Crown,
    color: 'text-purple-400',
    bgColor: 'bg-purple-400/20',
    borderColor: 'border-purple-400/50',
    description: 'Narzędzia do prowadzenia długotrwałych kampanii',
    component: CampaignManager
  },
  tables: {
    name: 'Tabele Losowe',
    icon: Dice6,
    color: 'text-green-400',
    bgColor: 'bg-green-400/20',
    borderColor: 'border-green-400/50',
    description: 'Kolekcja tabel losowych dla WFRP',
    component: RandomTables
  },
  maps: {
    name: 'Mapy i Lokacje',
    icon: Map,
    color: 'text-cyan-400',
    bgColor: 'bg-cyan-400/20',
    borderColor: 'border-cyan-400/50',
    description: 'Generatory lokacji i map dla Starego Świata',
    component: null // To be implemented
  }
}

// GM Session Tools
const SessionTools = [
  {
    id: 'initiative',
    name: 'Tracker Inicjatywy',
    icon: Zap,
    description: 'Śledź kolejność działań w walce'
  },
  {
    id: 'notes',
    name: 'Notatki Sesji',
    icon: BookOpen,
    description: 'Zapisuj ważne wydarzenia i decyzje'
  },
  {
    id: 'handouts',
    name: 'Materiały dla Graczy',
    icon: Scroll,
    description: 'Zarządzaj dokumentami i wskazówkami'
  },
  {
    id: 'music',
    name: 'Atmosfera Dźwiękowa',
    icon: Settings,
    description: 'Kontroluj muzykę i efekty dźwiękowe'
  }
]

export const GameMasterTools = ({ isVisible, onClose }) => {
  const [activeCategory, setActiveCategory] = useState('npcs')
  const [gmMode, setGmMode] = useState(false)
  const [sessionData, setSessionData] = useState({
    notes: '',
    initiative: [],
    handouts: [],
    timestamp: Date.now()
  })
  const [showSessionTools, setShowSessionTools] = useState(false)
  
  const { preferences, updatePreferences } = useAppStore()

  // Load GM preferences
  useEffect(() => {
    const savedGMData = localStorage.getItem('wfrp_gm_data')
    if (savedGMData) {
      try {
        const data = JSON.parse(savedGMData)
        setSessionData(data)
      } catch (error) {
        console.error('Error loading GM data:', error)
      }
    }
  }, [])

  // Save GM data
  const saveGMData = () => {
    try {
      localStorage.setItem('wfrp_gm_data', JSON.stringify(sessionData))
      toast.success('Dane MG zapisane!')
    } catch (error) {
      toast.error('Błąd podczas zapisywania danych')
    }
  }

  // Export GM data
  const exportGMData = () => {
    try {
      const dataStr = JSON.stringify(sessionData, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      
      const link = document.createElement('a')
      link.href = url
      link.download = `wfrp_gm_session_${new Date().toISOString().split('T')[0]}.json`
      link.click()
      
      URL.revokeObjectURL(url)
      toast.success('Dane wyeksportowane!')
    } catch (error) {
      toast.error('Błąd podczas eksportu')
    }
  }

  // Import GM data
  const importGMData = (event) => {
    const file = event.target.files[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result)
        setSessionData(data)
        toast.success('Dane zaimportowane!')
      } catch (error) {
        toast.error('Błąd podczas importu danych')
      }
    }
    reader.readAsText(file)
  }

  // Toggle GM mode
  const toggleGMMode = () => {
    setGmMode(!gmMode)
    updatePreferences({ gmMode: !gmMode })
    toast.success(gmMode ? 'Tryb gracza włączony' : 'Tryb MG włączony')
  }

  const ActiveComponent = GMToolCategories[activeCategory]?.component

  if (!isVisible) return null

  return (
    <WarhammerGSAPController faction="Empire" animationType="gm_tools">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/90 flex items-center justify-center z-50 p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="bg-secondary-800 rounded-lg w-full max-w-7xl h-[90vh] flex flex-col border border-secondary-700"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="p-6 border-b border-secondary-700 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="character-element">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-purple-600 to-purple-800 flex items-center justify-center">
                  <Crown className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <h2 className="text-3xl font-medieval text-white">
                  Narzędzia Mistrza Gry
                </h2>
                <p className="text-secondary-300">
                  Zaawansowane narzędzia do prowadzenia kampanii WFRP
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              {/* GM Mode Toggle */}
              <button
                onClick={toggleGMMode}
                className={`
                  px-4 py-2 rounded-lg font-semibold transition-all duration-300 flex items-center gap-2
                  ${gmMode 
                    ? 'bg-purple-600 hover:bg-purple-700 text-white' 
                    : 'bg-secondary-700 hover:bg-secondary-600 text-secondary-300'
                  }
                `}
              >
                {gmMode ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                {gmMode ? 'Tryb MG' : 'Tryb Gracza'}
              </button>

              {/* Session Tools Toggle */}
              <button
                onClick={() => setShowSessionTools(!showSessionTools)}
                className="p-2 bg-secondary-700 hover:bg-secondary-600 rounded-lg transition-colors"
              >
                <Settings className="w-5 h-5 text-white" />
              </button>

              {/* Save/Load */}
              <div className="flex gap-1">
                <button
                  onClick={saveGMData}
                  className="p-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
                  title="Zapisz dane"
                >
                  <Save className="w-4 h-4 text-white" />
                </button>
                
                <button
                  onClick={exportGMData}
                  className="p-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                  title="Eksportuj dane"
                >
                  <Download className="w-4 h-4 text-white" />
                </button>
                
                <label className="p-2 bg-amber-600 hover:bg-amber-700 rounded-lg transition-colors cursor-pointer" title="Importuj dane">
                  <Upload className="w-4 h-4 text-white" />
                  <input
                    type="file"
                    accept=".json"
                    onChange={importGMData}
                    className="hidden"
                  />
                </label>
              </div>

              <button
                onClick={onClose}
                className="p-2 bg-secondary-700 hover:bg-secondary-600 rounded-lg transition-colors text-white"
              >
                ✕
              </button>
            </div>
          </div>

          <div className="flex-1 flex overflow-hidden">
            {/* Sidebar - Tool Categories */}
            <div className="w-80 border-r border-secondary-700 p-4 overflow-y-auto">
              <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
                <Dice6 className="w-5 h-5" />
                Kategorie Narzędzi
              </h3>
              
              <div className="space-y-2 mb-6">
                {Object.entries(GMToolCategories).map(([key, category]) => {
                  const IconComponent = category.icon
                  return (
                    <motion.button
                      key={key}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => setActiveCategory(key)}
                      className={`
                        w-full p-4 rounded-lg border transition-all duration-200 text-left
                        ${activeCategory === key
                          ? `${category.bgColor} ${category.borderColor} shadow-lg`
                          : 'bg-secondary-700/50 border-secondary-600 hover:border-secondary-500'
                        }
                      `}
                    >
                      <div className="flex items-center gap-3 mb-2">
                        <IconComponent className={`w-5 h-5 ${
                          activeCategory === key ? category.color : 'text-secondary-400'
                        }`} />
                        <span className={`font-semibold ${
                          activeCategory === key ? 'text-white' : 'text-secondary-300'
                        }`}>
                          {category.name}
                        </span>
                      </div>
                      <p className="text-xs text-secondary-400">
                        {category.description}
                      </p>
                    </motion.button>
                  )
                })}
              </div>

              {/* Session Tools */}
              <AnimatePresence>
                {showSessionTools && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="border-t border-secondary-700 pt-4"
                  >
                    <h4 className="font-semibold text-white mb-3 flex items-center gap-2">
                      <Settings className="w-4 h-4" />
                      Narzędzia Sesji
                    </h4>
                    
                    <div className="space-y-2">
                      {SessionTools.map((tool) => {
                        const IconComponent = tool.icon
                        return (
                          <button
                            key={tool.id}
                            className="w-full p-3 bg-secondary-700/50 hover:bg-secondary-700 rounded-lg transition-colors text-left"
                          >
                            <div className="flex items-center gap-2 mb-1">
                              <IconComponent className="w-4 h-4 text-secondary-400" />
                              <span className="text-sm font-medium text-white">
                                {tool.name}
                              </span>
                            </div>
                            <p className="text-xs text-secondary-400">
                              {tool.description}
                            </p>
                          </button>
                        )
                      })}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Quick Stats */}
              <div className="mt-6 p-4 bg-secondary-700/30 rounded-lg">
                <h4 className="font-semibold text-white mb-3">Statystyki Sesji</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-secondary-400">Wygenerowane NPC:</span>
                    <span className="text-white">0</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-secondary-400">Spotkania:</span>
                    <span className="text-white">0</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-secondary-400">Zaczyny przygód:</span>
                    <span className="text-white">0</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 overflow-hidden">
              <AnimatePresence mode="wait">
                {ActiveComponent ? (
                  <motion.div
                    key={activeCategory}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="h-full"
                  >
                    <ActiveComponent 
                      gmMode={gmMode}
                      sessionData={sessionData}
                      onSessionDataUpdate={setSessionData}
                    />
                  </motion.div>
                ) : (
                  <motion.div
                    key="placeholder"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="h-full flex items-center justify-center"
                  >
                    <div className="text-center">
                      <Map className="w-24 h-24 text-secondary-400 mx-auto mb-4 opacity-50" />
                      <h3 className="text-xl font-medieval text-white mb-2">
                        Narzędzie w Budowie
                      </h3>
                      <p className="text-secondary-400">
                        To narzędzie będzie dostępne wkrótce
                      </p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Footer */}
          <div className="p-4 border-t border-secondary-700 bg-secondary-800/50">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-4 text-secondary-400">
                <span>WFRP Game Master Tools v2.0</span>
                <span>•</span>
                <span>Sesja: {new Date().toLocaleDateString()}</span>
              </div>
              
              <div className="flex items-center gap-2">
                <Star className="w-4 h-4 text-amber-400" />
                <span className="text-secondary-300">
                  Dla najlepszych Mistrzów Gry Starego Świata!
                </span>
              </div>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </WarhammerGSAPController>
  )
}
