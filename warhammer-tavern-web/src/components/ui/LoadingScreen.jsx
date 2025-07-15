import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { gsap } from 'gsap'

// Warhammer Fantasy loading quotes with lore
const WarhammerQuotes = [
  {
    text: "Sigmar chroni!",
    author: "Modlitwa Imperium",
    lore: "Sigmar Heldenhammer to założyciel i patron Imperium"
  },
  {
    text: "Krew dla Boga Krwi! Czaszki dla Tronu Czaszek!",
    author: "Wyznawcy Khorne'a",
    lore: "Khorne to jeden z czterech Bogów Chaosu, Bog Krwi i Wojny"
  },
  {
    text: "Asuryan nas prowadzi, Khaine nas wzmacnia",
    author: "Modlitwa Wysokich Elfów",
    lore: "Asuryan to Król Bogów elfów, Khaine to Bog Wojny"
  },
  {
    text: "Grudge settled, honor restored",
    author: "Przysłowie krasnoludzkie",
    lore: "Krasnoludzi prowadzą Księgę Krzywd, zapisując wszystkie zniewagi"
  },
  {
    text: "Waaagh! jest życiem, życie jest Waaagh!",
    author: "Filozofia orków",
    lore: "Waaagh! to orkowy sposób na wojnę i życie"
  },
  {
    text: "Śmierć nie jest końcem, lecz początkiem",
    author: "Nekromanta",
    lore: "Nekromancja pozwala na powrót z zaświatów"
  },
  {
    text: "Magia jest narzędziem, nie panem",
    author: "Nauki Kolegium Magów",
    lore: "Kolegium Magów w Altdorfie szkoli magów Imperium"
  },
  {
    text: "W cieniu lasu, prawda się ukrywa",
    author: "Mądrość Elfów Leśnych",
    lore: "Athel Loren to magiczny las, dom Elfów Leśnych"
  }
]

// Loading stages with Warhammer theme
const LoadingStages = [
  { text: "Rozpalanie kominka...", progress: 10 },
  { text: "Przygotowywanie ale...", progress: 20 },
  { text: "Sprawdzanie reputacji tawerny...", progress: 30 },
  { text: "Wyczyszczenie stołów...", progress: 40 },
  { text: "Inicjalizacja agentów CrewAI...", progress: 50 },
  { text: "Ładowanie frakcji...", progress: 60 },
  { text: "Ustanawianie relacji między postaciami...", progress: 70 },
  { text: "Generowanie wydarzeń...", progress: 80 },
  { text: "Synchronizacja z serwerem...", progress: 90 },
  { text: "Otwieranie drzwi tawerny...", progress: 100 }
]

const LoadingScreen = ({ message = "Ładowanie tawerny..." }) => {
  const [currentStage, setCurrentStage] = useState(0)
  const [currentQuote, setCurrentQuote] = useState(0)
  const [showQuote, setShowQuote] = useState(true)
  const [progress, setProgress] = useState(0)

  // Cycle through loading stages
  useEffect(() => {
    const stageInterval = setInterval(() => {
      setCurrentStage(prev => {
        const nextStage = (prev + 1) % LoadingStages.length
        setProgress(LoadingStages[nextStage].progress)
        return nextStage
      })
    }, 800)

    return () => clearInterval(stageInterval)
  }, [])

  // Cycle through quotes
  useEffect(() => {
    const quoteInterval = setInterval(() => {
      setShowQuote(false)
      setTimeout(() => {
        setCurrentQuote(prev => (prev + 1) % WarhammerQuotes.length)
        setShowQuote(true)
      }, 300)
    }, 4000)

    return () => clearInterval(quoteInterval)
  }, [])

  // Animate progress bar
  useEffect(() => {
    gsap.to('.progress-fill', {
      width: `${progress}%`,
      duration: 0.8,
      ease: "power2.out"
    })
  }, [progress])

  const quote = WarhammerQuotes[currentQuote]
  const stage = LoadingStages[currentStage]

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-tavern-shadow via-secondary-900 to-secondary-800 flex items-center justify-center">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-tavern-pattern opacity-10"></div>
      
      {/* Fireplace Glow Effect */}
      <div className="absolute bottom-10 left-10 w-32 h-32 bg-fire-glow rounded-full opacity-30 animate-flicker"></div>
      <div className="absolute top-20 right-20 w-24 h-24 bg-fire-glow rounded-full opacity-20 animate-flicker" style={{ animationDelay: '1s' }}></div>

      <div className="relative z-10 max-w-2xl w-full mx-auto p-8 text-center">
        {/* Main Logo/Title */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="mb-12"
        >
          <div className="text-8xl mb-4 animate-float">🏰</div>
          <h1 className="text-4xl md:text-6xl font-medieval text-primary-400 mb-4 text-glow">
            Warhammer Fantasy
          </h1>
          <h2 className="text-2xl md:text-3xl font-medieval text-secondary-300">
            Tavern Simulator
          </h2>
        </motion.div>

        {/* Loading Progress */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          className="mb-8"
        >
          <div className="bg-secondary-800/80 rounded-lg p-6 backdrop-blur-sm border border-secondary-700">
            <div className="mb-4">
              <p className="text-lg text-white font-semibold mb-2">
                {stage.text}
              </p>
              <div className="w-full bg-secondary-700 rounded-full h-3 overflow-hidden">
                <div 
                  className="progress-fill h-full bg-gradient-to-r from-primary-500 to-primary-400 rounded-full transition-all duration-300"
                  style={{ width: '0%' }}
                ></div>
              </div>
              <div className="flex justify-between items-center mt-2">
                <span className="text-sm text-secondary-400">
                  Postęp: {progress}%
                </span>
                <span className="text-sm text-secondary-400">
                  Etap {currentStage + 1}/{LoadingStages.length}
                </span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Warhammer Quote */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1, duration: 0.8 }}
          className="mb-8"
        >
          <div className="bg-secondary-800/60 rounded-lg p-6 backdrop-blur-sm border border-secondary-700/50">
            <AnimatePresence mode="wait">
              {showQuote && (
                <motion.div
                  key={currentQuote}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.3 }}
                >
                  <blockquote className="text-lg text-primary-300 font-medieval italic mb-3">
                    "{quote.text}"
                  </blockquote>
                  <cite className="text-sm text-secondary-400">
                    — {quote.author}
                  </cite>
                  <p className="text-xs text-secondary-500 mt-2 italic">
                    {quote.lore}
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>

        {/* Loading Animation */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 0.5 }}
          className="flex justify-center items-center gap-2"
        >
          <div className="flex gap-1">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="w-3 h-3 bg-primary-400 rounded-full"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.5, 1, 0.5]
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: i * 0.2
                }}
              />
            ))}
          </div>
          <span className="text-secondary-400 ml-4 font-medieval">
            Przygotowywanie doświadczenia...
          </span>
        </motion.div>

        {/* Faction Icons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2, duration: 1 }}
          className="mt-12 flex justify-center gap-8 flex-wrap"
        >
          {[
            { icon: '👑', name: 'Imperium', color: 'text-yellow-400' },
            { icon: '⚔️', name: 'Chaos', color: 'text-red-400' },
            { icon: '🏹', name: 'Elfy', color: 'text-green-400' },
            { icon: '🔨', name: 'Krasnoludzi', color: 'text-amber-400' },
            { icon: '💀', name: 'Nieumarli', color: 'text-purple-400' }
          ].map((faction, index) => (
            <motion.div
              key={faction.name}
              className="flex flex-col items-center"
              animate={{
                y: [0, -5, 0],
                opacity: [0.6, 1, 0.6]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: index * 0.3
              }}
            >
              <div className={`text-3xl mb-2 ${faction.color}`}>
                {faction.icon}
              </div>
              <span className="text-xs text-secondary-400 font-medieval">
                {faction.name}
              </span>
            </motion.div>
          ))}
        </motion.div>

        {/* Version Info */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 2.5, duration: 0.5 }}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <p className="text-xs text-secondary-500">
            Wersja 2.0.0 • Powered by CrewAI & React • {new Date().getFullYear()}
          </p>
        </motion.div>
      </div>

      {/* Ambient Particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-primary-400/30 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -20, 0],
              opacity: [0, 1, 0],
              scale: [0.5, 1, 0.5]
            }}
            transition={{
              duration: 3 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2
            }}
          />
        ))}
      </div>
    </div>
  )
}

export default LoadingScreen
