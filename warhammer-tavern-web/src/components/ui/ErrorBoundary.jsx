import React from 'react'
import { motion } from 'framer-motion'
import { AlertTriangle, RefreshCw, Home, Bug } from 'lucide-react'

// Warhammer Fantasy-themed error messages
const WarhammerErrorMessages = [
  {
    title: "Chaos Corruption Detected!",
    message: "The tavern has been touched by the Ruinous Powers. Reality itself seems unstable.",
    icon: "💀",
    color: "text-red-400",
    bgColor: "bg-red-400/10",
    borderColor: "border-red-400/30"
  },
  {
    title: "Waaagh! System Overload!",
    message: "Too many Orcs in the tavern! The system can't handle this much chaos.",
    icon: "⚔️",
    color: "text-green-400",
    bgColor: "bg-green-400/10",
    borderColor: "border-green-400/30"
  },
  {
    title: "Magical Miscast!",
    message: "A wizard's spell has gone awry, causing reality to glitch and fracture.",
    icon: "⚡",
    color: "text-purple-400",
    bgColor: "bg-purple-400/10",
    borderColor: "border-purple-400/30"
  },
  {
    title: "Dwarf Engineering Failure!",
    message: "The tavern's mechanical systems have suffered a catastrophic malfunction.",
    icon: "🔧",
    color: "text-amber-400",
    bgColor: "bg-amber-400/10",
    borderColor: "border-amber-400/30"
  },
  {
    title: "Elven Enchantment Disrupted!",
    message: "The delicate magical balance has been disturbed, causing system instability.",
    icon: "🌟",
    color: "text-blue-400",
    bgColor: "bg-blue-400/10",
    borderColor: "border-blue-400/30"
  },
  {
    title: "Imperial Bureaucracy Error!",
    message: "The paperwork has become so complex that even the system is confused.",
    icon: "📜",
    color: "text-yellow-400",
    bgColor: "bg-yellow-400/10",
    borderColor: "border-yellow-400/30"
  }
]

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { 
      hasError: false, 
      error: null, 
      errorInfo: null,
      errorTheme: null
    }
  }

  static getDerivedStateFromError(error) {
    // Select random Warhammer-themed error
    const randomTheme = WarhammerErrorMessages[
      Math.floor(Math.random() * WarhammerErrorMessages.length)
    ]
    
    return { 
      hasError: true, 
      errorTheme: randomTheme
    }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    })

    // Log error to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('🏰 Tavern Error Boundary caught an error:', error, errorInfo)
    }

    // Send error to monitoring service in production
    if (process.env.NODE_ENV === 'production') {
      // Example: Sentry, LogRocket, etc.
      console.error('Production error:', error)
    }
  }

  handleReload = () => {
    window.location.reload()
  }

  handleGoHome = () => {
    window.location.href = '/'
  }

  handleReportBug = () => {
    const errorReport = {
      error: this.state.error?.toString(),
      stack: this.state.error?.stack,
      componentStack: this.state.errorInfo?.componentStack,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      url: window.location.href
    }

    // In a real app, this would send to your error reporting service
    console.log('Bug report:', errorReport)
    
    // For now, copy to clipboard
    navigator.clipboard.writeText(JSON.stringify(errorReport, null, 2))
      .then(() => alert('Error report copied to clipboard!'))
      .catch(() => alert('Failed to copy error report'))
  }

  render() {
    if (this.state.hasError) {
      const theme = this.state.errorTheme || WarhammerErrorMessages[0]

      return (
        <div className="min-h-screen bg-gradient-to-br from-tavern-shadow via-secondary-900 to-secondary-800 flex items-center justify-center p-4">
          {/* Background Effects */}
          <div className="absolute inset-0 bg-tavern-pattern opacity-5"></div>
          <div className="absolute top-20 left-20 w-32 h-32 bg-red-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-20 w-24 h-24 bg-purple-500/10 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '1s' }}></div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className={`relative max-w-2xl w-full ${theme.bgColor} rounded-lg border-2 ${theme.borderColor} backdrop-blur-sm overflow-hidden`}
          >
            {/* Header */}
            <div className="p-8 text-center border-b border-secondary-700/50">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                className="text-6xl mb-4"
              >
                {theme.icon}
              </motion.div>
              
              <h1 className={`text-3xl font-medieval ${theme.color} mb-3`}>
                {theme.title}
              </h1>
              
              <p className="text-secondary-300 text-lg leading-relaxed">
                {theme.message}
              </p>
            </div>

            {/* Error Details (Development Only) */}
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                transition={{ delay: 0.4 }}
                className="p-6 border-b border-secondary-700/50"
              >
                <details className="group">
                  <summary className="cursor-pointer text-secondary-400 hover:text-secondary-300 flex items-center gap-2 mb-3">
                    <Bug className="w-4 h-4" />
                    Technical Details (Development)
                    <span className="text-xs bg-secondary-700 px-2 py-1 rounded">DEV</span>
                  </summary>
                  
                  <div className="bg-secondary-900 rounded-lg p-4 font-mono text-sm">
                    <div className="mb-4">
                      <h4 className="text-red-400 font-semibold mb-2">Error:</h4>
                      <pre className="text-red-300 whitespace-pre-wrap break-words">
                        {this.state.error.toString()}
                      </pre>
                    </div>
                    
                    {this.state.error.stack && (
                      <div className="mb-4">
                        <h4 className="text-yellow-400 font-semibold mb-2">Stack Trace:</h4>
                        <pre className="text-yellow-300 whitespace-pre-wrap break-words text-xs max-h-40 overflow-y-auto">
                          {this.state.error.stack}
                        </pre>
                      </div>
                    )}
                    
                    {this.state.errorInfo?.componentStack && (
                      <div>
                        <h4 className="text-blue-400 font-semibold mb-2">Component Stack:</h4>
                        <pre className="text-blue-300 whitespace-pre-wrap break-words text-xs max-h-32 overflow-y-auto">
                          {this.state.errorInfo.componentStack}
                        </pre>
                      </div>
                    )}
                  </div>
                </details>
              </motion.div>
            )}

            {/* Actions */}
            <div className="p-8">
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <motion.button
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.6 }}
                  onClick={this.handleReload}
                  className="flex items-center justify-center gap-2 px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-semibold transition-colors"
                >
                  <RefreshCw className="w-5 h-5" />
                  Restart Tavern
                </motion.button>

                <motion.button
                  initial={{ opacity: 0, x: 0 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 }}
                  onClick={this.handleGoHome}
                  className="flex items-center justify-center gap-2 px-6 py-3 bg-secondary-700 hover:bg-secondary-600 text-white rounded-lg font-semibold transition-colors"
                >
                  <Home className="w-5 h-5" />
                  Return Home
                </motion.button>

                <motion.button
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 }}
                  onClick={this.handleReportBug}
                  className="flex items-center justify-center gap-2 px-6 py-3 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-semibold transition-colors"
                >
                  <Bug className="w-5 h-5" />
                  Report Issue
                </motion.button>
              </div>

              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1 }}
                className="mt-6 text-center"
              >
                <p className="text-secondary-400 text-sm">
                  If the problem persists, the tavern keeper has been notified.
                </p>
                <p className="text-secondary-500 text-xs mt-2">
                  Error ID: {Date.now().toString(36).toUpperCase()}
                </p>
              </motion.div>
            </div>

            {/* Decorative Elements */}
            <div className="absolute top-4 right-4 opacity-20">
              <AlertTriangle className={`w-8 h-8 ${theme.color}`} />
            </div>
            
            <div className="absolute bottom-4 left-4 opacity-10">
              <div className="text-4xl">🏰</div>
            </div>

            {/* Animated Border */}
            <div className={`absolute inset-0 border-2 ${theme.borderColor} rounded-lg pointer-events-none`}>
              <div className={`absolute inset-0 border-2 ${theme.borderColor} rounded-lg animate-pulse opacity-50`}></div>
            </div>
          </motion.div>

          {/* Floating Particles */}
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            {[...Array(10)].map((_, i) => (
              <motion.div
                key={i}
                className={`absolute w-2 h-2 ${theme.color} rounded-full opacity-20`}
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                }}
                animate={{
                  y: [0, -30, 0],
                  opacity: [0.2, 0.8, 0.2],
                  scale: [0.5, 1, 0.5]
                }}
                transition={{
                  duration: 4 + Math.random() * 2,
                  repeat: Infinity,
                  delay: Math.random() * 2
                }}
              />
            ))}
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
