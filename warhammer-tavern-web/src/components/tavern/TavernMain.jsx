import React, { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sword, Crown, Coins, Users, Settings, RefreshCw, Volume2, VolumeX, MessageCircle } from 'lucide-react'
import { WarhammerGSAPController } from '../animations/WarhammerGSAPController'
import { WarhammerCharacterCard } from '../characters/WarhammerCharacterCard'
import { InteractionProposalSystem } from './InteractionProposalSystem'
import { ConversationSystem } from '../conversations/ConversationSystem'
import { ConversationBubbles } from '../conversations/ConversationBubbles'
import { QuickResponsePanel } from '../conversations/QuickResponsePanel'
import { GameMasterTools } from '../gamemaster/GameMasterTools'
import { useAppStore } from '@stores/appStore'
import { useWebSocketStore } from '@stores/webSocketStore'
import toast from 'react-hot-toast'

// Warhammer Fantasy tavern names with lore
const TavernNames = [
  'Złoty Gryf', 'Krwawy Topór', 'Srebrny Smok', 'Żelazna Korona',
  'Pijany Krasnolud', 'Elficki Liść', 'Orcza Głowa', 'Martwy Koń',
  'Płonący Miecz', 'Księżycowa Róża', 'Stalowy Młot', 'Czarna Perła'
]

// Tavern atmosphere descriptions
const TavernAtmospheres = {
  peaceful: {
    description: 'Spokojna atmosfera, goście cicho rozmawiają przy kominku',
    color: 'text-green-400',
    icon: '🕊️'
  },
  tense: {
    description: 'Napięta atmosfera, ręce spoczywają na rękojeściach mieczy',
    color: 'text-yellow-400',
    icon: '⚡'
  },
  chaotic: {
    description: 'Chaotyczna atmosfera, krzyki i kłótnie wypełniają powietrze',
    color: 'text-red-400',
    icon: '🔥'
  },
  mysterious: {
    description: 'Tajemnicza atmosfera, cienie tańczą w świetle świec',
    color: 'text-purple-400',
    icon: '🌙'
  }
}

const TavernMain = () => {
  const [selectedCharacter, setSelectedCharacter] = useState(null)
  const [showProposals, setShowProposals] = useState(false)
  const [tavernAtmosphere, setTavernAtmosphere] = useState('peaceful')
  const [audioEnabled, setAudioEnabled] = useState(true)
  const [showSettings, setShowSettings] = useState(false)
  const [showConversationSystem, setShowConversationSystem] = useState(false)
  const [showGameMasterTools, setShowGameMasterTools] = useState(false)
  const [activeConversations, setActiveConversations] = useState([])
  const [showQuickResponse, setShowQuickResponse] = useState(false)
  const [currentConversationTopic, setCurrentConversationTopic] = useState(null)
  const [userFaction, setUserFaction] = useState('Empire')
  
  const { 
    tavern, 
    agents, 
    updateTavernState, 
    generateNewTavern,
    startConversation,
    generateEvent,
    preferences,
    updatePreferences
  } = useAppStore()
  
  const { isConnected, send, subscribe } = useWebSocketStore()

  // Subscribe to WebSocket updates
  useEffect(() => {
    if (isConnected) {
      subscribe('tavern_updates')
      subscribe('conversations')
      subscribe('agent_actions')
      subscribe('events')
    }
  }, [isConnected, subscribe])

  // Handle conversation updates
  useEffect(() => {
    // Listen for conversation events from WebSocket
    const handleConversationUpdate = (data) => {
      if (data.type === 'conversation_start') {
        setActiveConversations(prev => [...prev, {
          id: Date.now(),
          participants: data.participants,
          topic: data.topic,
          position: { x: Math.random() * 80 + 10, y: Math.random() * 60 + 20 }
        }])
        setCurrentConversationTopic(data.topic)
        setShowQuickResponse(true)
      } else if (data.type === 'conversation_end') {
        setActiveConversations(prev => prev.filter(conv =>
          !conv.participants.every(p => data.participants.includes(p))
        ))
        setShowQuickResponse(false)
      }
    }

    // This would be connected to WebSocket in a real implementation
    // For now, we'll simulate it
  }, [])

  // Generate random tavern atmosphere
  const generateAtmosphere = useCallback(() => {
    const atmospheres = Object.keys(TavernAtmospheres)
    const randomAtmosphere = atmospheres[Math.floor(Math.random() * atmospheres.length)]
    setTavernAtmosphere(randomAtmosphere)
  }, [])

  // Handle character selection
  const handleCharacterSelect = (character) => {
    setSelectedCharacter(character)
    setShowProposals(true)
    
    // Play selection sound effect
    if (audioEnabled) {
      // This would integrate with Howler.js
      console.log('🔊 Playing character selection sound')
    }
  }

  // Handle proposal selection
  const handleProposalSelect = (proposal) => {
    toast.success(`Rozpoczęto: ${proposal.title}`)
    
    // Send to backend
    send({
      type: 'start_interaction',
      data: {
        character: selectedCharacter.name,
        proposal: proposal,
        timestamp: Date.now()
      }
    })
  }

  // Generate new tavern
  const handleGenerateNewTavern = async () => {
    try {
      await generateNewTavern()
      generateAtmosphere()
      setSelectedCharacter(null)
      setShowProposals(false)
      toast.success('Wygenerowano nową tawernę!')
    } catch (error) {
      toast.error('Błąd podczas generowania tawerny')
    }
  }

  // Start random conversation
  const handleStartConversation = async () => {
    if (agents.length < 2) {
      toast.error('Potrzeba co najmniej 2 postaci do rozmowy')
      return
    }

    const randomAgents = agents
      .filter(agent => agent.active)
      .sort(() => 0.5 - Math.random())
      .slice(0, 2)
      .map(agent => agent.name)

    try {
      await startConversation(randomAgents)

      // Add to active conversations
      setActiveConversations(prev => [...prev, {
        id: Date.now(),
        participants: randomAgents,
        topic: 'Losowa rozmowa',
        position: { x: Math.random() * 80 + 10, y: Math.random() * 60 + 20 }
      }])

      setCurrentConversationTopic('Losowa rozmowa')
      setShowQuickResponse(true)
      toast.success('Rozpoczęto losową rozmowę!')
    } catch (error) {
      toast.error('Błąd podczas rozpoczynania rozmowy')
    }
  }

  // Handle conversation bubble click
  const handleBubbleClick = (bubble) => {
    toast.info(`${bubble.characterName}: ${bubble.text}`)
    setShowQuickResponse(true)
  }

  // Handle quick response
  const handleQuickResponse = (response) => {
    send({
      type: 'user_response',
      data: {
        message: response.text,
        category: response.category,
        faction: response.faction,
        timestamp: response.timestamp
      }
    })

    toast.success(`Odpowiedziałeś: ${response.text}`)
  }

  // Handle reaction
  const handleReaction = (reaction) => {
    send({
      type: 'user_reaction',
      data: {
        emoji: reaction.emoji,
        name: reaction.name,
        faction: reaction.faction,
        timestamp: reaction.timestamp
      }
    })

    toast.success(`Zareagowałeś: ${reaction.emoji}`)
  }

  // Generate random event
  const handleGenerateEvent = async () => {
    try {
      await generateEvent()
      generateAtmosphere()
      toast.success('Wygenerowano wydarzenie!')
    } catch (error) {
      toast.error('Błąd podczas generowania wydarzenia')
    }
  }

  const currentAtmosphere = TavernAtmospheres[tavernAtmosphere]

  return (
    <WarhammerGSAPController faction="Empire" animationType="tavern_ambient">
      <div className="min-h-screen bg-gradient-to-br from-tavern-shadow via-secondary-900 to-secondary-800 p-4">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-8"
          >
            <h1 className="text-5xl font-medieval text-primary-400 mb-2 text-glow">
              🏰 {tavern.name || TavernNames[0]}
            </h1>
            <div className="flex items-center justify-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <span className={currentAtmosphere.color}>
                  {currentAtmosphere.icon}
                </span>
                <span className="text-secondary-300">
                  {currentAtmosphere.description}
                </span>
              </div>
            </div>
          </motion.div>

          {/* Tavern Stats */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8"
          >
            <div className="bg-secondary-800/80 rounded-lg p-4 backdrop-blur-sm border border-secondary-700">
              <div className="flex items-center gap-3">
                <Crown className="w-8 h-8 text-yellow-400" />
                <div>
                  <p className="text-sm text-secondary-400">Reputacja</p>
                  <p className="text-xl font-bold text-yellow-400">{tavern.reputation || 75}</p>
                </div>
              </div>
            </div>

            <div className="bg-secondary-800/80 rounded-lg p-4 backdrop-blur-sm border border-secondary-700">
              <div className="flex items-center gap-3">
                <Sword className="w-8 h-8 text-red-400" />
                <div>
                  <p className="text-sm text-secondary-400">Napięcie</p>
                  <p className="text-xl font-bold text-red-400">{tavern.tension || 25}</p>
                </div>
              </div>
            </div>

            <div className="bg-secondary-800/80 rounded-lg p-4 backdrop-blur-sm border border-secondary-700">
              <div className="flex items-center gap-3">
                <Coins className="w-8 h-8 text-amber-400" />
                <div>
                  <p className="text-sm text-secondary-400">Bogactwo</p>
                  <p className="text-xl font-bold text-amber-400">{tavern.wealth || 1250}</p>
                </div>
              </div>
            </div>

            <div className="bg-secondary-800/80 rounded-lg p-4 backdrop-blur-sm border border-secondary-700">
              <div className="flex items-center gap-3">
                <Users className="w-8 h-8 text-blue-400" />
                <div>
                  <p className="text-sm text-secondary-400">Goście</p>
                  <p className="text-xl font-bold text-blue-400">{agents.filter(a => a.active).length}</p>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Main Content */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            {/* Main Tavern View */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="xl:col-span-2 space-y-6"
            >
              {/* 3D Tavern Scene Placeholder */}
              <div className="bg-secondary-800/80 rounded-lg p-6 backdrop-blur-sm border border-secondary-700">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-2xl font-medieval text-white">Główna Sala Tawerny</h2>
                  <div className="flex gap-2">
                    <button
                      onClick={() => setAudioEnabled(!audioEnabled)}
                      className="p-2 bg-secondary-700 hover:bg-secondary-600 rounded-lg transition-colors"
                    >
                      {audioEnabled ? (
                        <Volume2 className="w-5 h-5 text-white" />
                      ) : (
                        <VolumeX className="w-5 h-5 text-white" />
                      )}
                    </button>
                    <button
                      onClick={() => setShowSettings(true)}
                      className="p-2 bg-secondary-700 hover:bg-secondary-600 rounded-lg transition-colors"
                    >
                      <Settings className="w-5 h-5 text-white" />
                    </button>
                  </div>
                </div>
                
                <div className="aspect-video bg-gradient-to-br from-tavern-wood to-tavern-shadow rounded-lg flex items-center justify-center relative overflow-hidden">
                  {/* Tavern Background */}
                  <div className="absolute inset-0 bg-tavern-pattern opacity-20"></div>
                  
                  {/* Fireplace Effect */}
                  <div className="absolute bottom-4 left-4 w-16 h-16 bg-fire-glow rounded-full opacity-60 animate-flicker"></div>
                  
                  {/* Character Positions */}
                  <div className="relative z-10 grid grid-cols-3 gap-8 w-full h-full p-8">
                    {agents.filter(agent => agent.active).slice(0, 6).map((agent, index) => (
                      <motion.div
                        key={agent.name}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: index * 0.1 }}
                        className={`flex items-center justify-center cursor-pointer transition-transform hover:scale-110 ${
                          selectedCharacter?.name === agent.name ? 'ring-2 ring-primary-400 rounded-full' : ''
                        }`}
                        onClick={() => handleCharacterSelect(agent)}
                      >
                        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white font-bold shadow-lg">
                          {agent.name.charAt(0)}
                        </div>
                      </motion.div>
                    ))}
                  </div>
                  
                  <div className="absolute inset-0 flex items-center justify-center">
                    <p className="text-secondary-400 text-lg font-medieval">
                      Kliknij na postać, aby rozpocząć interakcję
                    </p>
                  </div>

                  {/* Conversation Bubbles Overlay */}
                  <ConversationBubbles
                    characters={agents.filter(agent => agent.active).map(agent => ({
                      ...agent,
                      position: { x: Math.random() * 80 + 10, y: Math.random() * 60 + 20 }
                    }))}
                    activeConversations={activeConversations}
                    onBubbleClick={handleBubbleClick}
                  />
                </div>
              </div>

              {/* Action Buttons */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button
                  onClick={handleGenerateNewTavern}
                  className="p-4 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors text-white font-semibold flex items-center gap-2"
                >
                  <RefreshCw className="w-5 h-5" />
                  Nowa Tawerna
                </button>

                <button
                  onClick={handleStartConversation}
                  className="p-4 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors text-white font-semibold flex items-center gap-2"
                >
                  <Users className="w-5 h-5" />
                  Losowa Rozmowa
                </button>

                <button
                  onClick={() => setShowConversationSystem(true)}
                  className="p-4 bg-green-600 hover:bg-green-700 rounded-lg transition-colors text-white font-semibold flex items-center gap-2"
                >
                  <MessageCircle className="w-5 h-5" />
                  System Rozmów
                </button>

                <button
                  onClick={() => setShowGameMasterTools(true)}
                  className="p-4 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors text-white font-semibold flex items-center gap-2"
                >
                  <Crown className="w-5 h-5" />
                  Narzędzia MG
                </button>

                <button
                  onClick={handleGenerateEvent}
                  className="p-4 bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors text-white font-semibold flex items-center gap-2"
                >
                  <Sword className="w-5 h-5" />
                  Wydarzenie
                </button>

                <button
                  onClick={generateAtmosphere}
                  className="p-4 bg-amber-600 hover:bg-amber-700 rounded-lg transition-colors text-white font-semibold flex items-center gap-2"
                >
                  {currentAtmosphere.icon}
                  Atmosfera
                </button>
              </div>
            </motion.div>

            {/* Side Panel */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="space-y-6"
            >
              {/* Characters List */}
              <div className="bg-secondary-800/80 rounded-lg p-6 backdrop-blur-sm border border-secondary-700">
                <h3 className="text-xl font-medieval text-white mb-4 flex items-center gap-2">
                  <Users className="w-6 h-6" />
                  Postacie w Tawernie
                </h3>
                
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {agents.filter(agent => agent.active).map((agent) => (
                    <WarhammerCharacterCard
                      key={agent.name}
                      character={agent}
                      isSelected={selectedCharacter?.name === agent.name}
                      onClick={handleCharacterSelect}
                    />
                  ))}
                </div>

                {agents.filter(agent => agent.active).length === 0 && (
                  <div className="text-center py-8">
                    <Users className="w-16 h-16 text-secondary-400 mx-auto mb-4 opacity-50" />
                    <p className="text-secondary-400">Brak aktywnych postaci</p>
                  </div>
                )}
              </div>

              {/* Interaction Proposals */}
              <AnimatePresence>
                {showProposals && selectedCharacter && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                  >
                    <InteractionProposalSystem
                      selectedCharacter={selectedCharacter}
                      onProposalSelect={handleProposalSelect}
                    />
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          </div>
        </div>

        {/* Conversation System Modal */}
        <AnimatePresence>
          {showConversationSystem && (
            <ConversationSystem
              isVisible={showConversationSystem}
              onClose={() => setShowConversationSystem(false)}
            />
          )}
        </AnimatePresence>

        {/* Game Master Tools Modal */}
        <AnimatePresence>
          {showGameMasterTools && (
            <GameMasterTools
              isVisible={showGameMasterTools}
              onClose={() => setShowGameMasterTools(false)}
            />
          )}
        </AnimatePresence>

        {/* Quick Response Panel */}
        <QuickResponsePanel
          isVisible={showQuickResponse}
          onResponse={handleQuickResponse}
          onReaction={handleReaction}
          currentTopic={currentConversationTopic}
          userFaction={userFaction}
        />
      </div>
    </WarhammerGSAPController>
  )
}

export default TavernMain
