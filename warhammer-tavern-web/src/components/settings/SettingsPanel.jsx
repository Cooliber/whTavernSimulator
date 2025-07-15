import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useAppStore } from '@stores/appStore'
import { Settings, X, Monitor, Volume2, Gamepad2, Palette } from 'lucide-react'

const SettingsPanel = () => {
  const { theme, setTheme, settings, updateSettings } = useAppStore()
  const [activeTab, setActiveTab] = useState('display')

  const tabs = [
    { id: 'display', label: 'Display', icon: Monitor },
    { id: 'audio', label: 'Audio', icon: Volume2 },
    { id: 'gameplay', label: 'Gameplay', icon: Gamepad2 },
    { id: 'appearance', label: 'Appearance', icon: Palette }
  ]

  const themes = [
    { id: 'dark', name: 'Dark Tavern', description: 'Classic dark theme' },
    { id: 'light', name: 'Bright Tavern', description: 'Light theme for day time' },
    { id: 'warhammer', name: 'Warhammer Fantasy', description: 'Authentic Warhammer styling' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-tavern-shadow to-secondary-900 p-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-secondary-800 rounded-lg p-6 mb-6 border border-secondary-700"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Settings className="w-8 h-8 text-primary-400" />
              <div>
                <h1 className="text-2xl font-medieval text-primary-400">Tavern Settings</h1>
                <p className="text-secondary-300">Configure your tavern experience</p>
              </div>
            </div>
            <button
              onClick={() => window.history.back()}
              className="p-2 hover:bg-secondary-700 rounded-lg transition-colors"
            >
              <X className="w-6 h-6 text-secondary-400" />
            </button>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-1"
          >
            <div className="bg-secondary-800 rounded-lg p-4 border border-secondary-700">
              <nav className="space-y-2">
                {tabs.map((tab) => {
                  const Icon = tab.icon
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`w-full flex items-center gap-3 p-3 rounded-lg text-left transition-colors ${
                        activeTab === tab.id
                          ? 'bg-primary-600 text-white'
                          : 'hover:bg-secondary-700 text-secondary-300'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      {tab.label}
                    </button>
                  )
                })}
              </nav>
            </div>
          </motion.div>

          {/* Content */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-3"
          >
            <div className="bg-secondary-800 rounded-lg p-6 border border-secondary-700">
              {activeTab === 'display' && (
                <div className="space-y-6">
                  <h2 className="text-xl font-semibold text-primary-400">Display Settings</h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-secondary-300 mb-2">
                        Resolution
                      </label>
                      <select className="w-full bg-secondary-700 border border-secondary-600 rounded-lg p-3 text-white">
                        <option>Auto (Recommended)</option>
                        <option>1920x1080</option>
                        <option>1366x768</option>
                        <option>1280x720</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-secondary-300 mb-2">
                        Graphics Quality
                      </label>
                      <select className="w-full bg-secondary-700 border border-secondary-600 rounded-lg p-3 text-white">
                        <option>Ultra</option>
                        <option>High</option>
                        <option>Medium</option>
                        <option>Low</option>
                      </select>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-secondary-300">Enable Shadows</span>
                      <input type="checkbox" className="toggle" defaultChecked />
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-secondary-300">Anti-aliasing</span>
                      <input type="checkbox" className="toggle" defaultChecked />
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'audio' && (
                <div className="space-y-6">
                  <h2 className="text-xl font-semibold text-primary-400">Audio Settings</h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-secondary-300 mb-2">
                        Master Volume
                      </label>
                      <input type="range" min="0" max="100" defaultValue="80" className="w-full" />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-secondary-300 mb-2">
                        Music Volume
                      </label>
                      <input type="range" min="0" max="100" defaultValue="60" className="w-full" />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-secondary-300 mb-2">
                        Sound Effects
                      </label>
                      <input type="range" min="0" max="100" defaultValue="70" className="w-full" />
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-secondary-300">Spatial Audio</span>
                      <input type="checkbox" className="toggle" defaultChecked />
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'gameplay' && (
                <div className="space-y-6">
                  <h2 className="text-xl font-semibold text-primary-400">Gameplay Settings</h2>
                  
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-secondary-300">Auto-save</span>
                      <input type="checkbox" className="toggle" defaultChecked />
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-secondary-300">Show Tooltips</span>
                      <input type="checkbox" className="toggle" defaultChecked />
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-secondary-300">Enable Notifications</span>
                      <input type="checkbox" className="toggle" defaultChecked />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-secondary-300 mb-2">
                        Animation Speed
                      </label>
                      <select className="w-full bg-secondary-700 border border-secondary-600 rounded-lg p-3 text-white">
                        <option>Fast</option>
                        <option>Normal</option>
                        <option>Slow</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'appearance' && (
                <div className="space-y-6">
                  <h2 className="text-xl font-semibold text-primary-400">Appearance Settings</h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-secondary-300 mb-2">
                        Theme
                      </label>
                      <div className="grid grid-cols-1 gap-3">
                        {themes.map((themeOption) => (
                          <button
                            key={themeOption.id}
                            onClick={() => setTheme(themeOption.id)}
                            className={`p-4 rounded-lg border text-left transition-colors ${
                              theme === themeOption.id
                                ? 'border-primary-500 bg-primary-500/10'
                                : 'border-secondary-600 hover:border-secondary-500'
                            }`}
                          >
                            <div className="font-medium text-white">{themeOption.name}</div>
                            <div className="text-sm text-secondary-400">{themeOption.description}</div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Save Button */}
              <div className="mt-8 pt-6 border-t border-secondary-700">
                <div className="flex gap-3">
                  <button className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2 rounded-lg font-medium transition-colors">
                    Save Changes
                  </button>
                  <button className="bg-secondary-700 hover:bg-secondary-600 text-white px-6 py-2 rounded-lg font-medium transition-colors">
                    Reset to Defaults
                  </button>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default SettingsPanel
