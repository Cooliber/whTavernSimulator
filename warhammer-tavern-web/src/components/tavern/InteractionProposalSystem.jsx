import React, { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sword, Shield, Scroll, Coins, Skull, Crown, Zap, Users } from 'lucide-react'
import { WarhammerGSAPController } from '../animations/WarhammerGSAPController'
import { useAppStore } from '@stores/appStore'
import { useWebSocketStore } from '@stores/webSocketStore'
import toast from 'react-hot-toast'

// Warhammer Fantasy-specific interaction types
const InteractionTypes = {
  DIPLOMATIC: {
    icon: Crown,
    color: 'text-yellow-400',
    bgColor: 'bg-yellow-400/20',
    borderColor: 'border-yellow-400/50',
    title: 'Dyplomacja',
    description: 'Negocjacje i układy polityczne'
  },
  COMBAT: {
    icon: Sword,
    color: 'text-red-400',
    bgColor: 'bg-red-400/20',
    borderColor: 'border-red-400/50',
    title: 'Walka',
    description: 'Pojedynki i konflikty zbrojne'
  },
  TRADE: {
    icon: Coins,
    color: 'text-amber-400',
    bgColor: 'bg-amber-400/20',
    borderColor: 'border-amber-400/50',
    title: 'Handel',
    description: 'Wymiana towarów i usług'
  },
  MAGIC: {
    icon: Zap,
    color: 'text-purple-400',
    bgColor: 'bg-purple-400/20',
    borderColor: 'border-purple-400/50',
    title: 'Magia',
    description: 'Rzucanie zaklęć i rytuały'
  },
  INTRIGUE: {
    icon: Skull,
    color: 'text-gray-400',
    bgColor: 'bg-gray-400/20',
    borderColor: 'border-gray-400/50',
    title: 'Intryga',
    description: 'Spiski i tajne działania'
  },
  KNOWLEDGE: {
    icon: Scroll,
    color: 'text-blue-400',
    bgColor: 'bg-blue-400/20',
    borderColor: 'border-blue-400/50',
    title: 'Wiedza',
    description: 'Wymiana informacji i nauki'
  },
  ALLIANCE: {
    icon: Users,
    color: 'text-green-400',
    bgColor: 'bg-green-400/20',
    borderColor: 'border-green-400/50',
    title: 'Sojusz',
    description: 'Tworzenie paktów i koalicji'
  },
  DEFENSE: {
    icon: Shield,
    color: 'text-cyan-400',
    bgColor: 'bg-cyan-400/20',
    borderColor: 'border-cyan-400/50',
    title: 'Obrona',
    description: 'Ochrona i fortyfikacje'
  }
}

// Warhammer Fantasy-specific proposals with lore
const WarhammerProposals = {
  Empire: [
    {
      type: 'DIPLOMATIC',
      title: 'Pakt Handlowy z Marienburgiem',
      description: 'Zaproponuj korzystny układ handlowy z bogatymi kupcami z Marienburgiem',
      requirements: ['reputation >= 60', 'wealth >= 1000'],
      rewards: ['wealth +500', 'reputation +10'],
      risks: ['tension +5'],
      lore: 'Marienburg to najbogatsze miasto Starego Świata, kontrolujące handel morski.',
      difficulty: 'medium',
      duration: '2 tygodnie'
    },
    {
      type: 'COMBAT',
      title: 'Pojedynek Honorowy',
      description: 'Wyzwij na pojedynek rycerza z Bretonnii w imię honoru Imperium',
      requirements: ['reputation >= 40'],
      rewards: ['reputation +20', 'honor +15'],
      risks: ['health -20', 'tension +10'],
      lore: 'Rycerze Bretonnii słyną z kodeksu honorowego i mistrzostwa w pojedynkach.',
      difficulty: 'hard',
      duration: '1 dzień'
    },
    {
      type: 'MAGIC',
      title: 'Konsultacja z Kolegium Magów',
      description: 'Skonsultuj się z Kolegium Magów w Altdorfie w sprawie tajemniczych zjawisk',
      requirements: ['knowledge >= 30'],
      rewards: ['knowledge +25', 'magic_power +10'],
      risks: ['wealth -200'],
      lore: 'Kolegium Magów w Altdorfie to najważniejsza instytucja magiczna Imperium.',
      difficulty: 'medium',
      duration: '1 tydzień'
    }
  ],
  
  Chaos: [
    {
      type: 'INTRIGUE',
      title: 'Korupcja Urzędnika',
      description: 'Skorumpuj lokalnego urzędnika, aby służył Ciemnym Bogom',
      requirements: ['corruption >= 20'],
      rewards: ['influence +15', 'corruption +10'],
      risks: ['reputation -15', 'detection_risk +30'],
      lore: 'Chaos szerzy się przez korupcję serc i umysłów śmiertelników.',
      difficulty: 'medium',
      duration: '3 dni'
    },
    {
      type: 'MAGIC',
      title: 'Rytuał Przyzwania Demona',
      description: 'Przeprowadź niebezpieczny rytuał przyzwania mniejszego demona',
      requirements: ['corruption >= 50', 'magic_power >= 40'],
      rewards: ['demon_ally', 'chaos_favor +20'],
      risks: ['sanity -25', 'corruption +15', 'detection_risk +50'],
      lore: 'Demony to istoty z Królestwa Chaosu, potężne ale nieprzewidywalne.',
      difficulty: 'very_hard',
      duration: '1 noc'
    },
    {
      type: 'COMBAT',
      title: 'Atak na Karawanę',
      description: 'Zaatakuj kupiecką karawanę w imię Khorne\'a, Boga Krwi',
      requirements: ['combat_skill >= 35'],
      rewards: ['wealth +300', 'khorne_favor +15'],
      risks: ['reputation -20', 'wanted_level +25'],
      lore: 'Khorne żąda krwi i czaszek, a każda walka to ofiara dla Boga Krwi.',
      difficulty: 'hard',
      duration: '1 dzień'
    }
  ],
  
  HighElves: [
    {
      type: 'KNOWLEDGE',
      title: 'Studiowanie Starożytnych Tekstów',
      description: 'Przebadaj starożytne elfiie teksty w Wieży Hoeth',
      requirements: ['intelligence >= 50', 'knowledge >= 40'],
      rewards: ['knowledge +30', 'ancient_lore +20'],
      risks: ['time -7_days'],
      lore: 'Wieża Hoeth to największa biblioteka Wysokich Elfów, pełna pradawnej wiedzy.',
      difficulty: 'medium',
      duration: '2 tygodnie'
    },
    {
      type: 'MAGIC',
      title: 'Tkanie Wysokiej Magii',
      description: 'Spróbuj opanować zaawansowane techniki Wysokiej Magii',
      requirements: ['magic_power >= 60', 'elven_heritage'],
      rewards: ['high_magic_mastery', 'magic_power +25'],
      risks: ['magical_backlash', 'exhaustion'],
      lore: 'Wysoka Magia to najczystsza forma magii, dostępna tylko Wysokim Elfom.',
      difficulty: 'very_hard',
      duration: '1 miesiąc'
    },
    {
      type: 'DIPLOMATIC',
      title: 'Poselstwo do Dwóru Feniksa',
      description: 'Zostań wysłany jako poseł do Dworu Króla Feniksa w Lothern',
      requirements: ['reputation >= 70', 'diplomacy >= 45'],
      rewards: ['phoenix_king_favor', 'reputation +25'],
      risks: ['court_intrigue', 'political_enemies'],
      lore: 'Dwór Feniksa to serce polityki Wysokich Elfów, pełen intryg i ceremonii.',
      difficulty: 'hard',
      duration: '3 tygodnie'
    }
  ],
  
  Dwarfs: [
    {
      type: 'TRADE',
      title: 'Kontrakt na Gromril',
      description: 'Wynegocjuj kontrakt na dostawy cennego gromrilu z Karak Kadrin',
      requirements: ['reputation >= 50', 'wealth >= 800'],
      rewards: ['gromril_access', 'wealth +400', 'dwarf_favor +20'],
      risks: ['orc_raids', 'transport_costs'],
      lore: 'Gromril to najcenniejszy metal krasnoludzki, twardszy od stali.',
      difficulty: 'medium',
      duration: '1 miesiąc'
    },
    {
      type: 'COMBAT',
      title: 'Obrona Przełęczy',
      description: 'Pomóż krasnoludom obronić górską przełęcz przed atakiem orków',
      requirements: ['combat_skill >= 40', 'loyalty >= 30'],
      rewards: ['dwarf_honor', 'combat_experience +15'],
      risks: ['injury_risk', 'equipment_damage'],
      lore: 'Krasnoludzi nigdy nie zapominają długów wdzięczności ani krzywd.',
      difficulty: 'hard',
      duration: '3 dni'
    },
    {
      type: 'KNOWLEDGE',
      title: 'Nauka Rzemiosła Runicznego',
      description: 'Spróbuj poznać tajniki krasnoludzkich run od Mistrza Runicznego',
      requirements: ['intelligence >= 45', 'dwarf_trust >= 60'],
      rewards: ['runic_knowledge', 'crafting_skill +20'],
      risks: ['dwarf_suspicion', 'guild_politics'],
      lore: 'Runy to starożytna magia krasnoludzka, ściśle strzeżona przez Gildię Runiczną.',
      difficulty: 'very_hard',
      duration: '6 miesięcy'
    }
  ],
  
  Orcs: [
    {
      type: 'COMBAT',
      title: 'Waaagh! na Ludzkie Osady',
      description: 'Poprowadź hordę orków w niszczycielskim Waaagh! przeciwko ludziom',
      requirements: ['strength >= 50', 'orc_leadership >= 30'],
      rewards: ['loot +500', 'orc_respect +25', 'fear_reputation +20'],
      risks: ['human_retaliation', 'casualties'],
      lore: 'Waaagh! to orkowy sposób na wojnę - głośny, brutalny i destrukcyjny.',
      difficulty: 'medium',
      duration: '1 tydzień'
    },
    {
      type: 'ALLIANCE',
      title: 'Zjednoczenie Plemion',
      description: 'Spróbuj zjednoczyć wrogie sobie plemiona orków pod jednym sztandarem',
      requirements: ['charisma >= 35', 'combat_reputation >= 40'],
      rewards: ['orc_army', 'tribal_unity +30'],
      risks: ['tribal_warfare', 'assassination_attempts'],
      lore: 'Orki rzadko współpracują, ale potężny wódz może ich zjednoczyć.',
      difficulty: 'hard',
      duration: '2 tygodnie'
    },
    {
      type: 'INTRIGUE',
      title: 'Sabotaż Krasnoludzkich Kopalni',
      description: 'Infiltruj i sabotuj krasnoludzkie kopalnie, aby osłabić ich gospodarkę',
      requirements: ['stealth >= 25', 'explosives_knowledge >= 20'],
      rewards: ['dwarf_economy_damage', 'orc_favor +15'],
      risks: ['detection', 'dwarf_grudge'],
      lore: 'Orki i krasnoludzi to odwieczni wrogowie, walczący o kontrolę nad górami.',
      difficulty: 'hard',
      duration: '5 dni'
    }
  ]
}

export const InteractionProposalSystem = ({ selectedCharacter, onProposalSelect }) => {
  const [activeProposals, setActiveProposals] = useState([])
  const [selectedProposal, setSelectedProposal] = useState(null)
  const [showDetails, setShowDetails] = useState(false)
  const { agents, tavern } = useAppStore()
  const { send } = useWebSocketStore()

  // Generate faction-specific proposals
  const generateProposals = useCallback(() => {
    if (!selectedCharacter) return

    const characterFaction = selectedCharacter.faction || 'Empire'
    const factionProposals = WarhammerProposals[characterFaction] || WarhammerProposals.Empire
    
    // Filter proposals based on current tavern state and character requirements
    const availableProposals = factionProposals.filter(proposal => {
      return proposal.requirements.every(req => {
        const [stat, operator, value] = req.split(' ')
        const currentValue = tavern[stat] || 0
        
        switch (operator) {
          case '>=': return currentValue >= parseInt(value)
          case '<=': return currentValue <= parseInt(value)
          case '>': return currentValue > parseInt(value)
          case '<': return currentValue < parseInt(value)
          default: return true
        }
      })
    })

    // Add some randomness and limit to 3-5 proposals
    const shuffled = availableProposals.sort(() => 0.5 - Math.random())
    setActiveProposals(shuffled.slice(0, Math.min(5, shuffled.length)))
  }, [selectedCharacter, tavern])

  useEffect(() => {
    generateProposals()
  }, [generateProposals])

  const handleProposalClick = (proposal) => {
    setSelectedProposal(proposal)
    setShowDetails(true)
  }

  const handleAcceptProposal = async (proposal) => {
    try {
      // Send proposal acceptance to backend
      send({
        type: 'accept_proposal',
        data: {
          character: selectedCharacter.name,
          proposal: proposal,
          timestamp: Date.now()
        }
      })

      toast.success(`Zaakceptowano propozycję: ${proposal.title}`)
      
      if (onProposalSelect) {
        onProposalSelect(proposal)
      }
      
      setShowDetails(false)
      setSelectedProposal(null)
      
      // Regenerate proposals after acceptance
      setTimeout(generateProposals, 1000)
      
    } catch (error) {
      toast.error('Błąd podczas akceptacji propozycji')
      console.error('Proposal acceptance error:', error)
    }
  }

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'text-green-400'
      case 'medium': return 'text-yellow-400'
      case 'hard': return 'text-orange-400'
      case 'very_hard': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  const getDifficultyText = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'Łatwe'
      case 'medium': return 'Średnie'
      case 'hard': return 'Trudne'
      case 'very_hard': return 'Bardzo Trudne'
      default: return 'Nieznane'
    }
  }

  if (!selectedCharacter) {
    return (
      <div className="bg-secondary-800/50 rounded-lg p-6 text-center">
        <Scroll className="w-12 h-12 text-secondary-400 mx-auto mb-4" />
        <p className="text-secondary-300">
          Wybierz postać, aby zobaczyć dostępne propozycje interakcji
        </p>
      </div>
    )
  }

  return (
    <WarhammerGSAPController faction={selectedCharacter.faction} animationType="idle">
      <div className="bg-secondary-800/80 rounded-lg p-6 backdrop-blur-sm border border-secondary-700">
        <div className="flex items-center gap-3 mb-6">
          <div className="character-element">
            <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${
              selectedCharacter.faction === 'Empire' ? 'from-yellow-400 to-yellow-600' :
              selectedCharacter.faction === 'Chaos' ? 'from-red-600 to-red-800' :
              selectedCharacter.faction === 'HighElves' ? 'from-green-400 to-green-600' :
              selectedCharacter.faction === 'Dwarfs' ? 'from-amber-400 to-amber-600' :
              'from-green-600 to-green-800'
            } flex items-center justify-center text-white font-bold text-lg`}>
              {selectedCharacter.name.charAt(0)}
            </div>
          </div>
          <div>
            <h3 className="text-xl font-medieval text-primary-400">
              Propozycje dla {selectedCharacter.name}
            </h3>
            <p className="text-secondary-400 text-sm">
              Frakcja: {selectedCharacter.faction} • Dostępne interakcje: {activeProposals.length}
            </p>
          </div>
        </div>

        <div className="space-y-4">
          <AnimatePresence>
            {activeProposals.map((proposal, index) => {
              const InteractionIcon = InteractionTypes[proposal.type].icon
              const interactionConfig = InteractionTypes[proposal.type]
              
              return (
                <motion.div
                  key={`${proposal.title}-${index}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ delay: index * 0.1 }}
                  className={`character-element p-4 rounded-lg border cursor-pointer transition-all duration-300 hover:scale-105 ${
                    interactionConfig.bgColor
                  } ${interactionConfig.borderColor} hover:border-opacity-80`}
                  onClick={() => handleProposalClick(proposal)}
                >
                  <div className="flex items-start gap-4">
                    <div className={`p-2 rounded-lg ${interactionConfig.bgColor}`}>
                      <InteractionIcon className={`w-6 h-6 ${interactionConfig.color}`} />
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-white">{proposal.title}</h4>
                        <span className={`text-xs px-2 py-1 rounded ${getDifficultyColor(proposal.difficulty)} bg-secondary-700`}>
                          {getDifficultyText(proposal.difficulty)}
                        </span>
                      </div>
                      
                      <p className="text-secondary-300 text-sm mb-3">
                        {proposal.description}
                      </p>
                      
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-secondary-400">
                          Czas: {proposal.duration}
                        </span>
                        <span className={`${interactionConfig.color}`}>
                          {interactionConfig.title}
                        </span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </AnimatePresence>
        </div>

        {activeProposals.length === 0 && (
          <div className="text-center py-8">
            <Scroll className="w-16 h-16 text-secondary-400 mx-auto mb-4 opacity-50" />
            <p className="text-secondary-400">
              Brak dostępnych propozycji dla tej postaci
            </p>
            <button
              onClick={generateProposals}
              className="mt-4 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
            >
              Odśwież propozycje
            </button>
          </div>
        )}

        {/* Proposal Details Modal */}
        <AnimatePresence>
          {showDetails && selectedProposal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
              onClick={() => setShowDetails(false)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-secondary-800 rounded-lg p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-2xl font-medieval text-primary-400">
                    {selectedProposal.title}
                  </h3>
                  <button
                    onClick={() => setShowDetails(false)}
                    className="text-secondary-400 hover:text-white transition-colors"
                  >
                    ✕
                  </button>
                </div>

                <div className="space-y-6">
                  <div>
                    <h4 className="font-semibold text-white mb-2">Opis</h4>
                    <p className="text-secondary-300">{selectedProposal.description}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-white mb-2">Wiedza z Lore</h4>
                    <p className="text-secondary-300 italic">{selectedProposal.lore}</p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <h4 className="font-semibold text-green-400 mb-2">Nagrody</h4>
                      <ul className="text-sm text-secondary-300 space-y-1">
                        {selectedProposal.rewards.map((reward, index) => (
                          <li key={index}>• {reward}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-red-400 mb-2">Ryzyko</h4>
                      <ul className="text-sm text-secondary-300 space-y-1">
                        {selectedProposal.risks.map((risk, index) => (
                          <li key={index}>• {risk}</li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="font-semibold text-yellow-400 mb-2">Wymagania</h4>
                      <ul className="text-sm text-secondary-300 space-y-1">
                        {selectedProposal.requirements.map((req, index) => (
                          <li key={index}>• {req}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-4 border-t border-secondary-700">
                    <div className="text-sm text-secondary-400">
                      Trudność: <span className={getDifficultyColor(selectedProposal.difficulty)}>
                        {getDifficultyText(selectedProposal.difficulty)}
                      </span>
                      <br />
                      Czas trwania: {selectedProposal.duration}
                    </div>

                    <div className="flex gap-3">
                      <button
                        onClick={() => setShowDetails(false)}
                        className="px-4 py-2 bg-secondary-700 hover:bg-secondary-600 text-white rounded-lg transition-colors"
                      >
                        Anuluj
                      </button>
                      <button
                        onClick={() => handleAcceptProposal(selectedProposal)}
                        className="px-6 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors font-semibold"
                      >
                        Zaakceptuj Propozycję
                      </button>
                    </div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </WarhammerGSAPController>
  )
}
