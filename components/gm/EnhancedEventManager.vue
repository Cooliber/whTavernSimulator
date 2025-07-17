<template>
  <div class="enhanced-event-manager wh-card wh-card-parchment p-6 space-y-6">
    <!-- Event Timeline Visualization -->
    <div class="event-timeline-section">
      <h3 class="wh-title text-xl text-wh-dark-grey mb-4">Event Timeline</h3>
      <div class="timeline-container relative">
        <div class="timeline-track bg-wh-empire-gold h-2 rounded-full relative">
          <div 
            v-for="event in timelineEvents" 
            :key="event.id"
            class="timeline-event absolute top-0 transform -translate-y-1/2"
            :style="{ left: event.position + '%' }"
            @click="selectEvent(event)"
          >
            <div class="event-marker w-4 h-4 bg-wh-chaos-red rounded-full border-2 border-white cursor-pointer hover:scale-125 transition-transform">
              <Tooltip :content="event.name" />
            </div>
          </div>
        </div>
        <div class="timeline-labels flex justify-between mt-2 text-xs text-wh-dark-grey">
          <span>Now</span>
          <span>+30min</span>
          <span>+1hr</span>
          <span>+2hr</span>
        </div>
      </div>
    </div>

    <!-- Smart Event Suggestions -->
    <div class="event-suggestions-section">
      <h4 class="wh-subtitle text-lg text-wh-dark-grey mb-3">AI Event Suggestions</h4>
      <div class="suggestions-grid grid grid-cols-1 md:grid-cols-2 gap-3">
        <div 
          v-for="suggestion in aiSuggestions" 
          :key="suggestion.id"
          class="suggestion-card wh-ornate-border p-3 hover:bg-wh-parchment-light cursor-pointer transition-colors"
          @click="applySuggestion(suggestion)"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h5 class="font-medieval text-sm text-wh-dark-grey">{{ suggestion.title }}</h5>
              <p class="text-xs text-wh-muted mt-1">{{ suggestion.description }}</p>
              <div class="flex items-center mt-2 space-x-2">
                <span class="text-xs px-2 py-1 bg-wh-empire-gold text-wh-dark-grey rounded">
                  {{ suggestion.category }}
                </span>
                <span class="text-xs text-wh-muted">{{ suggestion.duration }}</span>
              </div>
            </div>
            <div class="flex flex-col items-center ml-2">
              <Icon :name="suggestion.icon" class="w-4 h-4 text-wh-empire-gold" />
              <span class="text-xs text-wh-empire-gold mt-1">{{ suggestion.probability }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Events Dashboard -->
    <div class="active-events-section">
      <div class="flex items-center justify-between mb-3">
        <h4 class="wh-subtitle text-lg text-wh-dark-grey">Active Events</h4>
        <div class="flex space-x-2">
          <RippleButton 
            class="bg-wh-empire-gold text-wh-dark-grey px-3 py-1 text-sm"
            @click="pauseAllEvents"
          >
            <Icon name="pause" class="w-4 h-4 mr-1" />
            Pause All
          </RippleButton>
          <ShimmerButton 
            class="bg-wh-chaos-red text-white px-3 py-1 text-sm"
            @click="createCustomEvent"
          >
            <Icon name="plus" class="w-4 h-4 mr-1" />
            Custom Event
          </ShimmerButton>
        </div>
      </div>

      <div class="events-grid space-y-3">
        <div 
          v-for="event in activeEvents" 
          :key="event.id"
          class="event-card wh-ornate-border p-4 space-y-3"
        >
          <div class="event-header flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="event-icon w-8 h-8 rounded-full bg-wh-empire-gold flex items-center justify-center">
                <Icon :name="event.icon" class="w-4 h-4 text-wh-dark-grey" />
              </div>
              <div>
                <h5 class="font-medieval text-sm text-wh-dark-grey">{{ event.name }}</h5>
                <p class="text-xs text-wh-muted">{{ event.description }}</p>
              </div>
            </div>
            <div class="event-controls flex items-center space-x-2">
              <button 
                class="text-wh-empire-gold hover:text-wh-empire-gold-dark"
                @click="editEvent(event)"
              >
                <Icon name="edit" class="w-4 h-4" />
              </button>
              <button 
                class="text-wh-chaos-red hover:text-wh-chaos-red-dark"
                @click="stopEvent(event)"
              >
                <Icon name="x" class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Event Progress -->
          <div class="event-progress">
            <div class="flex items-center justify-between mb-1">
              <span class="text-xs text-wh-muted">Progress</span>
              <span class="text-xs text-wh-dark-grey">{{ event.progress }}%</span>
            </div>
            <div class="progress-bar w-full h-2 bg-wh-muted rounded-full overflow-hidden">
              <div 
                class="progress-fill h-full bg-gradient-to-r from-wh-empire-gold to-wh-empire-gold-dark transition-all duration-500"
                :style="{ width: event.progress + '%' }"
              />
            </div>
          </div>

          <!-- Event Effects -->
          <div class="event-effects">
            <div class="flex items-center justify-between text-xs">
              <span class="text-wh-muted">Effects:</span>
              <div class="flex space-x-2">
                <span 
                  v-for="effect in event.effects" 
                  :key="effect"
                  class="px-2 py-1 bg-wh-parchment-light text-wh-dark-grey rounded"
                >
                  {{ effect }}
                </span>
              </div>
            </div>
          </div>

          <!-- Event Triggers -->
          <div class="event-triggers" v-if="event.triggers?.length">
            <div class="flex items-center justify-between text-xs">
              <span class="text-wh-muted">Triggers:</span>
              <div class="flex space-x-1">
                <button 
                  v-for="trigger in event.triggers" 
                  :key="trigger.id"
                  class="px-2 py-1 bg-wh-empire-gold text-wh-dark-grey rounded hover:bg-wh-empire-gold-dark transition-colors"
                  @click="executeTrigger(trigger)"
                >
                  {{ trigger.name }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Event Templates Library -->
    <div class="event-templates-section">
      <h4 class="wh-subtitle text-lg text-wh-dark-grey mb-3">Event Templates</h4>
      <div class="templates-grid grid grid-cols-2 md:grid-cols-4 gap-3">
        <div 
          v-for="template in eventTemplates" 
          :key="template.id"
          class="template-card wh-ornate-border p-3 text-center hover:bg-wh-parchment-light cursor-pointer transition-colors"
          @click="useTemplate(template)"
        >
          <Icon :name="template.icon" class="w-6 h-6 text-wh-empire-gold mx-auto mb-2" />
          <h6 class="font-medieval text-xs text-wh-dark-grey">{{ template.name }}</h6>
          <p class="text-xs text-wh-muted mt-1">{{ template.category }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface EventSuggestion {
  id: string
  title: string
  description: string
  category: string
  duration: string
  icon: string
  probability: number
}

interface ActiveEvent {
  id: string
  name: string
  description: string
  icon: string
  progress: number
  effects: string[]
  triggers?: Array<{ id: string; name: string }>
}

interface EventTemplate {
  id: string
  name: string
  category: string
  icon: string
}

// Reactive data
const timelineEvents = ref([
  { id: '1', name: 'Merchant Arrival', position: 25 },
  { id: '2', name: 'Storm Brewing', position: 60 },
  { id: '3', name: 'Mysterious Visitor', position: 85 }
])

const aiSuggestions = ref<EventSuggestion[]>([
  {
    id: 'sug-1',
    title: 'Traveling Merchant',
    description: 'A merchant caravan arrives with exotic goods',
    category: 'Commerce',
    duration: '45 min',
    icon: 'shopping-cart',
    probability: 85
  },
  {
    id: 'sug-2',
    title: 'Brawl Breaks Out',
    description: 'Tensions rise between patrons',
    category: 'Conflict',
    duration: '15 min',
    icon: 'sword',
    probability: 65
  },
  {
    id: 'sug-3',
    title: 'Weather Change',
    description: 'Storm clouds gather overhead',
    category: 'Environment',
    duration: '2 hours',
    icon: 'cloud-rain',
    probability: 40
  },
  {
    id: 'sug-4',
    title: 'Quest Opportunity',
    description: 'A desperate patron seeks help',
    category: 'Adventure',
    duration: '30 min',
    icon: 'scroll',
    probability: 70
  }
])

const activeEvents = ref<ActiveEvent[]>([
  {
    id: 'evt-1',
    name: 'Harvest Festival',
    description: 'The annual harvest celebration is in full swing',
    icon: 'calendar',
    progress: 65,
    effects: ['Increased Crowd', 'Festive Mood', 'Higher Prices'],
    triggers: [
      { id: 'trg-1', name: 'Start Contest' },
      { id: 'trg-2', name: 'Special Guest' }
    ]
  },
  {
    id: 'evt-2',
    name: 'Mysterious Hooded Figure',
    description: 'A cloaked stranger sits alone in the corner',
    icon: 'user-secret',
    progress: 30,
    effects: ['Tension', 'Curiosity'],
    triggers: [
      { id: 'trg-3', name: 'Reveal Identity' },
      { id: 'trg-4', name: 'Leave Quietly' }
    ]
  }
])

const eventTemplates = ref<EventTemplate[]>([
  { id: 'tmp-1', name: 'Merchant Visit', category: 'Commerce', icon: 'shopping-cart' },
  { id: 'tmp-2', name: 'Tavern Brawl', category: 'Conflict', icon: 'sword' },
  { id: 'tmp-3', name: 'Weather Event', category: 'Environment', icon: 'cloud' },
  { id: 'tmp-4', name: 'Quest Hook', category: 'Adventure', icon: 'scroll' },
  { id: 'tmp-5', name: 'Festival', category: 'Social', icon: 'calendar' },
  { id: 'tmp-6', name: 'Inspection', category: 'Authority', icon: 'shield' },
  { id: 'tmp-7', name: 'Performance', category: 'Entertainment', icon: 'music' },
  { id: 'tmp-8', name: 'Delivery', category: 'Commerce', icon: 'package' }
])

// Methods
const selectEvent = (event: any) => {
  console.log('Selected timeline event:', event)
}

const applySuggestion = (suggestion: EventSuggestion) => {
  console.log('Applying suggestion:', suggestion.title)
  // Convert suggestion to active event
}

const pauseAllEvents = () => {
  console.log('Pausing all events')
}

const createCustomEvent = () => {
  console.log('Creating custom event')
}

const editEvent = (event: ActiveEvent) => {
  console.log('Editing event:', event.name)
}

const stopEvent = (event: ActiveEvent) => {
  const index = activeEvents.value.findIndex(e => e.id === event.id)
  if (index > -1) {
    activeEvents.value.splice(index, 1)
  }
}

const executeTrigger = (trigger: any) => {
  console.log('Executing trigger:', trigger.name)
}

const useTemplate = (template: EventTemplate) => {
  console.log('Using template:', template.name)
}
</script>

<style scoped>
.timeline-container {
  padding: 1rem 0;
}

.event-marker {
  z-index: 10;
}

.suggestion-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.template-card:hover {
  transform: scale(1.05);
}

.progress-fill {
  transition: width 0.5s ease-in-out;
}
</style>
