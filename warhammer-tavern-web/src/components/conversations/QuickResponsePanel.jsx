import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ThumbsUp, ThumbsDown, Heart, Zap, Sword, Crown, Coins, Shield } from 'lucide-react'

// Warhammer Fantasy quick responses by category
const QuickResponses = {
  agreement: {
    icon: ThumbsUp,
    color: 'text-green-400',
    bgColor: 'bg-green-400/20',
    borderColor: 'border-green-400/50',
    responses: {
      Empire: [
        'Sigmar was błogosławi za te mądre słowa!',
        'Zgadzam się w pełni, obywatelu!',
        'To prawda godna Imperium!',
        'Mądrze powiedziane!'
      ],
      Chaos: [
        'Tak! Niech płynie krew!',
        'Chaos zatryumfuje!',
        'Śmierć i zniszczenie!',
        'Krew dla Boga Krwi!'
      ],
      HighElves: [
        'Oczywiście, jak przewidywałem',
        'Mądrość wieków potwierdza',
        'Zgoda, choć oczywiste',
        'Asuryan pokazuje prawdę'
      ],
      Dwarfs: [
        'Aye! Solidnie powiedziane!',
        'Przodkowie by się zgodzili!',
        'Baruk Khazâd! Prawda!',
        'To idzie do Księgi Pamiątek!'
      ],
      Orcs: [
        'Da! Waaagh zgoda!',
        'Dobry! Lubić!',
        'Tak! Bić razem!',
        'Waaagh! Prawda!'
      ]
    }
  },
  
  disagreement: {
    icon: ThumbsDown,
    color: 'text-red-400',
    bgColor: 'bg-red-400/20',
    borderColor: 'border-red-400/50',
    responses: {
      Empire: [
        'Sigmar by tego nie pochwalił!',
        'Sprzeciwiam się w imię Imperium!',
        'To nie jest właściwe!',
        'Nie mogę się z tym zgodzić!'
      ],
      Chaos: [
        'Słabość! Śmierć!',
        'Zdrajca! Krew za to!',
        'Khorne żąda krwi!',
        'Zniszczenie heretykom!'
      ],
      HighElves: [
        'Błędne myślenie młodszych ras',
        'Nie rozumiecie prawdy',
        'Typowe dla śmiertelników',
        'Asuryan pokazuje inaczej'
      ],
      Dwarfs: [
        'Bzdury! To idzie do Księgi!',
        'Hańba! Przodkowie się obrażają!',
        'Grudge! Zemsta!',
        'Nie! Baruk Khazâd!'
      ],
      Orcs: [
        'Nie! Głupi!',
        'Bić cię za to!',
        'Waaagh nie zgoda!',
        'Zły! Walka!'
      ]
    }
  },
  
  support: {
    icon: Heart,
    color: 'text-pink-400',
    bgColor: 'bg-pink-400/20',
    borderColor: 'border-pink-400/50',
    responses: {
      Empire: [
        'Sigmar was wspiera w trudach!',
        'Imperium stoi za wami!',
        'Jesteście prawdziwymi bohaterami!',
        'Chwała waszej odwadze!'
      ],
      Chaos: [
        'Khorne docenia waszą siłę!',
        'Chaos was wzmacnia!',
        'Krew czyni was silniejszymi!',
        'Mroczne Moce was wspierają!'
      ],
      HighElves: [
        'Asuryan was prowadzi',
        'Mądrość elfów z wami',
        'Gwiazdy was błogosławią',
        'Pradawna moc was wspiera'
      ],
      Dwarfs: [
        'Przodkowie was błogosławią!',
        'Khazad ai-mênu! Siła!',
        'Młot i kowadło z wami!',
        'Baruk Khazâd! Wsparcie!'
      ],
      Orcs: [
        'Waaagh! Pomagać!',
        'Razem silni!',
        'Waaagh wspiera!',
        'Dobry! Pomagać walka!'
      ]
    }
  },
  
  challenge: {
    icon: Sword,
    color: 'text-orange-400',
    bgColor: 'bg-orange-400/20',
    borderColor: 'border-orange-400/50',
    responses: {
      Empire: [
        'Wyzywam was na honorowy pojedynek!',
        'W imię Sigmara, stawcie czoła!',
        'Udowodnijcie swoją wartość!',
        'Honor wymaga odpowiedzi!'
      ],
      Chaos: [
        'Krew! Walka! Teraz!',
        'Khorne żąda pojedynku!',
        'Śmierć lub chwała!',
        'Czaszki dla Tronu Czaszek!'
      ],
      HighElves: [
        'Pokażcie swoją prawdziwą naturę',
        'Czas na próbę charakteru',
        'Asuryan osądzi was',
        'Udowodnijcie swoją wartość'
      ],
      Dwarfs: [
        'Grudge! Pojedynek!',
        'Młot przeciwko młotowi!',
        'Przodkowie będą świadkami!',
        'Baruk Khazâd! Walka!'
      ],
      Orcs: [
        'Waaagh! Walka teraz!',
        'Bić! Bić! Bić!',
        'Kto silniejszy?!',
        'Waaagh pojedynek!'
      ]
    }
  },
  
  trade: {
    icon: Coins,
    color: 'text-amber-400',
    bgColor: 'bg-amber-400/20',
    borderColor: 'border-amber-400/50',
    responses: {
      Empire: [
        'Proponuję korzystny handel!',
        'Imperium oferuje uczciwe ceny!',
        'Sigmar błogosławi uczciwym kupcom!',
        'Zawrzyjmy korzystną umowę!'
      ],
      Chaos: [
        'Dusze za złoto!',
        'Handel krwią i strachem!',
        'Chaos oferuje moc!',
        'Zniszczenie ma swoją cenę!'
      ],
      HighElves: [
        'Oferujemy elfickie rzemiosło',
        'Pradawne skarby do wymiany',
        'Mądrość ma swoją wartość',
        'Asuryan błogosławi uczciwym'
      ],
      Dwarfs: [
        'Gromril najlepszej jakości!',
        'Krasnoludzkie rzemiosło!',
        'Uczciwy handel, uczciwa cena!',
        'Przodkowie uczyli handlu!'
      ],
      Orcs: [
        'Wymiana! Ja dawać!',
        'Dobre rzeczy! Tanio!',
        'Waaagh handel!',
        'Błyszczące za jedzenie!'
      ]
    }
  },
  
  magic: {
    icon: Zap,
    color: 'text-purple-400',
    bgColor: 'bg-purple-400/20',
    borderColor: 'border-purple-400/50',
    responses: {
      Empire: [
        'Sigmar chroni przed Chaosem!',
        'Kolegium Magów was ostrzega!',
        'Magia wymaga ostrożności!',
        'Błogosławieństwo Sigmara!'
      ],
      Chaos: [
        'Warp płynie przez mnie!',
        'Mroczne zaklęcia!',
        'Chaos daje moc!',
        'Magia zniszczenia!'
      ],
      HighElves: [
        'Wysoka Magia przewyższa wszystko',
        'Asuryan daje nam moc',
        'Pradawne zaklęcia',
        'Magia w czystej formie'
      ],
      Dwarfs: [
        'Runy przodków!',
        'Krasnoludzka magia!',
        'Młot i runy!',
        'Starożytne znaki mocy!'
      ],
      Orcs: [
        'Waaagh magia!',
        'Szaman mówi!',
        'Zielona moc!',
        'Waaagh czary!'
      ]
    }
  }
}

// Reaction emojis with Warhammer theme
const ReactionEmojis = [
  { emoji: '⚔️', name: 'walka', color: 'hover:bg-red-400/20' },
  { emoji: '👑', name: 'szlachetność', color: 'hover:bg-yellow-400/20' },
  { emoji: '🔥', name: 'pasja', color: 'hover:bg-orange-400/20' },
  { emoji: '💀', name: 'chaos', color: 'hover:bg-purple-400/20' },
  { emoji: '🛡️', name: 'obrona', color: 'hover:bg-blue-400/20' },
  { emoji: '💰', name: 'bogactwo', color: 'hover:bg-amber-400/20' },
  { emoji: '⚡', name: 'magia', color: 'hover:bg-purple-400/20' },
  { emoji: '🏰', name: 'imperium', color: 'hover:bg-yellow-400/20' }
]

export const QuickResponsePanel = ({ 
  isVisible, 
  onResponse, 
  currentTopic, 
  userFaction = 'Empire',
  onReaction 
}) => {
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [showReactions, setShowReactions] = useState(false)

  // Auto-hide after inactivity
  useEffect(() => {
    if (!isVisible) return

    const timer = setTimeout(() => {
      setSelectedCategory(null)
    }, 10000) // Hide after 10 seconds of inactivity

    return () => clearTimeout(timer)
  }, [isVisible, selectedCategory])

  const handleCategorySelect = (category) => {
    setSelectedCategory(category)
  }

  const handleResponseSelect = (response) => {
    if (onResponse) {
      onResponse({
        text: response,
        category: selectedCategory,
        faction: userFaction,
        timestamp: Date.now()
      })
    }
    setSelectedCategory(null)
  }

  const handleReactionSelect = (reaction) => {
    if (onReaction) {
      onReaction({
        emoji: reaction.emoji,
        name: reaction.name,
        faction: userFaction,
        timestamp: Date.now()
      })
    }
  }

  if (!isVisible) return null

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-40"
    >
      <div className="bg-secondary-800/95 backdrop-blur-sm rounded-lg border border-secondary-700 p-4 shadow-xl">
        <AnimatePresence mode="wait">
          {!selectedCategory ? (
            // Category Selection
            <motion.div
              key="categories"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex items-center gap-3"
            >
              <span className="text-sm text-secondary-300 font-semibold mr-2">
                Szybka odpowiedź:
              </span>
              
              {Object.entries(QuickResponses).map(([key, category]) => {
                const IconComponent = category.icon
                return (
                  <motion.button
                    key={key}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleCategorySelect(key)}
                    className={`
                      p-3 rounded-lg border transition-all duration-200
                      ${category.bgColor} ${category.borderColor}
                      hover:scale-105 hover:shadow-lg
                    `}
                    title={key}
                  >
                    <IconComponent className={`w-5 h-5 ${category.color}`} />
                  </motion.button>
                )
              })}

              {/* Reactions Toggle */}
              <div className="border-l border-secondary-600 pl-3 ml-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowReactions(!showReactions)}
                  className="p-3 rounded-lg bg-secondary-700 hover:bg-secondary-600 transition-colors"
                  title="Reakcje"
                >
                  <span className="text-lg">😊</span>
                </motion.button>
              </div>
            </motion.div>
          ) : (
            // Response Selection
            <motion.div
              key="responses"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="space-y-3"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-secondary-300 font-semibold">
                  Wybierz odpowiedź ({userFaction}):
                </span>
                <button
                  onClick={() => setSelectedCategory(null)}
                  className="text-secondary-400 hover:text-white transition-colors"
                >
                  ← Wróć
                </button>
              </div>

              <div className="grid grid-cols-1 gap-2 max-w-md">
                {QuickResponses[selectedCategory].responses[userFaction]?.map((response, index) => (
                  <motion.button
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleResponseSelect(response)}
                    className={`
                      p-3 text-left rounded-lg border transition-all duration-200
                      ${QuickResponses[selectedCategory].bgColor}
                      ${QuickResponses[selectedCategory].borderColor}
                      hover:shadow-md text-sm
                    `}
                  >
                    <span className={QuickResponses[selectedCategory].color}>
                      {response}
                    </span>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Reaction Panel */}
        <AnimatePresence>
          {showReactions && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="border-t border-secondary-700 pt-3 mt-3"
            >
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs text-secondary-400 mr-2">Reakcje:</span>
                {ReactionEmojis.map((reaction, index) => (
                  <motion.button
                    key={reaction.name}
                    initial={{ opacity: 0, scale: 0 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.05 }}
                    whileHover={{ scale: 1.2 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => handleReactionSelect(reaction)}
                    className={`
                      p-2 rounded-lg transition-all duration-200
                      ${reaction.color} hover:shadow-md
                    `}
                    title={reaction.name}
                  >
                    <span className="text-lg">{reaction.emoji}</span>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Current Topic Indicator */}
        {currentTopic && (
          <div className="border-t border-secondary-700 pt-2 mt-3">
            <span className="text-xs text-secondary-400">
              Temat: <span className="text-secondary-300">{currentTopic}</span>
            </span>
          </div>
        )}
      </div>
    </motion.div>
  )
}
