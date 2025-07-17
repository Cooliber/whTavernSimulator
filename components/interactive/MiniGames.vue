<template>
  <div class="mini-games-hub">
    <!-- Games Overview -->
    <div v-if="!currentGame" class="games-overview">
      <div class="hub-header text-center mb-8">
        <h2 class="font-fantasy text-3xl text-primary heading-glow mb-4">
          Tavern Games & Contests
        </h2>
        <p class="font-medieval text-muted-foreground max-w-2xl mx-auto">
          Test your skills and luck in traditional tavern games. Win coin, reputation, and the respect of your fellow patrons.
        </p>
      </div>

      <!-- Available Games Grid -->
      <div class="games-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="game in availableGames"
          :key="game.id"
          :class="[
            'game-card card-enhanced cursor-pointer transition-all duration-300',
            game.isActive ? 'hover:shadow-xl' : 'opacity-50 cursor-not-allowed'
          ]"
          @click="game.isActive && selectGame(game)"
        >
          <!-- Game Icon -->
          <div class="game-icon text-center mb-4">
            <div :class="[
              'w-16 h-16 mx-auto rounded-full flex items-center justify-center text-2xl',
              getGameIconClass(game.type)
            ]">
              {{ getGameIcon(game.type) }}
            </div>
          </div>

          <!-- Game Info -->
          <div class="game-info text-center">
            <h3 class="font-medieval text-lg text-foreground mb-2">{{ game.name }}</h3>
            <div class="game-details space-y-2">
              <div class="difficulty flex items-center justify-center space-x-2">
                <span class="text-sm text-muted-foreground">Difficulty:</span>
                <span :class="getDifficultyClass(game.difficulty)">
                  {{ game.difficulty }}
                </span>
              </div>
              
              <div class="stakes text-sm text-muted-foreground">
                Entry: {{ game.stakes.entry }} coins • Reward: {{ game.stakes.reward }} coins
              </div>
              
              <div v-if="game.stakes.reputationGain" class="reputation-bonus text-sm text-accent">
                +{{ game.stakes.reputationGain }} Reputation
              </div>
            </div>
          </div>

          <!-- Requirements -->
          <div v-if="game.requirements" class="requirements mt-4 p-3 bg-card/30 rounded-lg">
            <h4 class="font-medieval text-sm text-foreground mb-2">Requirements:</h4>
            <div class="requirement-list text-xs text-muted-foreground space-y-1">
              <div v-if="game.requirements.skill">
                Skill: {{ game.requirements.skill }}
              </div>
              <div v-if="game.requirements.reputation">
                Reputation: {{ game.requirements.reputation }}+
              </div>
            </div>
          </div>

          <!-- Participants -->
          <div v-if="game.participants.length > 0" class="participants mt-4">
            <div class="text-xs text-muted-foreground">
              {{ game.participants.length }} participant(s) waiting
            </div>
          </div>

          <!-- Status -->
          <div class="game-status mt-4">
            <span v-if="!game.isActive" class="status-badge bg-muted/20 text-muted-foreground">
              Currently Unavailable
            </span>
            <span v-else-if="!canAfford(game.stakes.entry)" class="status-badge bg-destructive/20 text-destructive">
              Insufficient Funds
            </span>
            <span v-else class="status-badge bg-primary/20 text-primary">
              Ready to Play
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Game Interface -->
    <div v-else class="active-game">
      <!-- Game Header -->
      <div class="game-header flex items-center justify-between mb-6">
        <div class="game-title">
          <h2 class="font-medieval text-2xl text-foreground">{{ currentGame.name }}</h2>
          <p class="text-muted-foreground">{{ getGameDescription(currentGame.type) }}</p>
        </div>
        <button @click="exitGame" class="btn-enhanced text-sm">
          <Icon name="x" class="w-4 h-4 mr-2" />
          Exit Game
        </button>
      </div>

      <!-- Game Content -->
      <div class="game-content">
        <!-- Dice Game -->
        <div v-if="currentGame.type === 'dice'" class="dice-game">
          <DiceGameInterface 
            :game="currentGame"
            @game-result="handleGameResult"
            @game-action="handleGameAction"
          />
        </div>

        <!-- Arm Wrestling -->
        <div v-else-if="currentGame.type === 'arm_wrestling'" class="arm-wrestling">
          <ArmWrestlingInterface 
            :game="currentGame"
            @game-result="handleGameResult"
            @game-action="handleGameAction"
          />
        </div>

        <!-- Storytelling Contest -->
        <div v-else-if="currentGame.type === 'storytelling'" class="storytelling">
          <StorytellingInterface 
            :game="currentGame"
            @game-result="handleGameResult"
            @game-action="handleGameAction"
          />
        </div>

        <!-- Drinking Contest -->
        <div v-else-if="currentGame.type === 'drinking'" class="drinking-contest">
          <DrinkingContestInterface 
            :game="currentGame"
            @game-result="handleGameResult"
            @game-action="handleGameAction"
          />
        </div>

        <!-- Generic Game Interface -->
        <div v-else class="generic-game">
          <GenericGameInterface 
            :game="currentGame"
            @game-result="handleGameResult"
            @game-action="handleGameAction"
          />
        </div>
      </div>
    </div>

    <!-- Game Result Modal -->
    <div v-if="gameResult" class="game-result-modal fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="result-content card-enhanced max-w-md mx-4">
        <div class="result-header text-center mb-6">
          <div :class="[
            'result-icon w-16 h-16 mx-auto rounded-full flex items-center justify-center text-3xl mb-4',
            gameResult.success ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
          ]">
            {{ gameResult.success ? '🏆' : '💔' }}
          </div>
          <h3 class="font-medieval text-xl text-foreground">
            {{ gameResult.success ? 'Victory!' : 'Defeat!' }}
          </h3>
        </div>

        <div class="result-details text-center space-y-4">
          <p class="font-sharp text-muted-foreground">{{ gameResult.result }}</p>
          
          <div v-if="gameResult.rewards" class="rewards space-y-2">
            <div v-if="gameResult.rewards.coins" class="reward-item">
              <span class="font-medieval text-primary">+{{ gameResult.rewards.coins }} Coins</span>
            </div>
            <div v-if="gameResult.rewards.reputation" class="reward-item">
              <span class="font-medieval text-accent">+{{ gameResult.rewards.reputation }} Reputation</span>
            </div>
          </div>
        </div>

        <div class="result-actions mt-6 flex space-x-3">
          <button @click="playAgain" class="btn-enhanced flex-1">
            Play Again
          </button>
          <button @click="closeResult" class="btn-enhanced bg-secondary/90 hover:bg-secondary flex-1">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface GameResult {
  success: boolean
  result: string
  rewards?: {
    coins?: number
    reputation?: number
  }
}

// Composables
const { 
  availableMiniGames: availableGames, 
  currentMiniGame: currentGame,
  startMiniGame,
  playMiniGame,
  endMiniGame
} = useInteractiveTavernSystems()

const { canAfford } = useInteractiveTavernSystems()
const { gainExperience } = useEnhancedUserEngagement()

// Reactive state
const gameResult = ref<GameResult | null>(null)
const isPlaying = ref(false)

// Methods
const selectGame = async (game: any) => {
  if (!game.isActive || !canAfford(game.stakes.entry)) return
  
  const success = await startMiniGame(game.id)
  if (success) {
    isPlaying.value = true
  }
}

const handleGameAction = async (action: any) => {
  if (!currentGame.value) return
  
  const result = await playMiniGame(currentGame.value.id, action)
  gameResult.value = result
  
  // Gain experience for participating
  gainExperience(5, 'mini_game')
  
  if (result.success) {
    gainExperience(10, 'mini_game_victory')
  }
}

const handleGameResult = (result: GameResult) => {
  gameResult.value = result
}

const exitGame = () => {
  endMiniGame()
  isPlaying.value = false
}

const playAgain = () => {
  if (currentGame.value) {
    gameResult.value = null
    selectGame(currentGame.value)
  }
}

const closeResult = () => {
  gameResult.value = null
  exitGame()
}

const getGameIcon = (type: string): string => {
  const icons = {
    dice: '🎲',
    arm_wrestling: '💪',
    storytelling: '📖',
    drinking: '🍺',
    cards: '🃏',
    riddles: '🧩'
  }
  
  return icons[type as keyof typeof icons] || '🎮'
}

const getGameIconClass = (type: string): string => {
  const classes = {
    dice: 'bg-blue-500/20 text-blue-400',
    arm_wrestling: 'bg-red-500/20 text-red-400',
    storytelling: 'bg-purple-500/20 text-purple-400',
    drinking: 'bg-orange-500/20 text-orange-400',
    cards: 'bg-green-500/20 text-green-400',
    riddles: 'bg-yellow-500/20 text-yellow-400'
  }
  
  return classes[type as keyof typeof classes] || 'bg-gray-500/20 text-gray-400'
}

const getDifficultyClass = (difficulty: string): string => {
  const classes = {
    easy: 'text-green-400',
    medium: 'text-yellow-400',
    hard: 'text-red-400'
  }
  
  return classes[difficulty as keyof typeof classes] || 'text-gray-400'
}

const getGameDescription = (type: string): string => {
  const descriptions = {
    dice: 'Roll the dice and test your luck in this classic tavern game.',
    arm_wrestling: 'Prove your strength against worthy opponents.',
    storytelling: 'Weave tales that captivate and inspire your audience.',
    drinking: 'Show your constitution in this test of endurance.',
    cards: 'Outwit your opponents in games of skill and chance.',
    riddles: 'Challenge your mind with clever puzzles and wordplay.'
  }
  
  return descriptions[type as keyof typeof descriptions] || 'A classic tavern game of skill and chance.'
}
</script>

<style scoped>
.game-card {
  @apply p-6 transition-all duration-300;
}

.game-card:hover:not(.opacity-50) {
  @apply transform -translate-y-0.5;
}

.game-icon {
  @apply transition-all duration-300;
}

.game-card:hover .game-icon {
  @apply transform scale-110;
}

.status-badge {
  @apply px-3 py-1 rounded-full text-xs font-sharp;
}

.game-result-modal {
  animation: fadeIn 0.3s ease-out;
}

.result-content {
  animation: slideInUp 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .games-grid {
    @apply grid-cols-1 gap-4;
  }
  
  .game-header {
    @apply flex-col space-y-4;
  }
  
  .result-actions {
    @apply flex-col space-x-0 space-y-3;
  }
}
</style>
