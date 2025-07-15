import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Crown, Plus, Edit, Trash2, Users, Calendar, MapPin, Star } from 'lucide-react'
import toast from 'react-hot-toast'

// Campaign templates
const CampaignTemplates = {
  enemy_within: {
    name: 'Wróg Wewnętrzny',
    description: 'Klasyczna kampania WFRP o korupcji w Imperium',
    sessions: 20,
    locations: ['Altdorf', 'Bogenhafen', 'Middenheim', 'Talabheim'],
    themes: ['Korupcja', 'Intryga', 'Horror', 'Polityka'],
    difficulty: 'Średnia'
  },
  paths_damned: {
    name: 'Ścieżki Potępionych',
    description: 'Przygoda w Drakwaldzie pełna niebezpieczeństw',
    sessions: 15,
    locations: ['Drakwald', 'Ubersreik', 'Grunburg', 'Kemperbad'],
    themes: ['Eksploracja', 'Walka', 'Natura', 'Mutanci'],
    difficulty: 'Wysoka'
  },
  power_behind_throne: {
    name: 'Władza za Tronem',
    description: 'Intrygi dworskie i polityczne rozgrywki',
    sessions: 25,
    locations: ['Altdorf', 'Dwór Elektora', 'Nuln', 'Wissenland'],
    themes: ['Polityka', 'Intryga', 'Szlachta', 'Spiski'],
    difficulty: 'Wysoka'
  }
}

// Session tracking structure
const SessionTemplate = {
  id: Date.now(),
  number: 1,
  title: '',
  date: new Date().toISOString().split('T')[0],
  summary: '',
  events: [],
  npcs: [],
  locations: [],
  rewards: '',
  notes: ''
}

export const CampaignManager = ({ gmMode, sessionData, onSessionDataUpdate }) => {
  const [campaigns, setCampaigns] = useState([])
  const [activeCampaign, setActiveCampaign] = useState(null)
  const [sessions, setSessions] = useState([])
  const [showNewCampaign, setShowNewCampaign] = useState(false)
  const [showNewSession, setShowNewSession] = useState(false)
  const [editingSession, setEditingSession] = useState(null)

  // Load campaigns and sessions
  useEffect(() => {
    const savedCampaigns = localStorage.getItem('wfrp_campaigns')
    const savedSessions = localStorage.getItem('wfrp_sessions')
    
    if (savedCampaigns) {
      try {
        const campaignData = JSON.parse(savedCampaigns)
        setCampaigns(campaignData)
        if (campaignData.length > 0) {
          setActiveCampaign(campaignData[0])
        }
      } catch (error) {
        console.error('Error loading campaigns:', error)
      }
    }

    if (savedSessions) {
      try {
        setSessions(JSON.parse(savedSessions))
      } catch (error) {
        console.error('Error loading sessions:', error)
      }
    }
  }, [])

  // Save campaigns
  const saveCampaigns = (newCampaigns) => {
    setCampaigns(newCampaigns)
    localStorage.setItem('wfrp_campaigns', JSON.stringify(newCampaigns))
  }

  // Save sessions
  const saveSessions = (newSessions) => {
    setSessions(newSessions)
    localStorage.setItem('wfrp_sessions', JSON.stringify(newSessions))
  }

  // Create new campaign
  const createCampaign = (template) => {
    const newCampaign = {
      id: Date.now(),
      name: template ? template.name : 'Nowa Kampania',
      description: template ? template.description : '',
      template: template ? template : null,
      created: new Date().toISOString(),
      players: [],
      currentSession: 1,
      status: 'active'
    }

    const newCampaigns = [...campaigns, newCampaign]
    saveCampaigns(newCampaigns)
    setActiveCampaign(newCampaign)
    setShowNewCampaign(false)
    toast.success('Kampania utworzona!')
  }

  // Create new session
  const createSession = () => {
    if (!activeCampaign) return

    const newSession = {
      ...SessionTemplate,
      id: Date.now(),
      campaignId: activeCampaign.id,
      number: sessions.filter(s => s.campaignId === activeCampaign.id).length + 1
    }

    const newSessions = [...sessions, newSession]
    saveSessions(newSessions)
    setEditingSession(newSession)
    setShowNewSession(false)
    toast.success('Sesja utworzona!')
  }

  // Update session
  const updateSession = (updatedSession) => {
    const newSessions = sessions.map(s => 
      s.id === updatedSession.id ? updatedSession : s
    )
    saveSessions(newSessions)
    toast.success('Sesja zaktualizowana!')
  }

  // Delete session
  const deleteSession = (sessionId) => {
    const newSessions = sessions.filter(s => s.id !== sessionId)
    saveSessions(newSessions)
    setEditingSession(null)
    toast.success('Sesja usunięta!')
  }

  // Get sessions for active campaign
  const getCampaignSessions = () => {
    if (!activeCampaign) return []
    return sessions.filter(s => s.campaignId === activeCampaign.id)
      .sort((a, b) => b.number - a.number)
  }

  return (
    <div className="h-full flex flex-col p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-medieval text-white mb-2">Zarządzanie Kampanią</h3>
          <p className="text-secondary-300">
            Organizuj sesje, śledź postęp i zarządzaj kampaniami WFRP
          </p>
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={() => setShowNewCampaign(true)}
            className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            Nowa Kampania
          </button>
          
          {activeCampaign && (
            <button
              onClick={() => setShowNewSession(true)}
              className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Nowa Sesja
            </button>
          )}
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Campaign List */}
        <div className="space-y-4">
          <h4 className="font-semibold text-white">Kampanie</h4>
          
          <div className="space-y-2">
            {campaigns.map((campaign) => (
              <motion.button
                key={campaign.id}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setActiveCampaign(campaign)}
                className={`
                  w-full p-3 rounded-lg border transition-all duration-200 text-left
                  ${activeCampaign?.id === campaign.id
                    ? 'bg-purple-400/20 border-purple-400/50 text-purple-100'
                    : 'bg-secondary-700/50 border-secondary-600 hover:border-secondary-500 text-white'
                  }
                `}
              >
                <div className="font-medium">{campaign.name}</div>
                <div className="text-xs text-secondary-400">
                  Sesja {campaign.currentSession} • {campaign.status}
                </div>
              </motion.button>
            ))}
          </div>

          {campaigns.length === 0 && (
            <div className="text-center py-8">
              <Crown className="w-12 h-12 text-secondary-400 mx-auto mb-2 opacity-50" />
              <p className="text-secondary-400 text-sm">Brak kampanii</p>
            </div>
          )}
        </div>

        {/* Campaign Details & Sessions */}
        <div className="lg:col-span-3">
          {activeCampaign ? (
            <div className="space-y-6">
              {/* Campaign Info */}
              <div className="bg-secondary-700/50 rounded-lg p-4">
                <h4 className="font-semibold text-white mb-2">{activeCampaign.name}</h4>
                <p className="text-secondary-300 mb-4">{activeCampaign.description}</p>
                
                {activeCampaign.template && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                    <div>
                      <span className="text-secondary-400">Sesje:</span>
                      <div className="text-white">{activeCampaign.template.sessions}</div>
                    </div>
                    <div>
                      <span className="text-secondary-400">Trudność:</span>
                      <div className="text-white">{activeCampaign.template.difficulty}</div>
                    </div>
                    <div>
                      <span className="text-secondary-400">Lokacje:</span>
                      <div className="text-white">{activeCampaign.template.locations.length}</div>
                    </div>
                    <div>
                      <span className="text-secondary-400">Motywy:</span>
                      <div className="text-white">{activeCampaign.template.themes.length}</div>
                    </div>
                  </div>
                )}
              </div>

              {/* Sessions List */}
              <div className="bg-secondary-700/50 rounded-lg p-4">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-semibold text-white">Sesje</h4>
                  <span className="text-secondary-400 text-sm">
                    {getCampaignSessions().length} sesji
                  </span>
                </div>

                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {getCampaignSessions().map((session) => (
                    <div
                      key={session.id}
                      className="p-3 bg-secondary-600/50 rounded-lg cursor-pointer hover:bg-secondary-600 transition-colors"
                      onClick={() => setEditingSession(session)}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-white">
                          Sesja {session.number}: {session.title || 'Bez tytułu'}
                        </span>
                        <span className="text-xs text-secondary-400">
                          {session.date}
                        </span>
                      </div>
                      {session.summary && (
                        <p className="text-sm text-secondary-300 line-clamp-2">
                          {session.summary}
                        </p>
                      )}
                    </div>
                  ))}
                </div>

                {getCampaignSessions().length === 0 && (
                  <div className="text-center py-8">
                    <Calendar className="w-12 h-12 text-secondary-400 mx-auto mb-2 opacity-50" />
                    <p className="text-secondary-400 text-sm">Brak sesji</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <Crown className="w-24 h-24 text-secondary-400 mx-auto mb-4 opacity-50" />
                <h3 className="text-xl font-medieval text-white mb-2">
                  Wybierz Kampanię
                </h3>
                <p className="text-secondary-400 mb-4">
                  Wybierz kampanię z listy lub utwórz nową
                </p>
                <button
                  onClick={() => setShowNewCampaign(true)}
                  className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors flex items-center gap-2 mx-auto"
                >
                  <Plus className="w-5 h-5" />
                  Utwórz Pierwszą Kampanię
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* New Campaign Modal */}
      <AnimatePresence>
        {showNewCampaign && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
            onClick={() => setShowNewCampaign(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-secondary-800 rounded-lg w-full max-w-2xl p-6 border border-secondary-700"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-xl font-medieval text-white mb-4">Nowa Kampania</h3>
              
              <div className="space-y-4">
                <button
                  onClick={() => createCampaign(null)}
                  className="w-full p-4 bg-secondary-700 hover:bg-secondary-600 rounded-lg transition-colors text-left"
                >
                  <div className="font-medium text-white">Pusta Kampania</div>
                  <div className="text-sm text-secondary-300">
                    Zacznij od zera z własnym pomysłem
                  </div>
                </button>

                {Object.entries(CampaignTemplates).map(([key, template]) => (
                  <button
                    key={key}
                    onClick={() => createCampaign(template)}
                    className="w-full p-4 bg-secondary-700 hover:bg-secondary-600 rounded-lg transition-colors text-left"
                  >
                    <div className="font-medium text-white">{template.name}</div>
                    <div className="text-sm text-secondary-300 mb-2">
                      {template.description}
                    </div>
                    <div className="flex items-center gap-4 text-xs text-secondary-400">
                      <span>{template.sessions} sesji</span>
                      <span>{template.difficulty}</span>
                      <span>{template.locations.length} lokacji</span>
                    </div>
                  </button>
                ))}
              </div>

              <div className="flex justify-end gap-2 mt-6">
                <button
                  onClick={() => setShowNewCampaign(false)}
                  className="px-4 py-2 bg-secondary-700 hover:bg-secondary-600 text-white rounded-lg transition-colors"
                >
                  Anuluj
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Session Editor Modal */}
      <AnimatePresence>
        {editingSession && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
            onClick={() => setEditingSession(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-secondary-800 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto p-6 border border-secondary-700"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-medieval text-white">
                  Sesja {editingSession.number}
                </h3>
                <div className="flex gap-2">
                  <button
                    onClick={() => updateSession(editingSession)}
                    className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                  >
                    Zapisz
                  </button>
                  <button
                    onClick={() => deleteSession(editingSession.id)}
                    className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => setEditingSession(null)}
                    className="px-4 py-2 bg-secondary-700 hover:bg-secondary-600 text-white rounded-lg transition-colors"
                  >
                    Zamknij
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-secondary-300 mb-2">
                    Tytuł Sesji
                  </label>
                  <input
                    type="text"
                    value={editingSession.title}
                    onChange={(e) => setEditingSession({...editingSession, title: e.target.value})}
                    className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                    placeholder="Tytuł sesji..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-secondary-300 mb-2">
                    Data
                  </label>
                  <input
                    type="date"
                    value={editingSession.date}
                    onChange={(e) => setEditingSession({...editingSession, date: e.target.value})}
                    className="w-full bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white"
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-secondary-300 mb-2">
                    Podsumowanie Sesji
                  </label>
                  <textarea
                    value={editingSession.summary}
                    onChange={(e) => setEditingSession({...editingSession, summary: e.target.value})}
                    className="w-full h-24 bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white resize-none"
                    placeholder="Co wydarzyło się w tej sesji..."
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-secondary-300 mb-2">
                    Notatki MG
                  </label>
                  <textarea
                    value={editingSession.notes}
                    onChange={(e) => setEditingSession({...editingSession, notes: e.target.value})}
                    className="w-full h-32 bg-secondary-600 border border-secondary-500 rounded-lg px-3 py-2 text-white resize-none"
                    placeholder="Prywatne notatki dla MG..."
                  />
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
