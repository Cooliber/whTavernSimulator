<template>
  <div class="dice-game-interface">
    <!-- Game Rules -->
    <div class="game-rules card-enhanced mb-6 p-4">
      <h3 class="font-medieval text-lg text-foreground mb-3">Crown and Anchor Rules</h3>
      <p class="font-sharp text-sm text-muted-foreground mb-3">
        Roll three dice and bet on the symbols that will appear. Each matching symbol pays out your bet amount.
      </p>
      <div class="symbols-guide grid grid-cols-3 md:grid-cols-6 gap-2">
        <div v-for="symbol in gameSymbols" :key="symbol.name" class="symbol-item text-center">
          <div class="symbol text-2xl mb-1">{{ symbol.icon }}</div>
          <div class="symbol-name text-xs text-muted-foreground">{{ symbol.name }}</div>
        </div>
      </div>
    </div>

    <!-- Betting Interface -->
    <div class="betting-interface card-enhanced mb-6 p-6">
      <h3 class="font-medieval text-lg text-foreground mb-4">Place Your Bets</h3>
      
      <!-- Betting Grid -->
      <div class="betting-grid grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
        <div
          v-for="symbol in gameSymbols"
          :key="symbol.name"
          :class="[
            'betting-spot p-4 rounded-lg border-2 cursor-pointer transition-all duration-200',
            bets[symbol.name] > 0 
              ? 'border-primary bg-primary/10' 
              : 'border-border hover:border-primary/50'
          ]"
          @click="selectBettingSpot(symbol.name)"
        >
          <div class="text-center">
            <div class="symbol text-3xl mb-2">{{ symbol.icon }}</div>
            <div class="symbol-name font-medieval text-sm text-foreground mb-2">{{ symbol.name }}</div>
            <div class="bet-amount">
              <span class="text-primary font-bold">{{ bets[symbol.name] || 0 }} coins</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Betting Controls -->
      <div class="betting-controls">
        <div class="bet-amount-selector mb-4">
          <label class="font-medieval text-sm text-foreground mb-2 block">Bet Amount:</label>
          <div class="flex space-x-2">
            <button
              v-for="amount in betAmounts"
              :key="amount"
              @click="selectedBetAmount = amount"
              :class="[
                'bet-amount-btn px-3 py-2 rounded text-sm font-sharp transition-all duration-200',
                selectedBetAmount === amount
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary/20 text-secondary hover:bg-secondary/30'
              ]"
            >
              {{ amount }}
            </button>
          </div>
        </div>

        <div class="betting-actions flex space-x-3">
          <button
            @click="clearAllBets"
            :disabled="totalBetAmount === 0"
            class="btn-enhanced bg-destructive/90 hover:bg-destructive"
          >
            Clear Bets
          </button>
          <button
            @click="rollDice"
            :disabled="totalBetAmount === 0 || isRolling"
            class="btn-enhanced flex-1"
          >
            <Icon v-if="isRolling" name="loader" class="w-4 h-4 mr-2 animate-spin" />
            <Icon v-else name="dice" class="w-4 h-4 mr-2" />
            {{ isRolling ? 'Rolling...' : 'Roll Dice' }}
          </button>
        </div>

        <div class="bet-summary mt-4 p-3 bg-card/30 rounded-lg">
          <div class="flex justify-between items-center">
            <span class="font-medieval text-sm text-foreground">Total Bet:</span>
            <span class="font-bold text-primary">{{ totalBetAmount }} coins</span>
          </div>
          <div class="flex justify-between items-center mt-1">
            <span class="font-medieval text-sm text-foreground">Potential Payout:</span>
            <span class="font-bold text-accent">{{ potentialPayout }} coins</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Dice Display -->
    <div class="dice-display card-enhanced p-6">
      <h3 class="font-medieval text-lg text-foreground mb-4 text-center">The Dice</h3>
      
      <div class="dice-container flex justify-center space-x-6 mb-6">
        <div
          v-for="(die, index) in diceResults"
          :key="index"
          :class="[
            'die w-20 h-20 rounded-lg border-2 border-border flex items-center justify-center text-4xl transition-all duration-500',
            isRolling ? 'animate-bounce' : '',
            die ? 'bg-card' : 'bg-muted/20'
          ]"
        >
          {{ die || '?' }}
        </div>
      </div>

      <!-- Results -->
      <div v-if="lastRollResult" class="roll-results">
        <div class="results-summary text-center mb-4">
          <h4 class="font-medieval text-lg text-foreground mb-2">Roll Results</h4>
          <div class="results-grid grid grid-cols-2 md:grid-cols-3 gap-2">
            <div
              v-for="symbol in gameSymbols"
              :key="symbol.name"
              :class="[
                'result-item p-2 rounded text-center',
                lastRollResult.symbolCounts[symbol.name] > 0 
                  ? 'bg-primary/20 text-primary' 
                  : 'bg-muted/10 text-muted-foreground'
              ]"
            >
              <div class="symbol text-lg">{{ symbol.icon }}</div>
              <div class="count text-sm font-bold">{{ lastRollResult.symbolCounts[symbol.name] || 0 }}</div>
            </div>
          </div>
        </div>

        <div class="payout-summary text-center">
          <div class="total-payout">
            <span class="font-medieval text-lg text-foreground">Total Payout: </span>
            <span :class="[
              'font-bold text-xl',
              lastRollResult.totalPayout > 0 ? 'text-green-400' : 'text-red-400'
            ]">
              {{ lastRollResult.totalPayout }} coins
            </span>
          </div>
          <div class="net-result mt-2">
            <span class="font-medieval text-sm text-foreground">Net Result: </span>
            <span :class="[
              'font-bold',
              lastRollResult.netResult > 0 ? 'text-green-400' : 'text-red-400'
            ]">
              {{ lastRollResult.netResult > 0 ? '+' : '' }}{{ lastRollResult.netResult }} coins
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface DiceGameProps {
  game: any
}

interface RollResult {
  symbolCounts: Record<string, number>
  totalPayout: number
  netResult: number
  success: boolean
}

const props = defineProps<DiceGameProps>()
const emit = defineEmits<{
  gameResult: [result: { success: boolean; result: string; rewards?: any }]
  gameAction: [action: any]
}>()

// Game symbols for Crown and Anchor
const gameSymbols = [
  { name: 'crown', icon: '👑' },
  { name: 'anchor', icon: '⚓' },
  { name: 'heart', icon: '❤️' },
  { name: 'diamond', icon: '💎' },
  { name: 'spade', icon: '♠️' },
  { name: 'club', icon: '♣️' }
]

// Reactive state
const bets = ref<Record<string, number>>({})
const selectedBetAmount = ref(1)
const betAmounts = [1, 2, 5, 10]
const diceResults = ref<string[]>(['', '', ''])
const isRolling = ref(false)
const lastRollResult = ref<RollResult | null>(null)

// Computed properties
const totalBetAmount = computed(() => {
  return Object.values(bets.value).reduce((sum, bet) => sum + bet, 0)
})

const potentialPayout = computed(() => {
  // In Crown and Anchor, each matching symbol pays 1:1
  // Maximum payout would be if all three dice show the same symbol you bet on
  return Object.entries(bets.value).reduce((total, [symbol, betAmount]) => {
    return total + (betAmount * 3) // Maximum 3 matches possible
  }, 0)
})

// Methods
const selectBettingSpot = (symbolName: string) => {
  if (!bets.value[symbolName]) {
    bets.value[symbolName] = 0
  }
  
  bets.value[symbolName] += selectedBetAmount.value
}

const clearAllBets = () => {
  bets.value = {}
}

const rollDice = async () => {
  if (totalBetAmount.value === 0 || isRolling.value) return
  
  isRolling.value = true
  diceResults.value = ['', '', '']
  
  // Simulate rolling animation
  const rollDuration = 2000 // 2 seconds
  const rollInterval = 100 // Update every 100ms
  
  const rollAnimation = setInterval(() => {
    diceResults.value = diceResults.value.map(() => {
      const randomSymbol = gameSymbols[Math.floor(Math.random() * gameSymbols.length)]
      return randomSymbol.icon
    })
  }, rollInterval)
  
  // Stop animation and show final results
  setTimeout(() => {
    clearInterval(rollAnimation)
    
    // Generate final results
    const finalResults = Array(3).fill(null).map(() => {
      const randomSymbol = gameSymbols[Math.floor(Math.random() * gameSymbols.length)]
      return randomSymbol.icon
    })
    
    diceResults.value = finalResults
    
    // Calculate results
    const result = calculateResults(finalResults)
    lastRollResult.value = result
    
    isRolling.value = false
    
    // Emit game result
    emit('gameResult', {
      success: result.netResult > 0,
      result: result.netResult > 0 
        ? `You won ${result.totalPayout} coins!` 
        : `You lost ${Math.abs(result.netResult)} coins.`,
      rewards: result.netResult > 0 ? { coins: result.totalPayout } : undefined
    })
    
    // Clear bets for next round
    setTimeout(() => {
      bets.value = {}
    }, 3000)
    
  }, rollDuration)
}

const calculateResults = (diceIcons: string[]): RollResult => {
  // Count occurrences of each symbol
  const symbolCounts: Record<string, number> = {}
  
  gameSymbols.forEach(symbol => {
    symbolCounts[symbol.name] = diceIcons.filter(icon => icon === symbol.icon).length
  })
  
  // Calculate payout
  let totalPayout = 0
  
  Object.entries(bets.value).forEach(([symbolName, betAmount]) => {
    const matches = symbolCounts[symbolName] || 0
    totalPayout += betAmount * matches
  })
  
  const netResult = totalPayout - totalBetAmount.value
  
  return {
    symbolCounts,
    totalPayout,
    netResult,
    success: netResult > 0
  }
}

// Initialize empty bets
onMounted(() => {
  gameSymbols.forEach(symbol => {
    bets.value[symbol.name] = 0
  })
})
</script>

<style scoped>
.betting-spot {
  @apply transition-all duration-200;
}

.betting-spot:hover {
  @apply transform scale-105;
}

.die {
  @apply transition-all duration-300;
}

.die.animate-bounce {
  animation: diceRoll 0.1s infinite;
}

.bet-amount-btn:hover {
  @apply transform -translate-y-px;
}

.result-item {
  @apply transition-all duration-300;
}

@keyframes diceRoll {
  0%, 100% { transform: rotate(0deg) scale(1); }
  25% { transform: rotate(90deg) scale(1.1); }
  50% { transform: rotate(180deg) scale(1); }
  75% { transform: rotate(270deg) scale(1.1); }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .betting-grid {
    @apply grid-cols-2 gap-2;
  }
  
  .dice-container {
    @apply space-x-3;
  }
  
  .die {
    @apply w-16 h-16 text-3xl;
  }
  
  .betting-controls {
    @apply space-y-3;
  }
  
  .betting-actions {
    @apply flex-col space-x-0 space-y-3;
  }
}
</style>
