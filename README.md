# 🏰 Warhammer Tavern Simulator v3
## Powered by Nuxt.js & Inspira UI

### 🌟 Overview

Welcome to the most immersive Warhammer Fantasy tavern experience ever created! This v3 implementation leverages the full power of **Inspira UI** components with **Nuxt.js** to deliver stunning visual effects, smooth animations, and an unparalleled user experience.

### ✨ Key Features

#### 🎨 **Full Inspira UI Integration**
- **25+ Advanced Components** implemented with Warhammer theming
- **Spectacular Visual Effects**: Aurora backgrounds, meteors, particles, spotlights
- **Interactive Elements**: Lens magnification, direction-aware hover, 3D cards
- **Advanced Animations**: Text reveal, sparkles, border beams, ripple effects

#### 🏛️ **Immersive Warhammer Experience**
- **AI-Powered NPCs** with unique personalities and backstories
- **Dynamic Tavern Environment** with real-time events and atmosphere
- **Faction-Based Theming** for Empire, Chaos, Elves, Dwarfs, and more
- **Medieval Typography** with custom fonts (Cinzel, Uncial Antiqua, MedievalSharp)

#### 🎮 **Advanced Game Master Tools**
- **Enhanced NPC Management**: AI-powered quick generation, personality editor, template system
- **Smart Event Management**: Timeline visualization, AI suggestions, progress tracking
- **Atmosphere Control**: Real-time lighting, weather, and audio controls with presets
- **Focus Mode**: Streamlined interface for critical gaming moments
- **Real-time Collaboration**: Multi-GM support with WebSocket integration
- **Session Management**: Auto-save, emergency pause, and state restoration

#### 🚀 **Modern Tech Stack**
- **Nuxt.js v3** with Vue 3 Composition API
- **TypeScript** for type safety
- **TailwindCSS** with custom Warhammer color system
- **Pinia** for state management
- **Google Fonts** integration

### 🎮 Game Master Features

#### **Enhanced NPC Management**
- **AI-Powered Generation**: One-click random NPC creation with personality traits
- **Advanced Personality Editor**: Granular control over NPC traits with visual sliders
- **Template System**: Save and load NPC templates for consistent character types
- **Auto-save Functionality**: Prevent data loss during intense gaming sessions
- **Quick Actions**: Instant NPC spawning, behavior editing, and template management

#### **Smart Event Management**
- **AI Event Suggestions**: Context-aware event recommendations based on current tavern state
- **Timeline Visualization**: Visual timeline showing event progression and scheduling
- **Event Templates Library**: Pre-built events for common scenarios (merchant arrivals, brawls, weather)
- **Progress Tracking**: Real-time event progress with visual indicators
- **Trigger System**: Quick-action buttons for immediate event responses

#### **Advanced Atmosphere Control**
- **Preset System**: 8 atmospheric presets (Cozy Evening, Stormy Night, Festival, etc.)
- **Real-time Controls**: Live adjustment of lighting, weather, and audio
- **Atmosphere Timeline**: Plan and execute atmospheric sequences
- **Quick Actions**: Dramatic moment triggers, tension builders, mystery additions

#### **Focus Mode & Session Management**
- **Focus Mode Toggle**: Hide non-essential panels during critical moments
- **Emergency Pause**: Instantly pause all events and timers
- **Session Backup**: Automatic session state saving and restoration
- **Responsive Design**: Optimized for different screen sizes and devices

#### **Real-time Collaboration**
- **Multi-GM Support**: WebSocket-based real-time collaboration
- **Conflict Resolution**: Automatic handling of simultaneous changes
- **Action Broadcasting**: Share NPC updates, events, and atmosphere changes
- **Connection Management**: Automatic reconnection and offline queue

### 🎯 Inspira UI Components Implemented

#### Core UI Components
| Component | Purpose | Warhammer Enhancement |
|-----------|---------|----------------------|
| `AuroraBackground` | Mystical tavern atmosphere | Golden/amber color scheme |
| `ParticlesBg` | Magic effects | Fire particles, gold sparkles |
| `Meteors` | Dramatic sky effects | Customizable count and speed |
| `BorderBeam` | Animated borders | Faction-colored beams |
| `Spotlight` | Interactive highlighting | Character focus effects |
| `Lens` | Magnification effects | Character detail views |

#### Text & Typography
| Component | Purpose | Warhammer Enhancement |
|-----------|---------|----------------------|
| `HyperText` | Animated text reveal | Medieval character scramble |
| `SparklesText` | Magical text effects | Gold sparkles animation |
| `Text3D` | Dimensional text | Shadow depth effects |
| `TextReveal` | Character-by-character reveal | Smooth storytelling |
| `NumberTicker` | Animated counters | Tavern statistics |

#### Interactive Elements
| Component | Purpose | Warhammer Enhancement |
|-----------|---------|----------------------|
| `Card3D` | Interactive cards | Character portraits |
| `DirectionAwareHover` | Smart hover effects | Character interactions |
| `ExpandableGallery` | Character showcase | NPC gallery |
| `InteractiveGridPattern` | Background patterns | Tavern floor effects |
| `Timeline` | Event history | Tavern chronicles |

#### Buttons & Controls
| Component | Purpose | Warhammer Enhancement |
|-----------|---------|----------------------|
| `ShimmerButton` | Elegant buttons | Gold shimmer effects |
| `RippleButton` | Interactive feedback | Faction-colored ripples |
| `RainbowButton` | Multi-color effects | Elven magic buttons |
| `Dock` | Navigation | Floating tavern menu |

#### Advanced Features
| Component | Purpose | Warhammer Enhancement |
|-----------|---------|----------------------|
| `AnimatedTestimonials` | Character quotes | NPC storytelling |
| `Lens` | Magnification | Character details |
| `Spotlight` | Focus effects | Character highlighting |

### 🏗️ Project Structure

```
warhammer-tavern-v3/
├── assets/
│   └── css/
│       ├── main.css              # Base styles with Warhammer theme
│       ├── inspira-ui.css        # Inspira UI customizations
│       └── warhammer-theme.css   # Extended Warhammer styling
├── components/
│   ├── inspira/                  # Inspira UI components
│   │   ├── AuroraBackground.vue
│   │   ├── ParticlesBg.vue
│   │   ├── Meteors.vue
│   │   ├── BorderBeam.vue
│   │   ├── Spotlight.vue
│   │   ├── Lens.vue
│   │   ├── HyperText.vue
│   │   ├── SparklesText.vue
│   │   ├── Text3D.vue
│   │   ├── TextReveal.vue
│   │   ├── NumberTicker.vue
│   │   ├── Card3D.vue
│   │   ├── DirectionAwareHover.vue
│   │   ├── ExpandableGallery.vue
│   │   ├── InteractiveGridPattern.vue
│   │   ├── Timeline.vue
│   │   ├── ShimmerButton.vue
│   │   ├── RippleButton.vue
│   │   ├── RainbowButton.vue
│   │   ├── Dock.vue
│   │   ├── AnimatedTestimonials.vue
│   │   └── LiquidBackground.vue
│   ├── gm/                       # Game Master components
│   │   ├── NPCManager.vue        # Enhanced NPC management
│   │   ├── EnhancedEventManager.vue  # Smart event system
│   │   ├── SmartAtmosphereControl.vue # Advanced atmosphere controls
│   │   └── AtmosphericControls.vue   # Legacy atmosphere controls
│   └── ui/
│       └── Icon.vue              # Custom icon component
├── layouts/
│   └── default.vue               # Main layout with navigation
├── pages/
│   ├── index.vue                 # Homepage with character gallery
│   ├── characters.vue            # Character showcase
│   ├── tavern.vue               # Main tavern experience
│   ├── gm-dashboard.vue         # Game Master dashboard
│   └── conversations/
│       └── index.vue            # Conversation system
├── composables/                  # Vue composables
│   ├── useGMCollaboration.ts    # Real-time GM collaboration
│   ├── useWarhammerData.ts      # Warhammer data management
│   ├── useQuestGenerator.ts     # Quest generation system
│   └── useInteractiveTavernSystems.ts # Tavern systems
├── stores/                       # Pinia stores (future)
├── nuxt.config.ts               # Nuxt configuration
├── tailwind.config.js           # TailwindCSS with Warhammer theme
└── package.json                 # Dependencies
```

### 🎨 Design System

#### Color Palette
```css
/* Faction Colors */
--faction-empire: #ffd700      /* Empire Gold */
--faction-chaos: #8b0000       /* Chaos Red */
--faction-elves: #228b22       /* Elven Green */
--faction-dwarfs: #b8860b      /* Dwarf Bronze */
--faction-undead: #4b0082      /* Undead Purple */
--faction-orcs: #556b2f        /* Orc Green */

/* Atmospheric Colors */
--tavern-wood: #8b4513         /* Tavern Wood */
--tavern-stone: #696969        /* Stone Gray */
--tavern-fire: #ff4500         /* Fire Orange */
--tavern-shadow: #2f1b14       /* Deep Shadow */
```

#### Typography
- **Medieval Headers**: Cinzel (serif)
- **Fantasy Text**: Uncial Antiqua (cursive)
- **Sharp Accents**: MedievalSharp (cursive)
- **Body Text**: Inter (sans-serif)

### 🚀 Getting Started

#### Prerequisites
- Node.js 18+ 
- npm or yarn

#### Installation
```bash
# Clone the repository
cd warhammer-tavern-v3

# Install dependencies
npm install

# Start development server
npm run dev
```

#### Build for Production
```bash
# Build the application
npm run build

# Preview production build
npm run preview
```

### 🎮 Features Showcase

#### 🏠 **Homepage**
- **Hero Section** with SparklesText and Text3D
- **Character Gallery** with ExpandableGallery and DirectionAwareHover
- **Statistics Cards** with Card3D and NumberTicker
- **Timeline** of recent events
- **Call-to-Action** with BorderBeam effects

#### 👥 **Characters Page**
- **Advanced Character Cards** with Lens magnification
- **Faction Filtering** with morphing tabs
- **Character Details Modal** with BorderBeam
- **Interactive Stats** with animated progress bars
- **Spotlight Effects** on character portraits

#### 🍺 **Tavern Page**
- **Interactive Grid Background** with mouse effects
- **Live Patron System** with real-time updates
- **Atmosphere Controls** (fireplace, music)
- **Dynamic Events Feed** with Timeline
- **Tavern Statistics** with animated progress
- **Weather System** with atmospheric effects

#### 💬 **Conversations Page**
- **Character Testimonials** with AnimatedTestimonials
- **Lens-Enhanced Avatars** with detailed information
- **Trait Visualization** with animated progress bars
- **Conversation Tips** with BorderBeam cards

### 🎯 Performance Features

#### Optimizations
- **Lazy Loading** for all components
- **Animation Performance** with will-change properties
- **Responsive Design** with mobile-first approach
- **Bundle Optimization** with Vite
- **Image Optimization** with Nuxt Image

#### Accessibility
- **Keyboard Navigation** support
- **Screen Reader** compatibility
- **Focus Management** for interactive elements
- **Color Contrast** compliance
- **Reduced Motion** support

### 🔧 Customization

#### Adding New Characters
```typescript
// Add to characters array in pages/characters.vue
{
  id: 'new-character',
  name: 'Character Name',
  title: 'Character Title',
  faction: 'Empire',
  factionColor: 'bg-faction-empire-500',
  icon: 'sword',
  description: 'Character description...',
  stats: { attack: 85, defense: 78, magic: 45 }
}
```

#### Creating Custom Inspira UI Components
```vue
<template>
  <div class="custom-component">
    <!-- Your component content -->
  </div>
</template>

<script setup lang="ts">
// Component logic
</script>

<style scoped>
/* Component styles */
</style>
```

### 🌟 Advanced Features

#### Real-Time Events
- **Dynamic Tavern Events** generated every 30 seconds
- **Character Activity Updates** every 45 seconds
- **Weather System** with atmospheric changes
- **Fireplace Effects** with particle animations

#### Interactive Elements
- **Mouse-Responsive Grids** with proximity effects
- **Lens Magnification** for detailed views
- **Direction-Aware Hover** for smart interactions
- **Spotlight Following** mouse movement

#### Animation System
- **Entrance Animations** for all components
- **Staggered Reveals** for lists and grids
- **Particle Systems** for magical effects
- **Smooth Transitions** between states

### 📱 Responsive Design

#### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

#### Mobile Optimizations
- **Touch-Friendly** interactions
- **Optimized Animations** for performance
- **Simplified Layouts** for small screens
- **Gesture Support** for navigation

### 🎨 Theming System

#### CSS Variables
All colors and spacing use CSS variables for easy theming:
```css
:root {
  --primary: 255 215 0;
  --background: 47 25 16;
  --foreground: 255 215 0;
  /* ... more variables */
}
```

#### Faction Theming
Each faction has its own color scheme and styling:
```css
.faction-empire { @apply bg-gradient-to-r from-yellow-600 to-yellow-400; }
.faction-chaos { @apply bg-gradient-to-r from-red-900 to-red-700; }
/* ... more factions */
```

### 🎮 Using the GM Dashboard

#### **Getting Started**
1. Navigate to `/gm-dashboard` to access the Game Master interface
2. Use the **Focus Mode** toggle to streamline the interface during critical moments
3. Access **Emergency Pause** to instantly stop all events and timers

#### **NPC Management**
- **Quick Generate**: Create random NPCs with one click
- **AI Builder**: Use AI-powered personality generation
- **Template System**: Save frequently used NPC types
- **Personality Editor**: Fine-tune NPC traits with visual sliders

#### **Event Management**
- **AI Suggestions**: Get context-aware event recommendations
- **Timeline View**: Visualize event progression and scheduling
- **Quick Actions**: Trigger dramatic moments, build tension, or add mystery
- **Progress Tracking**: Monitor event completion with visual indicators

#### **Atmosphere Control**
- **Presets**: Choose from 8 atmospheric presets (Cozy Evening, Stormy Night, etc.)
- **Real-time Controls**: Adjust lighting, weather, and audio on the fly
- **Timeline Sequences**: Plan and execute atmospheric changes
- **Quick Actions**: Instant dramatic effects and mood changes

#### **Collaboration Features**
- **Multi-GM Support**: Multiple Game Masters can collaborate in real-time
- **Action Broadcasting**: Share NPC updates and events across sessions
- **Conflict Resolution**: Automatic handling of simultaneous changes
- **Session Management**: Save and restore complete session states

### 🚀 Future Enhancements

#### Planned Features
- [ ] **Real-time Chat** with AI NPCs
- [ ] **Quest System** with interactive storylines
- [ ] **Inventory Management** with drag-and-drop
- [ ] **Sound System** with ambient tavern sounds
- [ ] **Save System** for character progress
- [ ] **Multiplayer Support** for shared tavern experience

#### Technical Improvements
- [ ] **PWA Support** for offline functionality
- [ ] **WebGL Effects** for enhanced visuals
- [ ] **Voice Recognition** for character interactions
- [ ] **AI Integration** with advanced language models
- [ ] **Performance Monitoring** with analytics
- [ ] **Automated Testing** suite

### 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

### 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting pull requests.

### 🙏 Acknowledgments

- **Inspira UI** for the amazing component library
- **Nuxt.js Team** for the excellent framework
- **TailwindCSS** for the utility-first CSS framework
- **Warhammer Fantasy** for the rich lore and inspiration

---

**Built with ❤️ and ⚔️ for the Warhammer Fantasy community**