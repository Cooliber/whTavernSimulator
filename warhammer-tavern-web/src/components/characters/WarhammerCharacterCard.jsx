import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sword, Shield, Scroll, Crown, Skull, Zap, Heart, Star } from 'lucide-react'
import { WarhammerGSAPController } from '../animations/WarhammerGSAPController'
import { gsap } from 'gsap'

// Warhammer Fantasy character archetypes with lore
const CharacterArchetypes = {
  // IMPERIUM
  'Kapitan Straży': {
    faction: 'Empire',
    title: 'Kapitan Straży Imperialnej',
    description: 'Doświadczony weteran, który służył w wielu kampaniach przeciwko siłom Chaosu',
    lore: 'Straż Imperialna to kręgosłup armii Imperium, składająca się z profesjonalnych żołnierzy',
    stats: { combat: 85, leadership: 90, loyalty: 95, corruption: 5 },
    abilities: ['Dowodzenie', 'Taktyka', 'Walka Mieczem', 'Inspiracja'],
    equipment: ['Miecz Runiczny', 'Zbroja Płytowa', 'Tarcza Imperialna', 'Hełm Kapitana'],
    personality: 'Honorowy, lojalny, surowy ale sprawiedliwy',
    background: 'Pochodzący z Altdorfu, służył pod Karlem Franzem w wojnie przeciwko Archeonowi'
  },
  
  'Czarodziej Jasności': {
    faction: 'Empire',
    title: 'Mag Kolegium Jasności',
    description: 'Uczony mag specjalizujący się w magii światła i ochrony przed Chaosem',
    lore: 'Kolegium Jasności to jedno z ośmiu Kolegiów Magii w Altdorfie, walczące z Chaosem',
    stats: { magic: 95, knowledge: 90, wisdom: 85, corruption: 10 },
    abilities: ['Światło Banishingu', 'Ochrona przed Chaosem', 'Leczenie', 'Egzorcyzm'],
    equipment: ['Różdżka Mocy', 'Księga Zaklęć', 'Amulet Ochrony', 'Szaty Maga'],
    personality: 'Mądry, ostrożny, oddany walce z Chaosem',
    background: 'Absolwent Uniwersytetu w Altdorfie, specjalista od demonologii'
  },

  // CHAOS
  'Czempion Chaosu': {
    faction: 'Chaos',
    title: 'Czempion Mrocznych Bogów',
    description: 'Potężny wojownik naznaczony przez Bogów Chaosu, niosący zniszczenie',
    lore: 'Czempioni Chaosu to śmiertelnicy, którzy zyskali łaskę Mrocznych Bogów',
    stats: { combat: 95, strength: 90, corruption: 95, sanity: 20 },
    abilities: ['Berserkerski Szał', 'Mutacje Chaosu', 'Strach', 'Regeneracja'],
    equipment: ['Miecz Demona', 'Zbroja Chaosu', 'Tarcza Czaszek', 'Hełm Terroru'],
    personality: 'Brutalny, nieprzewidywalny, żądny krwi',
    background: 'Niegdyś rycerz Bretonnii, skorumpowany przez wizje Khorne\'a'
  },

  'Kultista Nurgle': {
    faction: 'Chaos',
    title: 'Wyznawca Dziadka Nurgle',
    description: 'Zarażony kultista szerzący choroby i rozkład w imię Nurgle',
    lore: 'Nurgle to Bog Zarazy, jego wyznawcy rozprzestrzeniają choroby i śmierć',
    stats: { corruption: 90, disease_resistance: 95, charisma: 30, sanity: 40 },
    abilities: ['Zaraza', 'Odporność na Ból', 'Trucizny', 'Nekromancja'],
    equipment: ['Kadzielnica Zarazy', 'Szaty Rozkładu', 'Księga Chorób', 'Fiolki z Trucizną'],
    personality: 'Wesoły w swojej chorobie, filozoficzny o śmierci',
    background: 'Były lekarz z Marienburgiem, który odkrył "prawdę" o cierpieniu'
  },

  // WYSOKIE ELFY
  'Mag Wysokich Elfów': {
    faction: 'HighElves',
    title: 'Arcymag z Saphery',
    description: 'Mistrz Wysokiej Magii, władający pradawnymi mocami elfów',
    lore: 'Saphery to królestwo magów wśród Wysokich Elfów, centrum nauki magicznej',
    stats: { magic: 98, intelligence: 95, wisdom: 90, arrogance: 80 },
    abilities: ['Wysoka Magia', 'Teleportacja', 'Iluzje', 'Przepowiednie'],
    equipment: ['Różdżka Asuryan', 'Księga Hoeth', 'Szaty Gwiazd', 'Kryształ Mocy'],
    personality: 'Wyniosły, mądry, pogardliwy wobec młodszych ras',
    background: 'Studiował w Wieży Hoeth przez 300 lat, mistrz wszystkich szkół magii'
  },

  'Strażnik Lasu': {
    faction: 'WoodElves',
    title: 'Strażnik Athel Loren',
    description: 'Tajemniczy elf leśny, ochronca pradawnego lasu',
    lore: 'Athel Loren to magiczny las, dom Elfów Leśnych i starożytnych duchów',
    stats: { archery: 95, stealth: 90, nature_magic: 85, wildness: 70 },
    abilities: ['Mistrzostwo Łuku', 'Niewidzialność', 'Rozmowa ze Zwierzętami', 'Magia Natury'],
    equipment: ['Łuk Starożytnego Drzewa', 'Strzały Elfickie', 'Płaszcz Liści', 'Nóż Ceremonialny'],
    personality: 'Dziki, nieprzewidywalny, ochronny wobec natury',
    background: 'Strażnik granic lasu, który widział upadek wielu królestw ludzkich'
  },

  // KRASNOLUDZI
  'Kowal Krasnoludzki': {
    faction: 'Dwarfs',
    title: 'Mistrz Kowal z Karak Kadrin',
    description: 'Legendarny kowal tworzący najlepsze bronie i zbroje',
    lore: 'Karak Kadrin to twierdza krasnoludzka słynąca z mistrzów kowalstwa',
    stats: { crafting: 98, strength: 85, stubbornness: 95, honor: 90 },
    abilities: ['Kowalstwo Runic', 'Ocena Metali', 'Naprawa Sprzętu', 'Tradycje Rzemieślnicze'],
    equipment: ['Młot Runic', 'Kowadło Przodków', 'Narzędzia Mistrza', 'Fartuch Kowalski'],
    personality: 'Uparty, dumny ze swojego rzemiosła, lojalny wobec tradycji',
    background: 'Potomek długiej linii kowali, twórca broni dla Króla Thorgrim\'a'
  },

  'Górnik Karak': {
    faction: 'Dwarfs',
    title: 'Górnik z Głębokich Szybów',
    description: 'Doświadczony górnik znający tajemnice podziemnych tuneli',
    lore: 'Górnicy krasnoludzcy to kręgosłup gospodarki, wydobywający cenne rudy',
    stats: { mining: 90, endurance: 95, underground_knowledge: 90, claustrophobia: 5 },
    abilities: ['Wykrywanie Rud', 'Nawigacja Podziemna', 'Wysadzanie', 'Geologia'],
    equipment: ['Kilof Gromrilowy', 'Lampa Górnicza', 'Dynamit', 'Mapa Tuneli'],
    personality: 'Praktyczny, wytrwały, ostrożny w podziemiach',
    background: 'Pracuje w kopalniach od 150 lat, zna każdy tunel w okolicy'
  },

  // ORKI
  'Wódz Orków': {
    faction: 'Orcs',
    title: 'Wielki Wódz Waaagh!',
    description: 'Potężny ork dowodzący hordami zielonoskórych',
    lore: 'Wódzowie orków rządzą siłą, prowadząc swoje plemiona do walki',
    stats: { combat: 90, strength: 95, leadership: 80, cunning: 60 },
    abilities: ['Waaagh!', 'Zastraszanie', 'Walka Wręcz', 'Dowodzenie Hordą'],
    equipment: ['Wielka Siekiera', 'Zbroja z Blach', 'Hełm Czaszek', 'Sztandar Plemienia'],
    personality: 'Agresywny, głośny, szanowany przez siłę',
    background: 'Zdobył władzę pokonując poprzedniego wodza w pojedynku'
  },

  // NIEUMARLI
  'Nekromanta': {
    faction: 'Undead',
    title: 'Mistrz Mrocznych Sztuk',
    description: 'Potężny nekromanta władający armią nieumarłych',
    lore: 'Nekromanci to magowie śmierci, budzący umarłych do ponownego życia',
    stats: { necromancy: 95, death_magic: 90, corruption: 85, sanity: 30 },
    abilities: ['Wskrzeszanie Umarłych', 'Kontrola Duchów', 'Magia Śmierci', 'Nieśmiertelność'],
    equipment: ['Kostur Kości', 'Księga Nagash', 'Amulet Duszy', 'Szaty Śmierci'],
    personality: 'Zimny, kalkulujący, obsesyjnie dążący do wiedzy',
    background: 'Niegdyś uczony z Altdorfu, skorumpowany przez zakazane księgi'
  }
}

export const WarhammerCharacterCard = ({ character, isSelected, onClick, showDetails = false }) => {
  const [isHovered, setIsHovered] = useState(false)
  const [showTooltip, setShowTooltip] = useState(false)
  const cardRef = useRef(null)
  const tooltipRef = useRef(null)

  const archetype = CharacterArchetypes[character.role] || CharacterArchetypes['Kapitan Straży']
  
  // Get faction colors
  const getFactionColors = (faction) => {
    switch (faction) {
      case 'Empire':
        return {
          primary: 'from-yellow-400 to-yellow-600',
          secondary: 'border-yellow-400/50',
          text: 'text-yellow-400',
          bg: 'bg-yellow-400/10'
        }
      case 'Chaos':
        return {
          primary: 'from-red-600 to-red-800',
          secondary: 'border-red-500/50',
          text: 'text-red-400',
          bg: 'bg-red-400/10'
        }
      case 'HighElves':
      case 'WoodElves':
        return {
          primary: 'from-green-400 to-green-600',
          secondary: 'border-green-400/50',
          text: 'text-green-400',
          bg: 'bg-green-400/10'
        }
      case 'Dwarfs':
        return {
          primary: 'from-amber-400 to-amber-600',
          secondary: 'border-amber-400/50',
          text: 'text-amber-400',
          bg: 'bg-amber-400/10'
        }
      case 'Orcs':
        return {
          primary: 'from-green-600 to-green-800',
          secondary: 'border-green-500/50',
          text: 'text-green-500',
          bg: 'bg-green-500/10'
        }
      case 'Undead':
        return {
          primary: 'from-purple-600 to-purple-800',
          secondary: 'border-purple-500/50',
          text: 'text-purple-400',
          bg: 'bg-purple-400/10'
        }
      default:
        return {
          primary: 'from-gray-400 to-gray-600',
          secondary: 'border-gray-400/50',
          text: 'text-gray-400',
          bg: 'bg-gray-400/10'
        }
    }
  }

  const colors = getFactionColors(archetype.faction)

  // Hover animations
  useEffect(() => {
    if (!cardRef.current) return

    const card = cardRef.current

    if (isHovered) {
      gsap.to(card, {
        scale: 1.05,
        rotationY: 5,
        z: 50,
        duration: 0.3,
        ease: "power2.out"
      })
    } else {
      gsap.to(card, {
        scale: 1,
        rotationY: 0,
        z: 0,
        duration: 0.3,
        ease: "power2.out"
      })
    }
  }, [isHovered])

  const handleMouseEnter = () => {
    setIsHovered(true)
    setShowTooltip(true)
  }

  const handleMouseLeave = () => {
    setIsHovered(false)
    setShowTooltip(false)
  }

  const getStatIcon = (statName) => {
    switch (statName) {
      case 'combat': return <Sword className="w-4 h-4" />
      case 'magic': return <Zap className="w-4 h-4" />
      case 'leadership': return <Crown className="w-4 h-4" />
      case 'knowledge': return <Scroll className="w-4 h-4" />
      case 'corruption': return <Skull className="w-4 h-4" />
      default: return <Star className="w-4 h-4" />
    }
  }

  const getStatColor = (value) => {
    if (value >= 90) return 'text-green-400'
    if (value >= 70) return 'text-yellow-400'
    if (value >= 50) return 'text-orange-400'
    return 'text-red-400'
  }

  return (
    <WarhammerGSAPController faction={archetype.faction} animationType="idle">
      <motion.div
        ref={cardRef}
        className={`character-element relative bg-secondary-800/90 rounded-lg border-2 cursor-pointer transition-all duration-300 backdrop-blur-sm ${
          isSelected ? `${colors.secondary} shadow-lg shadow-current/20` : 'border-secondary-700 hover:border-secondary-600'
        }`}
        onClick={() => onClick?.(character)}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        whileHover={{ y: -2 }}
        whileTap={{ scale: 0.98 }}
      >
        {/* Character Portrait */}
        <div className="p-4">
          <div className="flex items-center gap-4 mb-4">
            <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${colors.primary} flex items-center justify-center text-white font-bold text-xl shadow-lg`}>
              {character.name.charAt(0)}
            </div>
            
            <div className="flex-1">
              <h3 className="font-medieval text-lg text-white mb-1">
                {character.name}
              </h3>
              <p className={`text-sm ${colors.text} font-semibold`}>
                {archetype.title}
              </p>
              <p className="text-xs text-secondary-400">
                {archetype.faction}
              </p>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-2 mb-4">
            {Object.entries(archetype.stats).slice(0, 4).map(([stat, value]) => (
              <div key={stat} className="flex items-center gap-2">
                {getStatIcon(stat)}
                <span className="text-xs text-secondary-300 capitalize">
                  {stat}:
                </span>
                <span className={`text-xs font-semibold ${getStatColor(value)}`}>
                  {value}
                </span>
              </div>
            ))}
          </div>

          {/* Abilities Preview */}
          <div className="flex flex-wrap gap-1">
            {archetype.abilities.slice(0, 3).map((ability, index) => (
              <span
                key={index}
                className={`text-xs px-2 py-1 rounded ${colors.bg} ${colors.text} border ${colors.secondary}`}
              >
                {ability}
              </span>
            ))}
            {archetype.abilities.length > 3 && (
              <span className="text-xs px-2 py-1 rounded bg-secondary-700 text-secondary-300">
                +{archetype.abilities.length - 3}
              </span>
            )}
          </div>

          {/* Status Indicators */}
          <div className="flex items-center justify-between mt-4 pt-3 border-t border-secondary-700">
            <div className="flex items-center gap-2">
              <Heart className={`w-4 h-4 ${character.active ? 'text-green-400' : 'text-red-400'}`} />
              <span className="text-xs text-secondary-400">
                {character.active ? 'Aktywny' : 'Nieaktywny'}
              </span>
            </div>
            
            <div className="text-xs text-secondary-400">
              {character.mood || 'Neutralny'}
            </div>
          </div>
        </div>

        {/* Selection Indicator */}
        {isSelected && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className={`absolute -top-2 -right-2 w-6 h-6 rounded-full bg-gradient-to-br ${colors.primary} flex items-center justify-center`}
          >
            <Star className="w-3 h-3 text-white" />
          </motion.div>
        )}

        {/* Faction Badge */}
        <div className={`absolute top-2 right-2 px-2 py-1 rounded text-xs font-semibold ${colors.bg} ${colors.text} border ${colors.secondary}`}>
          {archetype.faction}
        </div>
      </motion.div>

      {/* Detailed Tooltip */}
      <AnimatePresence>
        {showTooltip && (
          <motion.div
            ref={tooltipRef}
            initial={{ opacity: 0, y: 10, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 10, scale: 0.9 }}
            className="absolute z-50 bg-secondary-900 border border-secondary-700 rounded-lg p-4 shadow-xl backdrop-blur-sm max-w-sm"
            style={{
              top: '100%',
              left: '50%',
              transform: 'translateX(-50%)',
              marginTop: '8px'
            }}
          >
            <div className="space-y-3">
              <div>
                <h4 className="font-semibold text-white mb-1">{archetype.title}</h4>
                <p className="text-sm text-secondary-300">{archetype.description}</p>
              </div>

              <div>
                <h5 className="text-xs font-semibold text-secondary-400 uppercase tracking-wide mb-1">
                  Lore
                </h5>
                <p className="text-xs text-secondary-300 italic">{archetype.lore}</p>
              </div>

              <div>
                <h5 className="text-xs font-semibold text-secondary-400 uppercase tracking-wide mb-1">
                  Osobowość
                </h5>
                <p className="text-xs text-secondary-300">{archetype.personality}</p>
              </div>

              <div>
                <h5 className="text-xs font-semibold text-secondary-400 uppercase tracking-wide mb-1">
                  Historia
                </h5>
                <p className="text-xs text-secondary-300">{archetype.background}</p>
              </div>
            </div>

            {/* Tooltip Arrow */}
            <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-4 h-4 bg-secondary-900 border-l border-t border-secondary-700 rotate-45"></div>
          </motion.div>
        )}
      </AnimatePresence>
    </WarhammerGSAPController>
  )
}
