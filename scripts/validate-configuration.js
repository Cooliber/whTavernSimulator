#!/usr/bin/env node

/**
 * Configuration Validation Script
 * Validates all system configurations and reports status
 */

const fs = require('fs')
const path = require('path')
const { execSync } = require('child_process')

class ConfigurationValidator {
  constructor() {
    this.results = []
    this.errors = []
    this.warnings = []
  }

  log(message, type = 'info') {
    const timestamp = new Date().toISOString()
    const logMessage = `[${timestamp}] ${type.toUpperCase()}: ${message}`
    
    console.log(logMessage)
    
    switch (type) {
      case 'error':
        this.errors.push(message)
        break
      case 'warning':
        this.warnings.push(message)
        break
      default:
        this.results.push(message)
    }
  }

  async validatePortConfiguration() {
    this.log('Validating port configuration...')
    
    try {
      // Check Nuxt config
      const nuxtConfigPath = path.join(process.cwd(), 'nuxt.config.ts')
      if (fs.existsSync(nuxtConfigPath)) {
        const nuxtConfig = fs.readFileSync(nuxtConfigPath, 'utf8')
        
        if (nuxtConfig.includes('port: 5920')) {
          this.log('✓ Nuxt.js configured for port 5920')
        } else {
          this.log('✗ Nuxt.js port configuration not found', 'error')
        }
        
        if (nuxtConfig.includes('host: \'0.0.0.0\'')) {
          this.log('✓ Nuxt.js configured for all interfaces')
        } else {
          this.log('✗ Nuxt.js host configuration not found', 'warning')
        }
      } else {
        this.log('✗ nuxt.config.ts not found', 'error')
      }

      // Check Playwright config
      const playwrightConfigPath = path.join(process.cwd(), 'playwright.config.ts')
      if (fs.existsSync(playwrightConfigPath)) {
        const playwrightConfig = fs.readFileSync(playwrightConfigPath, 'utf8')
        
        if (playwrightConfig.includes('localhost:5920')) {
          this.log('✓ Playwright configured for port 5920')
        } else {
          this.log('✗ Playwright port configuration not found', 'error')
        }
      } else {
        this.log('✗ playwright.config.ts not found', 'warning')
      }

    } catch (error) {
      this.log(`Error validating port configuration: ${error.message}`, 'error')
    }
  }

  async validateRoutingConfiguration() {
    this.log('Validating routing configuration...')
    
    try {
      const pagesDir = path.join(process.cwd(), 'pages')
      
      if (!fs.existsSync(pagesDir)) {
        this.log('✗ Pages directory not found', 'error')
        return
      }

      const requiredPages = [
        'index.vue',
        'characters.vue',
        'settings.vue',
        'about.vue',
        'generators.vue',
        'inspira-test.vue'
      ]

      const requiredDirs = [
        'conversations'
      ]

      // Check required pages
      for (const page of requiredPages) {
        const pagePath = path.join(pagesDir, page)
        if (fs.existsSync(pagePath)) {
          this.log(`✓ Page ${page} exists`)
        } else {
          this.log(`✗ Page ${page} missing`, 'error')
        }
      }

      // Check required directories
      for (const dir of requiredDirs) {
        const dirPath = path.join(pagesDir, dir)
        if (fs.existsSync(dirPath)) {
          this.log(`✓ Directory ${dir} exists`)
          
          // Check for dynamic route
          const dynamicRoute = path.join(dirPath, '[id].vue')
          if (fs.existsSync(dynamicRoute)) {
            this.log(`✓ Dynamic route ${dir}/[id].vue exists`)
          } else {
            this.log(`✗ Dynamic route ${dir}/[id].vue missing`, 'error')
          }
        } else {
          this.log(`✗ Directory ${dir} missing`, 'error')
        }
      }

    } catch (error) {
      this.log(`Error validating routing configuration: ${error.message}`, 'error')
    }
  }

  async validateCSSConfiguration() {
    this.log('Validating CSS configuration...')
    
    try {
      const assetsDir = path.join(process.cwd(), 'assets', 'css')
      
      if (!fs.existsSync(assetsDir)) {
        this.log('✗ CSS assets directory not found', 'error')
        return
      }

      const requiredCSSFiles = [
        'main.css',
        'warhammer-theme.css',
        'inspira-ui.css'
      ]

      for (const cssFile of requiredCSSFiles) {
        const cssPath = path.join(assetsDir, cssFile)
        if (fs.existsSync(cssPath)) {
          this.log(`✓ CSS file ${cssFile} exists`)
          
          // Check file content
          const content = fs.readFileSync(cssPath, 'utf8')
          if (content.length > 0) {
            this.log(`✓ CSS file ${cssFile} has content`)
          } else {
            this.log(`✗ CSS file ${cssFile} is empty`, 'warning')
          }
        } else {
          this.log(`✗ CSS file ${cssFile} missing`, 'error')
        }
      }

      // Check Tailwind config
      const tailwindConfigPath = path.join(process.cwd(), 'tailwind.config.js')
      if (fs.existsSync(tailwindConfigPath)) {
        this.log('✓ Tailwind CSS configuration exists')
        
        const tailwindConfig = fs.readFileSync(tailwindConfigPath, 'utf8')
        if (tailwindConfig.includes('faction')) {
          this.log('✓ Warhammer faction colors configured')
        } else {
          this.log('✗ Warhammer faction colors not found', 'warning')
        }
      } else {
        this.log('✗ Tailwind CSS configuration missing', 'error')
      }

    } catch (error) {
      this.log(`Error validating CSS configuration: ${error.message}`, 'error')
    }
  }

  async validateVueComponentStructure() {
    this.log('Validating Vue component structure...')
    
    try {
      const componentsDir = path.join(process.cwd(), 'components')
      
      if (!fs.existsSync(componentsDir)) {
        this.log('✗ Components directory not found', 'error')
        return
      }

      // Check InspiraUI components
      const inspiraDir = path.join(componentsDir, 'inspira')
      if (fs.existsSync(inspiraDir)) {
        this.log('✓ InspiraUI components directory exists')
        
        const inspiraComponents = fs.readdirSync(inspiraDir)
        this.log(`✓ Found ${inspiraComponents.length} InspiraUI components`)
        
        // Check key components
        const keyComponents = [
          'Card3D.vue',
          'RippleButton.vue',
          'SparklesText.vue',
          'AuroraBackground.vue',
          'WeatherSystem.vue'
        ]
        
        for (const component of keyComponents) {
          if (inspiraComponents.includes(component)) {
            this.log(`✓ Key component ${component} exists`)
          } else {
            this.log(`✗ Key component ${component} missing`, 'error')
          }
        }
      } else {
        this.log('✗ InspiraUI components directory missing', 'error')
      }

      // Check UI components
      const uiDir = path.join(componentsDir, 'ui')
      if (fs.existsSync(uiDir)) {
        this.log('✓ UI components directory exists')
      } else {
        this.log('✗ UI components directory missing', 'warning')
      }

    } catch (error) {
      this.log(`Error validating Vue component structure: ${error.message}`, 'error')
    }
  }

  async validateComposables() {
    this.log('Validating composables...')
    
    try {
      const composablesDir = path.join(process.cwd(), 'composables')
      
      if (!fs.existsSync(composablesDir)) {
        this.log('✗ Composables directory not found', 'error')
        return
      }

      const requiredComposables = [
        'useWarhammerTheme.ts',
        'useAnimation.ts',
        'useDeviceCapabilities.ts',
        'useScreenReader.ts',
        'useNPCGenerator.ts',
        'useQuestGenerator.ts',
        'useItemGenerator.ts'
      ]

      for (const composable of requiredComposables) {
        const composablePath = path.join(composablesDir, composable)
        if (fs.existsSync(composablePath)) {
          this.log(`✓ Composable ${composable} exists`)
          
          // Check if it exports a function
          const content = fs.readFileSync(composablePath, 'utf8')
          if (content.includes('export function')) {
            this.log(`✓ Composable ${composable} exports function`)
          } else {
            this.log(`✗ Composable ${composable} missing export`, 'warning')
          }
        } else {
          this.log(`✗ Composable ${composable} missing`, 'error')
        }
      }

    } catch (error) {
      this.log(`Error validating composables: ${error.message}`, 'error')
    }
  }

  async validateWarhammerPluginData() {
    this.log('Validating Warhammer plugin data...')
    
    try {
      const pluginDir = path.join(process.cwd(), 'plugins', 'warhammer-pl')
      
      if (!fs.existsSync(pluginDir)) {
        this.log('✗ Warhammer plugin directory not found', 'error')
        return
      }

      // Check module.json
      const moduleJsonPath = path.join(pluginDir, 'module.json')
      if (fs.existsSync(moduleJsonPath)) {
        this.log('✓ Warhammer plugin module.json exists')
        
        try {
          const moduleData = JSON.parse(fs.readFileSync(moduleJsonPath, 'utf8'))
          if (moduleData.name && moduleData.version) {
            this.log('✓ Module metadata is valid')
          } else {
            this.log('✗ Module metadata incomplete', 'warning')
          }
        } catch (parseError) {
          this.log('✗ Module.json is not valid JSON', 'error')
        }
      } else {
        this.log('✗ Warhammer plugin module.json missing', 'error')
      }

      // Check compendium data
      const compendiumDir = path.join(pluginDir, 'compendium')
      if (fs.existsSync(compendiumDir)) {
        this.log('✓ Compendium directory exists')
        
        const compendiumFiles = fs.readdirSync(compendiumDir)
        this.log(`✓ Found ${compendiumFiles.length} compendium files`)
        
        // Check key data files
        const keyFiles = [
          'wfrp4e-core.careers.json',
          'wfrp4e-core.talents.json',
          'wfrp4e-core.skills.json',
          'wfrp4e-core.trappings.json'
        ]
        
        for (const file of keyFiles) {
          if (compendiumFiles.includes(file)) {
            this.log(`✓ Key data file ${file} exists`)
          } else {
            this.log(`✗ Key data file ${file} missing`, 'error')
          }
        }
      } else {
        this.log('✗ Compendium directory missing', 'error')
      }

    } catch (error) {
      this.log(`Error validating Warhammer plugin data: ${error.message}`, 'error')
    }
  }

  async validatePackageConfiguration() {
    this.log('Validating package configuration...')
    
    try {
      const packageJsonPath = path.join(process.cwd(), 'package.json')
      
      if (!fs.existsSync(packageJsonPath)) {
        this.log('✗ package.json not found', 'error')
        return
      }

      const packageData = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'))
      
      // Check required dependencies
      const requiredDeps = [
        '@nuxtjs/tailwindcss',
        '@pinia/nuxt',
        '@vueuse/nuxt',
        '@nuxtjs/google-fonts'
      ]

      const dependencies = { ...packageData.dependencies, ...packageData.devDependencies }
      
      for (const dep of requiredDeps) {
        if (dependencies[dep]) {
          this.log(`✓ Dependency ${dep} installed`)
        } else {
          this.log(`✗ Dependency ${dep} missing`, 'error')
        }
      }

      // Check scripts
      const requiredScripts = ['dev', 'build', 'preview']
      
      for (const script of requiredScripts) {
        if (packageData.scripts && packageData.scripts[script]) {
          this.log(`✓ Script ${script} configured`)
        } else {
          this.log(`✗ Script ${script} missing`, 'warning')
        }
      }

    } catch (error) {
      this.log(`Error validating package configuration: ${error.message}`, 'error')
    }
  }

  async validateTypeScriptConfiguration() {
    this.log('Validating TypeScript configuration...')
    
    try {
      // Check tsconfig.json
      const tsconfigPath = path.join(process.cwd(), 'tsconfig.json')
      if (fs.existsSync(tsconfigPath)) {
        this.log('✓ TypeScript configuration exists')
        
        try {
          const tsconfig = JSON.parse(fs.readFileSync(tsconfigPath, 'utf8'))
          if (tsconfig.compilerOptions && tsconfig.compilerOptions.strict) {
            this.log('✓ TypeScript strict mode enabled')
          } else {
            this.log('✗ TypeScript strict mode not enabled', 'warning')
          }
        } catch (parseError) {
          this.log('✗ tsconfig.json is not valid JSON', 'error')
        }
      } else {
        this.log('✗ TypeScript configuration missing', 'warning')
      }

      // Check types directory
      const typesDir = path.join(process.cwd(), 'types')
      if (fs.existsSync(typesDir)) {
        this.log('✓ Types directory exists')
        
        const typeFiles = fs.readdirSync(typesDir)
        if (typeFiles.length > 0) {
          this.log(`✓ Found ${typeFiles.length} type definition files`)
        }
      } else {
        this.log('✗ Types directory missing', 'warning')
      }

    } catch (error) {
      this.log(`Error validating TypeScript configuration: ${error.message}`, 'error')
    }
  }

  async validateTestConfiguration() {
    this.log('Validating test configuration...')
    
    try {
      // Check Playwright config
      const playwrightConfigPath = path.join(process.cwd(), 'playwright.config.ts')
      if (fs.existsSync(playwrightConfigPath)) {
        this.log('✓ Playwright configuration exists')
      } else {
        this.log('✗ Playwright configuration missing', 'warning')
      }

      // Check tests directory
      const testsDir = path.join(process.cwd(), 'tests')
      if (fs.existsSync(testsDir)) {
        this.log('✓ Tests directory exists')
        
        const testFiles = fs.readdirSync(testsDir)
        this.log(`✓ Found ${testFiles.length} test files`)
      } else {
        this.log('✗ Tests directory missing', 'warning')
      }

    } catch (error) {
      this.log(`Error validating test configuration: ${error.message}`, 'error')
    }
  }

  async runAllValidations() {
    this.log('Starting comprehensive configuration validation...')
    this.log('=' * 60)
    
    await this.validatePortConfiguration()
    await this.validateRoutingConfiguration()
    await this.validateCSSConfiguration()
    await this.validateVueComponentStructure()
    await this.validateComposables()
    await this.validateWarhammerPluginData()
    await this.validatePackageConfiguration()
    await this.validateTypeScriptConfiguration()
    await this.validateTestConfiguration()
    
    this.log('=' * 60)
    this.generateReport()
  }

  generateReport() {
    this.log('Configuration Validation Report')
    this.log('=' * 60)
    
    this.log(`Total checks: ${this.results.length}`)
    this.log(`Errors: ${this.errors.length}`)
    this.log(`Warnings: ${this.warnings.length}`)
    
    if (this.errors.length > 0) {
      this.log('\nERRORS:')
      this.errors.forEach(error => this.log(`  - ${error}`))
    }
    
    if (this.warnings.length > 0) {
      this.log('\nWARNINGS:')
      this.warnings.forEach(warning => this.log(`  - ${warning}`))
    }
    
    if (this.errors.length === 0) {
      this.log('\n✓ All critical configurations are valid!')
      this.log('The Warhammer Tavern Simulator v3 is ready for use.')
    } else {
      this.log('\n✗ Configuration issues found!')
      this.log('Please address the errors above before proceeding.')
      process.exit(1)
    }
  }
}

// Run validation if called directly
if (require.main === module) {
  const validator = new ConfigurationValidator()
  validator.runAllValidations().catch(error => {
    console.error('Validation failed:', error)
    process.exit(1)
  })
}

module.exports = ConfigurationValidator
