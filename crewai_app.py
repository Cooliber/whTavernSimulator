"""
Warhammer Fantasy GSAP Tavern Simulator with CrewAI + Grok + Cerebras
Epic multi-agent crew simulation with 17 Warhammer characters
"""

import streamlit as st
import os
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import random

# CrewAI imports
from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM

# Streamlit components for GSAP
import streamlit.components.v1 as components

# Environment setup
from dotenv import load_dotenv
load_dotenv()

# Configuration
class CrewAIConfig:
    """Configuration for CrewAI Warhammer Tavern"""
    
    # LLM Configuration - Updated to match .env file keys
    GROK_API_KEY = os.getenv("groq_api_key", "")  # Note: Using Groq instead of Grok
    CEREBRAS_API_KEY = os.getenv("Cerebras_api", "")
    
    # Agent Configuration
    MAX_AGENTS = 17
    MAX_EXECUTION_TIME = 300  # 5 minutes
    
    # GSAP Configuration
    GSAP_VERSION = "3.12.5"
    ANIMATION_FPS = 60
    
    # Warhammer Lore
    FACTIONS = [
        "Empire", "Dwarf", "High Elf", "Wood Elf", "Bretonnian",
        "Orc", "Vampire", "Skaven", "Chaos", "Tomb King",
        "Dark Elf", "Lizardman", "Goblin"
    ]

# Mock LLM for testing
class MockLLM:
    """Mock LLM for testing CrewAI without real API keys"""

    def __init__(self, model_name="mock-llm"):
        self.model_name = model_name
        self.responses = {
            "Empire Leader": [
                "As Emperor Karl Franz, I assess the tavern situation with imperial wisdom. The tension levels appear moderate, requiring coordinated response from all agents. I assign the Witch Hunter to scan for threats, the Dwarf Engineer to check resources, the Elf Mage to divine future events, and the Orc Warboss to prepare for potential conflicts. Unity and order shall prevail!",
                "Strategic analysis complete. The tavern requires immediate attention to maintain imperial order and ensure patron safety.",
                "Coordination protocols activated. All agents report to your designated stations for optimal tavern management."
            ],
            "Witch Hunter": [
                "By Sigmar's hammer, I detect no immediate chaos corruption in this establishment. However, vigilance must be maintained. Several patrons bear watching - their auras suggest hidden secrets. I recommend continued surveillance and preparation for purification rituals if needed.",
                "Threat assessment: Low to moderate. No heretical activity detected at this time.",
                "The Emperor's light reveals all. This tavern remains pure for now."
            ],
            "Dwarf Engineer": [
                "Aye, the tavern's infrastructure is sound, though improvements could be made. Ale supplies are adequate for the evening, food stores well-stocked. The hearth needs attention - I'll craft a more efficient bellows system. By my beard, this establishment will run like clockwork!",
                "Resource status: Operational. Minor maintenance required on heating systems.",
                "Engineering solutions implemented. Efficiency increased by 23.7%!"
            ],
            "High Elf Mage": [
                "The Winds of Magic whisper of events yet to come. I foresee a night of revelry that may turn to conflict if not carefully managed. The threads of fate suggest three possible outcomes: peaceful celebration, minor altercation, or significant upheaval. Preparation for all contingencies is advised.",
                "Mystical divination reveals potential challenges ahead. The crew must remain vigilant.",
                "The future flows like water - changeable yet guided by our actions tonight."
            ],
            "Orc Warboss": [
                "WAAAGH! Da tavern looks ready for a good scrap if needed! I see some tough-lookin' gits who might cause trouble, but me choppa is ready! If anyone starts sumfin', I'll finish it quick and brutal-like. For now, I'll keep da peace... but I'm ready for action!",
                "Combat readiness: Maximum! Ready to krump any troublemakers!",
                "WAAAGH! Everything's under control, boss!"
            ]
        }
        self.call_count = {}

    def call(self, messages, **kwargs):
        """Mock LLM call that returns appropriate responses"""
        # Extract agent context from messages
        agent_type = "Empire Leader"  # Default

        if isinstance(messages, list) and messages:
            content = str(messages[-1].get("content", ""))
            if "witch hunter" in content.lower() or "chaos" in content.lower():
                agent_type = "Witch Hunter"
            elif "dwarf" in content.lower() or "engineer" in content.lower():
                agent_type = "Dwarf Engineer"
            elif "elf" in content.lower() or "mage" in content.lower():
                agent_type = "High Elf Mage"
            elif "orc" in content.lower() or "warboss" in content.lower():
                agent_type = "Orc Warboss"

        # Get response count for this agent
        count = self.call_count.get(agent_type, 0)
        self.call_count[agent_type] = count + 1

        # Return appropriate response
        responses = self.responses.get(agent_type, ["Mock response generated."])
        response_index = count % len(responses)

        # Mock response object
        class MockResponse:
            def __init__(self, content):
                self.content = content
                self.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': content})()})]

        return MockResponse(responses[response_index])

# LLM Setup
def setup_llms():
    """Setup Groq and Cerebras LLMs for CrewAI"""
    llms = {}

    # Groq LLM for complex reasoning (using groq_api_key from .env)
    if CrewAIConfig.GROK_API_KEY:
        try:
            # Use groq/ prefix for LiteLLM to recognize it as Groq provider
            llms["groq"] = LLM(
                model="groq/llama3-70b-8192",
                api_key=CrewAIConfig.GROK_API_KEY
            )
            print("✅ Groq LLM configured successfully")
        except Exception as e:
            print(f"❌ Failed to setup Groq LLM: {e}")

    # Cerebras LLM for fast responses - use openai/ prefix with custom base_url
    if CrewAIConfig.CEREBRAS_API_KEY:
        try:
            # For Cerebras, use openai/ prefix with custom base_url
            llms["cerebras"] = LLM(
                model="openai/llama3.1-8b",
                api_key=CrewAIConfig.CEREBRAS_API_KEY,
                base_url="https://api.cerebras.ai/v1"
            )
            print("✅ Cerebras LLM configured successfully")
        except Exception as e:
            print(f"❌ Failed to setup Cerebras LLM: {e}")

    # Always provide mock LLM as fallback
    llms["mock"] = MockLLM("mock-warhammer-llm")

    if not CrewAIConfig.GROK_API_KEY and not CrewAIConfig.CEREBRAS_API_KEY:
        print("⚠️ No API keys configured. Using mock LLM responses.")

    return llms

# Agent Definitions (MVP 5 agents first)
def create_karl_franz_agent(llm):
    """Create Karl Franz - Empire Leader Agent"""
    return Agent(
        role="Empire Leader",
        goal="Coordinate the tavern crew and maintain imperial order",
        backstory="""You are Karl Franz, Emperor of the Empire and supreme leader. 
        Your duty is to coordinate all agents in the tavern, assign strategic tasks, 
        and ensure the glory of the Empire. You possess natural leadership and 
        tactical brilliance that inspires others to greatness.""",
        llm=llm,
        verbose=True,
        allow_delegation=True,
        max_iter=3
    )

def create_witch_hunter_agent(llm):
    """Create Witch Hunter - Threat Detection Agent"""
    return Agent(
        role="Witch Hunter",
        goal="Detect and eliminate chaos threats in the tavern",
        backstory="""You are a Witch Hunter of the Temple of Sigmar, trained to 
        detect the taint of Chaos wherever it hides. Your keen senses can spot 
        heretics, mutants, and cultists. You work with ruthless efficiency to 
        purge corruption and protect the innocent.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=2
    )

def create_dwarf_engineer_agent(llm):
    """Create Dwarf Engineer - Resource Management Agent"""
    return Agent(
        role="Dwarf Engineer",
        goal="Manage tavern resources and create useful tools",
        backstory="""You are a Dwarf Engineer from Karaz-a-Karak, master of 
        mechanical devices and resource management. Your beard is long, your 
        ale is strong, and your engineering skills are unmatched. You ensure 
        the tavern runs efficiently and create ingenious solutions to problems.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=2
    )

def create_elf_mage_agent(llm):
    """Create Elf Mage - Oracle and Prediction Agent"""
    return Agent(
        role="High Elf Mage",
        goal="Predict events and generate mystical insights",
        backstory="""You are a High Elf Mage from Ulthuan, wielder of the Winds 
        of Magic and seer of future events. Your centuries of study have granted 
        you wisdom beyond mortal understanding. You divine the threads of fate 
        and provide mystical guidance to the crew.""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )

def create_orc_warboss_agent(llm):
    """Create Orc Warboss - Combat Resolution Agent"""
    return Agent(
        role="Orc Warboss",
        goal="Resolve conflicts through superior fighting prowess",
        backstory="""You are an Orc Warboss, the biggest and strongest of your 
        tribe. When diplomacy fails and tensions rise, you step in with brutal 
        efficiency. Your massive choppa and intimidating presence can end any 
        brawl quickly. WAAAGH!""",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=1
    )

# Task Definitions
def create_coordination_task(agent):
    """Create coordination task for Karl Franz"""
    return Task(
        description="""Analyze the current tavern situation and coordinate the crew response.
        Assess tension levels, identify priorities, and assign appropriate tasks to other agents.
        Provide strategic leadership and ensure all agents work together effectively.""",
        agent=agent,
        expected_output="Strategic coordination plan with task assignments for crew members"
    )

def create_threat_detection_task(agent):
    """Create threat detection task for Witch Hunter"""
    return Task(
        description="""Scan the tavern for signs of chaos corruption, heretical activity,
        or supernatural threats. Investigate suspicious characters and report findings.
        Recommend immediate actions if threats are detected.""",
        agent=agent,
        expected_output="Threat assessment report with recommended security measures"
    )

def create_resource_management_task(agent):
    """Create resource management task for Dwarf Engineer"""
    return Task(
        description="""Evaluate tavern resources including ale supplies, food stores,
        room availability, and equipment condition. Identify any shortages or maintenance
        needs. Propose engineering solutions to improve efficiency.""",
        agent=agent,
        expected_output="Resource status report with improvement recommendations"
    )

def create_divination_task(agent):
    """Create divination task for Elf Mage"""
    return Task(
        description="""Use mystical powers to divine potential future events in the tavern.
        Generate prophetic insights about upcoming challenges or opportunities.
        Provide magical guidance to help the crew prepare for what's to come.""",
        agent=agent,
        expected_output="Mystical prophecy with guidance for crew preparation"
    )

def create_combat_readiness_task(agent):
    """Create combat readiness task for Orc Warboss"""
    return Task(
        description="""Assess the tavern's combat readiness and potential for violence.
        Identify troublemakers and evaluate threat levels. Prepare for immediate action
        if brawls break out. Ensure the crew can handle any physical confrontations.""",
        agent=agent,
        expected_output="Combat assessment with readiness recommendations"
    )

# GSAP Renderer for CrewAI
class CrewAIGSAPRenderer:
    """Enhanced GSAP renderer for CrewAI multi-agent visualization"""
    
    def __init__(self):
        self.gsap_version = CrewAIConfig.GSAP_VERSION
    
    def get_crew_visualization_html(self, agents: List[Agent], tasks: List[Task]) -> str:
        """Generate GSAP-powered HTML for crew visualization"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/{self.gsap_version}/gsap.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/{self.gsap_version}/TextPlugin.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/{self.gsap_version}/MorphSVGPlugin.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/{self.gsap_version}/DrawSVGPlugin.min.js"></script>
            <style>
                {self._get_crew_css()}
            </style>
        </head>
        <body>
            <div id="crew-container">
                <h2 id="crew-title">🏰 Warhammer Tavern Crew</h2>
                <div id="agents-grid">
                    {self._generate_agent_boxes(agents)}
                </div>
                <div id="tasks-section">
                    <h3>Active Tasks</h3>
                    <div id="tasks-list">
                        {self._generate_task_boxes(tasks)}
                    </div>
                </div>
                <div id="communication-flow">
                    <svg id="comm-svg" width="100%" height="200">
                        <!-- Communication lines will be drawn here -->
                    </svg>
                </div>
            </div>
            
            <script>
                {self._get_crew_animations()}
            </script>
        </body>
        </html>
        """
    
    def _get_crew_css(self) -> str:
        """CSS styles for crew visualization"""
        return """
            #crew-container {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                border-radius: 15px;
                padding: 20px;
                color: #fff;
                font-family: 'Arial', sans-serif;
            }
            
            #crew-title {
                text-align: center;
                color: #ffd700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                margin-bottom: 20px;
            }
            
            #agents-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-bottom: 30px;
            }
            
            .agent-card {
                background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,215,0,0.05));
                border: 2px solid rgba(255,215,0,0.3);
                border-radius: 10px;
                padding: 15px;
                position: relative;
                opacity: 0;
                transform: translateY(50px);
                transition: all 0.3s ease;
            }
            
            .agent-card:hover {
                border-color: rgba(255,215,0,0.8);
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(255,215,0,0.2);
            }
            
            .agent-name {
                font-size: 18px;
                font-weight: bold;
                color: #ffd700;
                margin-bottom: 5px;
            }
            
            .agent-role {
                font-size: 14px;
                color: #ccc;
                margin-bottom: 10px;
                font-style: italic;
            }
            
            .agent-status {
                font-size: 12px;
                padding: 5px 10px;
                background: rgba(0,255,0,0.2);
                border-radius: 15px;
                display: inline-block;
            }
            
            .task-card {
                background: rgba(0,0,0,0.3);
                border-left: 4px solid #ffd700;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                opacity: 0;
                transform: translateX(-30px);
            }
            
            .task-description {
                font-size: 14px;
                color: #ddd;
            }
            
            #communication-flow {
                margin-top: 20px;
                background: rgba(0,0,0,0.2);
                border-radius: 10px;
                padding: 10px;
            }
        """

    def _generate_agent_boxes(self, agents: List[Agent]) -> str:
        """Generate HTML for agent visualization boxes"""
        agent_icons = {
            "Empire Leader": "👑",
            "Witch Hunter": "🔥",
            "Dwarf Engineer": "🔨",
            "High Elf Mage": "🔮",
            "Orc Warboss": "⚔️"
        }

        boxes = []
        for i, agent in enumerate(agents):
            icon = agent_icons.get(agent.role, "🎭")
            boxes.append(f"""
                <div class="agent-card" id="agent-{i}" data-role="{agent.role}">
                    <div class="agent-name">{icon} {agent.role}</div>
                    <div class="agent-role">{agent.goal}</div>
                    <div class="agent-status">Ready</div>
                </div>
            """)

        return "".join(boxes)

    def _generate_task_boxes(self, tasks: List[Task]) -> str:
        """Generate HTML for task visualization"""
        boxes = []
        for i, task in enumerate(tasks):
            boxes.append(f"""
                <div class="task-card" id="task-{i}">
                    <div class="task-description">{task.description[:100]}...</div>
                </div>
            """)

        return "".join(boxes)

    def _get_crew_animations(self) -> str:
        """GSAP animations for crew visualization"""
        return """
            // Initialize crew animations
            gsap.registerPlugin(TextPlugin, MorphSVGPlugin, DrawSVGPlugin);

            // Entrance animations
            function initializeCrewAnimations() {
                const agentCards = gsap.utils.toArray('.agent-card');
                const taskCards = gsap.utils.toArray('.task-card');

                // Staggered agent entrance
                gsap.fromTo(agentCards,
                    { opacity: 0, y: 50, scale: 0.8 },
                    {
                        opacity: 1,
                        y: 0,
                        scale: 1,
                        duration: 1.2,
                        ease: "back.out(1.7)",
                        stagger: 0.2
                    }
                );

                // Task cards slide in
                gsap.fromTo(taskCards,
                    { opacity: 0, x: -30 },
                    {
                        opacity: 1,
                        x: 0,
                        duration: 0.8,
                        ease: "power2.out",
                        stagger: 0.1,
                        delay: 1
                    }
                );
            }

            // Agent thinking animation
            function animateAgentThinking(agentId) {
                const agent = document.getElementById(agentId);
                if (!agent) return;

                gsap.to(agent, {
                    duration: 0.6,
                    boxShadow: "0 0 30px rgba(255,215,0,0.8)",
                    scale: 1.05,
                    ease: "power2.inOut",
                    yoyo: true,
                    repeat: 3
                });

                // Update status
                const status = agent.querySelector('.agent-status');
                if (status) {
                    gsap.to(status, {
                        duration: 0.3,
                        text: "Thinking...",
                        backgroundColor: "rgba(255,165,0,0.3)"
                    });
                }
            }

            // Task completion animation
            function animateTaskCompletion(taskId) {
                const task = document.getElementById(taskId);
                if (!task) return;

                gsap.to(task, {
                    duration: 0.5,
                    backgroundColor: "rgba(0,255,0,0.2)",
                    borderLeftColor: "#00ff00",
                    scale: 1.02,
                    ease: "power2.out"
                });
            }

            // Communication flow animation
            function animateCommunication(fromAgent, toAgent) {
                const svg = document.getElementById('comm-svg');
                if (!svg) return;

                // Create communication line
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', '10%');
                line.setAttribute('y1', '50%');
                line.setAttribute('x2', '90%');
                line.setAttribute('y2', '50%');
                line.setAttribute('stroke', '#ffd700');
                line.setAttribute('stroke-width', '3');
                line.setAttribute('opacity', '0');

                svg.appendChild(line);

                // Animate line
                gsap.fromTo(line,
                    { drawSVG: "0% 0%", opacity: 0 },
                    {
                        drawSVG: "0% 100%",
                        opacity: 1,
                        duration: 1.5,
                        ease: "power2.out",
                        onComplete: () => {
                            gsap.to(line, {
                                opacity: 0,
                                duration: 0.5,
                                delay: 1,
                                onComplete: () => line.remove()
                            });
                        }
                    }
                );
            }

            // Global functions
            window.animateAgentThinking = animateAgentThinking;
            window.animateTaskCompletion = animateTaskCompletion;
            window.animateCommunication = animateCommunication;

            // Initialize on load
            document.addEventListener('DOMContentLoaded', initializeCrewAnimations);
        """

# Main CrewAI Tavern Simulator
class WarhamerTavernCrew:
    """Main class for Warhammer Tavern CrewAI simulation"""

    def __init__(self):
        self.llms = setup_llms()
        self.agents = []
        self.tasks = []
        self.crew = None
        self.gsap_renderer = CrewAIGSAPRenderer()

    def initialize_mvp_crew(self):
        """Initialize MVP crew with 5 agents"""
        # Select appropriate LLMs
        groq_llm = self.llms.get("groq")
        cerebras_llm = self.llms.get("cerebras")
        fallback_llm = self.llms.get("mock")

        # Create agents with appropriate LLMs
        self.agents = [
            create_karl_franz_agent(groq_llm or fallback_llm),      # Complex planning
            create_witch_hunter_agent(cerebras_llm or fallback_llm), # Fast detection
            create_dwarf_engineer_agent(groq_llm or fallback_llm),   # Complex engineering
            create_elf_mage_agent(groq_llm or fallback_llm),         # Complex divination
            create_orc_warboss_agent(cerebras_llm or fallback_llm)   # Fast combat
        ]

        # Create corresponding tasks
        self.tasks = [
            create_coordination_task(self.agents[0]),
            create_threat_detection_task(self.agents[1]),
            create_resource_management_task(self.agents[2]),
            create_divination_task(self.agents[3]),
            create_combat_readiness_task(self.agents[4])
        ]

        # Create crew
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_execution_time=CrewAIConfig.MAX_EXECUTION_TIME
        )

        return True

    def execute_tavern_simulation(self) -> Dict[str, Any]:
        """Execute the tavern simulation with CrewAI"""
        if not self.crew:
            return {"error": "Crew not initialized"}

        try:
            start_time = time.time()

            # Execute crew tasks
            result = self.crew.kickoff()

            execution_time = time.time() - start_time

            return {
                "success": True,
                "result": result,
                "execution_time": execution_time,
                "agents_count": len(self.agents),
                "tasks_completed": len(self.tasks)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": time.time() - start_time
            }

    def get_crew_status(self) -> Dict[str, Any]:
        """Get current crew status"""
        return {
            "agents": [
                {
                    "role": agent.role,
                    "goal": agent.goal,
                    "llm_configured": agent.llm is not None
                }
                for agent in self.agents
            ],
            "tasks": [
                {
                    "description": task.description[:100] + "...",
                    "agent_role": task.agent.role if task.agent else "Unassigned"
                }
                for task in self.tasks
            ],
            "crew_ready": self.crew is not None
        }

# Streamlit UI
def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="🏰 Warhammer Tavern CrewAI",
        page_icon="⚔️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #ffd700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            font-size: 3rem;
            margin-bottom: 2rem;
        }
        .crew-stats {
            background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,215,0,0.05));
            border: 2px solid rgba(255,215,0,0.3);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="main-header">🏰 Warhammer Fantasy Tavern Simulator</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #ccc;">Powered by CrewAI + Grok + Cerebras + GSAP 138%</h3>', unsafe_allow_html=True)

    # Initialize session state
    if 'tavern_crew' not in st.session_state:
        st.session_state.tavern_crew = WarhamerTavernCrew()
        st.session_state.crew_initialized = False
        st.session_state.simulation_results = None

    # Sidebar controls
    with st.sidebar:
        st.header("🎮 Crew Controls")

        # API Configuration
        st.subheader("🔑 API Configuration")
        groq_key = st.text_input("Groq API Key", type="password", value=CrewAIConfig.GROK_API_KEY)
        cerebras_key = st.text_input("Cerebras API Key", type="password", value=CrewAIConfig.CEREBRAS_API_KEY)

        if groq_key:
            os.environ["groq_api_key"] = groq_key
        if cerebras_key:
            os.environ["Cerebras_api"] = cerebras_key

        st.divider()

        # Crew Management
        st.subheader("👥 Crew Management")

        if st.button("🚀 Initialize MVP Crew", type="primary"):
            with st.spinner("Initializing Warhammer Tavern Crew..."):
                try:
                    success = st.session_state.tavern_crew.initialize_mvp_crew()
                    if success:
                        st.session_state.crew_initialized = True
                        st.success("✅ MVP Crew initialized successfully!")
                    else:
                        st.error("❌ Failed to initialize crew")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        if st.session_state.crew_initialized:
            if st.button("⚔️ Execute Tavern Simulation", type="secondary"):
                with st.spinner("Executing tavern simulation..."):
                    results = st.session_state.tavern_crew.execute_tavern_simulation()
                    st.session_state.simulation_results = results

                    if results.get("success"):
                        st.success(f"✅ Simulation completed in {results['execution_time']:.2f}s")
                    else:
                        st.error(f"❌ Simulation failed: {results.get('error', 'Unknown error')}")

        st.divider()

        # Configuration
        st.subheader("⚙️ Configuration")
        st.write(f"**Max Agents:** {CrewAIConfig.MAX_AGENTS}")
        st.write(f"**GSAP Version:** {CrewAIConfig.GSAP_VERSION}")
        st.write(f"**Animation FPS:** {CrewAIConfig.ANIMATION_FPS}")

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("🎭 Crew Visualization")

        if st.session_state.crew_initialized:
            # Render GSAP visualization
            crew = st.session_state.tavern_crew
            gsap_html = crew.gsap_renderer.get_crew_visualization_html(crew.agents, crew.tasks)
            components.html(gsap_html, height=800, scrolling=True)
        else:
            st.info("👆 Initialize the crew first to see the visualization")

    with col2:
        st.header("📊 Crew Status")

        if st.session_state.crew_initialized:
            status = st.session_state.tavern_crew.get_crew_status()

            # Crew stats
            st.markdown('<div class="crew-stats">', unsafe_allow_html=True)
            st.metric("Active Agents", len(status["agents"]))
            st.metric("Pending Tasks", len(status["tasks"]))
            st.metric("Crew Ready", "✅" if status["crew_ready"] else "❌")
            st.markdown('</div>', unsafe_allow_html=True)

            # Agent details
            st.subheader("👥 Agents")
            for agent in status["agents"]:
                with st.expander(f"{agent['role']}"):
                    st.write(f"**Goal:** {agent['goal']}")
                    st.write(f"**LLM:** {'✅ Configured' if agent['llm_configured'] else '❌ Not configured'}")

            # Task details
            st.subheader("📋 Tasks")
            for i, task in enumerate(status["tasks"]):
                with st.expander(f"Task {i+1}: {task['agent_role']}"):
                    st.write(task["description"])

        # Simulation results
        if st.session_state.simulation_results:
            st.header("🎯 Simulation Results")
            results = st.session_state.simulation_results

            if results.get("success"):
                st.success("✅ Simulation Successful")
                st.metric("Execution Time", f"{results['execution_time']:.2f}s")
                st.metric("Agents Involved", results['agents_count'])
                st.metric("Tasks Completed", results['tasks_completed'])

                # Show results
                if results.get("result"):
                    st.subheader("📜 Crew Results")
                    st.text_area("Simulation Output", str(results["result"]), height=200)
            else:
                st.error("❌ Simulation Failed")
                st.error(results.get("error", "Unknown error"))

if __name__ == "__main__":
    main()
