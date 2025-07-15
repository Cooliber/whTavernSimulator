import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import App from '../App'

// Mock the stores
vi.mock('@stores/appStore', () => ({
  useAppStore: () => ({
    isInitialized: true,
    isLoading: false,
    error: null,
    theme: 'dark',
    initialize: vi.fn(),
  })
}))

vi.mock('@stores/webSocketStore', () => ({
  useWebSocketStore: () => ({
    connect: vi.fn(),
    isConnected: true,
    connectionStatus: 'connected'
  })
}))

// Mock the lazy-loaded components
vi.mock('@components/tavern/TavernMain', () => ({
  default: () => <div data-testid="tavern-main">Tavern Main Component</div>
}))

vi.mock('@components/settings/SettingsPanel', () => ({
  default: () => <div data-testid="settings-panel">Settings Panel Component</div>
}))

vi.mock('@components/debug/DebugPanel', () => ({
  default: () => <div data-testid="debug-panel">Debug Panel Component</div>
}))

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false }
  }
})

const renderWithProviders = (component) => {
  const queryClient = createTestQueryClient()
  return render(
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        {component}
      </QueryClientProvider>
    </BrowserRouter>
  )
}

describe('App Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders without crashing', async () => {
    renderWithProviders(<App />)
    
    await waitFor(() => {
      expect(screen.getByTestId('tavern-main')).toBeInTheDocument()
    })
  })

  it('shows connection status indicator', async () => {
    renderWithProviders(<App />)
    
    await waitFor(() => {
      expect(screen.getByText('Connected')).toBeInTheDocument()
    })
  })

  it('applies theme to document', async () => {
    renderWithProviders(<App />)
    
    await waitFor(() => {
      expect(document.documentElement.className).toContain('dark')
      expect(document.documentElement.getAttribute('data-theme')).toBe('dark')
    })
  })

  it('renders performance monitor in development', async () => {
    const originalEnv = import.meta.env.NODE_ENV
    import.meta.env.NODE_ENV = 'development'
    
    renderWithProviders(<App />)
    
    await waitFor(() => {
      expect(screen.getByText('FPS:')).toBeInTheDocument()
      expect(screen.getByText('Memory:')).toBeInTheDocument()
    })
    
    import.meta.env.NODE_ENV = originalEnv
  })
})
