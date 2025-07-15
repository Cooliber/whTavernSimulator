import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useAppStore } from '@stores/appStore'
import { useWebSocketStore } from '@stores/webSocketStore'
import { Bug, X, Activity, Database, Wifi, Code } from 'lucide-react'

const DebugPanel = () => {
  const [activeTab, setActiveTab] = useState('performance')
  const [logs, setLogs] = useState([])
  const [performance, setPerformance] = useState({
    fps: 60,
    memory: 0,
    loadTime: 0
  })

  const { isInitialized, error } = useAppStore()
  const { isConnected, connectionStatus, lastMessage } = useWebSocketStore()

  const tabs = [
    { id: 'performance', label: 'Performance', icon: Activity },
    { id: 'websocket', label: 'WebSocket', icon: Wifi },
    { id: 'state', label: 'App State', icon: Database },
    { id: 'logs', label: 'Console Logs', icon: Code }
  ]

  // Performance monitoring
  useEffect(() => {
    const updatePerformance = () => {
      if (performance.memory && performance.memory.usedJSHeapSize) {
        setPerformance(prev => ({
          ...prev,
          memory: Math.round(performance.memory.usedJSHeapSize / 1024 / 1024)
        }))
      }
    }

    const interval = setInterval(updatePerformance, 1000)
    return () => clearInterval(interval)
  }, [])

  // Console log capture
  useEffect(() => {
    const originalLog = console.log
    const originalError = console.error
    const originalWarn = console.warn

    const captureLog = (type, ...args) => {
      const timestamp = new Date().toLocaleTimeString()
      setLogs(prev => [...prev.slice(-99), {
        id: Date.now(),
        type,
        timestamp,
        message: args.join(' ')
      }])
    }

    console.log = (...args) => {
      originalLog(...args)
      captureLog('log', ...args)
    }

    console.error = (...args) => {
      originalError(...args)
      captureLog('error', ...args)
    }

    console.warn = (...args) => {
      originalWarn(...args)
      captureLog('warn', ...args)
    }

    return () => {
      console.log = originalLog
      console.error = originalError
      console.warn = originalWarn
    }
  }, [])

  const clearLogs = () => setLogs([])

  return (
    <div className="min-h-screen bg-gradient-to-br from-tavern-shadow to-secondary-900 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-secondary-800 rounded-lg p-6 mb-6 border border-secondary-700"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bug className="w-8 h-8 text-red-400" />
              <div>
                <h1 className="text-2xl font-medieval text-red-400">Debug Panel</h1>
                <p className="text-secondary-300">Development tools and diagnostics</p>
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
                          ? 'bg-red-600 text-white'
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
              {activeTab === 'performance' && (
                <div className="space-y-6">
                  <h2 className="text-xl font-semibold text-red-400">Performance Metrics</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-secondary-700 rounded-lg p-4">
                      <div className="text-2xl font-bold text-green-400">{performance.fps}</div>
                      <div className="text-sm text-secondary-300">FPS</div>
                    </div>
                    <div className="bg-secondary-700 rounded-lg p-4">
                      <div className="text-2xl font-bold text-blue-400">{performance.memory}</div>
                      <div className="text-sm text-secondary-300">Memory (MB)</div>
                    </div>
                    <div className="bg-secondary-700 rounded-lg p-4">
                      <div className="text-2xl font-bold text-yellow-400">{performance.loadTime}</div>
                      <div className="text-sm text-secondary-300">Load Time (ms)</div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="text-lg font-semibold text-white">Browser Information</h3>
                    <div className="bg-secondary-700 rounded-lg p-4 font-mono text-sm">
                      <div>User Agent: {navigator.userAgent}</div>
                      <div>Platform: {navigator.platform}</div>
                      <div>Language: {navigator.language}</div>
                      <div>Online: {navigator.onLine ? 'Yes' : 'No'}</div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'websocket' && (
                <div className="space-y-6">
                  <h2 className="text-xl font-semibold text-red-400">WebSocket Status</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-secondary-700 rounded-lg p-4">
                      <div className="text-lg font-semibold text-white mb-2">Connection Status</div>
                      <div className={`text-sm ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
                        {isConnected ? 'Connected' : 'Disconnected'}
                      </div>
                      <div className="text-xs text-secondary-400 mt-1">{connectionStatus}</div>
                    </div>
                    <div className="bg-secondary-700 rounded-lg p-4">
                      <div className="text-lg font-semibold text-white mb-2">Last Message</div>
                      <div className="text-sm text-secondary-300 font-mono">
                        {lastMessage ? JSON.stringify(lastMessage, null, 2) : 'No messages yet'}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'state' && (
                <div className="space-y-6">
                  <h2 className="text-xl font-semibold text-red-400">Application State</h2>
                  
                  <div className="space-y-4">
                    <div className="bg-secondary-700 rounded-lg p-4">
                      <div className="text-lg font-semibold text-white mb-2">App Store</div>
                      <pre className="text-sm text-secondary-300 font-mono overflow-auto">
                        {JSON.stringify({
                          isInitialized,
                          error: error?.message || null
                        }, null, 2)}
                      </pre>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'logs' && (
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-red-400">Console Logs</h2>
                    <button
                      onClick={clearLogs}
                      className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
                    >
                      Clear Logs
                    </button>
                  </div>
                  
                  <div className="bg-secondary-900 rounded-lg p-4 h-96 overflow-auto">
                    {logs.length === 0 ? (
                      <div className="text-secondary-400 text-center py-8">No logs captured yet</div>
                    ) : (
                      <div className="space-y-1">
                        {logs.map((log) => (
                          <div key={log.id} className="flex gap-2 text-sm font-mono">
                            <span className="text-secondary-500 w-20 flex-shrink-0">
                              {log.timestamp}
                            </span>
                            <span className={`w-12 flex-shrink-0 ${
                              log.type === 'error' ? 'text-red-400' :
                              log.type === 'warn' ? 'text-yellow-400' :
                              'text-green-400'
                            }`}>
                              {log.type.toUpperCase()}
                            </span>
                            <span className="text-secondary-300 break-all">
                              {log.message}
                            </span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default DebugPanel
