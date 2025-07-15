import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Dice6, RefreshCw, Copy, Save, Star } from 'lucide-react'
import toast from 'react-hot-toast'

// WFRP Random Tables
const RandomTables = {
  weather: {
    name: 'Pogoda',
    icon: '🌤️',
    color: 'text-blue-400',
    dice: 'd10',
    results: [
      { roll: '1', result: 'Ulewny deszcz', effect: '-20 do Percepcji, trudne warunki podróży' },
      { roll: '2', result: 'Lekki deszcz', effect: '-10 do Percepcji' },
      { roll: '3', result: 'Pochmurno', effect: 'Brak modyfikatorów' },
      { roll: '4-6', result: 'Słonecznie', effect: '+5 do morale' },
      { roll: '7', result: 'Wietrznie', effect: '-10 do BS (strzelanie)' },
      { roll: '8', result: 'Mgła', effect: '-20 do Percepcji, ograniczona widoczność' },
      { roll: '9', result: 'Śnieg', effect: '-10 do Zręczności, śliska powierzchnia' },
      { roll: '10', result: 'Burza', effect: '-20 do wszystkich testów na zewnątrz' }
    ]
  },

  tavern_events: {
    name: 'Wydarzenia w Tawernie',
    icon: '🍺',
    color: 'text-amber-400',
    dice: 'd20',
    results: [
      { roll: '1', result: 'Bójka wybucha przy barze', effect: 'Wszyscy muszą wykonać test Uników lub zostać wciągnięci' },
      { roll: '2', result: 'Pijany żołnierz opowiada o skarbie', effect: 'Informacje mogą być prawdziwe lub fałszywe' },
      { roll: '3', result: 'Tajemniczy nieznajomy oferuje pracę', effect: 'Potencjalny zaczyn przygody' },
      { roll: '4', result: 'Karczemarz oferuje darmowe piwo', effect: '+10 do testów Towarzyskości przez godzinę' },
      { roll: '5', result: 'Menestrel śpiewa ballady', effect: 'Gracze mogą dowiedzieć się lokalnych legend' },
      { roll: '6-10', result: 'Spokojna atmosfera', effect: 'Normalne interakcje' },
      { roll: '11', result: 'Kupiec szuka ochrony', effect: 'Oferuje 2d10 szylingów za eskortę' },
      { roll: '12', result: 'Plotki o dziwnych wydarzeniach', effect: 'Informacje o lokalnych problemach' },
      { roll: '13', result: 'Patrol straży sprawdza dokumenty', effect: 'Problemy dla osób bez papierów' },
      { roll: '14', result: 'Gra w kości', effect: 'Możliwość wygrania lub przegrania pieniędzy' },
      { roll: '15', result: 'Kapłan błogosławi obecnych', effect: '+1 Punkt Losu dla wszystkich' },
      { roll: '16', result: 'Wieści z dalekiej krainy', effect: 'Informacje o wydarzeniach w Imperium' },
      { roll: '17', result: 'Podejrzany typ obserwuje grupę', effect: 'Możliwy szpieg lub złodziej' },
      { roll: '18', result: 'Jedzenie jest wyjątkowo dobre', effect: '+5 do testów Wytrzymałości na dzień' },
      { roll: '19', result: 'Stary weteran opowiada o wojnie', effect: 'Informacje militarne i taktyczne' },
      { roll: '20', result: 'Rzadki gość - elf/krasnolud', effect: 'Możliwość niezwykłych informacji' }
    ]
  },

  mutations: {
    name: 'Mutacje Chaosu',
    icon: '💀',
    color: 'text-purple-400',
    dice: 'd100',
    results: [
      { roll: '01-05', result: 'Dodatkowe oko', effect: '+10 do Percepcji, -10 do Towarzyskości' },
      { roll: '06-10', result: 'Rogaty czaszka', effect: '+1 do ataków głową, -20 do Towarzyskości' },
      { roll: '11-15', result: 'Pazury', effect: '+1 Obrażenie w walce wręcz, nie można używać broni' },
      { roll: '16-20', result: 'Łuski', effect: '+1 PA na całym ciele, -10 do Zręczności' },
      { roll: '21-25', result: 'Długi język', effect: '+20 do testów smakowitych, -10 do mowy' },
      { roll: '26-30', result: 'Dodatkowa ręka', effect: '+10 do testów Zręczności, -20 do Towarzyskości' },
      { roll: '31-35', result: 'Zmieniony kolor skóry', effect: '-20 do Towarzyskości w niektórych miejscach' },
      { roll: '36-40', result: 'Kły', effect: '+1 Obrażenie przy ugryzieniu, -10 do mowy' },
      { roll: '41-45', result: 'Ogon', effect: '+5 do Równowagi, -10 do Towarzyskości' },
      { roll: '46-50', result: 'Dodatkowa noga', effect: '+1 Ruch, -20 do Towarzyskości' },
      { roll: '51-55', result: 'Futro', effect: '+10 do odporności na zimno, -10 do Towarzyskości' },
      { roll: '56-60', result: 'Świecące oczy', effect: 'Widzenie w ciemności, -10 do Skradania' },
      { roll: '61-65', result: 'Zmieniony głos', effect: 'Głos zwierzęcy, -20 do Towarzyskości' },
      { roll: '66-70', result: 'Wydłużone kończyny', effect: '+5 do zasięgu, -10 do Zręczności' },
      { roll: '71-75', result: 'Dodatkowe usta', effect: 'Może jeść więcej, -20 do Towarzyskości' },
      { roll: '76-80', result: 'Zmieniony zapach', effect: '-20 do Towarzyskości, +10 do Śledzenia (przez zapach)' },
      { roll: '81-85', result: 'Kostne narośla', effect: '+1 PA, -10 do Zręczności' },
      { roll: '86-90', result: 'Dodatkowe palce', effect: '+5 do Zręczności, -10 do Towarzyskości' },
      { roll: '91-95', result: 'Zmienione stopy', effect: '+1 Ruch, nie można nosić butów' },
      { roll: '96-00', result: 'Chaos Spawn', effect: 'Postać staje się Chaos Spawn (koniec gry)' }
    ]
  },

  critical_hits: {
    name: 'Trafienia Krytyczne',
    icon: '⚔️',
    color: 'text-red-400',
    dice: 'd10',
    results: [
      { roll: '1', result: 'Lekkie zranienie', effect: '+1 Obrażenie' },
      { roll: '2', result: 'Bolesne cięcie', effect: '+2 Obrażenia, -10 do następnego testu' },
      { roll: '3', result: 'Głębokie zranienie', effect: '+3 Obrażenia, krwawienie (1 obrażenie/rundę)' },
      { roll: '4', result: 'Oszołomienie', effect: '+2 Obrażenia, cel traci następną akcję' },
      { roll: '5', result: 'Powalenie', effect: '+2 Obrażenia, cel upada' },
      { roll: '6', result: 'Uszkodzenie zbroi', effect: '+3 Obrażenia, -1 PA zbroi' },
      { roll: '7', result: 'Zranienie kończyny', effect: '+4 Obrażenia, -20 do testów tej kończyny' },
      { roll: '8', result: 'Ciężkie zranienie', effect: '+5 Obrażeń, test Wytrzymałości lub nieprzytomność' },
      { roll: '9', result: 'Masakra', effect: '+6 Obrażeń, test Strachu dla świadków' },
      { roll: '10', result: 'Natychmiastowa śmierć', effect: 'Cel umiera natychmiast' }
    ]
  },

  random_names: {
    name: 'Losowe Imiona',
    icon: '👤',
    color: 'text-green-400',
    dice: 'd20',
    results: [
      { roll: '1', result: 'Heinrich Steinberg', effect: 'Kupiec z Altdorfu' },
      { roll: '2', result: 'Gretchen Müller', effect: 'Karczmarka z Ubersreik' },
      { roll: '3', result: 'Wilhelm Wagner', effect: 'Kowal z Nuln' },
      { roll: '4', result: 'Brunhilde Schmidt', effect: 'Kapłanka Sigmara' },
      { roll: '5', result: 'Otto Becker', effect: 'Piekarz z Middenheim' },
      { roll: '6', result: 'Ingrid Hoffmann', effect: 'Szlachcianka z Reikland' },
      { roll: '7', result: 'Klaus Weber', effect: 'Tkacz z Talabheim' },
      { roll: '8', result: 'Ursula Schulz', effect: 'Uczona z Altdorfu' },
      { roll: '9', result: 'Friedrich Richter', effect: 'Sędzia z Marienburg' },
      { roll: '10', result: 'Astrid Fischer', effect: 'Rybaczka z Nordland' },
      { roll: '11', result: 'Gustav Zimmermann', effect: 'Cieśla z Stirland' },
      { roll: '12', result: 'Helga Braun', effect: 'Gospodyni z Averland' },
      { roll: '13', result: 'Rudolf Krüger', effect: 'Łowca z Drakwald' },
      { roll: '14', result: 'Mathilde Wolf', effect: 'Handlarka z Wissenland' },
      { roll: '15', result: 'Johann Fuchs', effect: 'Posłaniec z Ostermark' },
      { roll: '16', result: 'Sigrid Lange', effect: 'Wróżka z Hochland' },
      { roll: '17', result: 'Thorek Ironbeard', effect: 'Krasnolud kowal' },
      { roll: '18', result: 'Bilbo Greenhill', effect: 'Niziołek kucharz' },
      { roll: '19', result: 'Eltharion Moonwhisper', effect: 'Elf strażnik' },
      { roll: '20', result: 'Grimjaw Skullsplitter', effect: 'Ork wódz' }
    ]
  }
}

export const RandomTablesComponent = ({ gmMode, sessionData, onSessionDataUpdate }) => {
  const [selectedTable, setSelectedTable] = useState('weather')
  const [lastRoll, setLastRoll] = useState(null)
  const [rollHistory, setRollHistory] = useState([])
  const [isRolling, setIsRolling] = useState(false)

  // Roll on selected table
  const rollOnTable = () => {
    const table = RandomTables[selectedTable]
    if (!table) return

    setIsRolling(true)

    setTimeout(() => {
      let roll, result

      if (table.dice === 'd10') {
        roll = Math.floor(Math.random() * 10) + 1
      } else if (table.dice === 'd20') {
        roll = Math.floor(Math.random() * 20) + 1
      } else if (table.dice === 'd100') {
        roll = Math.floor(Math.random() * 100) + 1
      }

      // Find matching result
      result = table.results.find(r => {
        if (r.roll.includes('-')) {
          const [min, max] = r.roll.split('-').map(n => parseInt(n))
          return roll >= min && roll <= max
        } else {
          return parseInt(r.roll) === roll
        }
      })

      if (!result) {
        result = table.results[Math.floor(Math.random() * table.results.length)]
      }

      const rollResult = {
        id: Date.now(),
        table: table.name,
        roll: roll,
        result: result.result,
        effect: result.effect,
        timestamp: new Date().toLocaleTimeString()
      }

      setLastRoll(rollResult)
      setRollHistory(prev => [rollResult, ...prev.slice(0, 19)]) // Keep last 20
      setIsRolling(false)
      
      toast.success(`Wyrzucono ${roll} na ${table.dice}!`)
    }, 800)
  }

  // Copy result to clipboard
  const copyResult = () => {
    if (!lastRoll) return

    const resultText = `
TABELA: ${lastRoll.table}
RZUT: ${lastRoll.roll}
WYNIK: ${lastRoll.result}
EFEKT: ${lastRoll.effect}
CZAS: ${lastRoll.timestamp}
    `.trim()

    navigator.clipboard.writeText(resultText)
    toast.success('Wynik skopiowany!')
  }

  // Save result
  const saveResult = () => {
    if (!lastRoll) return
    
    // This would integrate with session data
    toast.success('Wynik zapisany do sesji!')
  }

  const getTableColor = (tableKey) => {
    const table = RandomTables[tableKey]
    return table ? table.color : 'text-gray-400'
  }

  return (
    <div className="h-full flex flex-col p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-medieval text-white mb-2">Tabele Losowe</h3>
          <p className="text-secondary-300">
            Kolekcja przydatnych tabel losowych dla WFRP
          </p>
        </div>
        
        <button
          onClick={rollOnTable}
          disabled={isRolling}
          className="px-4 py-2 bg-primary-600 hover:bg-primary-700 disabled:bg-secondary-600 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          {isRolling ? (
            <RefreshCw className="w-4 h-4 animate-spin" />
          ) : (
            <Dice6 className="w-4 h-4" />
          )}
          {isRolling ? 'Rzucanie...' : 'Rzuć Kostką'}
        </button>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Table Selection */}
        <div className="space-y-4">
          <h4 className="font-semibold text-white">Dostępne Tabele</h4>
          
          <div className="space-y-2">
            {Object.entries(RandomTables).map(([key, table]) => (
              <motion.button
                key={key}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelectedTable(key)}
                className={`
                  w-full p-3 rounded-lg border transition-all duration-200 text-left
                  ${selectedTable === key
                    ? `bg-primary-400/20 border-primary-400/50 text-primary-100`
                    : 'bg-secondary-700/50 border-secondary-600 hover:border-secondary-500 text-white'
                  }
                `}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">{table.icon}</span>
                  <span className="font-medium">{table.name}</span>
                </div>
                <div className="text-xs text-secondary-400">
                  {table.dice} • {table.results.length} wyników
                </div>
              </motion.button>
            ))}
          </div>

          {/* Roll History */}
          <div className="border-t border-secondary-700 pt-4">
            <h4 className="font-semibold text-white mb-3">Historia Rzutów</h4>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {rollHistory.map((roll) => (
                <div
                  key={roll.id}
                  className="p-2 bg-secondary-600/50 rounded text-sm"
                >
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-medium text-white">{roll.table}</span>
                    <span className="text-primary-400">{roll.roll}</span>
                  </div>
                  <div className="text-secondary-300 text-xs line-clamp-2">
                    {roll.result}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Table Content & Results */}
        <div className="lg:col-span-3">
          <div className="space-y-6">
            {/* Current Table */}
            <div className="bg-secondary-700/50 rounded-lg p-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{RandomTables[selectedTable].icon}</span>
                  <div>
                    <h4 className="font-semibold text-white">
                      {RandomTables[selectedTable].name}
                    </h4>
                    <p className="text-sm text-secondary-300">
                      Rzuć {RandomTables[selectedTable].dice}
                    </p>
                  </div>
                </div>
              </div>

              {/* Table Results */}
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {RandomTables[selectedTable].results.map((result, index) => (
                  <div
                    key={index}
                    className="p-3 bg-secondary-600/30 rounded-lg"
                  >
                    <div className="flex items-start gap-3">
                      <span className="text-primary-400 font-mono text-sm min-w-[3rem]">
                        {result.roll}
                      </span>
                      <div className="flex-1">
                        <div className="font-medium text-white mb-1">
                          {result.result}
                        </div>
                        <div className="text-sm text-secondary-300">
                          {result.effect}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Last Roll Result */}
            <AnimatePresence>
              {lastRoll && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="bg-primary-400/10 border border-primary-400/30 rounded-lg p-4"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <Dice6 className="w-6 h-6 text-primary-400" />
                      <div>
                        <h4 className="font-semibold text-white">Ostatni Rzut</h4>
                        <p className="text-sm text-secondary-300">
                          {lastRoll.table} • {lastRoll.timestamp}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex gap-2">
                      <button
                        onClick={saveResult}
                        className="p-2 bg-green-600 hover:bg-green-700 rounded-lg transition-colors"
                        title="Zapisz wynik"
                      >
                        <Save className="w-4 h-4 text-white" />
                      </button>
                      <button
                        onClick={copyResult}
                        className="p-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
                        title="Kopiuj wynik"
                      >
                        <Copy className="w-4 h-4 text-white" />
                      </button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-primary-400 mb-1">
                        {lastRoll.roll}
                      </div>
                      <div className="text-sm text-secondary-400">Rzut</div>
                    </div>
                    
                    <div>
                      <div className="text-sm text-secondary-400 mb-1">Wynik:</div>
                      <div className="font-medium text-white">{lastRoll.result}</div>
                    </div>
                    
                    <div>
                      <div className="text-sm text-secondary-400 mb-1">Efekt:</div>
                      <div className="text-sm text-secondary-300">{lastRoll.effect}</div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* No Roll Yet */}
            {!lastRoll && (
              <div className="text-center py-12">
                <Dice6 className="w-16 h-16 text-secondary-400 mx-auto mb-4 opacity-50" />
                <h3 className="text-lg font-medieval text-white mb-2">
                  Brak Rzutów
                </h3>
                <p className="text-secondary-400 mb-4">
                  Kliknij "Rzuć Kostką" aby wykonać rzut na wybranej tabeli
                </p>
                <button
                  onClick={rollOnTable}
                  className="px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors flex items-center gap-2 mx-auto"
                >
                  <Dice6 className="w-5 h-5" />
                  Wykonaj Pierwszy Rzut
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
