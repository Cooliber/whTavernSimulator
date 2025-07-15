import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { ReactQueryDevtools } from 'react-query/devtools'
import { Toaster } from 'react-hot-toast'

import App from './App'
import './index.css'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

// Error boundary component
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Application Error:', error, errorInfo)
    
    // You could send this to an error reporting service
    if (window.gtag) {
      window.gtag('event', 'exception', {
        description: error.toString(),
        fatal: false
      })
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-tavern-shadow to-secondary-900 flex items-center justify-center p-4">
          <div className="bg-secondary-800 rounded-lg p-8 max-w-md w-full text-center border border-secondary-700">
            <div className="text-6xl mb-4">⚔️</div>
            <h1 className="text-2xl font-medieval text-primary-400 mb-4">
              The Tavern Has Encountered an Issue
            </h1>
            <p className="text-secondary-300 mb-6">
              Something went wrong in the tavern. The barkeep is looking into it.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            >
              Reload Tavern
            </button>
            {process.env.NODE_ENV === 'development' && (
              <details className="mt-4 text-left">
                <summary className="cursor-pointer text-secondary-400 hover:text-secondary-300">
                  Error Details
                </summary>
                <pre className="mt-2 text-xs text-red-400 bg-secondary-900 p-2 rounded overflow-auto">
                  {this.state.error?.toString()}
                </pre>
              </details>
            )}
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

// Performance monitoring
if (process.env.NODE_ENV === 'development') {
  // Enable React DevTools profiler
  window.__REACT_DEVTOOLS_GLOBAL_HOOK__?.onCommitFiberRoot = (id, root, priorityLevel) => {
    // Performance monitoring logic
  }
}

// Service Worker registration
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('🔧 Service Worker registered successfully')
      })
      .catch((error) => {
        console.log('❌ Service Worker registration failed')
      })
  })
}

// Initialize application
const root = ReactDOM.createRoot(document.getElementById('root'))

root.render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter>
        <QueryClientProvider client={queryClient}>
          <App />
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#1e293b',
                color: '#f1f5f9',
                border: '1px solid #475569',
                borderRadius: '0.5rem',
                fontFamily: 'Inter, system-ui, sans-serif'
              },
              success: {
                iconTheme: {
                  primary: '#22c55e',
                  secondary: '#1e293b'
                }
              },
              error: {
                iconTheme: {
                  primary: '#ef4444',
                  secondary: '#1e293b'
                }
              }
            }}
          />
          {process.env.NODE_ENV === 'development' && <ReactQueryDevtools />}
        </QueryClientProvider>
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>
)

// Global error handler
window.addEventListener('error', (event) => {
  console.error('Global error:', event.error)
})

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason)
})

// Performance observer
if ('PerformanceObserver' in window) {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (entry.entryType === 'largest-contentful-paint') {
        console.log('LCP:', entry.startTime)
      }
      if (entry.entryType === 'first-input') {
        console.log('FID:', entry.processingStart - entry.startTime)
      }
    }
  })
  
  observer.observe({ entryTypes: ['largest-contentful-paint', 'first-input'] })
}

// Expose development helpers
if (process.env.NODE_ENV === 'development') {
  window.__TAVERN_DEBUG__ = {
    queryClient,
    version: __APP_VERSION__,
    buildTime: __BUILD_TIME__
  }
}
