<template>
  <div class="battle-page relative min-h-screen overflow-hidden bg-gradient-to-br from-red-900/20 to-orange-900/20">
    <!-- Epic battle atmosphere -->
    <InteractiveGridPattern 
      :grid-size="60"
      grid-color="#8b0000"
      :stroke-width="2"
      :proximity-radius="100"
      proximity-color="#ff4500"
      class="absolute inset-0 opacity-20"
    />
    <Meteors :meteor-count="12" :meteor-speed="1.2" />
    <ParticlesBg 
      :particle-count="50"
      particle-color="#ff4500"
      :particle-size="2"
      :animation-speed="0.8"
      class="opacity-60"
    />
    
    <div class="relative z-10 space-y-6 p-6">
      <!-- Battle Header -->
      <section class="text-center space-y-4">
        <Spotlight 
          spotlight-color="rgba(255, 69, 0, 0.8)"
          :spotlight-size="700"
          class="inline-block"
        >
          <div class="space-y-3">
            <SparklesText 
              text="BATTLE ARENA"
              class="text-6xl md:text-8xl font-medieval text-foreground"
              :sparkles-count="35"
            />
            <Text3D 
              text="Tactical Combat System"
              class="text-2xl md:text-3xl font-fantasy text-primary"
              :depth="6"
            />
          </div>
        </Spotlight>
        
        <!-- Battle Status -->
        <div class="flex justify-center space-x-8">
          <div class="battle-status-item">
            <Icon name="sword" class="w-6 h-6 text-red-400 mx-auto" />
            <p class="text-sm font-medieval text-muted-foreground">Turn {{ currentTurn }}</p>
          </div>
          <div class="battle-status-item">
            <Icon name="clock" class="w-6 h-6 text-yellow-400 mx-auto" />
            <p class="text-sm font-medieval text-muted-foreground">{{ battleTimer }}s</p>
          </div>
          <div class="battle-status-item">
            <Icon name="zap" class="w-6 h-6 text-blue-400 mx-auto" />
            <p class="text-sm font-medieval text-muted-foreground">{{ battlePhase }}</p>
          </div>
        </div>
      </section>

      <!-- Battle Grid -->
      <section class="battle-grid-container">
        <BorderBeam 
          class="battle-grid bg-gradient-to-br from-card/90 to-card/70 backdrop-blur-md rounded-2xl p-6"
          :border-width="4"
          color-from="#8b0000"
          color-to="#ff4500"
        >
          <div class="grid grid-cols-1 xl:grid-cols-4 gap-6">
            <!-- Player Party -->
            <div class="party-panel player-party">
              <BorderBeam 
                class="bg-gradient-to-br from-blue-900/30 to-blue-800/30 rounded-xl p-4"
                :border-width="2"
                color-from="#3b82f6"
                color-to="#1d4ed8"
              >
                <div class="space-y-4">
                  <HyperText 
                    text="Your Party"
                    class="text-xl font-medieval text-foreground text-center"
                    :animation-duration="1000"
                  />
                  
                  <div class="space-y-3">
                    <div 
                      v-for="character in playerParty" 
                      :key="character.id"
                      class="character-card"
                      :class="{ 'active-character': activeCharacter?.id === character.id }"
                      @click="selectCharacter(character)"
                    >
                      <Lens 
                        :lens-size="100"
                        :magnification="1.4"
                        class="character-lens"
                      >
                        <Card3D 
                          class="character-card-inner p-3 rounded-lg transition-all duration-300"
                          :class="character.isAlive ? 'bg-gradient-to-br from-blue-600/50 to-blue-700/50' : 'bg-gradient-to-br from-gray-600/50 to-gray-700/50'"
                          :rotation-intensity="character.isAlive ? 10 : 2"
                        >
                          <div class="flex items-center space-x-3">
                            <!-- Character Avatar -->
                            <div class="relative">
                              <div 
                                class="w-12 h-12 rounded-full border-2 flex items-center justify-center"
                                :class="character.isAlive ? 'border-blue-400 bg-blue-500/20' : 'border-gray-400 bg-gray-500/20'"
                              >
                                <Icon :name="character.icon" class="w-6 h-6" :class="character.isAlive ? 'text-blue-300' : 'text-gray-400'" />
                              </div>
                              
                              <!-- Status Effects -->
                              <div v-if="character.statusEffects.length > 0" class="absolute -top-1 -right-1 flex space-x-1">
                                <div 
                                  v-for="effect in character.statusEffects" 
                                  :key="effect.type"
                                  class="w-3 h-3 rounded-full border border-white/50"
                                  :class="effect.color"
                                  :title="effect.name"
                                />
                              </div>
                            </div>
                            
                            <!-- Character Info -->
                            <div class="flex-1 min-w-0">
                              <h4 class="text-sm font-medieval text-foreground truncate">{{ character.name }}</h4>
                              <p class="text-xs text-muted-foreground">{{ character.class }}</p>
                              
                              <!-- Health Bar -->
                              <div class="mt-2 space-y-1">
                                <div class="flex justify-between text-xs">
                                  <span class="text-red-400">HP</span>
                                  <span class="text-red-400">{{ character.currentHp }}/{{ character.maxHp }}</span>
                                </div>
                                <div class="w-full h-2 bg-background/50 rounded-full overflow-hidden">
                                  <div 
                                    class="h-full bg-gradient-to-r from-red-500 to-red-400 transition-all duration-500"
                                    :style="{ width: (character.currentHp / character.maxHp * 100) + '%' }"
                                  />
                                </div>
                              </div>
                              
                              <!-- Mana Bar -->
                              <div class="mt-1 space-y-1">
                                <div class="flex justify-between text-xs">
                                  <span class="text-blue-400">MP</span>
                                  <span class="text-blue-400">{{ character.currentMp }}/{{ character.maxMp }}</span>
                                </div>
                                <div class="w-full h-2 bg-background/50 rounded-full overflow-hidden">
                                  <div 
                                    class="h-full bg-gradient-to-r from-blue-500 to-blue-400 transition-all duration-500"
                                    :style="{ width: (character.currentMp / character.maxMp * 100) + '%' }"
                                  />
                                </div>
                              </div>
                            </div>
                          </div>
                        </Card3D>
                        
                        <template #magnified>
                          <div class="character-details bg-black/95 text-white p-3 rounded-lg">
                            <h4 class="font-medieval text-sm mb-2">{{ character.name }}</h4>
                            <div class="grid grid-cols-2 gap-2 text-xs">
                              <div><strong>ATK:</strong> {{ character.attack }}</div>
                              <div><strong>DEF:</strong> {{ character.defense }}</div>
                              <div><strong>SPD:</strong> {{ character.speed }}</div>
                              <div><strong>LCK:</strong> {{ character.luck }}</div>
                            </div>
                            <div v-if="character.statusEffects.length > 0" class="mt-2">
                              <strong class="text-xs">Effects:</strong>
                              <div class="flex flex-wrap gap-1 mt-1">
                                <span 
                                  v-for="effect in character.statusEffects" 
                                  :key="effect.type"
                                  class="text-xs px-1 rounded"
                                  :class="effect.textColor"
                                >
                                  {{ effect.name }}
                                </span>
                              </div>
                            </div>
                          </div>
                        </template>
                      </Lens>
                    </div>
                  </div>
                </div>
              </BorderBeam>
            </div>
            
            <!-- Battle Field -->
            <div class="xl:col-span-2 battle-field">
              <BorderBeam 
                class="bg-gradient-to-br from-amber-900/20 to-amber-800/20 rounded-xl p-6"
                :border-width="3"
                color-from="#ffd700"
                color-to="#b8860b"
              >
                <div class="space-y-6">
                  <!-- Battle Field Grid -->
                  <div class="battle-grid-field relative">
                    <div class="grid grid-cols-8 grid-rows-6 gap-1 aspect-video bg-gradient-to-br from-amber-900/10 to-amber-800/10 rounded-lg p-2">
                      <div 
                        v-for="(cell, index) in battleGrid" 
                        :key="index"
                        class="battle-cell relative border border-amber-700/30 rounded transition-all duration-200"
                        :class="[
                          cell.type,
                          { 
                            'cell-highlighted': highlightedCells.includes(index),
                            'cell-target': targetCells.includes(index),
                            'cell-movement': movementCells.includes(index)
                          }
                        ]"
                        @click="handleCellClick(index)"
                        @mouseenter="handleCellHover(index)"
                      >
                        <!-- Cell Content -->
                        <div v-if="cell.character" class="absolute inset-0 flex items-center justify-center">
                          <div 
                            class="w-8 h-8 rounded-full border-2 flex items-center justify-center"
                            :class="cell.character.team === 'player' ? 'border-blue-400 bg-blue-500/30' : 'border-red-400 bg-red-500/30'"
                          >
                            <Icon :name="cell.character.icon" class="w-4 h-4 text-white" />
                          </div>
                        </div>
                        
                        <!-- Terrain Effects -->
                        <div v-if="cell.terrain" class="absolute inset-0 flex items-center justify-center opacity-30">
                          <Icon :name="cell.terrain.icon" class="w-3 h-3" :class="cell.terrain.color" />
                        </div>
                      </div>
                    </div>
                    
                    <!-- Battle Effects Overlay -->
                    <div class="absolute inset-0 pointer-events-none">
                      <div 
                        v-for="effect in battleEffects" 
                        :key="effect.id"
                        class="battle-effect absolute"
                        :style="effect.style"
                      >
                        <div class="effect-animation" :class="effect.animation">
                          {{ effect.symbol }}
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Action Log -->
                  <div class="action-log">
                    <h3 class="text-lg font-medieval text-foreground mb-3">Battle Log</h3>
                    <div class="space-y-2 max-h-32 overflow-y-auto">
                      <div 
                        v-for="log in battleLog" 
                        :key="log.id"
                        class="log-entry text-sm p-2 rounded bg-background/30"
                        :class="log.type"
                      >
                        <span class="text-muted-foreground">{{ log.turn }}:</span>
                        <span class="ml-2" :class="log.textColor">{{ log.message }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </BorderBeam>
            </div>
            
            <!-- Enemy Party -->
            <div class="party-panel enemy-party">
              <BorderBeam 
                class="bg-gradient-to-br from-red-900/30 to-red-800/30 rounded-xl p-4"
                :border-width="2"
                color-from="#ef4444"
                color-to="#dc2626"
              >
                <div class="space-y-4">
                  <HyperText 
                    text="Enemies"
                    class="text-xl font-medieval text-foreground text-center"
                    :animation-duration="1000"
                  />
                  
                  <div class="space-y-3">
                    <div 
                      v-for="enemy in enemyParty" 
                      :key="enemy.id"
                      class="character-card enemy-card"
                      @click="selectTarget(enemy)"
                    >
                      <Card3D 
                        class="character-card-inner p-3 rounded-lg transition-all duration-300"
                        :class="enemy.isAlive ? 'bg-gradient-to-br from-red-600/50 to-red-700/50' : 'bg-gradient-to-br from-gray-600/50 to-gray-700/50'"
                        :rotation-intensity="enemy.isAlive ? 10 : 2"
                      >
                        <div class="flex items-center space-x-3">
                          <!-- Enemy Avatar -->
                          <div class="relative">
                            <div 
                              class="w-12 h-12 rounded-full border-2 flex items-center justify-center"
                              :class="enemy.isAlive ? 'border-red-400 bg-red-500/20' : 'border-gray-400 bg-gray-500/20'"
                            >
                              <Icon :name="enemy.icon" class="w-6 h-6" :class="enemy.isAlive ? 'text-red-300' : 'text-gray-400'" />
                            </div>
                            
                            <!-- Threat Level -->
                            <div class="absolute -top-1 -right-1 w-4 h-4 rounded-full border border-white/50 flex items-center justify-center text-xs font-bold"
                                 :class="enemy.threatLevel.color">
                              {{ enemy.threatLevel.symbol }}
                            </div>
                          </div>
                          
                          <!-- Enemy Info -->
                          <div class="flex-1 min-w-0">
                            <h4 class="text-sm font-medieval text-foreground truncate">{{ enemy.name }}</h4>
                            <p class="text-xs text-muted-foreground">{{ enemy.type }}</p>
                            
                            <!-- Health Bar -->
                            <div class="mt-2">
                              <div class="w-full h-2 bg-background/50 rounded-full overflow-hidden">
                                <div 
                                  class="h-full bg-gradient-to-r from-red-500 to-red-400 transition-all duration-500"
                                  :style="{ width: (enemy.currentHp / enemy.maxHp * 100) + '%' }"
                                />
                              </div>
                            </div>
                          </div>
                        </div>
                      </Card3D>
                    </div>
                  </div>
                </div>
              </BorderBeam>
            </div>
          </div>
        </BorderBeam>
      </section>

      <!-- Action Panel -->
      <section v-if="activeCharacter && battlePhase === 'Player Turn'">
        <BorderBeam 
          class="action-panel bg-card/90 backdrop-blur-md rounded-xl p-6"
          :border-width="2"
          color-from="#ffd700"
          color-to="#b8860b"
        >
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <HyperText 
                :text="`${activeCharacter.name}'s Turn`"
                class="text-xl font-medieval text-foreground"
                :animation-duration="800"
              />
              
              <div class="flex items-center space-x-2">
                <Icon name="clock" class="w-4 h-4 text-yellow-400" />
                <span class="text-sm font-medieval text-muted-foreground">{{ turnTimer }}s</span>
              </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <RippleButton 
                v-for="action in availableActions" 
                :key="action.id"
                class="action-button p-4 text-center space-y-2"
                :class="[action.buttonClass, { 'opacity-50 cursor-not-allowed': !action.available }]"
                :ripple-color="action.rippleColor"
                :disabled="!action.available"
                @click="selectAction(action)"
              >
                <Icon :name="action.icon" class="w-6 h-6 mx-auto" />
                <div>
                  <p class="text-sm font-medieval">{{ action.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ action.cost }}</p>
                </div>
              </RippleButton>
            </div>
            
            <!-- Selected Action Details -->
            <div v-if="selectedAction" class="selected-action-details">
              <BorderBeam 
                class="bg-background/50 rounded-lg p-4"
                :border-width="1"
                color-from="#ffd700"
                color-to="#b8860b"
              >
                <div class="space-y-3">
                  <div class="flex items-center space-x-3">
                    <Icon :name="selectedAction.icon" class="w-6 h-6 text-primary" />
                    <div>
                      <h4 class="font-medieval text-foreground">{{ selectedAction.name }}</h4>
                      <p class="text-sm text-muted-foreground">{{ selectedAction.description }}</p>
                    </div>
                  </div>
                  
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                    <div v-if="selectedAction.damage">
                      <Icon name="sword" class="w-4 h-4 text-red-400 mx-auto" />
                      <p class="text-sm font-medieval text-red-400">{{ selectedAction.damage }}</p>
                    </div>
                    <div v-if="selectedAction.range">
                      <Icon name="target" class="w-4 h-4 text-yellow-400 mx-auto" />
                      <p class="text-sm font-medieval text-yellow-400">{{ selectedAction.range }}</p>
                    </div>
                    <div v-if="selectedAction.accuracy">
                      <Icon name="eye" class="w-4 h-4 text-blue-400 mx-auto" />
                      <p class="text-sm font-medieval text-blue-400">{{ selectedAction.accuracy }}%</p>
                    </div>
                    <div v-if="selectedAction.cooldown">
                      <Icon name="clock" class="w-4 h-4 text-purple-400 mx-auto" />
                      <p class="text-sm font-medieval text-purple-400">{{ selectedAction.cooldown }}T</p>
                    </div>
                  </div>
                  
                  <div class="flex space-x-3">
                    <RippleButton 
                      class="flex-1 faction-empire font-medieval"
                      ripple-color="rgb(255, 215, 0)"
                      @click="executeAction"
                    >
                      Execute Action
                    </RippleButton>
                    
                    <ShimmerButton 
                      class="px-6 py-2 bg-secondary text-secondary-foreground font-medieval"
                      shimmer-color="rgba(139, 69, 19, 0.5)"
                      @click="cancelAction"
                    >
                      Cancel
                    </ShimmerButton>
                  </div>
                </div>
              </BorderBeam>
            </div>
          </div>
        </BorderBeam>
      </section>
    </div>
  </div>
</template><script setup lang="ts">
// Page metadata
useHead({
  title: 'Battle Arena - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Engage in tactical turn-based combat with advanced battle mechanics and stunning visual effects.' }
  ]
})

// Battle state
const currentTurn = ref(1)
const battleTimer = ref(180)
const turnTimer = ref(30)
const battlePhase = ref('Player Turn')
const activeCharacter = ref(null)
const selectedAction = ref(null)
const selectedTarget = ref(null)

// Grid and positioning
const battleGrid = ref(Array(48).fill(null).map((_, index) => ({
  index,
  type: 'normal',
  character: null,
  terrain: Math.random() < 0.1 ? {
    type: 'obstacle',
    icon: 'mountain',
    color: 'text-gray-500'
  } : null
})))

const highlightedCells = ref([])
const targetCells = ref([])
const movementCells = ref([])

// Player party
const playerParty = ref([
  {
    id: 'player-1',
    name: 'Sir Marcus',
    class: 'Knight',
    icon: 'sword',
    team: 'player',
    isAlive: true,
    currentHp: 85,
    maxHp: 100,
    currentMp: 45,
    maxMp: 50,
    attack: 75,
    defense: 80,
    speed: 60,
    luck: 55,
    position: { x: 1, y: 2 },
    statusEffects: [
      { type: 'blessed', name: 'Blessed', color: 'bg-yellow-400', textColor: 'text-yellow-400' }
    ]
  },
  {
    id: 'player-2',
    name: 'Elara',
    class: 'Mage',
    icon: 'sparkles',
    team: 'player',
    isAlive: true,
    currentHp: 60,
    maxHp: 70,
    currentMp: 80,
    maxMp: 100,
    attack: 90,
    defense: 40,
    speed: 70,
    luck: 65,
    position: { x: 0, y: 3 },
    statusEffects: [
      { type: 'mana_shield', name: 'Mana Shield', color: 'bg-blue-400', textColor: 'text-blue-400' }
    ]
  },
  {
    id: 'player-3',
    name: 'Grimjaw',
    class: 'Berserker',
    icon: 'hammer',
    team: 'player',
    isAlive: true,
    currentHp: 95,
    maxHp: 120,
    currentMp: 20,
    maxMp: 30,
    attack: 95,
    defense: 60,
    speed: 75,
    luck: 45,
    position: { x: 2, y: 1 },
    statusEffects: [
      { type: 'rage', name: 'Berserker Rage', color: 'bg-red-400', textColor: 'text-red-400' }
    ]
  },
  {
    id: 'player-4',
    name: 'Thorgrim',
    class: 'Ranger',
    icon: 'bow',
    team: 'player',
    isAlive: false,
    currentHp: 0,
    maxHp: 80,
    currentMp: 40,
    maxMp: 60,
    attack: 70,
    defense: 65,
    speed: 85,
    luck: 70,
    position: { x: 1, y: 4 },
    statusEffects: []
  }
])

// Enemy party
const enemyParty = ref([
  {
    id: 'enemy-1',
    name: 'Orc Warboss',
    type: 'Elite',
    icon: 'skull',
    team: 'enemy',
    isAlive: true,
    currentHp: 140,
    maxHp: 160,
    attack: 85,
    defense: 70,
    speed: 50,
    position: { x: 6, y: 2 },
    threatLevel: { symbol: '★', color: 'bg-red-500' }
  },
  {
    id: 'enemy-2',
    name: 'Goblin Shaman',
    type: 'Caster',
    icon: 'flame',
    team: 'enemy',
    isAlive: true,
    currentHp: 45,
    maxHp: 60,
    attack: 60,
    defense: 30,
    speed: 65,
    position: { x: 7, y: 4 },
    threatLevel: { symbol: '◆', color: 'bg-purple-500' }
  },
  {
    id: 'enemy-3',
    name: 'Orc Warrior',
    type: 'Melee',
    icon: 'sword',
    team: 'enemy',
    isAlive: true,
    currentHp: 80,
    maxHp: 90,
    attack: 70,
    defense: 60,
    speed: 55,
    position: { x: 5, y: 1 },
    threatLevel: { symbol: '●', color: 'bg-orange-500' }
  },
  {
    id: 'enemy-4',
    name: 'Goblin Archer',
    type: 'Ranged',
    icon: 'bow',
    team: 'enemy',
    isAlive: true,
    currentHp: 35,
    maxHp: 50,
    attack: 55,
    defense: 35,
    speed: 80,
    position: { x: 7, y: 0 },
    threatLevel: { symbol: '▲', color: 'bg-green-500' }
  }
])

// Available actions
const availableActions = ref([
  {
    id: 'attack',
    name: 'Attack',
    icon: 'sword',
    cost: '0 MP',
    available: true,
    buttonClass: 'bg-red-600 text-white',
    rippleColor: 'rgba(220, 38, 38, 0.6)',
    description: 'Basic melee attack against adjacent enemies',
    damage: '75-85',
    range: '1',
    accuracy: 85,
    cooldown: 0
  },
  {
    id: 'defend',
    name: 'Defend',
    icon: 'shield',
    cost: '0 MP',
    available: true,
    buttonClass: 'bg-blue-600 text-white',
    rippleColor: 'rgba(37, 99, 235, 0.6)',
    description: 'Increase defense and reduce incoming damage',
    damage: null,
    range: 'Self',
    accuracy: 100,
    cooldown: 0
  },
  {
    id: 'spell',
    name: 'Cast Spell',
    icon: 'sparkles',
    cost: '15 MP',
    available: true,
    buttonClass: 'bg-purple-600 text-white',
    rippleColor: 'rgba(147, 51, 234, 0.6)',
    description: 'Cast a magical spell with various effects',
    damage: '90-110',
    range: '3',
    accuracy: 75,
    cooldown: 2
  },
  {
    id: 'move',
    name: 'Move',
    icon: 'footprints',
    cost: '0 MP',
    available: true,
    buttonClass: 'bg-green-600 text-white',
    rippleColor: 'rgba(34, 197, 94, 0.6)',
    description: 'Move to a different position on the battlefield',
    damage: null,
    range: '3',
    accuracy: 100,
    cooldown: 0
  },
  {
    id: 'item',
    name: 'Use Item',
    icon: 'package',
    cost: '1 Item',
    available: true,
    buttonClass: 'bg-yellow-600 text-white',
    rippleColor: 'rgba(245, 158, 11, 0.6)',
    description: 'Use a consumable item from inventory',
    damage: null,
    range: 'Varies',
    accuracy: 100,
    cooldown: 0
  },
  {
    id: 'special',
    name: 'Special',
    icon: 'zap',
    cost: '25 MP',
    available: false,
    buttonClass: 'bg-orange-600 text-white',
    rippleColor: 'rgba(234, 88, 12, 0.6)',
    description: 'Powerful special ability unique to this character',
    damage: '120-150',
    range: '2',
    accuracy: 90,
    cooldown: 5
  }
])

// Battle log
const battleLog = ref([
  {
    id: 1,
    turn: 1,
    message: 'Battle begins! Sir Marcus takes the initiative.',
    type: 'info',
    textColor: 'text-blue-400'
  },
  {
    id: 2,
    turn: 1,
    message: 'Orc Warboss roars menacingly, intimidating nearby enemies.',
    type: 'enemy',
    textColor: 'text-red-400'
  },
  {
    id: 3,
    turn: 1,
    message: 'Elara casts Mana Shield, protecting herself from magical attacks.',
    type: 'player',
    textColor: 'text-green-400'
  }
])

// Battle effects
const battleEffects = ref([])
let effectId = 0

// Methods
const selectCharacter = (character: any) => {
  if (character.isAlive && character.team === 'player') {
    activeCharacter.value = character
    highlightMovementRange(character)
  }
}

const selectTarget = (target: any) => {
  selectedTarget.value = target
  highlightTargetCells([target.position])
}

const selectAction = (action: any) => {
  if (!action.available) return
  
  selectedAction.value = action
  
  // Highlight valid targets/cells based on action
  if (action.id === 'move') {
    highlightMovementRange(activeCharacter.value)
  } else if (action.id === 'attack' || action.id === 'spell') {
    highlightAttackRange(action)
  }
}

const executeAction = () => {
  if (!selectedAction.value || !activeCharacter.value) return
  
  // Execute the selected action
  console.log(`${activeCharacter.value.name} uses ${selectedAction.value.name}`)
  
  // Add battle effect
  createBattleEffect(selectedAction.value)
  
  // Add to battle log
  addToBattleLog(`${activeCharacter.value.name} uses ${selectedAction.value.name}!`, 'player')
  
  // Reset selection
  selectedAction.value = null
  selectedTarget.value = null
  clearHighlights()
  
  // Next turn
  nextTurn()
}

const cancelAction = () => {
  selectedAction.value = null
  selectedTarget.value = null
  clearHighlights()
}

const handleCellClick = (index: number) => {
  const cell = battleGrid.value[index]
  
  if (selectedAction.value?.id === 'move' && movementCells.value.includes(index)) {
    // Move character
    moveCharacter(activeCharacter.value, index)
  } else if (selectedAction.value?.id === 'attack' && targetCells.value.includes(index)) {
    // Attack target
    executeAttack(index)
  }
}

const handleCellHover = (index: number) => {
  // Show preview of action effects
  if (selectedAction.value) {
    previewActionEffect(index)
  }
}

const highlightMovementRange = (character: any) => {
  const range = character.speed / 20 // Movement range based on speed
  movementCells.value = getValidMovementCells(character.position, range)
}

const highlightAttackRange = (action: any) => {
  const range = parseInt(action.range) || 1
  targetCells.value = getValidTargetCells(activeCharacter.value.position, range)
}

const highlightTargetCells = (positions: any[]) => {
  targetCells.value = positions.map(pos => pos.x + pos.y * 8)
}

const clearHighlights = () => {
  highlightedCells.value = []
  targetCells.value = []
  movementCells.value = []
}

const getValidMovementCells = (position: any, range: number) => {
  const cells = []
  for (let x = Math.max(0, position.x - range); x <= Math.min(7, position.x + range); x++) {
    for (let y = Math.max(0, position.y - range); y <= Math.min(5, position.y + range); y++) {
      const distance = Math.abs(x - position.x) + Math.abs(y - position.y)
      if (distance <= range && distance > 0) {
        const index = x + y * 8
        if (!battleGrid.value[index].character) {
          cells.push(index)
        }
      }
    }
  }
  return cells
}

const getValidTargetCells = (position: any, range: number) => {
  const cells = []
  enemyParty.value.forEach(enemy => {
    if (enemy.isAlive) {
      const distance = Math.abs(enemy.position.x - position.x) + Math.abs(enemy.position.y - position.y)
      if (distance <= range) {
        cells.push(enemy.position.x + enemy.position.y * 8)
      }
    }
  })
  return cells
}

const moveCharacter = (character: any, targetIndex: number) => {
  const x = targetIndex % 8
  const y = Math.floor(targetIndex / 8)
  
  character.position = { x, y }
  addToBattleLog(`${character.name} moves to position (${x}, ${y})`, 'player')
  
  executeAction()
}

const executeAttack = (targetIndex: number) => {
  const target = findCharacterAtPosition(targetIndex)
  if (target) {
    const damage = Math.floor(Math.random() * 20) + 60 // Random damage
    target.currentHp = Math.max(0, target.currentHp - damage)
    
    if (target.currentHp === 0) {
      target.isAlive = false
      addToBattleLog(`${target.name} is defeated!`, 'combat')
    } else {
      addToBattleLog(`${target.name} takes ${damage} damage!`, 'combat')
    }
    
    createDamageEffect(targetIndex, damage)
  }
  
  executeAction()
}

const findCharacterAtPosition = (index: number) => {
  const x = index % 8
  const y = Math.floor(index / 8)
  
  return [...playerParty.value, ...enemyParty.value].find(char => 
    char.position.x === x && char.position.y === y && char.isAlive
  )
}

const createBattleEffect = (action: any) => {
  const effect = {
    id: effectId++,
    symbol: getActionSymbol(action.id),
    animation: getActionAnimation(action.id),
    style: {
      left: Math.random() * 80 + 10 + '%',
      top: Math.random() * 60 + 20 + '%',
      fontSize: '2rem',
      color: getActionColor(action.id)
    }
  }
  
  battleEffects.value.push(effect)
  
  setTimeout(() => {
    battleEffects.value = battleEffects.value.filter(e => e.id !== effect.id)
  }, 2000)
}

const createDamageEffect = (position: number, damage: number) => {
  const x = (position % 8) * 12.5 + 6.25
  const y = Math.floor(position / 8) * 16.67 + 8.33
  
  const effect = {
    id: effectId++,
    symbol: `-${damage}`,
    animation: 'damage-float',
    style: {
      left: x + '%',
      top: y + '%',
      fontSize: '1.5rem',
      color: '#ef4444',
      fontWeight: 'bold'
    }
  }
  
  battleEffects.value.push(effect)
  
  setTimeout(() => {
    battleEffects.value = battleEffects.value.filter(e => e.id !== effect.id)
  }, 1500)
}

const getActionSymbol = (actionId: string) => {
  const symbols = {
    attack: '⚔️',
    defend: '🛡️',
    spell: '✨',
    move: '👣',
    item: '📦',
    special: '💥'
  }
  return symbols[actionId] || '❓'
}

const getActionAnimation = (actionId: string) => {
  const animations = {
    attack: 'attack-slash',
    defend: 'defend-glow',
    spell: 'spell-sparkle',
    move: 'move-trail',
    item: 'item-use',
    special: 'special-burst'
  }
  return animations[actionId] || 'default-effect'
}

const getActionColor = (actionId: string) => {
  const colors = {
    attack: '#ef4444',
    defend: '#3b82f6',
    spell: '#8b5cf6',
    move: '#22c55e',
    item: '#f59e0b',
    special: '#f97316'
  }
  return colors[actionId] || '#6b7280'
}

const addToBattleLog = (message: string, type: string) => {
  const logEntry = {
    id: Date.now(),
    turn: currentTurn.value,
    message,
    type,
    textColor: type === 'player' ? 'text-green-400' : type === 'enemy' ? 'text-red-400' : 'text-yellow-400'
  }
  
  battleLog.value.unshift(logEntry)
  
  // Keep only last 10 entries
  if (battleLog.value.length > 10) {
    battleLog.value = battleLog.value.slice(0, 10)
  }
}

const nextTurn = () => {
  // Simple turn progression
  currentTurn.value++
  turnTimer.value = 30
  
  // Switch between player and enemy turns
  battlePhase.value = battlePhase.value === 'Player Turn' ? 'Enemy Turn' : 'Player Turn'
  
  if (battlePhase.value === 'Player Turn') {
    // Select next alive player character
    const aliveCharacters = playerParty.value.filter(char => char.isAlive)
    if (aliveCharacters.length > 0) {
      activeCharacter.value = aliveCharacters[0]
    }
  } else {
    // AI enemy turn
    setTimeout(() => {
      executeEnemyTurn()
    }, 1000)
  }
}

const executeEnemyTurn = () => {
  const aliveEnemies = enemyParty.value.filter(enemy => enemy.isAlive)
  
  if (aliveEnemies.length > 0) {
    const enemy = aliveEnemies[Math.floor(Math.random() * aliveEnemies.length)]
    const target = playerParty.value.find(char => char.isAlive)
    
    if (target) {
      const damage = Math.floor(Math.random() * 25) + 15
      target.currentHp = Math.max(0, target.currentHp - damage)
      
      addToBattleLog(`${enemy.name} attacks ${target.name} for ${damage} damage!`, 'enemy')
      
      if (target.currentHp === 0) {
        target.isAlive = false
        addToBattleLog(`${target.name} is defeated!`, 'combat')
      }
    }
  }
  
  // End enemy turn
  setTimeout(() => {
    nextTurn()
  }, 1500)
}

const previewActionEffect = (index: number) => {
  // Show preview of what would happen if action is executed at this position
  // This could highlight damage numbers, movement paths, etc.
}

// Initialize battle
onMounted(() => {
  console.log('Battle system initialized')
  
  // Set initial active character
  const firstAliveCharacter = playerParty.value.find(char => char.isAlive)
  if (firstAliveCharacter) {
    activeCharacter.value = firstAliveCharacter
  }
  
  // Place characters on grid
  playerParty.value.forEach(char => {
    const index = char.position.x + char.position.y * 8
    battleGrid.value[index].character = char
  })
  
  enemyParty.value.forEach(enemy => {
    const index = enemy.position.x + enemy.position.y * 8
    battleGrid.value[index].character = enemy
  })
  
  // Start battle timer
  const battleInterval = setInterval(() => {
    battleTimer.value--
    if (battleTimer.value <= 0) {
      clearInterval(battleInterval)
      // Battle timeout logic
    }
  }, 1000)
  
  // Start turn timer
  const turnInterval = setInterval(() => {
    if (battlePhase.value === 'Player Turn') {
      turnTimer.value--
      if (turnTimer.value <= 0) {
        // Auto-skip turn
        nextTurn()
      }
    }
  }, 1000)
})
</script>

<style scoped>
/* Battle-specific animations and styles */
.battle-page {
  background-attachment: fixed;
}

.character-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.character-card:hover {
  transform: scale(1.05);
}

.character-card.active-character {
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.6);
  border: 2px solid rgb(59, 130, 246);
}

.enemy-card:hover {
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.6);
}

.battle-cell {
  aspect-ratio: 1;
  cursor: pointer;
  transition: all 0.2s ease;
}

.battle-cell:hover {
  background-color: rgba(255, 215, 0, 0.2);
}

.battle-cell.cell-highlighted {
  background-color: rgba(59, 130, 246, 0.3);
  border-color: rgb(59, 130, 246);
}

.battle-cell.cell-target {
  background-color: rgba(239, 68, 68, 0.3);
  border-color: rgb(239, 68, 68);
}

.battle-cell.cell-movement {
  background-color: rgba(34, 197, 94, 0.3);
  border-color: rgb(34, 197, 94);
}

.action-button {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.battle-effect {
  pointer-events: none;
  z-index: 100;
}

.effect-animation {
  animation-fill-mode: forwards;
}

.effect-animation.attack-slash {
  animation: attack-slash 0.8s ease-out;
}

.effect-animation.defend-glow {
  animation: defend-glow 1s ease-in-out;
}

.effect-animation.spell-sparkle {
  animation: spell-sparkle 1.5s ease-out;
}

.effect-animation.move-trail {
  animation: move-trail 1s ease-out;
}

.effect-animation.damage-float {
  animation: damage-float 1.5s ease-out;
}

.effect-animation.special-burst {
  animation: special-burst 2s ease-out;
}

/* Battle effect animations */
@keyframes attack-slash {
  0% {
    transform: scale(0) rotate(-45deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.5) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: scale(0.5) rotate(45deg);
    opacity: 0;
  }
}

@keyframes defend-glow {
  0%, 100% {
    transform: scale(1);
    opacity: 0.5;
  }
  50% {
    transform: scale(1.2);
    opacity: 1;
  }
}

@keyframes spell-sparkle {
  0% {
    transform: scale(0) rotate(0deg);
    opacity: 0;
  }
  25% {
    transform: scale(1) rotate(90deg);
    opacity: 1;
  }
  75% {
    transform: scale(1.5) rotate(270deg);
    opacity: 0.8;
  }
  100% {
    transform: scale(0) rotate(360deg);
    opacity: 0;
  }
}

@keyframes move-trail {
  0% {
    transform: translateX(-50px) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateX(50px) scale(0);
    opacity: 0;
  }
}

@keyframes damage-float {
  0% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateY(-50px) scale(1.2);
    opacity: 0;
  }
}

@keyframes special-burst {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  50% {
    transform: scale(2);
    opacity: 0.8;
  }
  100% {
    transform: scale(4);
    opacity: 0;
  }
}

.log-entry {
  animation: log-slide-in 0.3s ease-out;
}

@keyframes log-slide-in {
  0% {
    transform: translateX(-20px);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Responsive design */
@media (max-width: 1280px) {
  .battle-grid-field {
    transform: scale(0.8);
  }
}

@media (max-width: 768px) {
  .battle-grid-field {
    transform: scale(0.6);
  }
  
  .action-button {
    padding: 0.75rem;
  }
}

/* Performance optimizations */
.character-card,
.battle-cell,
.action-button,
.battle-effect {
  will-change: transform;
}
</style>