import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Settings, Volume2, VolumeX, Eye, EyeOff, Clock, Users, MessageCircle } from 'lucide-react'

// Warhammer Fantasy faction selection for user
const UserFactionOptions = [
  {
    id: 'Empire',
    name: 'Imperium',
    icon: '👑',
    color: 'text-yellow-400',
    bgColor: 'bg-yellow-400/20',
    borderColor: 'border-yellow-400/50',
    description: 'Szlachetni i honorowi obywatele Imperium Sigmara'
  },
  {
    id: 'Chaos',
    name: 'Chaos',
    icon: '💀',
    color: 'text-red-400',
    bgColor: 'bg-red-400/20',
    borderColor: 'border-red-400/50',
    description: 'Służący Mrocznym Bogom, siający zniszczenie'
  },
  {
    id: 'HighElves',
    name: 'Wysokie Elfy',
    icon: '🌟',
    color: 'text-blue-400',
    bgColor: 'bg-blue-400/20',
    borderColor: 'border-blue-400/50',
    description: 'Pradawni i mądrzy mieszkańcy Ulthuan'
  },
  {
    id: 'Dwarfs',
    name: 'Krasnoludzi',
    icon: '🔨',
    color: 'text-amber-400',
    bgColor: 'bg-amber-400/20',
    borderColor: 'border-amber-400/50',
    description: 'Dumni i uparci mieszkańcy gór'
  },
  {
    id: 'Orcs',
    name: 'Orki',
    icon: '⚔️',
    color: 'text-green-400',
    bgColor: 'bg-green-400/20',
    borderColor: 'border-green-400/50',
    description: 'Brutalni i prymitywni wojownicy'
  }
]

// Conversation display options
const DisplayOptions = [
  {
    id: 'bubbles',
    name: 'Bąbelki nad postaciami',
    icon: MessageCircle,
    description: 'Wyświetlaj rozmowy jako bąbelki nad postaciami w tawernie'
  },
  {
    id: 'sidebar',
    name: 'Panel boczny',
    icon: Users,
    description: 'Pokaż rozmowy w panelu bocznym'
  },
  {
    id: 'fullscreen',
    name: 'Pełny ekran',
    icon: Eye,
    description: 'Otwórz rozmowy w trybie pełnoekranowym'
  }
]

export const ConversationSettings = ({ isVisible, onClose, settings, onSettingsChange }) => {
  const [localSettings, setLocalSettings] = useState({
    userFaction: 'Empire',
    audioEnabled: true,
    showBubbles: true,
    autoJoinConversations: false,
    conversationSpeed: 'normal',
    displayMode: 'bubbles',
    showEmotions: true,
    enableQuickResponses: true,
    bubbleTimeout: 5000,
    maxBubblesVisible: 5,
    ...settings
  })

  const handleSettingChange = (key, value) => {
    const newSettings = { ...localSettings, [key]: value }
    setLocalSettings(newSettings)
    
    if (onSettingsChange) {
      onSettingsChange(newSettings)
    }
  }

  const handleSave = () => {
    if (onSettingsChange) {
      onSettingsChange(localSettings)
    }
    onClose()
  }

  const handleReset = () => {
    const defaultSettings = {
      userFaction: 'Empire',
      audioEnabled: true,
      showBubbles: true,
      autoJoinConversations: false,
      conversationSpeed: 'normal',
      displayMode: 'bubbles',
      showEmotions: true,
      enableQuickResponses: true,
      bubbleTimeout: 5000,
      maxBubblesVisible: 5
    }
    
    setLocalSettings(defaultSettings)
    if (onSettingsChange) {
      onSettingsChange(defaultSettings)
    }
  }

  if (!isVisible) return null

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-secondary-800 rounded-lg w-full max-w-2xl max-h-[80vh] overflow-y-auto border border-secondary-700"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-6 border-b border-secondary-700 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Settings className="w-8 h-8 text-primary-400" />
            <div>
              <h2 className="text-2xl font-medieval text-white">
                Ustawienia Rozmów
              </h2>
              <p className="text-sm text-secondary-300">
                Dostosuj system rozmów do swoich preferencji
              </p>
            </div>
          </div>
          
          <button
            onClick={onClose}
            className="p-2 bg-secondary-700 hover:bg-secondary-600 rounded-lg transition-colors text-white"
          >
            ✕
          </button>
        </div>

        <div className="p-6 space-y-8">
          {/* User Faction Selection */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <span className="text-2xl">👤</span>
              Twoja Frakcja
            </h3>
            <p className="text-sm text-secondary-300 mb-4">
              Wybierz frakcję, która będzie reprezentować Twój styl rozmowy
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {UserFactionOptions.map((faction) => (
                <motion.button
                  key={faction.id}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => handleSettingChange('userFaction', faction.id)}
                  className={`
                    p-4 rounded-lg border-2 transition-all duration-200 text-left
                    ${localSettings.userFaction === faction.id 
                      ? `${faction.bgColor} ${faction.borderColor} shadow-lg` 
                      : 'bg-secondary-700/50 border-secondary-600 hover:border-secondary-500'
                    }
                  `}
                >
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-2xl">{faction.icon}</span>
                    <span className={`font-semibold ${
                      localSettings.userFaction === faction.id ? faction.color : 'text-white'
                    }`}>
                      {faction.name}
                    </span>
                  </div>
                  <p className="text-xs text-secondary-300">
                    {faction.description}
                  </p>
                </motion.button>
              ))}
            </div>
          </div>

          {/* Audio Settings */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Volume2 className="w-6 h-6" />
              Ustawienia Dźwięku
            </h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-secondary-700/50 rounded-lg">
                <div>
                  <span className="text-white font-medium">Dźwięki rozmów</span>
                  <p className="text-sm text-secondary-300">
                    Odtwarzaj dźwięki podczas rozmów
                  </p>
                </div>
                <button
                  onClick={() => handleSettingChange('audioEnabled', !localSettings.audioEnabled)}
                  className={`
                    p-2 rounded-lg transition-colors
                    ${localSettings.audioEnabled 
                      ? 'bg-green-600 hover:bg-green-700' 
                      : 'bg-secondary-600 hover:bg-secondary-500'
                    }
                  `}
                >
                  {localSettings.audioEnabled ? (
                    <Volume2 className="w-5 h-5 text-white" />
                  ) : (
                    <VolumeX className="w-5 h-5 text-white" />
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Display Settings */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Eye className="w-6 h-6" />
              Wyświetlanie Rozmów
            </h3>
            
            <div className="space-y-4">
              {DisplayOptions.map((option) => {
                const IconComponent = option.icon
                return (
                  <motion.button
                    key={option.id}
                    whileHover={{ scale: 1.01 }}
                    whileTap={{ scale: 0.99 }}
                    onClick={() => handleSettingChange('displayMode', option.id)}
                    className={`
                      w-full p-4 rounded-lg border transition-all duration-200 text-left
                      ${localSettings.displayMode === option.id
                        ? 'bg-primary-400/20 border-primary-400/50 text-primary-100'
                        : 'bg-secondary-700/50 border-secondary-600 hover:border-secondary-500 text-white'
                      }
                    `}
                  >
                    <div className="flex items-center gap-3 mb-2">
                      <IconComponent className="w-5 h-5" />
                      <span className="font-medium">{option.name}</span>
                    </div>
                    <p className="text-sm opacity-80">
                      {option.description}
                    </p>
                  </motion.button>
                )
              })}
            </div>
          </div>

          {/* Bubble Settings */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <MessageCircle className="w-6 h-6" />
              Ustawienia Bąbelków
            </h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-secondary-700/50 rounded-lg">
                <div>
                  <span className="text-white font-medium">Pokaż bąbelki</span>
                  <p className="text-sm text-secondary-300">
                    Wyświetlaj bąbelki rozmów nad postaciami
                  </p>
                </div>
                <button
                  onClick={() => handleSettingChange('showBubbles', !localSettings.showBubbles)}
                  className={`
                    w-12 h-6 rounded-full transition-colors relative
                    ${localSettings.showBubbles ? 'bg-green-600' : 'bg-secondary-600'}
                  `}
                >
                  <div className={`
                    w-5 h-5 bg-white rounded-full absolute top-0.5 transition-transform
                    ${localSettings.showBubbles ? 'translate-x-6' : 'translate-x-0.5'}
                  `} />
                </button>
              </div>

              <div className="p-4 bg-secondary-700/50 rounded-lg">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-white font-medium">Czas wyświetlania bąbelka</span>
                  <span className="text-primary-400 font-semibold">
                    {localSettings.bubbleTimeout / 1000}s
                  </span>
                </div>
                <input
                  type="range"
                  min="2000"
                  max="10000"
                  step="500"
                  value={localSettings.bubbleTimeout}
                  onChange={(e) => handleSettingChange('bubbleTimeout', parseInt(e.target.value))}
                  className="w-full h-2 bg-secondary-600 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-xs text-secondary-400 mt-1">
                  <span>2s</span>
                  <span>10s</span>
                </div>
              </div>

              <div className="p-4 bg-secondary-700/50 rounded-lg">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-white font-medium">Maksymalna liczba bąbelków</span>
                  <span className="text-primary-400 font-semibold">
                    {localSettings.maxBubblesVisible}
                  </span>
                </div>
                <input
                  type="range"
                  min="3"
                  max="15"
                  step="1"
                  value={localSettings.maxBubblesVisible}
                  onChange={(e) => handleSettingChange('maxBubblesVisible', parseInt(e.target.value))}
                  className="w-full h-2 bg-secondary-600 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-xs text-secondary-400 mt-1">
                  <span>3</span>
                  <span>15</span>
                </div>
              </div>
            </div>
          </div>

          {/* Quick Response Settings */}
          <div>
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
              <Clock className="w-6 h-6" />
              Szybkie Odpowiedzi
            </h3>
            
            <div className="flex items-center justify-between p-4 bg-secondary-700/50 rounded-lg">
              <div>
                <span className="text-white font-medium">Włącz szybkie odpowiedzi</span>
                <p className="text-sm text-secondary-300">
                  Pokaż panel szybkich odpowiedzi podczas rozmów
                </p>
              </div>
              <button
                onClick={() => handleSettingChange('enableQuickResponses', !localSettings.enableQuickResponses)}
                className={`
                  w-12 h-6 rounded-full transition-colors relative
                  ${localSettings.enableQuickResponses ? 'bg-green-600' : 'bg-secondary-600'}
                `}
              >
                <div className={`
                  w-5 h-5 bg-white rounded-full absolute top-0.5 transition-transform
                  ${localSettings.enableQuickResponses ? 'translate-x-6' : 'translate-x-0.5'}
                `} />
              </button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="p-6 border-t border-secondary-700 flex items-center justify-between">
          <button
            onClick={handleReset}
            className="px-4 py-2 bg-secondary-700 hover:bg-secondary-600 text-white rounded-lg transition-colors"
          >
            Przywróć domyślne
          </button>
          
          <div className="flex gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-secondary-700 hover:bg-secondary-600 text-white rounded-lg transition-colors"
            >
              Anuluj
            </button>
            <button
              onClick={handleSave}
              className="px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors font-semibold"
            >
              Zapisz
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  )
}
