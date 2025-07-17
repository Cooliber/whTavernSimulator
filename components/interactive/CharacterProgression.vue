<template>
  <div class="character-progression">
    <!-- Character Overview -->
    <div class="character-overview card-enhanced mb-6 p-6">
      <div class="flex items-center justify-between mb-6">
        <div class="character-info flex items-center space-x-4">
          <div class="character-avatar">
            <div class="w-16 h-16 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center">
              <Icon name="user" class="w-8 h-8 text-primary" />
            </div>
          </div>
          <div>
            <h2 class="font-medieval text-2xl text-foreground">{{ character.name }}</h2>
            <p class="text-muted-foreground font-sharp">Level {{ character.level }} Adventurer</p>
            <div class="flex items-center space-x-2 mt-1">
              <span v-for="title in character.titles" :key="title" 
                class="text-xs px-2 py-1 rounded-full bg-accent/20 text-accent font-medieval">
                {{ title }}
              </span>
            </div>
          </div>
        </div>
        
        <div class="character-stats text-right">
          <div class="stat-item">
            <span class="font-medieval text-sm text-muted-foreground">Experience:</span>
            <span class="font-bold text-primary ml-2">{{ character.experience }}</span>
          </div>
          <div class="stat-item">
            <span class="font-medieval text-sm text-muted-foreground">Next Level:</span>
            <span class="font-bold text-accent ml-2">{{ character.experienceToNext }}</span>
          </div>
        </div>
      </div>

      <!-- Experience Progress Bar -->
      <div class="experience-progress">
        <div class="flex justify-between items-center mb-2">
          <span class="font-medieval text-sm text-foreground">Progress to Level {{ character.level + 1 }}</span>
          <span class="text-sm text-muted-foreground">
            {{ Math.floor(experienceProgress * 100) }}%
          </span>
        </div>
        <div class="w-full bg-muted/20 rounded-full h-3">
          <div 
            class="bg-gradient-to-r from-primary to-accent h-3 rounded-full transition-all duration-500"
            :style="{ width: `${experienceProgress * 100}%` }"
          ></div>
        </div>
      </div>
    </div>

    <!-- Attributes Section -->
    <div class="attributes-section card-enhanced mb-6 p-6">
      <h3 class="font-medieval text-xl text-foreground mb-4">Attributes</h3>
      <div class="attributes-grid grid grid-cols-2 md:grid-cols-3 gap-4">
        <div
          v-for="(value, attribute) in character.attributes"
          :key="attribute"
          class="attribute-item p-4 bg-card/30 rounded-lg text-center"
        >
          <div class="attribute-name font-medieval text-sm text-muted-foreground uppercase mb-2">
            {{ attribute }}
          </div>
          <div class="attribute-value text-2xl font-bold text-primary mb-2">
            {{ value }}
          </div>
          <div class="attribute-modifier text-sm text-accent">
            {{ getAttributeModifier(value) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Skills Section -->
    <div class="skills-section card-enhanced mb-6 p-6">
      <h3 class="font-medieval text-xl text-foreground mb-4">Skills</h3>
      <div class="skills-grid grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="(value, skill) in character.skills"
          :key="skill"
          class="skill-item p-3 bg-card/30 rounded-lg"
        >
          <div class="flex justify-between items-center mb-2">
            <span class="font-medieval text-sm text-foreground">{{ skill }}</span>
            <span class="font-bold text-primary">{{ value }}</span>
          </div>
          <div class="skill-progress w-full bg-muted/20 rounded-full h-2">
            <div 
              class="bg-gradient-to-r from-secondary to-accent h-2 rounded-full transition-all duration-300"
              :style="{ width: `${Math.min(value, 100)}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Achievements Section -->
    <div class="achievements-section card-enhanced mb-6 p-6">
      <h3 class="font-medieval text-xl text-foreground mb-4">Achievements</h3>
      <div v-if="achievements.length > 0" class="achievements-grid grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="achievement in achievements"
          :key="achievement"
          class="achievement-item p-4 bg-gradient-to-br from-accent/10 to-accent/5 rounded-lg border border-accent/20"
        >
          <div class="achievement-icon text-2xl mb-2">🏆</div>
          <div class="achievement-name font-medieval text-sm text-accent">
            {{ formatAchievementName(achievement) }}
          </div>
        </div>
      </div>
      <div v-else class="no-achievements text-center py-8">
        <Icon name="trophy" class="w-12 h-12 text-muted-foreground/50 mx-auto mb-4" />
        <p class="font-medieval text-muted-foreground">No achievements yet. Keep adventuring!</p>
      </div>
    </div>

    <!-- Level Up Modal -->
    <div v-if="isLevelingUp" class="level-up-modal fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="level-up-content card-enhanced max-w-md mx-4">
        <div class="level-up-header text-center mb-6">
          <div class="level-up-icon w-20 h-20 mx-auto rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-4xl mb-4">
            ⭐
          </div>
          <h3 class="font-fantasy text-2xl text-primary heading-glow">Level Up!</h3>
          <p class="font-medieval text-muted-foreground">You have reached level {{ character.level }}</p>
        </div>

        <div class="upgrade-options space-y-3">
          <h4 class="font-medieval text-lg text-foreground mb-3">Choose an upgrade:</h4>
          <button
            v-for="upgrade in availableUpgrades"
            :key="upgrade"
            @click="selectUpgrade(upgrade)"
            class="upgrade-option w-full p-4 bg-card/50 rounded-lg border border-border hover:border-primary/50 transition-all duration-200 text-left"
          >
            <div class="upgrade-title font-medieval text-foreground mb-1">
              {{ formatUpgradeName(upgrade) }}
            </div>
            <div class="upgrade-description text-sm text-muted-foreground">
              {{ getUpgradeDescription(upgrade) }}
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="recent-activity card-enhanced p-6">
      <h3 class="font-medieval text-xl text-foreground mb-4">Recent Activity</h3>
      <div class="activity-list space-y-3">
        <div
          v-for="activity in recentActivities"
          :key="activity.id"
          class="activity-item p-3 bg-card/30 rounded-lg flex items-center space-x-3"
        >
          <div class="activity-icon">
            <Icon :name="getActivityIcon(activity.type)" class="w-5 h-5 text-accent" />
          </div>
          <div class="activity-content flex-1">
            <div class="activity-description font-sharp text-sm text-foreground">
              {{ activity.description }}
            </div>
            <div class="activity-time text-xs text-muted-foreground">
              {{ formatActivityTime(activity.timestamp) }}
            </div>
          </div>
          <div v-if="activity.experience" class="activity-reward">
            <span class="text-xs text-primary">+{{ activity.experience }} XP</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Activity {
  id: string
  type: 'conversation' | 'mini_game' | 'quest' | 'achievement' | 'level_up'
  description: string
  timestamp: Date
  experience?: number
}

// Composables
const { 
  playerCharacter: character, 
  isLevelingUp, 
  availableUpgrades,
  selectUpgrade,
  checkAchievements
} = useEnhancedUserEngagement()

// Reactive state
const recentActivities = ref<Activity[]>([
  {
    id: '1',
    type: 'conversation',
    description: 'Had a meaningful conversation with Magnus the Bold',
    timestamp: new Date(Date.now() - 5 * 60 * 1000),
    experience: 10
  },
  {
    id: '2',
    type: 'mini_game',
    description: 'Won a dice game against local patrons',
    timestamp: new Date(Date.now() - 15 * 60 * 1000),
    experience: 15
  },
  {
    id: '3',
    type: 'achievement',
    description: 'Earned the "Social Butterfly" achievement',
    timestamp: new Date(Date.now() - 30 * 60 * 1000),
    experience: 25
  }
])

// Computed properties
const experienceProgress = computed(() => {
  const totalNeeded = character.value.experienceToNext
  const currentProgress = character.value.experience
  return Math.min(currentProgress / totalNeeded, 1)
})

const achievements = computed(() => {
  return checkAchievements()
})

// Methods
const getAttributeModifier = (value: number): string => {
  const modifier = Math.floor((value - 10) / 2)
  return modifier >= 0 ? `+${modifier}` : `${modifier}`
}

const formatAchievementName = (achievement: string): string => {
  return achievement
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const formatUpgradeName = (upgrade: string): string => {
  return upgrade
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const getUpgradeDescription = (upgrade: string): string => {
  const descriptions = {
    increase_charisma: 'Improve your ability to influence and charm others',
    increase_intelligence: 'Enhance your reasoning and knowledge capabilities',
    increase_strength: 'Boost your physical power and endurance',
    improve_persuasion: 'Become more convincing in conversations',
    improve_investigation: 'Better at uncovering secrets and solving mysteries',
    new_title: 'Earn a new title that reflects your achievements',
    special_ability: 'Unlock a unique ability based on your experiences'
  }
  
  return descriptions[upgrade as keyof typeof descriptions] || 'A mysterious upgrade awaits...'
}

const getActivityIcon = (type: string): string => {
  const icons = {
    conversation: 'message-circle',
    mini_game: 'dice',
    quest: 'scroll',
    achievement: 'trophy',
    level_up: 'star'
  }
  
  return icons[type as keyof typeof icons] || 'activity'
}

const formatActivityTime = (timestamp: Date): string => {
  const now = new Date()
  const diff = now.getTime() - timestamp.getTime()
  const minutes = Math.floor(diff / (1000 * 60))
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes} minutes ago`
  
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} hours ago`
  
  const days = Math.floor(hours / 24)
  return `${days} days ago`
}

// Add activity when experience is gained
watch(() => character.value.experience, (newExp, oldExp) => {
  if (newExp > oldExp) {
    const gainedExp = newExp - oldExp
    recentActivities.value.unshift({
      id: `activity_${Date.now()}`,
      type: 'conversation',
      description: `Gained ${gainedExp} experience`,
      timestamp: new Date(),
      experience: gainedExp
    })
    
    // Keep only last 10 activities
    if (recentActivities.value.length > 10) {
      recentActivities.value = recentActivities.value.slice(0, 10)
    }
  }
})
</script>

<style scoped>
.character-progression {
  @apply max-w-6xl mx-auto;
}

.attribute-item {
  @apply transition-all duration-300;
}

.attribute-item:hover {
  @apply transform scale-105;
}

.skill-item {
  @apply transition-all duration-300;
}

.skill-item:hover {
  @apply bg-card/50;
}

.achievement-item {
  @apply transition-all duration-300;
}

.achievement-item:hover {
  @apply transform -translate-y-0.5;
}

.level-up-modal {
  animation: fadeIn 0.3s ease-out;
}

.level-up-content {
  animation: slideInUp 0.3s ease-out;
}

.upgrade-option:hover {
  @apply transform -translate-y-px;
}

.activity-item {
  @apply transition-all duration-200;
}

.activity-item:hover {
  @apply bg-card/50;
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
  .character-overview {
    @apply flex-col space-y-4;
  }
  
  .character-info {
    @apply w-full;
  }
  
  .character-stats {
    @apply text-left;
  }
  
  .attributes-grid {
    @apply grid-cols-2;
  }
  
  .skills-grid {
    @apply grid-cols-1;
  }
  
  .achievements-grid {
    @apply grid-cols-1;
  }
}
</style>
