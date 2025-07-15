import React, { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { MessageCircle, Volume2, VolumeX } from 'lucide-react'
import { gsap } from 'gsap'

// Warhammer Fantasy speech patterns and expressions
const FactionExpressions = {
  Empire: {
    thinking: ['Hmm...', 'W imię Sigmara...', 'Zastanówmy się...', 'Ciekawe...'],
    agreement: ['Zgoda!', 'Tak jest!', 'Sigmar was błogosławi!', 'Mądrze!'],
    disagreement: ['Nie!', 'To błąd!', 'Sigmar by nie pochwalił!', 'Sprzeciwiam się!'],
    surprise: ['Co?!', 'Niemożliwe!', 'Sigmar nas strzeże!', 'Nie do wiary!'],
    anger: ['Hańba!', 'To oburzające!', 'W imię Sigmara!', 'Nie toleruję tego!'],
    joy: ['Wspaniale!', 'Chwała Sigmarowi!', 'Doskonale!', 'Radość!'],
    fear: ['Sigmar nas ochroni!', 'To straszne!', 'Boję się!', 'Pomocy!']
  },
  
  Chaos: {
    thinking: ['Krew...', 'Zniszczenie...', 'Chaos szepcze...', 'Mroczne wizje...'],
    agreement: ['Tak! Śmierć!', 'Krew i czaszki!', 'Chaos zatryumfuje!', 'Zniszczenie!'],
    disagreement: ['Słabość!', 'Zdrajca!', 'Śmierć!', 'Krew za to!'],
    surprise: ['Co?! Krew!', 'Niemożliwe!', 'Chaos!', 'Szaleństwo!'],
    anger: ['KREW!', 'ŚMIERĆ!', 'KHORNE!', 'ZABIĆ!'],
    joy: ['Krew płynie!', 'Czaszki!', 'Chwała Khorne!', 'Śmierć wreszcie!'],
    fear: ['Nie... słabość...', 'Chaos mnie opuszcza...', 'Strach...', 'Pomocy...']
  },
  
  HighElves: {
    thinking: ['Rozważmy to...', 'Mądrość wieków...', 'Asuryan pokazuje...', 'Pradawna wiedza...'],
    agreement: ['Oczywiście', 'Jak przewidywałem', 'Mądrze zauważone', 'Zgoda'],
    disagreement: ['Błędne', 'Typowe dla młodszych ras', 'Nie rozumiecie', 'Mylicie się'],
    surprise: ['Ciekawe...', 'Nieoczekiwane', 'To nowe', 'Zaskakujące'],
    anger: ['Niedopuszczalne!', 'Barbarzyństwo!', 'Hańba!', 'Oburzające!'],
    joy: ['Doskonale', 'Jak należy', 'Właściwie', 'Satysfakcjonujące'],
    fear: ['Asuryan nas strzeże', 'To niepokojące', 'Niebezpieczeństwo', 'Ostrożnie']
  },
  
  Dwarfs: {
    thinking: ['Hmm, aye...', 'Przodkowie mówią...', 'Zastanówmy się...', 'Baruk Khazâd...'],
    agreement: ['Aye!', 'Prawda!', 'Solidnie!', 'Tak mówią przodkowie!'],
    disagreement: ['Nie!', 'Bzdury!', 'To idzie do Księgi!', 'Hańba!'],
    surprise: ['Co?!', 'Baruk Khazâd!', 'Niemożliwe!', 'Przodkowie!'],
    anger: ['Grudge!', 'Do Księgi!', 'Hańba!', 'Zemsta!'],
    joy: ['Aye! Dobrze!', 'Khazad ai-mênu!', 'Wspaniale!', 'Chwała przodkom!'],
    fear: ['Przodkowie...', 'Niebezpieczeństwo!', 'Ostrożnie!', 'Khazad-dûm!']
  },
  
  Orcs: {
    thinking: ['Ugh...', 'Myśleć trudno...', 'Waaagh?', 'Hmm... walka?'],
    agreement: ['Da! Waaagh!', 'Tak! Bić!', 'Dobry!', 'Waaagh zgoda!'],
    disagreement: ['Nie! Głupi!', 'Bić cię!', 'Zły!', 'Waaagh nie!'],
    surprise: ['Co?! Waaagh!', 'Dziwne!', 'Nie rozumieć!', 'Waaagh?!'],
    anger: ['WAAAGH!', 'BIĆ!', 'WALKA!', 'ZABIĆ!'],
    joy: ['Waaagh! Dobrze!', 'Walka!', 'Bić rzeczy!', 'Waaagh szczęśliwy!'],
    fear: ['Strach...', 'Uciekać!', 'Nie walczyć!', 'Pomocy!']
  }
}

// Emotion-based bubble styles
const EmotionStyles = {
  thinking: {
    bgColor: 'bg-blue-400/20',
    borderColor: 'border-blue-400/50',
    textColor: 'text-blue-100',
    icon: '🤔',
    animation: 'float'
  },
  agreement: {
    bgColor: 'bg-green-400/20',
    borderColor: 'border-green-400/50',
    textColor: 'text-green-100',
    icon: '👍',
    animation: 'bounce'
  },
  disagreement: {
    bgColor: 'bg-red-400/20',
    borderColor: 'border-red-400/50',
    textColor: 'text-red-100',
    icon: '👎',
    animation: 'shake'
  },
  surprise: {
    bgColor: 'bg-yellow-400/20',
    borderColor: 'border-yellow-400/50',
    textColor: 'text-yellow-100',
    icon: '😲',
    animation: 'scale'
  },
  anger: {
    bgColor: 'bg-red-600/30',
    borderColor: 'border-red-600/70',
    textColor: 'text-red-100',
    icon: '😠',
    animation: 'shake-intense'
  },
  joy: {
    bgColor: 'bg-yellow-300/20',
    borderColor: 'border-yellow-300/50',
    textColor: 'text-yellow-100',
    icon: '😊',
    animation: 'bounce-happy'
  },
  fear: {
    bgColor: 'bg-purple-400/20',
    borderColor: 'border-purple-400/50',
    textColor: 'text-purple-100',
    icon: '😨',
    animation: 'tremble'
  },
  neutral: {
    bgColor: 'bg-gray-400/20',
    borderColor: 'border-gray-400/50',
    textColor: 'text-gray-100',
    icon: '💬',
    animation: 'float'
  }
}

export const ConversationBubbles = ({ characters, activeConversations, onBubbleClick }) => {
  const [bubbles, setBubbles] = useState([])
  const [audioEnabled, setAudioEnabled] = useState(true)
  const bubblesRef = useRef({})

  // Generate random conversation bubbles
  useEffect(() => {
    const interval = setInterval(() => {
      if (characters.length > 0 && Math.random() < 0.3) {
        generateRandomBubble()
      }
    }, 3000 + Math.random() * 5000) // Random interval between 3-8 seconds

    return () => clearInterval(interval)
  }, [characters])

  // Clean up old bubbles
  useEffect(() => {
    const cleanup = setInterval(() => {
      setBubbles(prev => prev.filter(bubble => 
        Date.now() - bubble.timestamp < 10000 // Remove bubbles older than 10 seconds
      ))
    }, 1000)

    return () => clearInterval(cleanup)
  }, [])

  const generateRandomBubble = () => {
    if (characters.length === 0) return

    const character = characters[Math.floor(Math.random() * characters.length)]
    const faction = character.faction || 'Empire'
    const emotions = Object.keys(FactionExpressions[faction] || FactionExpressions.Empire)
    const emotion = emotions[Math.floor(Math.random() * emotions.length)]
    
    const expressions = FactionExpressions[faction]?.[emotion] || FactionExpressions.Empire[emotion]
    const expression = expressions[Math.floor(Math.random() * expressions.length)]

    const bubble = {
      id: Date.now() + Math.random(),
      characterName: character.name,
      faction: faction,
      emotion: emotion,
      text: expression,
      timestamp: Date.now(),
      position: character.position || { x: Math.random() * 100, y: Math.random() * 100 },
      duration: 3000 + Math.random() * 4000 // 3-7 seconds
    }

    setBubbles(prev => [...prev, bubble])

    // Play sound effect
    if (audioEnabled) {
      playBubbleSound(emotion, faction)
    }

    // Auto-remove bubble after duration
    setTimeout(() => {
      setBubbles(prev => prev.filter(b => b.id !== bubble.id))
    }, bubble.duration)
  }

  const playBubbleSound = (emotion, faction) => {
    // This would integrate with Howler.js for faction-specific sounds
    console.log(`🔊 Playing ${faction} ${emotion} sound`)
  }

  // Animate bubble entrance
  const animateBubbleEntrance = (bubbleElement, emotion) => {
    if (!bubbleElement) return

    const style = EmotionStyles[emotion] || EmotionStyles.neutral

    switch (style.animation) {
      case 'bounce':
        gsap.fromTo(bubbleElement, 
          { scale: 0, y: 20 },
          { scale: 1, y: 0, duration: 0.5, ease: "bounce.out" }
        )
        break
      
      case 'shake':
        gsap.fromTo(bubbleElement,
          { scale: 0, rotation: -5 },
          { scale: 1, rotation: 0, duration: 0.3, ease: "power2.out" }
        )
        gsap.to(bubbleElement, {
          x: "+=2",
          duration: 0.1,
          repeat: 5,
          yoyo: true,
          ease: "power2.inOut"
        })
        break
      
      case 'scale':
        gsap.fromTo(bubbleElement,
          { scale: 0 },
          { scale: 1.1, duration: 0.2, ease: "power2.out" }
        )
        gsap.to(bubbleElement, {
          scale: 1,
          duration: 0.3,
          ease: "elastic.out(1, 0.3)"
        })
        break
      
      case 'shake-intense':
        gsap.fromTo(bubbleElement,
          { scale: 0, rotation: -10 },
          { scale: 1, rotation: 0, duration: 0.3, ease: "power2.out" }
        )
        gsap.to(bubbleElement, {
          x: "+=4",
          rotation: "+=2",
          duration: 0.08,
          repeat: 8,
          yoyo: true,
          ease: "power2.inOut"
        })
        break
      
      case 'bounce-happy':
        gsap.fromTo(bubbleElement,
          { scale: 0, y: 30 },
          { scale: 1, y: 0, duration: 0.6, ease: "bounce.out" }
        )
        gsap.to(bubbleElement, {
          y: "-=5",
          duration: 0.5,
          repeat: -1,
          yoyo: true,
          ease: "sine.inOut"
        })
        break
      
      case 'tremble':
        gsap.fromTo(bubbleElement,
          { scale: 0, opacity: 0 },
          { scale: 1, opacity: 1, duration: 0.4, ease: "power2.out" }
        )
        gsap.to(bubbleElement, {
          x: "+=1",
          y: "+=1",
          duration: 0.05,
          repeat: -1,
          yoyo: true,
          ease: "none"
        })
        break
      
      default: // float
        gsap.fromTo(bubbleElement,
          { scale: 0, y: 10, opacity: 0 },
          { scale: 1, y: 0, opacity: 1, duration: 0.4, ease: "power2.out" }
        )
        gsap.to(bubbleElement, {
          y: "-=3",
          duration: 2,
          repeat: -1,
          yoyo: true,
          ease: "sine.inOut"
        })
    }
  }

  // Handle bubble click
  const handleBubbleClick = (bubble) => {
    if (onBubbleClick) {
      onBubbleClick(bubble)
    }
    
    // Remove clicked bubble
    setBubbles(prev => prev.filter(b => b.id !== bubble.id))
  }

  return (
    <div className="absolute inset-0 pointer-events-none">
      {/* Audio Control */}
      <div className="absolute top-4 right-4 pointer-events-auto">
        <button
          onClick={() => setAudioEnabled(!audioEnabled)}
          className="p-2 bg-secondary-800/80 hover:bg-secondary-700 rounded-lg transition-colors backdrop-blur-sm border border-secondary-600"
        >
          {audioEnabled ? (
            <Volume2 className="w-4 h-4 text-white" />
          ) : (
            <VolumeX className="w-4 h-4 text-white" />
          )}
        </button>
      </div>

      {/* Conversation Bubbles */}
      <AnimatePresence>
        {bubbles.map((bubble) => {
          const style = EmotionStyles[bubble.emotion] || EmotionStyles.neutral
          
          return (
            <motion.div
              key={bubble.id}
              ref={el => {
                if (el && !bubblesRef.current[bubble.id]) {
                  bubblesRef.current[bubble.id] = el
                  animateBubbleEntrance(el, bubble.emotion)
                }
              }}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0 }}
              className="absolute pointer-events-auto cursor-pointer"
              style={{
                left: `${bubble.position.x}%`,
                top: `${bubble.position.y}%`,
                transform: 'translate(-50%, -100%)'
              }}
              onClick={() => handleBubbleClick(bubble)}
            >
              {/* Speech Bubble */}
              <div className={`
                relative max-w-xs p-3 rounded-lg border backdrop-blur-sm
                ${style.bgColor} ${style.borderColor} ${style.textColor}
                hover:scale-105 transition-transform duration-200
              `}>
                {/* Bubble Content */}
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{style.icon}</span>
                  <span className="text-xs font-semibold opacity-80">
                    {bubble.characterName}
                  </span>
                </div>
                
                <div className="text-sm font-medieval">
                  {bubble.text}
                </div>

                {/* Faction Indicator */}
                <div className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-gradient-to-br opacity-80 flex items-center justify-center text-xs">
                  {bubble.faction === 'Empire' && '👑'}
                  {bubble.faction === 'Chaos' && '💀'}
                  {bubble.faction === 'HighElves' && '🌟'}
                  {bubble.faction === 'Dwarfs' && '🔨'}
                  {bubble.faction === 'Orcs' && '⚔️'}
                </div>

                {/* Speech Bubble Tail */}
                <div className={`
                  absolute top-full left-1/2 transform -translate-x-1/2
                  w-0 h-0 border-l-4 border-r-4 border-t-8 border-transparent
                  ${style.borderColor.replace('border-', 'border-t-').replace('/50', '')}
                `}></div>
              </div>

              {/* Ripple Effect on Hover */}
              <div className="absolute inset-0 rounded-lg opacity-0 hover:opacity-20 bg-white transition-opacity duration-200"></div>
            </motion.div>
          )
        })}
      </AnimatePresence>

      {/* Active Conversation Indicators */}
      {activeConversations.map((conversation) => (
        <div
          key={conversation.id}
          className="absolute pointer-events-auto"
          style={{
            left: `${conversation.position?.x || 50}%`,
            top: `${conversation.position?.y || 50}%`,
            transform: 'translate(-50%, -50%)'
          }}
        >
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.7, 1, 0.7]
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="w-8 h-8 bg-primary-400/30 rounded-full flex items-center justify-center border-2 border-primary-400/50"
          >
            <MessageCircle className="w-4 h-4 text-primary-400" />
          </motion.div>
        </div>
      ))}
    </div>
  )
}
