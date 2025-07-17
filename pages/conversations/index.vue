<template>
  <div class="conversations-page space-y-8">
    <!-- Meteors background -->
    <Meteors :meteor-count="3" :meteor-speed="0.4" />
    
    <!-- Page header -->
    <section class="text-center space-y-6">
      <Spotlight 
        spotlight-color="rgba(255, 215, 0, 0.3)"
        :spotlight-size="350"
        class="inline-block"
      >
        <SparklesText
          :text="$t('conversations.title')"
          class="text-5xl md:text-7xl font-medieval text-foreground"
          :sparkles-count="18"
        />
      </Spotlight>
      
      <Text3D 
        text="Engage with AI-Powered NPCs"
        class="text-xl md:text-2xl font-fantasy text-primary"
        :depth="3"
      />
    </section>

    <!-- Available characters testimonials -->
    <section class="space-y-6">
      <HyperText 
        text="Choose Your Conversation Partner"
        class="text-2xl font-medieval text-foreground text-center"
        :animation-duration="1200"
      />
      
      <!-- Character testimonials -->
      <AnimatedTestimonials 
        :testimonials="characterTestimonials"
        :auto-play="true"
        :auto-play-interval="6000"
        class="mx-auto"
      >
        <template #testimonial="{ testimonial }">
          <div class="character-testimonial space-y-6">
            <!-- Character header -->
            <div class="flex items-center space-x-6">
              <Lens 
                :lens-size="100"
                :magnification="1.5"
                class="character-avatar"
              >
                <div class="w-20 h-20 rounded-full bg-gradient-to-br from-amber-800 to-amber-900 flex items-center justify-center border-4 border-primary/30">
                  <Icon :name="testimonial.icon" class="w-10 h-10 text-primary" />
                </div>
                
                <template #magnified>
                  <div class="character-details bg-black/90 text-white p-3 rounded-lg">
                    <h4 class="font-medieval text-sm mb-1">{{ testimonial.name }}</h4>
                    <p class="text-xs mb-2">{{ testimonial.title }}</p>
                    <div class="space-y-1 text-xs">
                      <p><strong>Faction:</strong> {{ testimonial.faction }}</p>
                      <p><strong>Mood:</strong> {{ testimonial.mood }}</p>
                      <p><strong>Specialty:</strong> {{ testimonial.specialty }}</p>
                    </div>
                  </div>
                </template>
              </Lens>
              
              <div class="flex-1">
                <SparklesText 
                  :text="testimonial.name"
                  class="text-2xl font-medieval text-foreground"
                  :sparkles-count="10"
                />
                <p class="text-lg text-muted-foreground mb-2">{{ testimonial.title }}</p>
                <div class="flex items-center space-x-2">
                  <div class="w-3 h-3 rounded-full" :class="testimonial.factionColor" />
                  <span class="text-sm font-medieval text-muted-foreground">{{ testimonial.faction }}</span>
                </div>
              </div>
            </div>
            
            <!-- Character quote -->
            <div class="bg-background/30 rounded-lg p-6 border-l-4 border-primary">
              <TextReveal 
                :text="testimonial.quote"
                class="text-lg text-foreground leading-relaxed italic"
                :reveal-speed="40"
                trigger="immediate"
              />
            </div>
            
            <!-- Character traits -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div 
                v-for="trait in testimonial.traits" 
                :key="trait.name"
                class="trait-item text-center"
              >
                <div class="w-12 h-12 mx-auto rounded-full bg-primary/20 flex items-center justify-center mb-2">
                  <Icon :name="trait.icon" class="w-6 h-6 text-primary" />
                </div>
                <p class="text-sm font-medieval text-foreground">{{ trait.name }}</p>
                <div class="w-full h-1 bg-muted rounded-full mt-1 overflow-hidden">
                  <div 
                    class="h-full bg-gradient-to-r from-primary to-primary/60 transition-all duration-1000"
                    :style="{ width: trait.level + '%' }"
                  />
                </div>
              </div>
            </div>
            
            <!-- Action button -->
            <div class="text-center">
              <RippleButton 
                class="px-8 py-3 font-medieval text-lg faction-empire"
                ripple-color="rgb(255, 215, 0)"
                @click="startConversation(testimonial)"
              >
                <Icon name="message-circle" class="w-5 h-5 mr-2" />
                Start Conversation
              </RippleButton>
            </div>
          </div>
        </template>
      </AnimatedTestimonials>
    </section>

    <!-- Conversation tips -->
    <section class="space-y-6">
      <HyperText 
        text="Conversation Tips"
        class="text-2xl font-medieval text-foreground text-center"
        :animation-duration="1200"
      />
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <BorderBeam 
          v-for="tip in conversationTips" 
          :key="tip.id"
          class="tip-card bg-card/50 backdrop-blur-md rounded-xl p-6"
          :border-width="1"
          color-from="#ffd700"
          color-to="#b8860b"
        >
          <div class="text-center space-y-4">
            <div class="w-16 h-16 mx-auto rounded-full bg-gradient-to-br from-primary/20 to-primary/10 flex items-center justify-center">
              <Icon :name="tip.icon" class="w-8 h-8 text-primary" />
            </div>
            <h3 class="text-lg font-medieval text-foreground">{{ tip.title }}</h3>
            <p class="text-sm text-muted-foreground leading-relaxed">{{ tip.description }}</p>
          </div>
        </BorderBeam>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// Page metadata
useHead({
  title: 'Conversations - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Engage in immersive conversations with AI-powered NPCs in the Warhammer Fantasy world.' }
  ]
})

// Character testimonials data
const characterTestimonials = ref([
  {
    id: 'marcus',
    name: 'Sir Marcus Brightblade',
    title: 'Knight of the Blazing Sun',
    faction: 'Empire',
    factionColor: 'bg-faction-empire-500',
    factionBg: 'bg-faction-empire-600',
    icon: 'sword',
    mood: 'Honorable',
    specialty: 'Combat & Leadership',
    quote: "Honor is not just a word, young one. It is the foundation upon which the Empire stands. Every battle I fight, every oath I swear, is in service to Sigmar and the protection of the innocent.",
    traits: [
      { name: 'Honor', level: 95, icon: 'shield' },
      { name: 'Combat', level: 90, icon: 'sword' },
      { name: 'Leadership', level: 85, icon: 'crown' },
      { name: 'Faith', level: 80, icon: 'star' }
    ]
  },
  {
    id: 'grimjaw',
    name: 'Grimjaw Ironbeard',
    title: 'Slayer of the Broken Chain',
    faction: 'Dwarfs',
    factionColor: 'bg-faction-dwarfs-500',
    factionBg: 'bg-faction-dwarfs-600',
    icon: 'hammer',
    mood: 'Brooding',
    specialty: 'Berserker Combat',
    quote: "I have taken the Slayer Oath, and death is my only redemption. But until that glorious end comes, I'll send as many enemies to their doom as I can. Khazad ai-mênu!",
    traits: [
      { name: 'Rage', level: 98, icon: 'flame' },
      { name: 'Strength', level: 95, icon: 'hammer' },
      { name: 'Endurance', level: 90, icon: 'shield' },
      { name: 'Fearless', level: 100, icon: 'heart' }
    ]
  },
  {
    id: 'elara',
    name: 'Elara Moonwhisper',
    title: 'High Mage of Hoeth',
    faction: 'High Elves',
    factionColor: 'bg-faction-elves-500',
    factionBg: 'bg-faction-elves-600',
    icon: 'sparkles',
    mood: 'Wise',
    specialty: 'High Magic',
    quote: "The winds of magic flow through all things, mortal. To understand them is to understand the very fabric of reality. I have spent centuries studying their mysteries, and still I learn.",
    traits: [
      { name: 'Wisdom', level: 98, icon: 'book' },
      { name: 'Magic', level: 95, icon: 'sparkles' },
      { name: 'Knowledge', level: 92, icon: 'scroll' },
      { name: 'Patience', level: 88, icon: 'clock' }
    ]
  },
  {
    id: 'valdris',
    name: 'Valdris Shadowbane',
    title: 'Witch Hunter Captain',
    faction: 'Empire',
    factionColor: 'bg-faction-empire-500',
    factionBg: 'bg-faction-empire-600',
    icon: 'flame',
    mood: 'Vigilant',
    specialty: 'Heretic Hunting',
    quote: "In the darkness, heretics and daemons lurk, waiting to corrupt the innocent. My faith is my armor, my pistol my sword. I am the Emperor's wrath made manifest.",
    traits: [
      { name: 'Faith', level: 95, icon: 'star' },
      { name: 'Detection', level: 92, icon: 'eye' },
      { name: 'Marksmanship', level: 88, icon: 'target' },
      { name: 'Resolve', level: 90, icon: 'shield' }
    ]
  },
  {
    id: 'lyralei',
    name: 'Lyralei Starweaver',
    title: 'Scout of Athel Loren',
    faction: 'Wood Elves',
    factionColor: 'bg-faction-elves-500',
    factionBg: 'bg-faction-elves-600',
    icon: 'leaf',
    mood: 'Curious',
    specialty: 'Forest Lore',
    quote: "The forest speaks to those who know how to listen. Every leaf, every branch tells a story. I am but a humble translator of nature's ancient wisdom.",
    traits: [
      { name: 'Nature', level: 95, icon: 'leaf' },
      { name: 'Archery', level: 90, icon: 'bow' },
      { name: 'Stealth', level: 92, icon: 'eye-off' },
      { name: 'Tracking', level: 88, icon: 'footprints' }
    ]
  }
])

// Conversation tips
const conversationTips = ref([
  {
    id: 1,
    title: 'Be Respectful',
    description: 'Each character has their own personality and background. Approach them with respect and they will share their stories.',
    icon: 'heart'
  },
  {
    id: 2,
    title: 'Ask About Their Past',
    description: 'NPCs love to share tales of their adventures, battles, and experiences. Ask about their history for rich storytelling.',
    icon: 'book'
  },
  {
    id: 3,
    title: 'Discuss Current Events',
    description: 'Talk about what\'s happening in the tavern, the weather, or recent events to get dynamic, contextual responses.',
    icon: 'newspaper'
  }
])

// Methods
const startConversation = (character: any) => {
  // Navigate to individual conversation page
  navigateTo(`/conversations/${character.id}`)
}

// Lifecycle
onMounted(() => {
  console.log('Conversations page loaded with', characterTestimonials.value.length, 'characters')
})
</script>

<style scoped>
/* Conversation page specific styles */
.conversations-page {
  min-height: 100vh;
}

.character-testimonial {
  animation: testimonial-entrance 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.trait-item {
  animation: trait-fade-in 0.6s ease-out forwards;
}

.tip-card {
  animation: tip-slide-up 0.6s ease-out forwards;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tip-card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 
    0 20px 40px -10px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 215, 0, 0.2);
}

/* Custom animations */
@keyframes testimonial-entrance {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes trait-fade-in {
  0% {
    opacity: 0;
    transform: translateY(10px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes tip-slide-up {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .character-testimonial {
    padding: 1rem;
  }
  
  .trait-item {
    animation-delay: 0s;
  }
}

/* Performance optimizations */
.character-testimonial,
.trait-item,
.tip-card {
  will-change: transform;
}
</style>