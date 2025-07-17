<template>
  <div class="gm-dashboard relative min-h-screen overflow-hidden bg-gradient-to-br from-purple-900/20 to-indigo-900/20">
    <!-- Epic GM Background -->
    <InteractiveGridPattern 
      :grid-size="80"
      grid-color="#8b5cf6"
      :stroke-width="2"
      :proximity-radius="120"
      proximity-color="#a855f7"
      class="absolute inset-0 opacity-15"
    />
    <Meteors :meteor-count="6" :meteor-speed="0.8" />
    <ParticlesBg 
      :particle-count="40"
      particle-color="#8b5cf6"
      :particle-size="1"
      :animation-speed="0.5"
      class="opacity-40"
    />
    
    <div class="relative z-10 space-y-8 p-8">
      <!-- GM Header -->
      <section class="text-center space-y-6">
        <Spotlight 
          spotlight-color="rgba(139, 92, 246, 0.6)"
          :spotlight-size="600"
          class="inline-block"
        >
          <div class="space-y-4">
            <SparklesText 
              text="GAME MASTER DASHBOARD"
              class="text-6xl md:text-8xl font-medieval text-foreground"
              :sparkles-count="30"
            />
            <Text3D 
              text="Control the Warhammer Fantasy Experience"
              class="text-2xl md:text-3xl font-fantasy text-primary"
              :depth="5"
            />
          </div>
        </Spotlight>
        
        <!-- GM Status Bar -->
        <div class="flex justify-center space-x-8">
          <div class="gm-status-item">
            <Icon name="users" class="w-6 h-6 text-blue-400 mx-auto" />
            <p class="text-sm font-medieval text-muted-foreground">{{ activeNPCs }} Active NPCs</p>
          </div>
          <div class="gm-status-item">
            <Icon name="scroll" class="w-6 h-6 text-green-400 mx-auto" />
            <p class="text-sm font-medieval text-muted-foreground">{{ activeEvents }} Events Running</p>
          </div>
          <div class="gm-status-item">
            <Icon name="eye" class="w-6 h-6 text-purple-400 mx-auto" />
            <p class="text-sm font-medieval text-muted-foreground">{{ playersOnline }} Players Online</p>
          </div>
        </div>
      </section>

      <!-- GM Focus Mode Toggle -->
      <div class="focus-mode-controls mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <span class="text-sm text-muted-foreground">Focus Mode:</span>
            <button
              class="focus-toggle px-3 py-1 rounded-full text-xs transition-colors"
              :class="focusMode ? 'bg-red-600 text-white' : 'bg-purple-600 text-white'"
              @click="toggleFocusMode"
            >
              {{ focusMode ? 'ON' : 'OFF' }}
            </button>
          </div>
        </div>
        <div class="quick-actions flex items-center space-x-2">
          <RippleButton
            class="bg-green-600 text-white px-4 py-2 text-sm font-medieval"
            ripple-color="rgba(34, 197, 94, 0.6)"
            @click="saveSession"
          >
            <Icon name="save" class="w-4 h-4 mr-1" />
            Save Session
          </RippleButton>
          <ShimmerButton
            class="bg-red-600 text-white px-4 py-2 text-sm font-medieval"
            shimmer-color="rgba(220, 38, 38, 0.5)"
            @click="emergencyPause"
          >
            <Icon name="pause" class="w-4 h-4 mr-1" />
            {{ sessionPaused ? 'Resume' : 'Emergency Pause' }}
          </ShimmerButton>
        </div>
      </div>

      <!-- GM Control Panels -->
      <div class="grid grid-cols-1 xl:grid-cols-4 gap-8">
        <!-- Atmospheric Controls Panel -->
        <div class="gm-panel">
          <AtmosphericControls
            @weather-change="handleWeatherChange"
            @time-change="handleTimeChange"
            @fireplace-change="handleFireplaceChange"
            @candle-change="handleCandleChange"
            @audio-change="handleAudioChange"
            @crowd-change="handleCrowdChange"
            @preset-applied="handlePresetApplied"
          />
        </div>
        <!-- Enhanced NPC Management Panel -->
        <div class="gm-panel">
          <NPCManager />
        </div>

        <!-- Original NPC Management Panel (Legacy) -->
        <div class="gm-panel">
          <BorderBeam
            class="bg-card/80 backdrop-blur-md rounded-2xl p-6"
            :border-width="3"
            color-from="#3b82f6"
            color-to="#1d4ed8"
          >
            <div class="space-y-6">
              <HyperText 
                text="NPC Management"
                class="text-2xl font-medieval text-foreground"
                :animation-duration="1200"
              />
              
              <!-- NPC Quick Actions -->
              <div class="grid grid-cols-2 gap-3">
                <RippleButton 
                  class="bg-blue-600 text-white p-3 text-sm font-medieval"
                  ripple-color="rgba(37, 99, 235, 0.6)"
                  @click="openNPCEditor"
                >
                  <Icon name="user-plus" class="w-4 h-4 mr-2" />
                  Create NPC
                </RippleButton>
                
                <ShimmerButton 
                  class="bg-secondary text-secondary-foreground p-3 text-sm font-medieval"
                  shimmer-color="rgba(139, 69, 19, 0.5)"
                  @click="openBehaviorEditor"
                >
                  <Icon name="brain" class="w-4 h-4 mr-2" />
                  AI Behavior
                </ShimmerButton>
                
                <RippleButton 
                  class="bg-green-600 text-white p-3 text-sm font-medieval"
                  ripple-color="rgba(34, 197, 94, 0.6)"
                  @click="spawnRandomNPC"
                >
                  <Icon name="shuffle" class="w-4 h-4 mr-2" />
                  Random Spawn
                </RippleButton>
                
                <RainbowButton 
                  :colors="['#8b5cf6', '#a855f7', '#c084fc']"
                  class="p-3 text-sm font-medieval"
                  @click="openNPCTemplates"
                >
                  <Icon name="copy" class="w-4 h-4 mr-2" />
                  Templates
                </RainbowButton>
              </div>
              
              <!-- Active NPCs List -->
              <div class="space-y-3">
                <h4 class="text-lg font-medieval text-foreground">Active NPCs</h4>
                <div class="space-y-2 max-h-64 overflow-y-auto">
                  <div 
                    v-for="npc in activeNPCList" 
                    :key="npc.id"
                    class="npc-item flex items-center justify-between p-3 rounded-lg bg-background/30 hover:bg-background/50 transition-colors cursor-pointer"
                    @click="selectNPC(npc)"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center">
                        <Icon :name="npc.icon" class="w-4 h-4 text-white" />
                      </div>
                      <div>
                        <p class="text-sm font-medieval text-foreground">{{ npc.name }}</p>
                        <p class="text-xs text-muted-foreground">{{ npc.status }}</p>
                      </div>
                    </div>
                    
                    <div class="flex items-center space-x-2">
                      <div 
                        class="w-2 h-2 rounded-full"
                        :class="npc.active ? 'bg-green-400' : 'bg-red-400'"
                      />
                      <RippleButton 
                        class="w-6 h-6 rounded-full bg-secondary text-secondary-foreground flex items-center justify-center"
                        ripple-color="rgba(139, 69, 19, 0.5)"
                        @click.stop="editNPC(npc)"
                      >
                        <Icon name="edit" class="w-3 h-3" />
                      </RippleButton>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </BorderBeam>
        </div>
        
        <!-- Enhanced Event Management Panel -->
        <div class="gm-panel">
          <EnhancedEventManager />
        </div>

        <!-- Smart Atmosphere Control Panel -->
        <div class="gm-panel">
          <SmartAtmosphereControl />
        </div>

        <!-- Legacy Event Management Panel (Hidden in Focus Mode) -->
        <div class="gm-panel legacy-panel" v-show="!focusMode">
          <BorderBeam
            class="bg-card/80 backdrop-blur-md rounded-2xl p-6"
            :border-width="3"
            color-from="#10b981"
            color-to="#059669"
          >
            <div class="space-y-6">
              <HyperText
                text="Legacy Event Management"
                class="text-2xl font-medieval text-foreground"
                :animation-duration="1200"
              />
              
              <!-- Event Quick Actions -->
              <div class="grid grid-cols-2 gap-3">
                <RippleButton 
                  class="bg-green-600 text-white p-3 text-sm font-medieval"
                  ripple-color="rgba(34, 197, 94, 0.6)"
                  @click="createEvent"
                >
                  <Icon name="plus" class="w-4 h-4 mr-2" />
                  Create Event
                </RippleButton>
                
                <ShimmerButton 
                  class="bg-secondary text-secondary-foreground p-3 text-sm font-medieval"
                  shimmer-color="rgba(139, 69, 19, 0.5)"
                  @click="openEventScripting"
                >
                  <Icon name="code" class="w-4 h-4 mr-2" />
                  Scripting
                </ShimmerButton>
                
                <RippleButton 
                  class="bg-yellow-600 text-white p-3 text-sm font-medieval"
                  ripple-color="rgba(245, 158, 11, 0.6)"
                  @click="triggerRandomEvent"
                >
                  <Icon name="zap" class="w-4 h-4 mr-2" />
                  Random Event
                </RippleButton>
                
                <RainbowButton 
                  :colors="['#10b981', '#059669', '#047857']"
                  class="p-3 text-sm font-medieval"
                  @click="openEventTemplates"
                >
                  <Icon name="bookmark" class="w-4 h-4 mr-2" />
                  Templates
                </RainbowButton>
              </div>
              
              <!-- Active Events -->
              <div class="space-y-3">
                <h4 class="text-lg font-medieval text-foreground">Running Events</h4>
                <div class="space-y-2 max-h-64 overflow-y-auto">
                  <div 
                    v-for="event in runningEvents" 
                    :key="event.id"
                    class="event-item p-3 rounded-lg bg-background/30"
                  >
                    <div class="flex items-center justify-between">
                      <div>
                        <p class="text-sm font-medieval text-foreground">{{ event.name }}</p>
                        <p class="text-xs text-muted-foreground">{{ event.description }}</p>
                      </div>
                      <div class="flex items-center space-x-2">
                        <span class="text-xs text-muted-foreground">{{ event.timeLeft }}</span>
                        <RippleButton 
                          class="w-6 h-6 rounded-full bg-red-600 text-white flex items-center justify-center"
                          ripple-color="rgba(220, 38, 38, 0.6)"
                          @click="stopEvent(event)"
                        >
                          <Icon name="x" class="w-3 h-3" />
                        </RippleButton>
                      </div>
                    </div>
                    
                    <!-- Event Progress -->
                    <div class="mt-2 w-full h-1 bg-muted rounded-full overflow-hidden">
                      <div 
                        class="h-full bg-gradient-to-r from-green-500 to-green-400 transition-all duration-1000"
                        :style="{ width: event.progress + '%' }"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </BorderBeam>
        </div>
        
        <!-- Economy & Settings Panel -->
        <div class="gm-panel">
          <BorderBeam 
            class="bg-card/80 backdrop-blur-md rounded-2xl p-6"
            :border-width="3"
            color-from="#f59e0b"
            color-to="#d97706"
          >
            <div class="space-y-6">
              <HyperText 
                text="Economy & Settings"
                class="text-2xl font-medieval text-foreground"
                :animation-duration="1200"
              />
              
              <!-- Economy Controls -->
              <div class="space-y-4">
                <h4 class="text-lg font-medieval text-foreground">Economy Controls</h4>
                
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-sm text-muted-foreground">Gold Inflation</span>
                    <span class="text-sm text-foreground">{{ economySettings.goldInflation }}%</span>
                  </div>
                  <input 
                    v-model="economySettings.goldInflation"
                    type="range"
                    min="-50"
                    max="200"
                    step="5"
                    class="gm-slider w-full"
                    @input="updateEconomy"
                  />
                  
                  <div class="flex items-center justify-between">
                    <span class="text-sm text-muted-foreground">Trade Volume</span>
                    <span class="text-sm text-foreground">{{ economySettings.tradeVolume }}%</span>
                  </div>
                  <input 
                    v-model="economySettings.tradeVolume"
                    type="range"
                    min="0"
                    max="200"
                    step="10"
                    class="gm-slider w-full"
                    @input="updateEconomy"
                  />
                  
                  <div class="flex items-center justify-between">
                    <span class="text-sm text-muted-foreground">Quest Rewards</span>
                    <span class="text-sm text-foreground">{{ economySettings.questRewards }}%</span>
                  </div>
                  <input 
                    v-model="economySettings.questRewards"
                    type="range"
                    min="50"
                    max="300"
                    step="25"
                    class="gm-slider w-full"
                    @input="updateEconomy"
                  />
                </div>
              </div>
              
              <!-- Quick Settings -->
              <div class="space-y-4">
                <h4 class="text-lg font-medieval text-foreground">Quick Settings</h4>
                
                <div class="grid grid-cols-1 gap-3">
                  <RippleButton 
                    class="bg-yellow-600 text-white p-3 text-sm font-medieval"
                    ripple-color="rgba(245, 158, 11, 0.6)"
                    @click="openSaveLoad"
                  >
                    <Icon name="save" class="w-4 h-4 mr-2" />
                    Save/Load State
                  </RippleButton>
                  
                  <ShimmerButton 
                    class="bg-secondary text-secondary-foreground p-3 text-sm font-medieval"
                    shimmer-color="rgba(139, 69, 19, 0.5)"
                    @click="openQuestCreator"
                  >
                    <Icon name="scroll" class="w-4 h-4 mr-2" />
                    Quest Creator
                  </ShimmerButton>
                  
                  <RippleButton 
                    class="bg-purple-600 text-white p-3 text-sm font-medieval"
                    ripple-color="rgba(147, 51, 234, 0.6)"
                    @click="openDialogueEditor"
                  >
                    <Icon name="message-square" class="w-4 h-4 mr-2" />
                    Dialogue Editor
                  </RippleButton>
                  
                  <RainbowButton 
                    :colors="['#f59e0b', '#d97706', '#b45309']"
                    class="p-3 text-sm font-medieval"
                    @click="resetToDefaults"
                  >
                    <Icon name="refresh-cw" class="w-4 h-4 mr-2" />
                    Reset Defaults
                  </RainbowButton>
                </div>
              </div>
            </div>
          </BorderBeam>
        </div>
      </div>
      
      <!-- GM Tools Tabs -->
      <section>
        <BorderBeam 
          class="gm-tools bg-card/90 backdrop-blur-md rounded-2xl p-6"
          :border-width="2"
          color-from="#8b5cf6"
          color-to="#7c3aed"
        >
          <div class="space-y-6">
            <!-- Tab Navigation -->
            <div class="flex space-x-4 border-b border-border">
              <button 
                v-for="tab in gmTabs" 
                :key="tab.id"
                class="tab-button px-4 py-2 font-medieval transition-all duration-300"
                :class="activeTab === tab.id ? 'text-primary border-b-2 border-primary' : 'text-muted-foreground hover:text-foreground'"
                @click="activeTab = tab.id"
              >
                <Icon :name="tab.icon" class="w-4 h-4 mr-2 inline" />
                {{ tab.name }}
              </button>
            </div>
            
            <!-- Tab Content -->
            <div class="tab-content min-h-96">
              <!-- NPC Editor Tab -->
              <div v-if="activeTab === 'npc-editor'" class="space-y-6">
                <h3 class="text-2xl font-medieval text-foreground">NPC Personality Editor</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- NPC Selection -->
                  <div class="space-y-4">
                    <h4 class="text-lg font-medieval text-foreground">Select NPC</h4>
                    <select 
                      v-model="selectedNPCId"
                      class="w-full p-3 bg-background border border-border rounded-lg font-medieval text-foreground"
                    >
                      <option value="">Choose an NPC...</option>
                      <option 
                        v-for="npc in activeNPCList" 
                        :key="npc.id"
                        :value="npc.id"
                      >
                        {{ npc.name }} - {{ npc.title }}
                      </option>
                    </select>
                    
                    <!-- NPC Preview -->
                    <div v-if="selectedNPC" class="npc-preview p-4 rounded-lg bg-background/30">
                      <div class="flex items-center space-x-3 mb-4">
                        <div class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-600 to-blue-700 flex items-center justify-center">
                          <Icon :name="selectedNPC.icon" class="w-6 h-6 text-white" />
                        </div>
                        <div>
                          <h5 class="font-medieval text-foreground">{{ selectedNPC.name }}</h5>
                          <p class="text-sm text-muted-foreground">{{ selectedNPC.title }}</p>
                        </div>
                      </div>
                      
                      <div class="space-y-2 text-sm">
                        <p><strong>Faction:</strong> {{ selectedNPC.faction }}</p>
                        <p><strong>Mood:</strong> {{ selectedNPC.mood }}</p>
                        <p><strong>Current Activity:</strong> {{ selectedNPC.activity }}</p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Personality Editor -->
                  <div v-if="selectedNPC" class="space-y-4">
                    <h4 class="text-lg font-medieval text-foreground">Personality Traits</h4>
                    
                    <div class="space-y-4">
                      <div 
                        v-for="trait in personalityTraits" 
                        :key="trait.id"
                        class="trait-editor"
                      >
                        <div class="flex items-center justify-between mb-2">
                          <span class="text-sm font-medieval text-foreground">{{ trait.name }}</span>
                          <span class="text-sm text-muted-foreground">{{ trait.value }}%</span>
                        </div>
                        <input 
                          v-model="trait.value"
                          type="range"
                          min="0"
                          max="100"
                          step="5"
                          class="gm-slider w-full"
                          @input="updatePersonality"
                        />
                      </div>
                    </div>
                    
                    <!-- Dialogue Responses -->
                    <div class="space-y-3">
                      <h5 class="text-md font-medieval text-foreground">Dialogue Responses</h5>
                      <textarea 
                        v-model="selectedNPC.dialogueStyle"
                        class="w-full h-24 p-3 bg-background border border-border rounded-lg font-medieval text-foreground resize-none"
                        placeholder="Describe how this NPC speaks and responds..."
                      />
                    </div>
                    
                    <!-- Save Changes -->
                    <RippleButton 
                      class="w-full faction-empire font-medieval"
                      ripple-color="rgb(255, 215, 0)"
                      @click="saveNPCChanges"
                    >
                      <Icon name="save" class="w-4 h-4 mr-2" />
                      Save Changes
                    </RippleButton>
                  </div>
                </div>
              </div>
              
              <!-- Event Scripting Tab -->
              <div v-if="activeTab === 'event-scripting'" class="space-y-6">
                <h3 class="text-2xl font-medieval text-foreground">Event Scripting System</h3>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <!-- Script Editor -->
                  <div class="space-y-4">
                    <h4 class="text-lg font-medieval text-foreground">Event Script</h4>
                    <textarea 
                      v-model="eventScript"
                      class="w-full h-64 p-4 bg-background border border-border rounded-lg font-mono text-sm text-foreground resize-none"
                      placeholder="// Event Script Example
event.onTrigger(() => {
  tavern.addPatron('Mysterious Stranger');
  tavern.setMood('tense');
  dialogue.show('A hooded figure enters...');
});"
                    />
                    
                    <div class="flex space-x-3">
                      <RippleButton 
                        class="flex-1 bg-green-600 text-white font-medieval"
                        ripple-color="rgba(34, 197, 94, 0.6)"
                        @click="testScript"
                      >
                        <Icon name="play" class="w-4 h-4 mr-2" />
                        Test Script
                      </RippleButton>
                      
                      <ShimmerButton 
                        class="flex-1 bg-secondary text-secondary-foreground font-medieval"
                        shimmer-color="rgba(139, 69, 19, 0.5)"
                        @click="saveScript"
                      >
                        <Icon name="save" class="w-4 h-4 mr-2" />
                        Save Script
                      </ShimmerButton>
                    </div>
                  </div>
                  
                  <!-- Script Templates -->
                  <div class="space-y-4">
                    <h4 class="text-lg font-medieval text-foreground">Script Templates</h4>
                    
                    <div class="space-y-2 max-h-64 overflow-y-auto">
                      <div 
                        v-for="template in scriptTemplates" 
                        :key="template.id"
                        class="template-item p-3 rounded-lg bg-background/30 hover:bg-background/50 transition-colors cursor-pointer"
                        @click="loadTemplate(template)"
                      >
                        <h5 class="font-medieval text-foreground">{{ template.name }}</h5>
                        <p class="text-xs text-muted-foreground">{{ template.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Save/Load Tab -->
              <div v-if="activeTab === 'save-load'" class="space-y-6">
                <h3 class="text-2xl font-medieval text-foreground">Save & Load System</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- Save State -->
                  <div class="space-y-4">
                    <h4 class="text-lg font-medieval text-foreground">Save Current State</h4>
                    
                    <input 
                      v-model="saveStateName"
                      type="text"
                      class="w-full p-3 bg-background border border-border rounded-lg font-medieval text-foreground"
                      placeholder="Enter save state name..."
                    />
                    
                    <textarea 
                      v-model="saveStateDescription"
                      class="w-full h-24 p-3 bg-background border border-border rounded-lg font-medieval text-foreground resize-none"
                      placeholder="Describe this save state..."
                    />
                    
                    <RippleButton 
                      class="w-full bg-green-600 text-white font-medieval"
                      ripple-color="rgba(34, 197, 94, 0.6)"
                      @click="saveCurrentState"
                    >
                      <Icon name="save" class="w-4 h-4 mr-2" />
                      Save Current State
                    </RippleButton>
                  </div>
                  
                  <!-- Load State -->
                  <div class="space-y-4">
                    <h4 class="text-lg font-medieval text-foreground">Load Saved State</h4>
                    
                    <div class="space-y-2 max-h-64 overflow-y-auto">
                      <div 
                        v-for="save in savedStates" 
                        :key="save.id"
                        class="save-item p-3 rounded-lg bg-background/30 hover:bg-background/50 transition-colors"
                      >
                        <div class="flex items-center justify-between">
                          <div>
                            <h5 class="font-medieval text-foreground">{{ save.name }}</h5>
                            <p class="text-xs text-muted-foreground">{{ save.date }}</p>
                          </div>
                          
                          <div class="flex space-x-2">
                            <RippleButton 
                              class="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center"
                              ripple-color="rgba(37, 99, 235, 0.6)"
                              @click="loadState(save)"
                            >
                              <Icon name="download" class="w-3 h-3" />
                            </RippleButton>
                            
                            <RippleButton 
                              class="w-8 h-8 rounded-full bg-red-600 text-white flex items-center justify-center"
                              ripple-color="rgba(220, 38, 38, 0.6)"
                              @click="deleteSave(save)"
                            >
                              <Icon name="trash" class="w-3 h-3" />
                            </RippleButton>
                          </div>
                        </div>
                        
                        <p class="text-sm text-muted-foreground mt-2">{{ save.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </BorderBeam>
      </section>
    </div>
  </div>
</template><script setup lang="ts">
// Page metadata
useHead({
  title: 'GM Dashboard - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Comprehensive Game Master dashboard for managing NPCs, events, economy, and tavern scenarios.' }
  ]
})

// GM Dashboard state
const activeNPCs = ref(12)
const activeEvents = ref(3)
const playersOnline = ref(8)
const activeTab = ref('npc-editor')

// Focus Mode for GM Interface
const focusMode = ref(false)
const sessionPaused = ref(false)

// NPC Management
const selectedNPCId = ref('')
const activeNPCList = ref([
  {
    id: 'npc-1',
    name: 'Wilhelm the Barkeep',
    title: 'Tavern Owner',
    icon: 'user',
    status: 'Serving customers',
    active: true,
    faction: 'Empire',
    mood: 'Cheerful',
    activity: 'Cleaning mugs',
    dialogueStyle: 'Friendly and welcoming, speaks with a slight accent. Often mentions local gossip and offers advice to travelers.'
  },
  {
    id: 'npc-2',
    name: 'Brunhilde the Cook',
    title: 'Head Chef',
    icon: 'utensils',
    status: 'Preparing meals',
    active: true,
    faction: 'Empire',
    mood: 'Busy',
    activity: 'Cooking stew',
    dialogueStyle: 'Direct and no-nonsense, but caring. Speaks loudly over kitchen noise and takes pride in her cooking.'
  },
  {
    id: 'npc-3',
    name: 'Gareth the Bard',
    title: 'Traveling Musician',
    icon: 'music',
    status: 'Entertaining guests',
    active: true,
    faction: 'Neutral',
    mood: 'Artistic',
    activity: 'Playing lute',
    dialogueStyle: 'Eloquent and dramatic, speaks in verse when excited. Loves to tell stories and share news from distant lands.'
  },
  {
    id: 'npc-4',
    name: 'Old Henrik',
    title: 'Regular Patron',
    icon: 'user-check',
    status: 'Drinking ale',
    active: true,
    faction: 'Empire',
    mood: 'Grumpy',
    activity: 'Complaining',
    dialogueStyle: 'Gruff and pessimistic, but has a good heart. Often complains about "the good old days" and current politics.'
  },
  {
    id: 'npc-5',
    name: 'Sister Mathilde',
    title: 'Priestess of Shallya',
    icon: 'heart',
    status: 'Tending wounded',
    active: true,
    faction: 'Empire',
    mood: 'Compassionate',
    activity: 'Healing',
    dialogueStyle: 'Gentle and caring, speaks softly. Often offers blessings and healing to those in need.'
  },
  {
    id: 'npc-6',
    name: 'Captain Richter',
    title: 'City Watch',
    icon: 'shield',
    status: 'On patrol',
    active: false,
    faction: 'Empire',
    mood: 'Vigilant',
    activity: 'Investigating',
    dialogueStyle: 'Authoritative and professional, speaks in military terms. Always alert for trouble and maintains order.'
  }
])

// Event Management
const runningEvents = ref([
  {
    id: 'event-1',
    name: 'Merchant Caravan Arrival',
    description: 'A wealthy merchant caravan has arrived, bringing exotic goods and news',
    timeLeft: '45 min',
    progress: 65
  },
  {
    id: 'event-2',
    name: 'Mysterious Stranger',
    description: 'A hooded figure sits alone in the corner, watching everyone',
    timeLeft: '1h 20min',
    progress: 30
  },
  {
    id: 'event-3',
    name: 'Drinking Contest',
    description: 'Local patrons are competing in a drinking contest',
    timeLeft: '25 min',
    progress: 80
  }
])

// Economy Settings
const economySettings = ref({
  goldInflation: 15,
  tradeVolume: 120,
  questRewards: 150
})

// GM Tabs
const gmTabs = ref([
  { id: 'npc-editor', name: 'NPC Editor', icon: 'users' },
  { id: 'event-scripting', name: 'Event Scripting', icon: 'code' },
  { id: 'save-load', name: 'Save/Load', icon: 'save' }
])

// NPC Personality Editor
const personalityTraits = ref([
  { id: 'friendliness', name: 'Friendliness', value: 75 },
  { id: 'aggression', name: 'Aggression', value: 25 },
  { id: 'intelligence', name: 'Intelligence', value: 60 },
  { id: 'curiosity', name: 'Curiosity', value: 80 },
  { id: 'trustworthiness', name: 'Trustworthiness', value: 90 },
  { id: 'greed', name: 'Greed', value: 30 },
  { id: 'courage', name: 'Courage', value: 70 },
  { id: 'humor', name: 'Sense of Humor', value: 65 }
])

// Event Scripting
const eventScript = ref(`// Event Script Example
event.onTrigger(() => {
  tavern.addPatron('Mysterious Stranger');
  tavern.setMood('tense');
  dialogue.show('A hooded figure enters the tavern, their eyes scanning the room...');
  
  // Set up interaction options
  dialogue.addOption('Approach the stranger', () => {
    dialogue.show('The stranger looks up as you approach. "I seek information," they whisper.');
  });
  
  dialogue.addOption('Ignore them', () => {
    tavern.addEvent('Stranger becomes suspicious');
  });
});`)

const scriptTemplates = ref([
  {
    id: 'template-1',
    name: 'New Patron Arrival',
    description: 'Script for when a new patron enters the tavern',
    script: `event.onTrigger(() => {
  const patron = tavern.generateRandomPatron();
  tavern.addPatron(patron);
  dialogue.show(\`\${patron.name} enters the tavern.\`);
});`
  },
  {
    id: 'template-2',
    name: 'Weather Change',
    description: 'Script for weather-related events',
    script: `event.onTrigger(() => {
  weather.change('storm');
  tavern.setMood('cozy');
  dialogue.show('Thunder rumbles outside as rain begins to fall.');
});`
  },
  {
    id: 'template-3',
    name: 'Quest Giver',
    description: 'Script for introducing quest opportunities',
    script: `event.onTrigger(() => {
  const questGiver = tavern.findNPC('questGiver');
  dialogue.show(\`\${questGiver.name} approaches with an urgent request.\`);
  quest.offer('Rescue Mission', 'A merchant needs help retrieving stolen goods.');
});`
  }
])

// Save/Load System
const saveStateName = ref('')
const saveStateDescription = ref('')
const savedStates = ref([
  {
    id: 'save-1',
    name: 'Peaceful Evening',
    description: 'Quiet tavern atmosphere with regular patrons',
    date: '2024-01-15 20:30'
  },
  {
    id: 'save-2',
    name: 'Festival Night',
    description: 'Crowded tavern during the Harvest Festival',
    date: '2024-01-14 22:15'
  },
  {
    id: 'save-3',
    name: 'Storm Shelter',
    description: 'Travelers seeking shelter from a fierce storm',
    date: '2024-01-13 19:45'
  }
])

// Computed properties
const selectedNPC = computed(() => {
  return activeNPCList.value.find(npc => npc.id === selectedNPCId.value) || null
})

// NPC Management Methods
const openNPCEditor = () => {
  activeTab.value = 'npc-editor'
  console.log('Opening NPC Editor...')
}

const openBehaviorEditor = () => {
  console.log('Opening AI Behavior Editor...')
  // This would open a more advanced AI behavior configuration panel
}

const spawnRandomNPC = () => {
  const randomNames = ['Aldric', 'Gwendolyn', 'Thorek', 'Elara', 'Magnus', 'Isolde']
  const randomTitles = ['Merchant', 'Soldier', 'Scholar', 'Pilgrim', 'Artisan', 'Noble']
  const randomIcons = ['user', 'briefcase', 'sword', 'book', 'hammer', 'crown']
  
  const newNPC = {
    id: `npc-${Date.now()}`,
    name: randomNames[Math.floor(Math.random() * randomNames.length)],
    title: randomTitles[Math.floor(Math.random() * randomTitles.length)],
    icon: randomIcons[Math.floor(Math.random() * randomIcons.length)],
    status: 'Just arrived',
    active: true,
    faction: 'Empire',
    mood: 'Curious',
    activity: 'Looking around',
    dialogueStyle: 'Polite and inquisitive, new to the area.'
  }
  
  activeNPCList.value.push(newNPC)
  activeNPCs.value++
  
  console.log('Spawned random NPC:', newNPC.name)
}

const openNPCTemplates = () => {
  console.log('Opening NPC Templates...')
  // This would show pre-made NPC templates
}

const selectNPC = (npc: any) => {
  selectedNPCId.value = npc.id
  activeTab.value = 'npc-editor'
}

const editNPC = (npc: any) => {
  selectedNPCId.value = npc.id
  activeTab.value = 'npc-editor'
}

const updatePersonality = () => {
  if (selectedNPC.value) {
    console.log('Updating personality for:', selectedNPC.value.name)
    // Update NPC personality based on trait values
  }
}

const saveNPCChanges = () => {
  if (selectedNPC.value) {
    console.log('Saving changes for:', selectedNPC.value.name)
    // Save NPC changes to persistent storage
    alert(`Changes saved for ${selectedNPC.value.name}!`)
  }
}

// Event Management Methods
const createEvent = () => {
  console.log('Creating new event...')
  // This would open an event creation dialog
}

const openEventScripting = () => {
  activeTab.value = 'event-scripting'
}

const triggerRandomEvent = () => {
  const randomEvents = [
    'A traveling merchant offers rare goods',
    'Local militia recruits volunteers',
    'A mysterious letter is delivered',
    'Strange lights appear in the sky',
    'A famous bard requests to perform'
  ]
  
  const randomEvent = randomEvents[Math.floor(Math.random() * randomEvents.length)]
  
  const newEvent = {
    id: `event-${Date.now()}`,
    name: 'Random Event',
    description: randomEvent,
    timeLeft: '30 min',
    progress: 0
  }
  
  runningEvents.value.push(newEvent)
  activeEvents.value++
  
  console.log('Triggered random event:', randomEvent)
}

const openEventTemplates = () => {
  console.log('Opening event templates...')
}

const stopEvent = (event: any) => {
  const index = runningEvents.value.findIndex(e => e.id === event.id)
  if (index > -1) {
    runningEvents.value.splice(index, 1)
    activeEvents.value--
    console.log('Stopped event:', event.name)
  }
}

// Event Scripting Methods
const testScript = () => {
  console.log('Testing script:', eventScript.value)
  try {
    // In a real implementation, this would safely execute the script
    alert('Script test completed successfully!')
  } catch (error) {
    alert('Script error: ' + error.message)
  }
}

const saveScript = () => {
  console.log('Saving script...')
  // Save script to persistent storage
  alert('Script saved successfully!')
}

const loadTemplate = (template: any) => {
  eventScript.value = template.script
  console.log('Loaded template:', template.name)
}

// Economy Methods
const updateEconomy = () => {
  console.log('Updating economy settings:', economySettings.value)
  // Apply economy changes to the game world
}

// Save/Load Methods
const openSaveLoad = () => {
  activeTab.value = 'save-load'
}

const saveCurrentState = () => {
  if (!saveStateName.value.trim()) {
    alert('Please enter a name for the save state.')
    return
  }
  
  const newSave = {
    id: `save-${Date.now()}`,
    name: saveStateName.value,
    description: saveStateDescription.value || 'No description provided',
    date: new Date().toLocaleString()
  }
  
  savedStates.value.unshift(newSave)
  
  // Clear form
  saveStateName.value = ''
  saveStateDescription.value = ''
  
  console.log('Saved state:', newSave.name)
  alert('State saved successfully!')
}

const loadState = (save: any) => {
  console.log('Loading state:', save.name)
  // Load the saved state
  alert(`Loading state: ${save.name}`)
}

const deleteSave = (save: any) => {
  if (confirm(`Are you sure you want to delete "${save.name}"?`)) {
    const index = savedStates.value.findIndex(s => s.id === save.id)
    if (index > -1) {
      savedStates.value.splice(index, 1)
      console.log('Deleted save:', save.name)
    }
  }
}

// Other GM Tools
const openQuestCreator = () => {
  console.log('Opening Quest Creator...')
  // Navigate to quest creation tool
}

const openDialogueEditor = () => {
  console.log('Opening Dialogue Editor...')
  // Open dialogue tree editor
}

const resetToDefaults = () => {
  if (confirm('Are you sure you want to reset all settings to defaults?')) {
    // Reset all settings
    economySettings.value = {
      goldInflation: 0,
      tradeVolume: 100,
      questRewards: 100
    }

    console.log('Reset to defaults')
    alert('Settings reset to defaults!')
  }
}

// Focus Mode and Session Management Methods
const toggleFocusMode = () => {
  focusMode.value = !focusMode.value
  console.log('Focus mode:', focusMode.value ? 'ON' : 'OFF')

  if (focusMode.value) {
    // Hide non-essential panels and maximize critical focus areas
    document.body.classList.add('gm-focus-mode')
  } else {
    document.body.classList.remove('gm-focus-mode')
  }
}

const saveSession = () => {
  const sessionData = {
    timestamp: new Date().toISOString(),
    activeNPCs: activeNPCList.value,
    runningEvents: runningEvents.value,
    economySettings: economySettings.value,
    atmosphereSettings: {
      // This would include current atmosphere state
    }
  }

  console.log('Saving session:', sessionData)
  localStorage.setItem('gm-session-backup', JSON.stringify(sessionData))
  alert('Session saved successfully!')
}

const emergencyPause = () => {
  sessionPaused.value = !sessionPaused.value

  if (sessionPaused.value) {
    // Pause all active events and timers
    console.log('Emergency pause activated - all events paused')
    alert('Session paused - all events and timers stopped')
  } else {
    console.log('Session resumed')
    alert('Session resumed')
  }
}

// Atmospheric Control Handlers
const handleWeatherChange = (weather: string, intensity: number) => {
  console.log('Weather changed:', weather, intensity)
  // Apply weather changes to the tavern
}

const handleTimeChange = (time: string) => {
  console.log('Time changed:', time)
  // Apply time of day changes
}

const handleFireplaceChange = (active: boolean, intensity: number) => {
  console.log('Fireplace changed:', active, intensity)
  // Apply fireplace changes
}

const handleCandleChange = (count: number) => {
  console.log('Candle count changed:', count)
  // Apply candle lighting changes
}

const handleAudioChange = (layer: string, active: boolean, volume: number) => {
  console.log('Audio layer changed:', layer, active, volume)
  // Apply audio layer changes
}

const handleCrowdChange = (size: string, mood: string, noise: number) => {
  console.log('Crowd changed:', size, mood, noise)
  // Apply crowd changes
}

const handlePresetApplied = (preset: any) => {
  console.log('Atmosphere preset applied:', preset.name)
  // Apply all preset changes
}

// Lifecycle
onMounted(() => {
  console.log('GM Dashboard initialized')

  // Start real-time updates
  setInterval(() => {
    // Update running events progress
    runningEvents.value.forEach(event => {
      if (event.progress < 100) {
        event.progress += Math.random() * 5
        if (event.progress >= 100) {
          event.progress = 100
          // Event completed
        }
      }
    })
  }, 5000)
})
</script>

<style scoped>
/* GM Dashboard specific styles */
.gm-dashboard {
  background-attachment: fixed;
}

.gm-panel {
  animation: panel-slide-up 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.gm-status-item {
  animation: status-bounce 0.6s ease-out forwards;
}

.npc-item,
.event-item {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.npc-item:hover,
.event-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.tab-button {
  transition: all 0.3s ease;
}

.tab-button:hover {
  transform: translateY(-1px);
}

.gm-slider {
  appearance: none;
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(to right, #8b5cf6 0%, #8b5cf6 var(--value, 0%), #374151 var(--value, 0%), #374151 100%);
  outline: none;
  transition: all 0.2s ease;
}

.gm-slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #8b5cf6;
  cursor: pointer;
  border: 2px solid #7c3aed;
  transition: all 0.2s ease;
}

.gm-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
  box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
}

.gm-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #8b5cf6;
  cursor: pointer;
  border: 2px solid #7c3aed;
  transition: all 0.2s ease;
}

.npc-preview {
  animation: preview-fade-in 0.4s ease-out;
}

.trait-editor {
  animation: trait-slide-in 0.5s ease-out;
}

.template-item,
.save-item {
  transition: all 0.2s ease;
}

.template-item:hover,
.save-item:hover {
  transform: translateX(4px);
}

/* Custom animations */
@keyframes panel-slide-up {
  0% {
    opacity: 0;
    transform: translateY(30px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes status-bounce {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.8);
  }
  60% {
    transform: translateY(-5px) scale(1.1);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes preview-fade-in {
  0% {
    opacity: 0;
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes trait-slide-in {
  0% {
    opacity: 0;
    transform: translateX(-10px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Responsive design */
@media (max-width: 1280px) {
  .gm-panel {
    animation-delay: 0s;
  }
}

@media (max-width: 768px) {
  .gm-status-item {
    animation-delay: 0s;
  }
  
  .tab-content {
    min-height: 300px;
  }
}

/* Focus Mode Styles */
.gm-focus-mode .legacy-panel {
  display: none !important;
}

.gm-focus-mode .gm-panel {
  transition: all 0.3s ease;
}

.focus-mode .dashboard-grid {
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.focus-mode .left-panel.collapsed {
  transform: translateX(-100%);
  opacity: 0;
  pointer-events: none;
}

.focus-toggle {
  transition: all 0.3s ease;
}

.focus-toggle:hover {
  transform: scale(1.05);
}

/* Performance optimizations */
.gm-panel,
.npc-item,
.event-item,
.tab-button,
.gm-slider,
.template-item,
.save-item {
  will-change: transform;
}
</style>