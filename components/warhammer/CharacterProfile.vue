<template>
  <div class="character-profile card-enhanced">
    <!-- Character Header -->
    <div class="character-header mb-6">
      <div class="flex items-center space-x-4">
        <div class="character-avatar">
          <div class="w-16 h-16 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center">
            <Icon name="user" class="w-8 h-8 text-primary" />
          </div>
        </div>
        <div class="character-info flex-1">
          <h3 class="font-medieval text-xl text-foreground heading-glow">{{ character.name }}</h3>
          <p class="text-muted-foreground font-sharp">{{ character.career?.name || 'Wanderer' }}</p>
          <div class="flex items-center space-x-2 mt-1">
            <span class="text-xs px-2 py-1 rounded-full bg-primary/20 text-primary font-medieval">
              {{ character.species || 'Human' }}
            </span>
            <span v-if="character.career?.class" class="text-xs px-2 py-1 rounded-full bg-secondary/20 text-secondary font-medieval">
              {{ character.career.class }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Character Characteristics -->
    <div v-if="character.characteristics" class="characteristics-grid mb-6">
      <h4 class="font-medieval text-lg mb-3 text-foreground">Characteristics</h4>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
        <div v-for="(value, key) in character.characteristics" :key="key" class="characteristic-stat">
          <div class="text-center p-3 bg-card/50 rounded-lg border border-border/50">
            <div class="text-xs font-medieval text-muted-foreground uppercase">{{ key }}</div>
            <div class="text-lg font-bold text-primary">{{ value || '-' }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Skills -->
    <div v-if="character.skills && character.skills.length > 0" class="skills-section mb-6">
      <h4 class="font-medieval text-lg mb-3 text-foreground">Skills</h4>
      <div class="flex flex-wrap gap-2">
        <span 
          v-for="skill in character.skills.slice(0, showAllSkills ? character.skills.length : 6)" 
          :key="skill"
          class="skill-tag px-3 py-1 bg-secondary/20 text-secondary rounded-full text-sm font-sharp"
        >
          {{ skill }}
        </span>
        <button 
          v-if="character.skills.length > 6"
          @click="showAllSkills = !showAllSkills"
          class="skill-toggle px-3 py-1 bg-muted/20 text-muted-foreground rounded-full text-sm font-sharp hover:bg-muted/30 transition-colors"
        >
          {{ showAllSkills ? 'Show Less' : `+${character.skills.length - 6} more` }}
        </button>
      </div>
    </div>

    <!-- Talents -->
    <div v-if="character.talents && character.talents.length > 0" class="talents-section mb-6">
      <h4 class="font-medieval text-lg mb-3 text-foreground">Talents</h4>
      <div class="flex flex-wrap gap-2">
        <span 
          v-for="talent in character.talents.slice(0, showAllTalents ? character.talents.length : 4)" 
          :key="talent"
          class="talent-tag px-3 py-1 bg-accent/20 text-accent rounded-full text-sm font-sharp"
        >
          {{ talent }}
        </span>
        <button 
          v-if="character.talents.length > 4"
          @click="showAllTalents = !showAllTalents"
          class="talent-toggle px-3 py-1 bg-muted/20 text-muted-foreground rounded-full text-sm font-sharp hover:bg-muted/30 transition-colors"
        >
          {{ showAllTalents ? 'Show Less' : `+${character.talents.length - 4} more` }}
        </button>
      </div>
    </div>

    <!-- Trappings -->
    <div v-if="character.trappings && character.trappings.length > 0" class="trappings-section mb-6">
      <h4 class="font-medieval text-lg mb-3 text-foreground">Equipment</h4>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
        <div 
          v-for="trapping in character.trappings.slice(0, showAllTrappings ? character.trappings.length : 6)" 
          :key="trapping"
          class="trapping-item p-2 bg-card/30 rounded border border-border/30 text-sm font-sharp text-card-foreground"
        >
          {{ trapping }}
        </div>
        <button 
          v-if="character.trappings.length > 6"
          @click="showAllTrappings = !showAllTrappings"
          class="trapping-toggle p-2 bg-muted/20 text-muted-foreground rounded border border-border/30 text-sm font-sharp hover:bg-muted/30 transition-colors"
        >
          {{ showAllTrappings ? 'Show Less' : `+${character.trappings.length - 6} more` }}
        </button>
      </div>
    </div>

    <!-- Description -->
    <div v-if="character.description" class="description-section">
      <h4 class="font-medieval text-lg mb-3 text-foreground">Background</h4>
      <div class="prose prose-sm max-w-none">
        <p class="text-muted-foreground font-sharp leading-relaxed">{{ character.description }}</p>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="character-actions mt-6 pt-4 border-t border-border/30">
      <div class="flex flex-wrap gap-3">
        <button class="btn-enhanced text-sm">
          <Icon name="dice" class="w-4 h-4 mr-2" />
          Roll Initiative
        </button>
        <button class="btn-enhanced text-sm bg-secondary/90 hover:bg-secondary">
          <Icon name="scroll" class="w-4 h-4 mr-2" />
          View Details
        </button>
        <button class="btn-enhanced text-sm bg-accent/90 hover:bg-accent">
          <Icon name="edit" class="w-4 h-4 mr-2" />
          Edit Character
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface CharacterProfileProps {
  character: {
    id?: string
    name: string
    species?: string
    career?: {
      name: string
      class?: string
    }
    characteristics?: {
      ws?: number
      bs?: number
      s?: number
      t?: number
      i?: number
      ag?: number
      dex?: number
      int?: number
      wp?: number
      fel?: number
    }
    skills?: string[]
    talents?: string[]
    trappings?: string[]
    description?: string
  }
}

const props = defineProps<CharacterProfileProps>()

// Reactive state for expandable sections
const showAllSkills = ref(false)
const showAllTalents = ref(false)
const showAllTrappings = ref(false)
</script>

<style scoped>
.character-profile {
  @apply transition-all duration-300;
}

.character-profile:hover {
  @apply shadow-2xl;
}

.characteristic-stat {
  @apply transition-all duration-200;
}

.characteristic-stat:hover {
  @apply transform scale-105;
}

.skill-tag,
.talent-tag {
  @apply transition-all duration-200 cursor-default;
}

.skill-tag:hover {
  @apply bg-secondary/30 transform scale-105;
}

.talent-tag:hover {
  @apply bg-accent/30 transform scale-105;
}

.trapping-item {
  @apply transition-all duration-200;
}

.trapping-item:hover {
  @apply bg-card/50 transform scale-105;
}

.character-actions button {
  @apply transition-all duration-200;
}

.character-actions button:hover {
  @apply transform -translate-y-px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .characteristics-grid {
    @apply grid-cols-2;
  }
  
  .character-actions {
    @apply flex-col;
  }
  
  .character-actions button {
    @apply w-full justify-center;
  }
}
</style>
