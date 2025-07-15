import React, { useEffect, useRef, useCallback } from 'react'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { TextPlugin } from 'gsap/TextPlugin'
import { MorphSVGPlugin } from 'gsap/MorphSVGPlugin'
import { DrawSVGPlugin } from 'gsap/DrawSVGPlugin'
import { MotionPathPlugin } from 'gsap/MotionPathPlugin'
import { CustomEase } from 'gsap/CustomEase'

// Register GSAP plugins
gsap.registerPlugin(ScrollTrigger, TextPlugin, MorphSVGPlugin, DrawSVGPlugin, MotionPathPlugin, CustomEase)

// Warhammer Fantasy-specific easing curves
const WarhammerEasing = {
  // Imperium - Noble and steady
  imperial: CustomEase.create("imperial", "M0,0 C0.175,0.885 0.32,1.275 1,1"),
  
  // Chaos - Unpredictable and violent
  chaos: CustomEase.create("chaos", "M0,0 C0.68,-0.55 0.265,1.55 1,1"),
  
  // Elves - Graceful and flowing
  elven: CustomEase.create("elven", "M0,0 C0.25,0.46 0.45,0.94 1,1"),
  
  // Dwarfs - Sturdy and determined
  dwarven: CustomEase.create("dwarven", "M0,0 C0.55,0.055 0.68,0.19 1,1"),
  
  // Orcs - Brutal and direct
  orcish: CustomEase.create("orcish", "M0,0 C0.895,0.03 0.685,0.22 1,1"),
  
  // Undead - Eerie and unnatural
  undead: CustomEase.create("undead", "M0,0 C0.23,1 0.32,0 1,1"),
  
  // Magic - Mystical and otherworldly
  magical: CustomEase.create("magical", "M0,0 C0.42,0 0.58,1 1,1")
}

// Faction-specific animation configurations
const FactionAnimations = {
  Empire: {
    colors: ['#FFD700', '#B8860B', '#8B6914'],
    particles: 'golden_sparks',
    entrance: 'imperial_march',
    idle: 'noble_stance',
    combat: 'disciplined_strike',
    magic: 'divine_blessing',
    sound: 'imperial_fanfare'
  },
  
  Chaos: {
    colors: ['#8B0000', '#FF0000', '#4A0000'],
    particles: 'chaos_corruption',
    entrance: 'chaotic_emergence',
    idle: 'malevolent_presence',
    combat: 'berserker_rage',
    magic: 'warp_distortion',
    sound: 'chaos_whispers'
  },
  
  HighElves: {
    colors: ['#98FB98', '#228B22', '#006400'],
    particles: 'elven_light',
    entrance: 'graceful_arrival',
    idle: 'serene_meditation',
    combat: 'elegant_swordplay',
    magic: 'high_magic_weaving',
    sound: 'elven_chimes'
  },
  
  Dwarfs: {
    colors: ['#DAA520', '#B8860B', '#8B6914'],
    particles: 'forge_sparks',
    entrance: 'sturdy_march',
    idle: 'steadfast_guard',
    combat: 'axe_cleave',
    magic: 'runic_power',
    sound: 'dwarven_chant'
  },
  
  Orcs: {
    colors: ['#228B22', '#006400', '#8FBC8F'],
    particles: 'crude_smoke',
    entrance: 'brutal_charge',
    idle: 'aggressive_posture',
    combat: 'savage_assault',
    magic: 'shamanic_ritual',
    sound: 'orcish_roar'
  },
  
  Undead: {
    colors: ['#800080', '#4B0082', '#2F1B69'],
    particles: 'necromantic_mist',
    entrance: 'spectral_manifestation',
    idle: 'undead_sway',
    combat: 'deathly_strike',
    magic: 'dark_necromancy',
    sound: 'ghostly_wail'
  }
}

export const WarhammerGSAPController = ({ children, faction = 'Empire', animationType = 'idle' }) => {
  const containerRef = useRef(null)
  const timelineRef = useRef(null)
  const particleSystemRef = useRef(null)

  // Initialize faction-specific animations
  const initializeFactionAnimations = useCallback(() => {
    if (!containerRef.current) return

    const factionConfig = FactionAnimations[faction]
    const container = containerRef.current

    // Set faction-specific CSS variables
    container.style.setProperty('--faction-primary', factionConfig.colors[0])
    container.style.setProperty('--faction-secondary', factionConfig.colors[1])
    container.style.setProperty('--faction-tertiary', factionConfig.colors[2])

    // Create main timeline
    timelineRef.current = gsap.timeline({ paused: true })

    // Add faction-specific entrance animation
    createEntranceAnimation(factionConfig, container)
    
    // Add idle animations
    createIdleAnimation(factionConfig, container)
    
    // Initialize particle system
    initializeParticleSystem(factionConfig, container)

  }, [faction])

  // Create entrance animations based on faction
  const createEntranceAnimation = (config, container) => {
    const elements = container.querySelectorAll('.character-element')
    
    switch (config.entrance) {
      case 'imperial_march':
        gsap.fromTo(elements, 
          { 
            x: -100, 
            opacity: 0, 
            rotationY: -15,
            scale: 0.8
          },
          { 
            x: 0, 
            opacity: 1, 
            rotationY: 0,
            scale: 1,
            duration: 1.2,
            ease: WarhammerEasing.imperial,
            stagger: 0.2,
            onComplete: () => playFactionSound(config.sound)
          }
        )
        break

      case 'chaotic_emergence':
        gsap.fromTo(elements,
          {
            scale: 0,
            rotation: 360,
            opacity: 0,
            filter: 'hue-rotate(0deg)'
          },
          {
            scale: 1,
            rotation: 0,
            opacity: 1,
            filter: 'hue-rotate(360deg)',
            duration: 1.5,
            ease: WarhammerEasing.chaos,
            stagger: {
              amount: 0.8,
              from: "random"
            }
          }
        )
        break

      case 'graceful_arrival':
        gsap.fromTo(elements,
          {
            y: -50,
            opacity: 0,
            scale: 0.9,
            filter: 'blur(5px)'
          },
          {
            y: 0,
            opacity: 1,
            scale: 1,
            filter: 'blur(0px)',
            duration: 2,
            ease: WarhammerEasing.elven,
            stagger: 0.15
          }
        )
        break

      case 'sturdy_march':
        gsap.fromTo(elements,
          {
            x: -200,
            opacity: 0,
            scaleX: 0.7
          },
          {
            x: 0,
            opacity: 1,
            scaleX: 1,
            duration: 1.8,
            ease: WarhammerEasing.dwarven,
            stagger: 0.1
          }
        )
        break

      case 'brutal_charge':
        gsap.fromTo(elements,
          {
            x: 300,
            opacity: 0,
            rotation: 15,
            scale: 1.2
          },
          {
            x: 0,
            opacity: 1,
            rotation: 0,
            scale: 1,
            duration: 0.8,
            ease: WarhammerEasing.orcish,
            stagger: 0.05
          }
        )
        break

      case 'spectral_manifestation':
        gsap.fromTo(elements,
          {
            opacity: 0,
            scale: 1.5,
            filter: 'blur(10px) brightness(2)'
          },
          {
            opacity: 0.9,
            scale: 1,
            filter: 'blur(0px) brightness(1)',
            duration: 2.5,
            ease: WarhammerEasing.undead,
            stagger: 0.3
          }
        )
        break
    }
  }

  // Create faction-specific idle animations
  const createIdleAnimation = (config, container) => {
    const elements = container.querySelectorAll('.character-element')
    
    switch (config.idle) {
      case 'noble_stance':
        gsap.to(elements, {
          y: "+=3",
          duration: 2,
          ease: "sine.inOut",
          yoyo: true,
          repeat: -1,
          stagger: 0.1
        })
        break

      case 'malevolent_presence':
        gsap.to(elements, {
          scale: 1.02,
          filter: 'brightness(1.1) contrast(1.1)',
          duration: 1.5,
          ease: "power2.inOut",
          yoyo: true,
          repeat: -1,
          stagger: 0.2
        })
        break

      case 'serene_meditation':
        gsap.to(elements, {
          rotationY: "+=2",
          y: "+=2",
          duration: 3,
          ease: "sine.inOut",
          yoyo: true,
          repeat: -1,
          stagger: 0.15
        })
        break

      case 'steadfast_guard':
        gsap.to(elements, {
          x: "+=1",
          duration: 4,
          ease: "power1.inOut",
          yoyo: true,
          repeat: -1,
          stagger: 0.05
        })
        break

      case 'aggressive_posture':
        gsap.to(elements, {
          rotation: "+=1",
          scale: 1.01,
          duration: 1,
          ease: "rough({ template: none.out, strength: 1, points: 20, taper: none, randomize: true, clamp: false})",
          yoyo: true,
          repeat: -1,
          stagger: 0.1
        })
        break

      case 'undead_sway':
        gsap.to(elements, {
          x: "+=2",
          y: "+=1",
          rotation: "+=0.5",
          opacity: 0.95,
          duration: 2.5,
          ease: "sine.inOut",
          yoyo: true,
          repeat: -1,
          stagger: 0.2
        })
        break
    }
  }

  // Initialize particle system for faction effects
  const initializeParticleSystem = (config, container) => {
    const particleContainer = document.createElement('div')
    particleContainer.className = 'particle-system'
    particleContainer.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      overflow: hidden;
    `
    container.appendChild(particleContainer)
    particleSystemRef.current = particleContainer

    // Create faction-specific particles
    createFactionParticles(config, particleContainer)
  }

  // Create faction-specific particle effects
  const createFactionParticles = (config, container) => {
    const particleCount = 20
    
    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div')
      particle.className = `particle ${config.particles}`
      
      // Faction-specific particle styling
      switch (config.particles) {
        case 'golden_sparks':
          particle.style.cssText = `
            position: absolute;
            width: 3px;
            height: 3px;
            background: radial-gradient(circle, #FFD700, #FFA500);
            border-radius: 50%;
            box-shadow: 0 0 6px #FFD700;
          `
          break

        case 'chaos_corruption':
          particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: radial-gradient(circle, #8B0000, #FF0000);
            border-radius: 50%;
            box-shadow: 0 0 8px #8B0000;
            filter: blur(1px);
          `
          break

        case 'elven_light':
          particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 2px;
            background: radial-gradient(circle, #98FB98, #00FF7F);
            border-radius: 50%;
            box-shadow: 0 0 10px #98FB98;
          `
          break

        case 'forge_sparks':
          particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 6px;
            background: linear-gradient(to bottom, #FFD700, #FF4500);
            border-radius: 1px;
            box-shadow: 0 0 4px #FFD700;
          `
          break

        case 'crude_smoke':
          particle.style.cssText = `
            position: absolute;
            width: 8px;
            height: 8px;
            background: radial-gradient(circle, rgba(105,105,105,0.6), rgba(169,169,169,0.3));
            border-radius: 50%;
            filter: blur(2px);
          `
          break

        case 'necromantic_mist':
          particle.style.cssText = `
            position: absolute;
            width: 6px;
            height: 6px;
            background: radial-gradient(circle, rgba(128,0,128,0.7), rgba(75,0,130,0.4));
            border-radius: 50%;
            box-shadow: 0 0 12px rgba(128,0,128,0.5);
            filter: blur(1px);
          `
          break
      }

      container.appendChild(particle)

      // Animate particles
      gsap.set(particle, {
        x: Math.random() * container.offsetWidth,
        y: Math.random() * container.offsetHeight,
        opacity: 0
      })

      gsap.to(particle, {
        y: "-=50",
        x: `+=${(Math.random() - 0.5) * 30}`,
        opacity: Math.random() * 0.8 + 0.2,
        duration: Math.random() * 3 + 2,
        ease: "none",
        repeat: -1,
        yoyo: true,
        delay: Math.random() * 2
      })
    }
  }

  // Play faction-specific sounds
  const playFactionSound = (soundType) => {
    // This would integrate with Howler.js or Web Audio API
    console.log(`🔊 Playing ${soundType} sound effect`)
  }

  // Combat animation system
  const triggerCombatAnimation = useCallback((combatType = 'basic') => {
    if (!containerRef.current) return

    const config = FactionAnimations[faction]
    const elements = containerRef.current.querySelectorAll('.character-element')

    switch (config.combat) {
      case 'disciplined_strike':
        gsap.timeline()
          .to(elements, { x: 10, duration: 0.1, ease: WarhammerEasing.imperial })
          .to(elements, { x: -5, duration: 0.2, ease: "power2.out" })
          .to(elements, { x: 0, duration: 0.3, ease: "elastic.out(1, 0.3)" })
        break

      case 'berserker_rage':
        gsap.timeline()
          .to(elements, { 
            scale: 1.1, 
            rotation: "+=5", 
            filter: 'brightness(1.3) saturate(1.5)',
            duration: 0.2, 
            ease: WarhammerEasing.chaos 
          })
          .to(elements, { 
            scale: 1, 
            rotation: 0, 
            filter: 'brightness(1) saturate(1)',
            duration: 0.5, 
            ease: "elastic.out(1, 0.5)" 
          })
        break

      // Add more combat animations for other factions...
    }
  }, [faction])

  // Magic casting animation
  const triggerMagicAnimation = useCallback((spellType = 'basic') => {
    if (!containerRef.current) return

    const config = FactionAnimations[faction]
    const elements = containerRef.current.querySelectorAll('.character-element')

    // Create magic circle effect
    const magicCircle = document.createElement('div')
    magicCircle.className = 'magic-circle'
    magicCircle.style.cssText = `
      position: absolute;
      width: 100px;
      height: 100px;
      border: 2px solid ${config.colors[0]};
      border-radius: 50%;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      opacity: 0;
      box-shadow: 0 0 20px ${config.colors[0]};
    `
    
    containerRef.current.appendChild(magicCircle)

    gsap.timeline()
      .to(magicCircle, { 
        opacity: 1, 
        scale: 1.5, 
        rotation: 360, 
        duration: 1, 
        ease: WarhammerEasing.magical 
      })
      .to(elements, { 
        y: -10, 
        filter: `drop-shadow(0 0 10px ${config.colors[0]})`,
        duration: 0.5, 
        ease: "power2.out" 
      }, "-=0.5")
      .to(magicCircle, { 
        opacity: 0, 
        scale: 2, 
        duration: 0.5, 
        ease: "power2.out",
        onComplete: () => magicCircle.remove()
      })
      .to(elements, { 
        y: 0, 
        filter: 'none',
        duration: 0.5, 
        ease: "bounce.out" 
      }, "-=0.3")
  }, [faction])

  useEffect(() => {
    initializeFactionAnimations()

    return () => {
      if (timelineRef.current) {
        timelineRef.current.kill()
      }
      if (particleSystemRef.current) {
        particleSystemRef.current.remove()
      }
    }
  }, [initializeFactionAnimations])

  return (
    <div 
      ref={containerRef}
      className={`warhammer-animation-container faction-${faction.toLowerCase()}`}
      style={{ position: 'relative', overflow: 'hidden' }}
    >
      {children}
      
      {/* Faction-specific overlay effects */}
      <div className="faction-overlay" style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: `radial-gradient(circle at center, transparent 60%, ${FactionAnimations[faction]?.colors[0]}10 100%)`,
        pointerEvents: 'none'
      }} />
    </div>
  )
}

// Export animation triggers for external use
export const useWarhammerAnimations = (faction) => {
  return {
    triggerCombat: () => {
      // Trigger combat animation
    },
    triggerMagic: () => {
      // Trigger magic animation
    },
    triggerSpecialAbility: () => {
      // Trigger faction-specific special ability
    }
  }
}
