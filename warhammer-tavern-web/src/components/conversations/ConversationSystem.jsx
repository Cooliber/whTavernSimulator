import React, { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Users, Volume2, VolumeX, Settings, MessageCircle, Crown, Sword } from 'lucide-react'
import { WarhammerGSAPController } from '../animations/WarhammerGSAPController'
import { useAppStore } from '@stores/appStore'
import { useWebSocketStore } from '@stores/webSocketStore'
import toast from 'react-hot-toast'

// Warhammer Fantasy conversation topics with lore
const ConversationTopics = {
  politics: {
    name: 'Polityka',
    icon: '👑',
    color: 'text-yellow-400',
    topics: [
      'Sytuacja w Imperium po ostatniej wojnie',
      'Nowe podatki wprowadzone przez Elektorów',
      'Relacje z Bretonnią i ich rycerzami',
      'Zagrożenie ze strony Norscy',
      'Handel z Marienburgiem'
    ]
  },
  war: {
    name: 'Wojna',
    icon: '⚔️',
    color: 'text-red-400',
    topics: [
      'Ostatnie starcia z hordami Chaosu',
      'Obrona przed najazdami orków',
      'Taktyki przeciwko nieumarłym',
      'Nowe bronie i technologie',
      'Rekrutacja do Straży Imperialnej'
    ]
  },
  magic: {
    name: 'Magia',
    icon: '⚡',
    color: 'text-purple-400',
    topics: [
      'Nowe zaklęcia odkryte w Kolegium',
      'Niebezpieczeństwa magii Chaosu',
      'Starożytne artefakty magiczne',
      'Rytuały ochronne przed demonami',
      'Przepowiednie i wizje przyszłości'
    ]
  },
  trade: {
    name: 'Handel',
    icon: '💰',
    color: 'text-amber-400',
    topics: [
      'Ceny towarów na rynkach',
      'Nowe szlaki handlowe',
      'Problemy z bandytami na drogach',
      'Eksport do Kislev',
      'Konkurencja z kupcami elfickimi'
    ]
  },
  rumors: {
    name: 'Plotki',
    icon: '👂',
    color: 'text-gray-400',
    topics: [
      'Dziwne zjawiska w lasach',
      'Zaginięcia w pobliskich wioskach',
      'Skarby ukryte w ruinach',
      'Tajemniczy podróżnicy',
      'Legendy o starożytnych bohaterach'
    ]
  },
  religion: {
    name: 'Religia',
    icon: '🙏',
    color: 'text-blue-400',
    topics: [
      'Błogosławieństwa Sigmara',
      'Święta i ceremonie religijne',
      'Walka z herezją',
      'Cuda i objawienia',
      'Pielgrzymki do świętych miejsc'
    ]
  }
}

// Faction-specific conversation styles
const FactionConversationStyles = {
  Empire: {
    greeting: ['Sigmar was z wami!', 'Cześć i chwała Imperium!', 'Niech Sigmar was błogosławi!'],
    farewell: ['Niech Sigmar was strzeże!', 'Do zobaczenia, obywatelu!', 'Chwała Imperium!'],
    agreement: ['Zgadzam się całkowicie!', 'Mądrze powiedziane!', 'Tak jest, towarzyszu!'],
    disagreement: ['Nie mogę się z tym zgodzić!', 'To nie jest właściwe!', 'Sigmar by tego nie pochwalił!'],
    style: 'formal',
    accent: 'imperial'
  },
  Chaos: {
    greeting: ['Niech Chaos panuje!', 'Krew i chwała!', 'Mroczne Moce was widzą!'],
    farewell: ['Niech Chaos was pochłonie!', 'Krew dla Boga Krwi!', 'Śmierć wrogom!'],
    agreement: ['Tak! Zniszczenie!', 'Chaos zatryumfuje!', 'Krew i czaszki!'],
    disagreement: ['Słabość!', 'Zdrajca!', 'Śmierć heretykom!'],
    style: 'aggressive',
    accent: 'chaotic'
  },
  HighElves: {
    greeting: ['Asuryan was błogosławi', 'Pokój z wami, młodsze rasy', 'Mądrość elfów z wami'],
    farewell: ['Niech gwiazdy was prowadzą', 'Do widzenia, śmiertelnicy', 'Asuryan was strzeże'],
    agreement: ['Mądrze zauważone', 'Zgoda, choć oczywiste', 'Tak, jak przewidywałem'],
    disagreement: ['Błędne myślenie', 'Typowe dla młodszych ras', 'Nie rozumiecie'],
    style: 'arrogant',
    accent: 'elven'
  },
  Dwarfs: {
    greeting: ['Khazad ai-mênu!', 'Cześć, brodaty!', 'Niech przodkowie was błogosławią!'],
    farewell: ['Niech młot was prowadzi!', 'Baruk Khazâd!', 'Do zobaczenia w kuźni!'],
    agreement: ['Aye, prawda!', 'Solidnie powiedziane!', 'Tak mówią przodkowie!'],
    disagreement: ['Bzdury!', 'To idzie do Księgi!', 'Hańba!'],
    style: 'gruff',
    accent: 'dwarven'
  },
  Orcs: {
    greeting: ['Waaagh!', 'Oi, ty!', 'Gotowy do walki?'],
    farewell: ['Waaagh!', 'Idę walczyć!', 'Do boju!'],
    agreement: ['Da! Walka!', 'Waaagh! Zgoda!', 'Tak! Bić!'],
    disagreement: ['Nie! Walka!', 'Głupi!', 'Bić cię!'],
    style: 'primitive',
    accent: 'orcish'
  }
}

export const ConversationSystem = ({ isVisible, onClose }) => {
  const [activeConversations, setActiveConversations] = useState([])
  const [selectedTopic, setSelectedTopic] = useState(null)
  const [userMessage, setUserMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [conversationHistory, setConversationHistory] = useState([])
  const [participants, setParticipants] = useState([])
  const [audioEnabled, setAudioEnabled] = useState(true)
  const [showTopicSelector, setShowTopicSelector] = useState(false)
  
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  
  const { agents, tavern } = useAppStore()
  const { send, subscribe } = useWebSocketStore()

  // Subscribe to conversation updates
  useEffect(() => {
    subscribe('conversations')
    subscribe('agent_actions')
  }, [subscribe])

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [conversationHistory])

  // Handle incoming conversation messages
  const handleConversationMessage = useCallback((message) => {
    const newMessage = {
      id: Date.now(),
      speaker: message.speaker,
      content: message.message,
      emotion: message.emotion || 'neutral',
      timestamp: new Date(message.timestamp),
      type: 'agent'
    }
    
    setConversationHistory(prev => [...prev, newMessage])
    
    // Play sound effect
    if (audioEnabled) {
      playMessageSound(message.emotion)
    }
  }, [audioEnabled])

  // Start conversation with selected topic
  const startConversation = async (topic) => {
    if (participants.length < 2) {
      toast.error('Wybierz co najmniej 2 postacie do rozmowy')
      return
    }

    const topicData = ConversationTopics[topic]
    const randomTopic = topicData.topics[Math.floor(Math.random() * topicData.topics.length)]

    try {
      send({
        type: 'start_conversation',
        data: {
          participants: participants.map(p => p.name),
          topic: randomTopic,
          category: topic,
          user_participating: true
        }
      })

      setSelectedTopic({ ...topicData, specificTopic: randomTopic })
      setShowTopicSelector(false)
      toast.success(`Rozpoczęto rozmowę o: ${randomTopic}`)
      
    } catch (error) {
      toast.error('Błąd podczas rozpoczynania rozmowy')
    }
  }

  // Send user message
  const sendUserMessage = async () => {
    if (!userMessage.trim() || !selectedTopic) return

    const message = {
      id: Date.now(),
      speaker: 'Użytkownik',
      content: userMessage,
      emotion: 'neutral',
      timestamp: new Date(),
      type: 'user'
    }

    setConversationHistory(prev => [...prev, message])
    
    // Send to backend
    send({
      type: 'user_message',
      data: {
        message: userMessage,
        topic: selectedTopic.specificTopic,
        participants: participants.map(p => p.name)
      }
    })

    setUserMessage('')
    setIsTyping(true)

    // Simulate agent responses
    setTimeout(() => {
      generateAgentResponse(message)
      setIsTyping(false)
    }, 1000 + Math.random() * 2000)
  }

  // Generate agent response based on faction and topic
  const generateAgentResponse = (userMessage) => {
    if (participants.length === 0) return

    const respondingAgent = participants[Math.floor(Math.random() * participants.length)]
    const faction = respondingAgent.faction || 'Empire'
    const style = FactionConversationStyles[faction] || FactionConversationStyles.Empire

    // Generate contextual response
    let response = generateContextualResponse(userMessage.content, faction, selectedTopic)
    
    const agentMessage = {
      id: Date.now() + 1,
      speaker: respondingAgent.name,
      content: response,
      emotion: getEmotionFromFaction(faction),
      timestamp: new Date(),
      type: 'agent',
      faction: faction
    }

    setConversationHistory(prev => [...prev, agentMessage])
  }

  // Generate contextual response based on faction and topic
  const generateContextualResponse = (userMessage, faction, topic) => {
    const style = FactionConversationStyles[faction]
    const responses = {
      Empire: [
        `W imię Sigmara, ${userMessage.toLowerCase().includes('wojna') ? 'musimy bronić Imperium!' : 'to ważna sprawa.'}`,
        `Jako lojalny obywatel Imperium, ${userMessage.toLowerCase().includes('handel') ? 'popieram uczciwy handel.' : 'zgadzam się z tym.'}`,
        `Sigmar nas prowadzi w ${topic?.name.toLowerCase() || 'tej sprawie'}.`
      ],
      Chaos: [
        `Krew i czaszki! ${userMessage.toLowerCase().includes('walka') ? 'Khorne będzie zadowolony!' : 'Chaos zatryumfuje!'}`,
        `Mroczne Moce szepczą o ${topic?.name.toLowerCase() || 'zniszczeniu'}...`,
        `Słabość! ${userMessage.toLowerCase().includes('pokój') ? 'Tylko wojna ma znaczenie!' : 'Tylko silni przetrwają!'}`
      ],
      HighElves: [
        `Młodsze rasy nie rozumieją ${topic?.name.toLowerCase() || 'tej kwestii'} tak jak my, elfy.`,
        `W naszej pradawnej mądrości widzimy, że ${userMessage.toLowerCase().includes('magia') ? 'magia wymaga ostrożności.' : 'to oczywiste.'}`,
        `Asuryan pokazał nam prawdę o ${topic?.name.toLowerCase() || 'tym wszystkim'}.`
      ],
      Dwarfs: [
        `Baruk Khazâd! ${userMessage.toLowerCase().includes('handel') ? 'Uczciwy handel to podstawa!' : 'Przodkowie by się zgodzili!'}`,
        `To idzie do Księgi Pamiątek jako ${topic?.name.toLowerCase() || 'ważna sprawa'}.`,
        `Młot i kowadło! ${userMessage.toLowerCase().includes('wojna') ? 'Pokażemy im krasnoludzką stal!' : 'Solidnie powiedziane!'}`
      ],
      Orcs: [
        `Waaagh! ${userMessage.toLowerCase().includes('walka') ? 'Więcej walki!' : 'Nudne gadanie!'}`,
        `Ja lubić ${topic?.name.toLowerCase() || 'bić rzeczy'}!`,
        `Głupi ${userMessage.toLowerCase().includes('pokój') ? 'pokój! Tylko walka!' : 'gadanie! Waaagh!'}`
      ]
    }

    const factionResponses = responses[faction] || responses.Empire
    return factionResponses[Math.floor(Math.random() * factionResponses.length)]
  }

  // Get emotion based on faction
  const getEmotionFromFaction = (faction) => {
    const emotions = {
      Empire: ['confident', 'noble', 'determined'],
      Chaos: ['aggressive', 'mad', 'violent'],
      HighElves: ['arrogant', 'wise', 'condescending'],
      Dwarfs: ['gruff', 'stubborn', 'proud'],
      Orcs: ['excited', 'aggressive', 'simple']
    }
    
    const factionEmotions = emotions[faction] || emotions.Empire
    return factionEmotions[Math.floor(Math.random() * factionEmotions.length)]
  }

  // Play message sound based on emotion
  const playMessageSound = (emotion) => {
    // This would integrate with Howler.js
    console.log(`🔊 Playing ${emotion} message sound`)
  }

  // Add participant to conversation
  const addParticipant = (agent) => {
    if (participants.find(p => p.name === agent.name)) return
    
    setParticipants(prev => [...prev, agent])
    toast.success(`${agent.name} dołączył do rozmowy`)
  }

  // Remove participant from conversation
  const removeParticipant = (agentName) => {
    setParticipants(prev => prev.filter(p => p.name !== agentName))
    toast.info(`${agentName} opuścił rozmowę`)
  }

  // Get message bubble style based on speaker type and faction
  const getMessageStyle = (message) => {
    if (message.type === 'user') {
      return {
        container: 'ml-auto bg-primary-600 text-white',
        bubble: 'rounded-tl-lg rounded-tr-lg rounded-bl-lg',
        align: 'text-right'
      }
    }

    const factionColors = {
      Empire: 'bg-yellow-400/20 border-yellow-400/50 text-yellow-100',
      Chaos: 'bg-red-400/20 border-red-400/50 text-red-100',
      HighElves: 'bg-green-400/20 border-green-400/50 text-green-100',
      Dwarfs: 'bg-amber-400/20 border-amber-400/50 text-amber-100',
      Orcs: 'bg-green-600/20 border-green-600/50 text-green-100'
    }

    return {
      container: `mr-auto ${factionColors[message.faction] || factionColors.Empire} border`,
      bubble: 'rounded-tl-lg rounded-tr-lg rounded-br-lg',
      align: 'text-left'
    }
  }

  if (!isVisible) return null

  return (
    <WarhammerGSAPController faction="Empire" animationType="conversation">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ y: 50 }}
          animate={{ y: 0 }}
          className="bg-secondary-800 rounded-lg w-full max-w-4xl h-[80vh] flex flex-col border border-secondary-700"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="p-6 border-b border-secondary-700 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <MessageCircle className="w-8 h-8 text-primary-400" />
              <div>
                <h2 className="text-2xl font-medieval text-white">
                  Rozmowy w Tawernie
                </h2>
                {selectedTopic && (
                  <p className="text-sm text-secondary-300">
                    Temat: {selectedTopic.specificTopic}
                  </p>
                )}
              </div>
            </div>
            
            <div className="flex items-center gap-2">
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
                onClick={() => setShowTopicSelector(!showTopicSelector)}
                className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
              >
                Nowy Temat
              </button>
              
              <button
                onClick={onClose}
                className="p-2 bg-secondary-700 hover:bg-secondary-600 rounded-lg transition-colors text-white"
              >
                ✕
              </button>
            </div>
          </div>

          <div className="flex-1 flex">
            {/* Participants Panel */}
            <div className="w-80 border-r border-secondary-700 p-4">
              <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
                <Users className="w-5 h-5" />
                Uczestnicy ({participants.length})
              </h3>
              
              <div className="space-y-2 mb-4">
                {participants.map((participant) => (
                  <div
                    key={participant.name}
                    className="flex items-center justify-between p-2 bg-secondary-700 rounded-lg"
                  >
                    <div className="flex items-center gap-2">
                      <div className={`w-8 h-8 rounded-full bg-gradient-to-br ${
                        participant.faction === 'Empire' ? 'from-yellow-400 to-yellow-600' :
                        participant.faction === 'Chaos' ? 'from-red-600 to-red-800' :
                        participant.faction === 'HighElves' ? 'from-green-400 to-green-600' :
                        participant.faction === 'Dwarfs' ? 'from-amber-400 to-amber-600' :
                        'from-green-600 to-green-800'
                      } flex items-center justify-center text-white text-sm font-bold`}>
                        {participant.name.charAt(0)}
                      </div>
                      <span className="text-white text-sm">{participant.name}</span>
                    </div>
                    <button
                      onClick={() => removeParticipant(participant.name)}
                      className="text-red-400 hover:text-red-300 text-sm"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>

              <div className="space-y-2">
                <h4 className="text-sm font-semibold text-secondary-300">Dodaj uczestnika:</h4>
                {agents.filter(agent => agent.active && !participants.find(p => p.name === agent.name)).map((agent) => (
                  <button
                    key={agent.name}
                    onClick={() => addParticipant(agent)}
                    className="w-full text-left p-2 bg-secondary-700/50 hover:bg-secondary-700 rounded-lg transition-colors text-white text-sm"
                  >
                    {agent.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Main Conversation Area */}
            <div className="flex-1 flex flex-col">
              {/* Topic Selector */}
              <AnimatePresence>
                {showTopicSelector && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="border-b border-secondary-700 p-4"
                  >
                    <h4 className="font-semibold text-white mb-3">Wybierz temat rozmowy:</h4>
                    <div className="grid grid-cols-3 gap-2">
                      {Object.entries(ConversationTopics).map(([key, topic]) => (
                        <button
                          key={key}
                          onClick={() => startConversation(key)}
                          className={`p-3 rounded-lg border transition-colors ${topic.color} bg-secondary-700/50 hover:bg-secondary-700 border-secondary-600`}
                        >
                          <div className="text-2xl mb-1">{topic.icon}</div>
                          <div className="text-sm font-semibold">{topic.name}</div>
                        </button>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <AnimatePresence>
                  {conversationHistory.map((message) => {
                    const style = getMessageStyle(message)
                    return (
                      <motion.div
                        key={message.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className={`max-w-xs ${style.container} p-3 ${style.bubble} ${style.align}`}
                      >
                        <div className="font-semibold text-xs mb-1 opacity-80">
                          {message.speaker}
                        </div>
                        <div className="text-sm">
                          {message.content}
                        </div>
                        <div className="text-xs opacity-60 mt-1">
                          {message.timestamp.toLocaleTimeString()}
                        </div>
                      </motion.div>
                    )
                  })}
                </AnimatePresence>
                
                {isTyping && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="flex items-center gap-2 text-secondary-400"
                  >
                    <div className="flex gap-1">
                      {[0, 1, 2].map((i) => (
                        <motion.div
                          key={i}
                          className="w-2 h-2 bg-secondary-400 rounded-full"
                          animate={{ scale: [1, 1.2, 1] }}
                          transition={{ duration: 1, repeat: Infinity, delay: i * 0.2 }}
                        />
                      ))}
                    </div>
                    <span className="text-sm">Ktoś pisze...</span>
                  </motion.div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Message Input */}
              {selectedTopic && (
                <div className="border-t border-secondary-700 p-4">
                  <div className="flex gap-2">
                    <input
                      ref={inputRef}
                      type="text"
                      value={userMessage}
                      onChange={(e) => setUserMessage(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && sendUserMessage()}
                      placeholder="Napisz swoją wiadomość..."
                      className="flex-1 bg-secondary-700 border border-secondary-600 rounded-lg px-4 py-2 text-white placeholder-secondary-400 focus:outline-none focus:border-primary-400"
                    />
                    <button
                      onClick={sendUserMessage}
                      disabled={!userMessage.trim()}
                      className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-secondary-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors flex items-center gap-2"
                    >
                      <Send className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </motion.div>
    </WarhammerGSAPController>
  )
}
