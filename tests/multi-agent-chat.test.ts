import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import MultiAgentChat from '../components/conversations/MultiAgentChat.vue'

// Mock the i18n composable
vi.mock('#app', () => ({
  useI18n: () => ({
    t: (key: string, params?: any) => {
      const translations: Record<string, string> = {
        'conversations.multiAgent.title': 'Multi-Agent Conversation',
        'conversations.multiAgent.participants': 'Participants',
        'conversations.multiAgent.addAgent': 'Add Agent',
        'conversations.multiAgent.removeAgent': 'Remove Agent',
        'conversations.multiAgent.agentJoined': '{name} joined the conversation',
        'conversations.multiAgent.agentLeft': '{name} left the conversation',
        'conversations.typeMessage': 'Type a message...',
        'conversations.thinking': 'Thinking...',
        'conversations.selectCharacter': 'Select Character',
        'common.cancel': 'Cancel',
        'common.you': 'You'
      }
      
      let result = translations[key] || key
      if (params) {
        Object.keys(params).forEach(param => {
          result = result.replace(`{${param}}`, params[param])
        })
      }
      return result
    }
  })
}))

// Mock the Warhammer icons composable
vi.mock('../composables/useWarhammerIcons', () => ({
  useWarhammerIcons: () => ({
    getIcon: (concept: string) => concept,
    getFactionColor: (faction: string) => 'blue',
    getRarityColor: (rarity: string) => 'green',
    getDifficultyColor: (difficulty: string) => 'red'
  })
}))

describe('MultiAgentChat Component', () => {
  let wrapper: any

  beforeEach(() => {
    wrapper = mount(MultiAgentChat, {
      global: {
        stubs: {
          Icon: true,
          Teleport: true
        }
      }
    })
  })

  it('should render the chat interface', () => {
    expect(wrapper.find('.multi-agent-chat').exists()).toBe(true)
    expect(wrapper.find('.chat-header').exists()).toBe(true)
    expect(wrapper.find('.messages-area').exists()).toBe(true)
    expect(wrapper.find('.input-area').exists()).toBe(true)
  })

  it('should display active agents', () => {
    const agentIndicators = wrapper.findAll('.agent-indicator')
    expect(agentIndicators.length).toBeGreaterThan(0)
    
    // Should show at least the default agent (Sir Marcus)
    expect(wrapper.text()).toContain('Sir Marcus')
  })

  it('should show participant count', () => {
    const participantText = wrapper.find('.chat-header p')
    expect(participantText.text()).toContain('Participants: 1')
  })

  it('should handle message input', async () => {
    const textarea = wrapper.find('textarea')
    expect(textarea.exists()).toBe(true)
    
    await textarea.setValue('Hello, tavern!')
    expect(textarea.element.value).toBe('Hello, tavern!')
  })

  it('should send messages when button is clicked', async () => {
    const textarea = wrapper.find('textarea')
    const sendButton = wrapper.find('button[type="button"]')
    
    await textarea.setValue('Test message')
    await sendButton.trigger('click')
    
    await nextTick()
    
    // Should add message to the conversation
    expect(wrapper.text()).toContain('Test message')
  })

  it('should send messages on Enter key', async () => {
    const textarea = wrapper.find('textarea')
    
    await textarea.setValue('Enter key message')
    await textarea.trigger('keydown.enter')
    
    await nextTick()
    
    expect(wrapper.text()).toContain('Enter key message')
  })

  it('should disable send button when input is empty', () => {
    const sendButton = wrapper.find('button[type="button"]')
    expect(sendButton.attributes('disabled')).toBeDefined()
  })

  it('should enable send button when input has text', async () => {
    const textarea = wrapper.find('textarea')
    const sendButton = wrapper.find('button[type="button"]')
    
    await textarea.setValue('Some text')
    await nextTick()
    
    expect(sendButton.attributes('disabled')).toBeUndefined()
  })

  it('should show agent selector when add agent button is clicked', async () => {
    const addAgentButton = wrapper.find('button:contains("Add Agent")')
    await addAgentButton.trigger('click')
    
    await nextTick()
    
    expect(wrapper.vm.showAgentSelector).toBe(true)
  })

  it('should add new agents to conversation', async () => {
    // Open agent selector
    wrapper.vm.showAgentSelector = true
    await nextTick()
    
    // Get initial agent count
    const initialCount = wrapper.vm.activeAgents.length
    
    // Add a new agent
    const availableAgent = wrapper.vm.availableAgents[0]
    await wrapper.vm.addAgent(availableAgent)
    
    expect(wrapper.vm.activeAgents.length).toBe(initialCount + 1)
    expect(wrapper.vm.showAgentSelector).toBe(false)
  })

  it('should remove agents from conversation', async () => {
    // Ensure we have at least one agent
    const initialCount = wrapper.vm.activeAgents.length
    expect(initialCount).toBeGreaterThan(0)
    
    // Remove the first agent
    const agentToRemove = wrapper.vm.activeAgents[0]
    await wrapper.vm.removeAgent(agentToRemove.id)
    
    expect(wrapper.vm.activeAgents.length).toBe(initialCount - 1)
  })

  it('should show typing indicators', async () => {
    // Set an agent as typing
    wrapper.vm.activeAgents[0].isTyping = true
    await nextTick()
    
    expect(wrapper.find('.typing-indicator').exists()).toBe(true)
  })

  it('should display messages with correct styling', async () => {
    // Add a user message
    const userMessage = {
      id: '1',
      content: 'User message',
      timestamp: new Date(),
      isUser: true
    }
    wrapper.vm.messages.push(userMessage)
    
    // Add an agent message
    const agentMessage = {
      id: '2',
      content: 'Agent response',
      timestamp: new Date(),
      isUser: false,
      agent: wrapper.vm.activeAgents[0]
    }
    wrapper.vm.messages.push(agentMessage)
    
    await nextTick()
    
    const messages = wrapper.findAll('.message-bubble')
    expect(messages.length).toBe(2)
    
    // Check user message styling
    const userMessageEl = messages.find(msg => msg.text().includes('User message'))
    expect(userMessageEl.classes()).toContain('flex-row-reverse')
    
    // Check agent message styling
    const agentMessageEl = messages.find(msg => msg.text().includes('Agent response'))
    expect(agentMessageEl.exists()).toBe(true)
  })

  it('should show agent avatars', async () => {
    const agentMessage = {
      id: '1',
      content: 'Agent message',
      timestamp: new Date(),
      isUser: false,
      agent: wrapper.vm.activeAgents[0]
    }
    wrapper.vm.messages.push(agentMessage)
    
    await nextTick()
    
    const agentAvatar = wrapper.find('.agent-avatar')
    expect(agentAvatar.exists()).toBe(true)
    expect(agentAvatar.text()).toBe('S') // First letter of "Sir Marcus"
  })

  it('should format timestamps correctly', () => {
    const testDate = new Date('2024-01-01T12:30:00')
    const formatted = wrapper.vm.formatTime(testDate)
    
    expect(formatted).toMatch(/\d{1,2}:\d{2}/)
  })

  it('should handle agent responses simulation', async () => {
    const initialMessageCount = wrapper.vm.messages.length
    
    // Send a message to trigger agent responses
    wrapper.vm.newMessage = 'Hello everyone!'
    await wrapper.vm.sendMessage()
    
    // Wait for simulated responses
    await new Promise(resolve => setTimeout(resolve, 100))
    
    expect(wrapper.vm.messages.length).toBeGreaterThan(initialMessageCount)
  })

  it('should prevent duplicate agents', async () => {
    const agent = wrapper.vm.availableAgents[0]
    const initialCount = wrapper.vm.activeAgents.length
    
    // Try to add the same agent twice
    await wrapper.vm.addAgent(agent)
    await wrapper.vm.addAgent(agent)
    
    expect(wrapper.vm.activeAgents.length).toBe(initialCount + 1) // Should only add once
  })

  it('should handle empty message submission', async () => {
    const initialMessageCount = wrapper.vm.messages.length
    
    wrapper.vm.newMessage = ''
    await wrapper.vm.sendMessage()
    
    expect(wrapper.vm.messages.length).toBe(initialMessageCount) // No new message
  })

  it('should handle whitespace-only messages', async () => {
    const initialMessageCount = wrapper.vm.messages.length
    
    wrapper.vm.newMessage = '   '
    await wrapper.vm.sendMessage()
    
    expect(wrapper.vm.messages.length).toBe(initialMessageCount) // No new message
  })

  it('should scroll to bottom when new messages arrive', async () => {
    const scrollSpy = vi.spyOn(wrapper.vm, 'scrollToBottom')
    
    wrapper.vm.newMessage = 'New message'
    await wrapper.vm.sendMessage()
    
    expect(scrollSpy).toHaveBeenCalled()
  })

  it('should show join/leave messages', async () => {
    const agent = wrapper.vm.availableAgents[0]
    
    // Add agent
    await wrapper.vm.addAgent(agent)
    expect(wrapper.text()).toContain(`${agent.name} joined the conversation`)
    
    // Remove agent
    await wrapper.vm.removeAgent(agent.id)
    expect(wrapper.text()).toContain(`${agent.name} left the conversation`)
  })

  it('should handle accessibility features', () => {
    // Check ARIA labels
    const messagesArea = wrapper.find('.messages-area')
    expect(messagesArea.attributes('role')).toBe('log')
    expect(messagesArea.attributes('aria-live')).toBe('polite')
    
    // Check button labels
    const addButton = wrapper.find('button[aria-label*="Add Agent"]')
    expect(addButton.exists()).toBe(true)
  })

  it('should support keyboard navigation', async () => {
    const agentSelector = wrapper.find('.agent-selector')
    
    // Should close on Escape key
    wrapper.vm.showAgentSelector = true
    await nextTick()
    
    await agentSelector.trigger('keydown.escape')
    expect(wrapper.vm.showAgentSelector).toBe(false)
  })

  it('should handle reduced motion preferences', async () => {
    // Mock reduced motion preference
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: vi.fn().mockImplementation(query => ({
        matches: query === '(prefers-reduced-motion: reduce)',
        media: query,
        onchange: null,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      })),
    })
    
    const reducedMotionWrapper = mount(MultiAgentChat)
    expect(reducedMotionWrapper.vm.prefersReducedMotion).toBe(true)
  })
})
