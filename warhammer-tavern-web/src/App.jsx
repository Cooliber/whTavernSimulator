import React, { Suspense, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

// Stores
import { useAppStore } from '@stores/appStore'
import { useWebSocketStore } from '@stores/webSocketStore'

// Components
import LoadingScreen from '@components/ui/LoadingScreen'
import ErrorBoundary from '@components/ui/ErrorBoundary'

// Lazy load main components for better performance
const TavernMain = React.lazy(() => import('@components/tavern/TavernMain'))
const SettingsPanel = React.lazy(() => import('@components/settings/SettingsPanel'))
const DebugPanel = React.lazy(() => import('@components/debug/DebugPanel'))

// Page transition variants
const pageVariants = {
  initial: {
    opacity: 0,
    scale: 0.98,
    y: 20
  },
  in: {
    opacity: 1,
    scale: 1,
    y: 0
  },
  out: {
    opacity: 0,
    scale: 1.02,
    y: -20
  }
}

const pageTransition = {
  type: 'tween',
  ease: 'anticipate',
  duration: 0.4
}

function App() {
  const { 
    isInitialized, 
    isLoading, 
    error, 
    theme,
    initialize 
  } = useAppStore()
  
  const { 
    connect, 
    isConnected, 
    connectionStatus 
  } = useWebSocketStore()

  // Initialize application
  useEffect(() => {
    const initApp = async () => {
      try {
        // Initialize app state
        await initialize()
        
        // Connect to WebSocket
        const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'
        await connect(wsUrl)
        
      } catch (error) {
        console.error('Failed to initialize application:', error)
      }
    }

    initApp()
  }, [initialize, connect])

  // Apply theme to document
  useEffect(() => {
    document.documentElement.className = theme
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  // Handle keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event) => {
      // Toggle debug panel with Ctrl+Shift+D
      if (event.ctrlKey && event.shiftKey && event.key === 'D') {
        event.preventDefault()
        // Toggle debug panel logic
      }
      
      // Toggle settings with Ctrl+,
      if (event.ctrlKey && event.key === ',') {
        event.preventDefault()
        // Toggle settings logic
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  // Show loading screen during initialization
  if (!isInitialized || isLoading) {
    return <LoadingScreen />
  }

  // Show error screen if initialization failed
  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-tavern-shadow to-secondary-900 flex items-center justify-center p-4">
        <div className="bg-secondary-800 rounded-lg p-8 max-w-md w-full text-center border border-red-500/20">
          <div className="text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-medieval text-red-400 mb-4">
            Tavern Initialization Failed
          </h1>
          <p className="text-secondary-300 mb-6">
            {error.message || 'Failed to initialize the tavern systems.'}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="app min-h-screen bg-gradient-to-br from-tavern-shadow via-secondary-900 to-secondary-800">
      {/* Connection Status Indicator */}
      <div className="fixed top-4 right-4 z-50">
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className={`px-3 py-1 rounded-full text-xs font-medium flex items-center gap-2 ${
            isConnected 
              ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
              : 'bg-red-500/20 text-red-400 border border-red-500/30'
          }`}
        >
          <div className={`w-2 h-2 rounded-full ${
            isConnected ? 'bg-green-400' : 'bg-red-400'
          } ${isConnected ? 'animate-pulse' : ''}`} />
          {isConnected ? 'Connected' : 'Disconnected'}
        </motion.div>
      </div>

      {/* Main Application Routes */}
      <ErrorBoundary>
        <AnimatePresence mode="wait">
          <Routes>
            <Route 
              path="/" 
              element={
                <motion.div
                  key="tavern"
                  initial="initial"
                  animate="in"
                  exit="out"
                  variants={pageVariants}
                  transition={pageTransition}
                >
                  <Suspense fallback={<LoadingScreen />}>
                    <TavernMain />
                  </Suspense>
                </motion.div>
              } 
            />
            
            <Route 
              path="/settings" 
              element={
                <motion.div
                  key="settings"
                  initial="initial"
                  animate="in"
                  exit="out"
                  variants={pageVariants}
                  transition={pageTransition}
                >
                  <Suspense fallback={<LoadingScreen />}>
                    <SettingsPanel />
                  </Suspense>
                </motion.div>
              } 
            />
            
            {/* Debug panel - only in development */}
            {process.env.NODE_ENV === 'development' && (
              <Route 
                path="/debug" 
                element={
                  <motion.div
                    key="debug"
                    initial="initial"
                    animate="in"
                    exit="out"
                    variants={pageVariants}
                    transition={pageTransition}
                  >
                    <Suspense fallback={<LoadingScreen />}>
                      <DebugPanel />
                    </Suspense>
                  </motion.div>
                } 
              />
            )}
            
            {/* Redirect unknown routes to home */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AnimatePresence>
      </ErrorBoundary>

      {/* Global Modals and Overlays */}
      <div id="modal-root" />
      <div id="tooltip-root" />
      
      {/* Performance Monitor (Development Only) */}
      {process.env.NODE_ENV === 'development' && (
        <div className="fixed bottom-4 left-4 bg-black/80 text-green-400 p-2 rounded text-xs font-mono">
          <div>FPS: <span id="fps-counter">60</span></div>
          <div>Memory: <span id="memory-counter">0 MB</span></div>
          <div>WS: {connectionStatus}</div>
        </div>
      )}
    </div>
  )
}

export default App
