# AI Configuration Guide - Warhammer Tavern v3

## Overview

This guide provides comprehensive instructions for configuring and managing the advanced AI systems in Warhammer Tavern v3, including Groq API, Cerebras API, and the 17 distinct Warhammer Fantasy AI agents.

## 🔧 AI Provider Setup

### Groq API Configuration

1. **Obtain API Key**
   - Visit [Groq Console](https://console.groq.com)
   - Create an account or sign in
   - Navigate to "API Keys" section
   - Generate a new API key

2. **Environment Configuration**
   ```bash
   # Add to your .env file
   GROQ_API_KEY=your_groq_api_key_here
   ```

3. **Rate Limits**
   - Free tier: 30 requests per minute
   - Paid tier: Higher limits available
   - Automatic rate limiting implemented in the system

4. **Supported Models**
   - `llama-3.3-70b-versatile` (default)
   - `llama-3.1-8b-instant`
   - `mixtral-8x7b-32768`

### Cerebras API Configuration

1. **Obtain API Key**
   - Visit [Cerebras Cloud](https://cloud.cerebras.ai)
   - Create an account
   - Navigate to API Keys section
   - Generate a new API key

2. **Environment Configuration**
   ```bash
   # Add to your .env file
   CEREBRAS_API_KEY=your_cerebras_api_key_here
   ```

3. **Rate Limits**
   - Check current limits in Cerebras dashboard
   - Automatic rate limiting implemented

4. **Supported Models**
   - `llama-4-scout-17b-16e-instruct` (default)
   - Other models as available

### Fallback System

The system includes a rule-based fallback that activates when:
- All AI providers are unavailable
- API keys are missing or invalid
- Rate limits are exceeded
- Network connectivity issues occur

## 🤖 Agent System Configuration

### The 17 Warhammer Fantasy Agents

1. **Wilhelm Steinhart** - Human Bartender (Empire)
   - Role: Tavern heart, information hub
   - Personality: Wise, diplomatic, observant
   - Specialties: Local politics, brewing, conflict resolution

2. **Greta Goldweaver** - Human Merchant (Empire)
   - Role: Trade and commerce
   - Personality: Shrewd, ambitious, charming
   - Specialties: Negotiation, market trends, luxury goods

3. **Marcus Ironwall** - Human Guard (Empire)
   - Role: Security and law enforcement
   - Personality: Loyal, disciplined, protective
   - Specialties: Combat training, threat assessment

4. **Elara Moonwhisper** - Elf Scholar (Elves)
   - Role: Knowledge and magic
   - Personality: Intelligent, curious, aloof
   - Specialties: Arcane research, ancient history

5. **Finn Lightfinger** - Halfling Entertainer (Neutral)
   - Role: Music and stories
   - Personality: Charismatic, witty, optimistic
   - Specialties: Performance, crowd reading

6. **Baron Heinrich von Carstein** - Human Noble (Empire)
   - Role: Politics and intrigue
   - Personality: Arrogant, manipulative, sophisticated
   - Specialties: Court intrigue, social climbing

7. **Thorek Ironforge** - Dwarf Artisan (Dwarfs)
   - Role: Craftsmanship and tradition
   - Personality: Stubborn, proud, skilled
   - Specialties: Metalworking, weapon crafting

8. **Shadow** - Human Rogue (Neutral)
   - Role: Underworld connections
   - Personality: Secretive, cunning, pragmatic
   - Specialties: Information brokering, stealth

9. **Johann Brenner** - Human Witch Hunter (Empire)
   - Role: Faith and purification
   - Personality: Zealous, paranoid, righteous
   - Specialties: Detecting corruption, interrogation

10. **Seraphina the Seer** - Human Mystic (Neutral)
    - Role: Spiritual guidance
    - Personality: Mystical, wise, enigmatic
    - Specialties: Divination, spirit communication

11. **Klaus Grimwald** - Human Veteran (Empire)
    - Role: Military experience
    - Personality: Gruff, experienced, haunted
    - Specialties: Battlefield tactics, survival

12. **Anna Brightsmile** - Human Barmaid (Neutral)
    - Role: Service and gossip
    - Personality: Friendly, observant, hardworking
    - Specialties: Customer service, local gossip

13. **Brother Marcus** - Human Pilgrim (Empire)
    - Role: Faith and healing
    - Personality: Devout, humble, peaceful
    - Specialties: Spiritual guidance, herbal medicine

14. **Thomas Brightflame** - Human Apprentice Wizard (Empire)
    - Role: Learning and magical experimentation
    - Personality: Eager, ambitious, reckless
    - Specialties: Fire magic, potion brewing

15. **Hassan al-Qadim** - Human Traveling Merchant (Neutral)
    - Role: Exotic goods and foreign knowledge
    - Personality: Exotic, mysterious, worldly
    - Specialties: Foreign trade, cultural knowledge

16. **Grim Sewer-walker** - Human Ratcatcher (Neutral)
    - Role: Urban survival and underground knowledge
    - Personality: Gritty, practical, cynical
    - Specialties: Sewer navigation, pest control

17. **Old Meg** - Human Hedge Wizard (Neutral)
    - Role: Folk magic and natural wisdom
    - Personality: Eccentric, wise, unpredictable
    - Specialties: Herbalism, curse removal

## ⚙️ System Configuration

### AI Service Settings

```typescript
// Default configuration in useUnifiedAIService.ts
const config = {
  providers: [
    {
      name: 'groq',
      baseUrl: 'https://api.groq.com/openai/v1',
      model: 'llama-3.3-70b-versatile',
      maxTokens: 1024,
      temperature: 0.7
    },
    {
      name: 'cerebras',
      baseUrl: 'https://api.cerebras.ai/v1',
      model: 'llama-4-scout-17b-16e-instruct',
      maxTokens: 1024,
      temperature: 0.7
    }
  ],
  fallbackOrder: ['groq', 'cerebras', 'fallback'],
  retryAttempts: 3,
  timeoutMs: 30000,
  enableRateLimiting: true,
  enableCaching: true
}
```

### Customizing Agent Behavior

Agents can be customized by modifying their properties in `useWarhammerAgents.ts`:

```typescript
// Example: Modifying an agent's personality
const agent = getAgentById('agent_bartender_wilhelm')
if (agent) {
  agent.personality.mood = 'cheerful'
  agent.personality.traits.push('helpful')
}
```

### Relationship Management

```typescript
// Update relationships between agents
updateAgentRelationship('agent_guard_marcus', 'agent_rogue_shadow', 'rivals')
```

## 🔍 Monitoring and Debugging

### Agent Management Dashboard

Access the dashboard through the AI Conversations feature:
1. Navigate to the tavern page
2. Click on "AI Conversations" feature card
3. View the Agent Management Dashboard

Dashboard features:
- AI service provider status
- Agent overview statistics
- Individual agent details
- Active conversation monitoring
- Relationship visualization

### Debugging Tools

1. **Console Logging**
   ```javascript
   // Enable detailed logging
   localStorage.setItem('ai-debug', 'true')
   ```

2. **Provider Status Check**
   ```javascript
   // Check provider availability
   const { getProviderStatus } = useUnifiedAIService()
   console.log(getProviderStatus())
   ```

3. **Agent Inspection**
   ```javascript
   // Inspect agent data
   const { agents } = useWarhammerAgents()
   console.log(agents.value)
   ```

## 🚨 Troubleshooting

### Common Issues

1. **API Keys Not Working**
   - Verify keys are correctly set in environment variables
   - Check for extra spaces or characters
   - Ensure keys have proper permissions

2. **Rate Limiting**
   - Monitor usage in provider dashboards
   - Implement request queuing if needed
   - Consider upgrading to paid tiers

3. **Slow Responses**
   - Check network connectivity
   - Verify provider status
   - Consider adjusting timeout settings

4. **Agent Not Responding**
   - Check if agent exists in the system
   - Verify conversation initialization
   - Review console for error messages

### Error Codes

- `AI_PROVIDER_UNAVAILABLE`: All AI providers are down
- `RATE_LIMIT_EXCEEDED`: Too many requests to AI provider
- `AGENT_NOT_FOUND`: Requested agent doesn't exist
- `CONVERSATION_FAILED`: Unable to generate response

## 🔒 Security Considerations

1. **API Key Management**
   - Never commit API keys to version control
   - Use environment variables or secure key management
   - Rotate keys regularly

2. **Rate Limiting**
   - Implement client-side rate limiting
   - Monitor usage patterns
   - Set up alerts for unusual activity

3. **Content Filtering**
   - Review AI responses for inappropriate content
   - Implement content moderation if needed
   - Monitor conversation logs

## 📈 Performance Optimization

1. **Caching**
   - Enable response caching for repeated queries
   - Set appropriate cache expiration times
   - Clear cache when needed

2. **Provider Selection**
   - Use faster providers for real-time interactions
   - Reserve high-quality providers for important conversations
   - Implement smart provider switching

3. **Request Optimization**
   - Limit conversation history sent to AI
   - Use appropriate token limits
   - Optimize system prompts

## 🔄 Updates and Maintenance

1. **Regular Updates**
   - Monitor provider API changes
   - Update models when new versions are available
   - Review and update agent personalities

2. **Backup and Recovery**
   - Backup conversation histories
   - Export agent configurations
   - Maintain fallback systems

3. **Monitoring**
   - Set up health checks for AI providers
   - Monitor response times and quality
   - Track user engagement metrics

---

For additional support or questions, refer to the main documentation or contact the development team.
