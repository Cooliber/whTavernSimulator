<template>
  <div class="min-h-screen bg-background text-foreground p-8">
    <div class="max-w-4xl mx-auto space-y-8">
      <h1 class="text-4xl font-medieval text-center text-primary">Component Test Page</h1>
      
      <!-- Test basic text -->
      <div class="text-center">
        <h2 class="text-2xl font-medieval mb-4">Welcome to the Warhammer Tavern</h2>
        <p class="text-muted-foreground">This is a simple test to verify components are working.</p>
      </div>

      <!-- Test Icon component -->
      <div class="text-center space-y-4">
        <h3 class="text-xl font-medieval">Icon Component Test</h3>
        <div class="flex justify-center space-x-4">
          <Icon name="sword" class="w-8 h-8 text-primary" />
          <Icon name="shield" class="w-8 h-8 text-secondary" />
          <Icon name="crown" class="w-8 h-8 text-accent" />
        </div>
      </div>

      <!-- Test SparklesText if available -->
      <div class="text-center">
        <h3 class="text-xl font-medieval mb-4">SparklesText Component Test</h3>
        <SparklesText 
          text="Magical Text Effect"
          class="text-2xl font-medieval text-primary"
          :sparkles-count="10"
        />
      </div>

      <!-- Test RippleButton if available -->
      <div class="text-center">
        <h3 class="text-xl font-medieval mb-4">Button Component Test</h3>
        <RippleButton 
          class="px-6 py-3 bg-primary text-primary-foreground font-medieval rounded-lg"
          ripple-color="rgb(255, 215, 0)"
        >
          Test Ripple Button
        </RippleButton>
      </div>

      <!-- Test basic styling -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 bg-card rounded-lg border">
          <h4 class="font-medieval text-lg mb-2">Card 1</h4>
          <p class="text-muted-foreground">Basic card styling test</p>
        </div>
        <div class="p-6 bg-card rounded-lg border">
          <h4 class="font-medieval text-lg mb-2">Card 2</h4>
          <p class="text-muted-foreground">Another card for layout test</p>
        </div>
        <div class="p-6 bg-card rounded-lg border">
          <h4 class="font-medieval text-lg mb-2">Card 3</h4>
          <p class="text-muted-foreground">Third card to complete the grid</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Page metadata
useHead({
  title: 'Component Test - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Testing page for Inspira UI components' }
  ]
})
</script>

<style scoped>
/* Test page specific styles */
.font-medieval {
  font-family: 'Cinzel', serif;
}
</style>
