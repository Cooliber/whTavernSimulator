"""
Tavern Economy System for resource management, reputation, and rumor-based currency
Integrates with narrative engine and agent memory for dynamic economic consequences
"""

import time
import random
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from .agent_memory import AgentMemorySystem, MemoryType, MemoryImportance

class ResourceType(Enum):
    GOLD = "gold"
    REPUTATION = "reputation"
    INFORMATION = "information"
    INFLUENCE = "influence"
    SUPPLIES = "supplies"
    FAVORS = "favors"

class TransactionType(Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    BRIBE = "bribe"
    INFORMATION_TRADE = "information_trade"
    FAVOR_EXCHANGE = "favor_exchange"
    REPUTATION_GAIN = "reputation_gain"
    REPUTATION_LOSS = "reputation_loss"

@dataclass
class EconomicResource:
    """Economic resource with value and metadata"""
    resource_type: ResourceType
    amount: float
    quality: int  # 1-10 quality rating
    source: str
    timestamp: float
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class Transaction:
    """Economic transaction record"""
    id: str
    transaction_type: TransactionType
    participants: List[str]
    resources_exchanged: Dict[ResourceType, float]
    description: str
    timestamp: float
    success: bool
    consequences: List[str] = None
    
    def __post_init__(self):
        if self.consequences is None:
            self.consequences = []

@dataclass
class TavernEconomicState:
    """Current economic state of the tavern"""
    total_wealth: float = 100.0
    reputation_score: float = 50.0  # 0-100
    information_value: float = 25.0
    influence_level: float = 30.0
    supply_quality: float = 60.0
    patron_satisfaction: float = 70.0
    
    # Economic modifiers
    price_multiplier: float = 1.0
    reputation_decay_rate: float = 0.1
    information_decay_rate: float = 0.05

class TavernEconomySystem:
    """Comprehensive tavern economy management system"""
    
    def __init__(self, memory_system: AgentMemorySystem = None):
        self.memory_system = memory_system or AgentMemorySystem()
        self.economic_state = TavernEconomicState()
        
        # Resource inventories by agent
        self.agent_resources: Dict[str, Dict[ResourceType, float]] = {}
        
        # Transaction history
        self.transaction_history: List[Transaction] = []
        
        # Market prices (base values)
        self.market_prices = {
            ResourceType.GOLD: 1.0,
            ResourceType.REPUTATION: 5.0,  # Gold per reputation point
            ResourceType.INFORMATION: 10.0,  # Gold per information unit
            ResourceType.INFLUENCE: 15.0,  # Gold per influence point
            ResourceType.SUPPLIES: 2.0,  # Gold per supply unit
            ResourceType.FAVORS: 20.0  # Gold per favor
        }
        
        # Rumor economy - rumors as currency
        self.rumor_market = {
            "active_rumors": [],
            "rumor_values": {},  # rumor_id -> value
            "rumor_traders": {},  # agent_id -> [rumor_ids]
        }
        
        # Initialize agent resources
        self._initialize_agent_resources()
    
    def _initialize_agent_resources(self):
        """Initialize starting resources for all 17 agents"""
        agent_starting_resources = self._get_17_agent_resources()

        for agent, resources in agent_starting_resources.items():
            self.agent_resources[agent] = resources.copy()

    def _get_17_agent_resources(self) -> Dict[str, Dict[ResourceType, float]]:
        """Get starting resources for all 17 agents organized by faction"""
        return {
            # Empire Faction - Well-funded, high reputation
            "Karczmarz": {
                ResourceType.GOLD: 150.0, ResourceType.REPUTATION: 60.0, ResourceType.INFORMATION: 40.0,
                ResourceType.INFLUENCE: 30.0, ResourceType.SUPPLIES: 80.0, ResourceType.FAVORS: 10.0
            },
            "Kapitan_Straży": {
                ResourceType.GOLD: 120.0, ResourceType.REPUTATION: 70.0, ResourceType.INFORMATION: 50.0,
                ResourceType.INFLUENCE: 60.0, ResourceType.SUPPLIES: 60.0, ResourceType.FAVORS: 15.0
            },
            "Kupiec_Imperialny": {
                ResourceType.GOLD: 200.0, ResourceType.REPUTATION: 55.0, ResourceType.INFORMATION: 60.0,
                ResourceType.INFLUENCE: 40.0, ResourceType.SUPPLIES: 90.0, ResourceType.FAVORS: 25.0
            },
            "Czarodziej_Jasności": {
                ResourceType.GOLD: 80.0, ResourceType.REPUTATION: 65.0, ResourceType.INFORMATION: 85.0,
                ResourceType.INFLUENCE: 50.0, ResourceType.SUPPLIES: 30.0, ResourceType.FAVORS: 20.0
            },

            # Chaos Faction - Low reputation, high influence/information
            "Czempion": {
                ResourceType.GOLD: 120.0, ResourceType.REPUTATION: 20.0, ResourceType.INFORMATION: 30.0,
                ResourceType.INFLUENCE: 60.0, ResourceType.SUPPLIES: 40.0, ResourceType.FAVORS: 15.0
            },
            "Kultista_Nurgle": {
                ResourceType.GOLD: 60.0, ResourceType.REPUTATION: 15.0, ResourceType.INFORMATION: 40.0,
                ResourceType.INFLUENCE: 45.0, ResourceType.SUPPLIES: 25.0, ResourceType.FAVORS: 30.0
            },
            "Berserker_Khorne": {
                ResourceType.GOLD: 90.0, ResourceType.REPUTATION: 25.0, ResourceType.INFORMATION: 20.0,
                ResourceType.INFLUENCE: 55.0, ResourceType.SUPPLIES: 35.0, ResourceType.FAVORS: 10.0
            },
            "Mag_Tzeentch": {
                ResourceType.GOLD: 70.0, ResourceType.REPUTATION: 30.0, ResourceType.INFORMATION: 75.0,
                ResourceType.INFLUENCE: 70.0, ResourceType.SUPPLIES: 20.0, ResourceType.FAVORS: 35.0
            },

            # Elves Faction - High information, moderate resources
            "Zwiadowca": {
                ResourceType.GOLD: 100.0, ResourceType.REPUTATION: 40.0, ResourceType.INFORMATION: 80.0,
                ResourceType.INFLUENCE: 35.0, ResourceType.SUPPLIES: 50.0, ResourceType.FAVORS: 20.0
            },
            "Mag_Wysokich_Elfów": {
                ResourceType.GOLD: 110.0, ResourceType.REPUTATION: 75.0, ResourceType.INFORMATION: 95.0,
                ResourceType.INFLUENCE: 65.0, ResourceType.SUPPLIES: 40.0, ResourceType.FAVORS: 30.0
            },
            "Strażnik_Lasu": {
                ResourceType.GOLD: 70.0, ResourceType.REPUTATION: 50.0, ResourceType.INFORMATION: 70.0,
                ResourceType.INFLUENCE: 40.0, ResourceType.SUPPLIES: 60.0, ResourceType.FAVORS: 25.0
            },
            "Tancerz_Cieni": {
                ResourceType.GOLD: 85.0, ResourceType.REPUTATION: 35.0, ResourceType.INFORMATION: 85.0,
                ResourceType.INFLUENCE: 55.0, ResourceType.SUPPLIES: 30.0, ResourceType.FAVORS: 40.0
            },

            # Dwarfs Faction - High supplies, moderate gold
            "Kowal_Krasnoludzki": {
                ResourceType.GOLD: 130.0, ResourceType.REPUTATION: 65.0, ResourceType.INFORMATION: 45.0,
                ResourceType.INFLUENCE: 35.0, ResourceType.SUPPLIES: 95.0, ResourceType.FAVORS: 20.0
            },
            "Górnik_Karak": {
                ResourceType.GOLD: 110.0, ResourceType.REPUTATION: 55.0, ResourceType.INFORMATION: 35.0,
                ResourceType.INFLUENCE: 30.0, ResourceType.SUPPLIES: 85.0, ResourceType.FAVORS: 15.0
            },
            "Inżynier_Gildii": {
                ResourceType.GOLD: 140.0, ResourceType.REPUTATION: 60.0, ResourceType.INFORMATION: 55.0,
                ResourceType.INFLUENCE: 45.0, ResourceType.SUPPLIES: 90.0, ResourceType.FAVORS: 25.0
            },

            # Neutral Faction - Balanced resources
            "Wiedźma": {
                ResourceType.GOLD: 60.0, ResourceType.REPUTATION: 45.0, ResourceType.INFORMATION: 90.0,
                ResourceType.INFLUENCE: 70.0, ResourceType.SUPPLIES: 30.0, ResourceType.FAVORS: 35.0
            },
            "Łowca_Nagród": {
                ResourceType.GOLD: 95.0, ResourceType.REPUTATION: 40.0, ResourceType.INFORMATION: 60.0,
                ResourceType.INFLUENCE: 45.0, ResourceType.SUPPLIES: 55.0, ResourceType.FAVORS: 20.0
            },
            "Handlarz_Halfling": {
                ResourceType.GOLD: 160.0, ResourceType.REPUTATION: 70.0, ResourceType.INFORMATION: 50.0,
                ResourceType.INFLUENCE: 35.0, ResourceType.SUPPLIES: 75.0, ResourceType.FAVORS: 30.0
            }
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((Exception,))
    )
    def execute_transaction(self, transaction_type: TransactionType,
                          participants: List[str],
                          resources: Dict[ResourceType, float],
                          description: str) -> Transaction:
        """Execute an economic transaction between participants with retry mechanism"""
        
        transaction_id = f"txn_{int(time.time())}_{random.randint(1000, 9999)}"
        
        # Validate transaction
        if not self._validate_transaction(participants, resources):
            transaction = Transaction(
                id=transaction_id,
                transaction_type=transaction_type,
                participants=participants,
                resources_exchanged=resources,
                description=description,
                timestamp=time.time(),
                success=False,
                consequences=["Transaction validation failed"]
            )
            self.transaction_history.append(transaction)
            return transaction
        
        # Execute resource transfers
        success = self._transfer_resources(participants, resources, transaction_type)
        
        # Calculate consequences
        consequences = self._calculate_transaction_consequences(
            transaction_type, participants, resources, success
        )
        
        # Create transaction record
        transaction = Transaction(
            id=transaction_id,
            transaction_type=transaction_type,
            participants=participants,
            resources_exchanged=resources,
            description=description,
            timestamp=time.time(),
            success=success,
            consequences=consequences
        )
        
        self.transaction_history.append(transaction)
        
        # Store in agent memories
        self._record_transaction_in_memory(transaction)
        
        # Update economic state
        self._update_economic_state(transaction)
        
        return transaction
    
    def trade_rumor_for_resources(self, trader: str, rumor_content: str, 
                                 target_resource: ResourceType, 
                                 target_amount: float) -> bool:
        """Trade a rumor for resources (rumors as currency)"""
        
        # Evaluate rumor value
        rumor_value = self._evaluate_rumor_value(rumor_content, trader)
        
        # Calculate resource cost
        resource_cost = self._calculate_resource_cost(target_resource, target_amount)
        
        if rumor_value >= resource_cost:
            # Execute trade
            self.agent_resources[trader][target_resource] += target_amount
            
            # Add rumor to market
            rumor_id = f"rumor_{int(time.time())}_{random.randint(100, 999)}"
            self.rumor_market["active_rumors"].append({
                "id": rumor_id,
                "content": rumor_content,
                "trader": trader,
                "value": rumor_value,
                "timestamp": time.time()
            })
            
            self.rumor_market["rumor_values"][rumor_id] = rumor_value
            
            if trader not in self.rumor_market["rumor_traders"]:
                self.rumor_market["rumor_traders"][trader] = []
            self.rumor_market["rumor_traders"][trader].append(rumor_id)
            
            # Record transaction
            transaction = self.execute_transaction(
                TransactionType.INFORMATION_TRADE,
                [trader, "TavernMarket"],
                {target_resource: target_amount},
                f"Traded rumor for {target_amount} {target_resource.value}"
            )
            
            return True
        
        return False
    
    def get_agent_wealth_status(self, agent: str) -> Dict[str, Any]:
        """Get comprehensive wealth status for an agent"""
        if agent not in self.agent_resources:
            return {"error": "Agent not found"}
        
        resources = self.agent_resources[agent]
        
        # Calculate total wealth in gold equivalent
        total_wealth = 0.0
        for resource_type, amount in resources.items():
            total_wealth += amount * self.market_prices[resource_type]
        
        # Determine wealth class
        if total_wealth < 100:
            wealth_class = "Poor"
        elif total_wealth < 300:
            wealth_class = "Modest"
        elif total_wealth < 600:
            wealth_class = "Comfortable"
        elif total_wealth < 1000:
            wealth_class = "Wealthy"
        else:
            wealth_class = "Rich"
        
        return {
            "agent": agent,
            "resources": dict(resources),
            "total_wealth": total_wealth,
            "wealth_class": wealth_class,
            "market_power": self._calculate_market_power(agent),
            "recent_transactions": self._get_recent_transactions(agent, 5)
        }
    
    def simulate_economic_events(self) -> List[Dict[str, Any]]:
        """Simulate random economic events affecting the tavern"""
        events = []
        
        # Market fluctuations
        if random.random() < 0.3:
            resource_type = random.choice(list(ResourceType))
            change = random.uniform(-0.2, 0.3)
            old_price = self.market_prices[resource_type]
            self.market_prices[resource_type] *= (1 + change)
            
            events.append({
                "type": "market_fluctuation",
                "resource": resource_type.value,
                "price_change": change,
                "old_price": old_price,
                "new_price": self.market_prices[resource_type],
                "description": f"{resource_type.value} price {'increased' if change > 0 else 'decreased'} by {abs(change)*100:.1f}%"
            })
        
        # Reputation events
        if random.random() < 0.2:
            reputation_change = random.uniform(-10, 15)
            self.economic_state.reputation_score += reputation_change
            self.economic_state.reputation_score = max(0, min(100, self.economic_state.reputation_score))
            
            events.append({
                "type": "reputation_event",
                "change": reputation_change,
                "new_reputation": self.economic_state.reputation_score,
                "description": f"Tavern reputation {'improved' if reputation_change > 0 else 'declined'}"
            })
        
        # Supply events
        if random.random() < 0.25:
            supply_change = random.uniform(-20, 25)
            self.economic_state.supply_quality += supply_change
            self.economic_state.supply_quality = max(0, min(100, self.economic_state.supply_quality))
            
            events.append({
                "type": "supply_event",
                "change": supply_change,
                "new_quality": self.economic_state.supply_quality,
                "description": f"Supply quality {'improved' if supply_change > 0 else 'deteriorated'}"
            })
        
        return events
    
    def _validate_transaction(self, participants: List[str], 
                            resources: Dict[ResourceType, float]) -> bool:
        """Validate if transaction is possible"""
        for participant in participants:
            if participant not in self.agent_resources and participant != "TavernMarket":
                return False
        
        # Check if participants have required resources (simplified)
        return True
    
    def _transfer_resources(self, participants: List[str], 
                          resources: Dict[ResourceType, float],
                          transaction_type: TransactionType) -> bool:
        """Transfer resources between participants"""
        try:
            if len(participants) == 2:
                giver, receiver = participants
                
                for resource_type, amount in resources.items():
                    if giver != "TavernMarket":
                        if self.agent_resources[giver][resource_type] >= amount:
                            self.agent_resources[giver][resource_type] -= amount
                        else:
                            return False
                    
                    if receiver != "TavernMarket":
                        self.agent_resources[receiver][resource_type] += amount
            
            return True
        except Exception:
            return False
    
    def _calculate_transaction_consequences(self, transaction_type: TransactionType,
                                         participants: List[str],
                                         resources: Dict[ResourceType, float],
                                         success: bool) -> List[str]:
        """Calculate economic consequences of transaction"""
        consequences = []
        
        if success:
            if transaction_type == TransactionType.BRIBE:
                consequences.append("Corruption increased in tavern")
                consequences.append("Reputation risk if discovered")
            
            elif transaction_type == TransactionType.INFORMATION_TRADE:
                consequences.append("Information network strengthened")
                consequences.append("Knowledge economy expanded")
            
            elif transaction_type == TransactionType.FAVOR_EXCHANGE:
                consequences.append("Social bonds reinforced")
                consequences.append("Future obligations created")
        
        return consequences
    
    def _record_transaction_in_memory(self, transaction: Transaction):
        """Record transaction in agent memories"""
        for participant in transaction.participants:
            if participant in self.agent_resources:
                # Convert transaction to dict and handle enum keys
                transaction_dict = asdict(transaction)
                # Convert ResourceType keys to strings in resources_exchanged
                if 'resources_exchanged' in transaction_dict:
                    transaction_dict['resources_exchanged'] = {
                        (k.value if hasattr(k, 'value') else str(k)): v
                        for k, v in transaction_dict['resources_exchanged'].items()
                    }

                self.memory_system.store_memory(
                    agent_id=participant,
                    memory_type=MemoryType.INTERACTION,
                    content=f"Economic transaction: {transaction.description}",
                    importance=MemoryImportance.MEDIUM,
                    context=transaction_dict,
                    tags=["economy", "transaction", transaction.transaction_type.value]
                )
    
    def _update_economic_state(self, transaction: Transaction):
        """Update overall economic state based on transaction"""
        # Update tavern wealth
        if "TavernMarket" in transaction.participants:
            for resource_type, amount in transaction.resources_exchanged.items():
                if resource_type == ResourceType.GOLD:
                    self.economic_state.total_wealth += amount * 0.1  # Tavern takes 10% cut
        
        # Update reputation based on transaction type
        reputation_effects = {
            TransactionType.BRIBE: -2.0,
            TransactionType.INFORMATION_TRADE: 1.0,
            TransactionType.FAVOR_EXCHANGE: 0.5,
            TransactionType.PURCHASE: 0.1,
            TransactionType.SALE: 0.1
        }
        
        effect = reputation_effects.get(transaction.transaction_type, 0.0)
        self.economic_state.reputation_score += effect
        self.economic_state.reputation_score = max(0, min(100, self.economic_state.reputation_score))
    
    def _evaluate_rumor_value(self, rumor_content: str, trader: str) -> float:
        """Evaluate the economic value of a rumor"""
        base_value = 25.0  # Increased base value to make rumors more valuable

        # Value modifiers based on content (more generous)
        content_lower = rumor_content.lower()
        if "chaos" in content_lower:
            base_value *= 2.5
        if "treasure" in content_lower:
            base_value *= 2.0
        if "danger" in content_lower:
            base_value *= 1.8
        if "secret" in content_lower:
            base_value *= 1.7
        if "ancient" in content_lower:
            base_value *= 1.6
        if "hidden" in content_lower:
            base_value *= 1.5
        if "cultist" in content_lower:
            base_value *= 1.4
        if "passage" in content_lower:
            base_value *= 1.3

        # Trader reputation modifier (more forgiving)
        trader_reputation = self.agent_resources.get(trader, {}).get(ResourceType.REPUTATION, 50.0)
        reputation_modifier = max(0.5, trader_reputation / 50.0)  # Minimum 50% value

        return base_value * reputation_modifier
    
    def _calculate_resource_cost(self, resource_type: ResourceType, amount: float) -> float:
        """Calculate cost of resources in rumor value equivalent"""
        base_cost = self.market_prices[resource_type] * amount

        # Apply economic state modifiers with rumor trade discount
        cost_modifier = self.economic_state.price_multiplier * 0.6  # 40% discount for rumor trades

        # Additional discounts for certain resources
        if resource_type == ResourceType.INFORMATION:
            cost_modifier *= 0.5  # Information is cheaper with rumors
        elif resource_type == ResourceType.REPUTATION:
            cost_modifier *= 0.7  # Reputation is moderately discounted

        return base_cost * cost_modifier
    
    def _calculate_market_power(self, agent: str) -> float:
        """Calculate agent's market power (0-100)"""
        if agent not in self.agent_resources:
            return 0.0
        
        resources = self.agent_resources[agent]
        
        # Weight different resources for market power
        power = (
            resources[ResourceType.GOLD] * 0.3 +
            resources[ResourceType.REPUTATION] * 0.25 +
            resources[ResourceType.INFLUENCE] * 0.25 +
            resources[ResourceType.INFORMATION] * 0.15 +
            resources[ResourceType.FAVORS] * 0.05
        )
        
        return min(power / 10.0, 100.0)  # Scale to 0-100
    
    def _get_recent_transactions(self, agent: str, limit: int) -> List[Dict[str, Any]]:
        """Get recent transactions involving an agent"""
        agent_transactions = [
            asdict(txn) for txn in self.transaction_history
            if agent in txn.participants
        ]
        
        # Sort by timestamp, most recent first
        agent_transactions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return agent_transactions[:limit]
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=3),
        retry=retry_if_exception_type((Exception,))
    )
    def update_reputation_on_event(self, event: Dict[str, Any]) -> Dict[str, float]:
        """Update reputation based on narrative events with retry mechanism"""
        reputation_changes = {}

        event_type = event.get("type", "")
        event_title = event.get("title", "")
        event_description = event.get("description", "")
        tension_change = event.get("tension_change", 0)
        participants = event.get("participants", [])

        # Base reputation change based on event type
        event_reputation_effects = {
            "tavern_entrance": 1.0,  # New patrons boost reputation
            "mysterious_stranger": -2.0,  # Suspicious activity hurts reputation
            "brawl_brewing": -5.0,  # Violence is bad for business
            "rumor_spreading": 2.0,  # Information hub increases reputation
            "quest_opportunity": 3.0,  # Being a quest hub is prestigious
            "threat_detected": -3.0,  # Danger scares customers
            "alliance_forming": 4.0,  # Diplomatic success
            "betrayal_revealed": -8.0,  # Trust issues hurt business
            "combat_challenge": -1.0,  # Violence concerns
            "mystical_ritual": -2.0,  # Supernatural events unnerve patrons
            "diplomatic_mission": 5.0,  # High-class clientele
        }

        base_reputation_change = event_reputation_effects.get(event_type, 0.0)

        # Modify based on tension change (high tension events hurt reputation more)
        tension_modifier = -tension_change * 0.1

        # Total tavern reputation change
        total_reputation_change = base_reputation_change + tension_modifier

        # Apply to tavern reputation
        old_reputation = self.economic_state.reputation_score
        self.economic_state.reputation_score += total_reputation_change
        self.economic_state.reputation_score = max(0, min(100, self.economic_state.reputation_score))

        reputation_changes["tavern"] = total_reputation_change

        # Apply individual agent reputation changes for participants
        for participant in participants:
            if participant in self.agent_resources:
                # Participants get different reputation effects
                if event_type in ["quest_opportunity", "alliance_forming", "diplomatic_mission"]:
                    agent_change = abs(base_reputation_change) * 0.5  # Positive events boost agent rep
                elif event_type in ["brawl_brewing", "betrayal_revealed", "threat_detected"]:
                    agent_change = base_reputation_change * 0.3  # Negative events hurt less for individuals
                else:
                    agent_change = base_reputation_change * 0.2  # Neutral events have small effect

                old_agent_rep = self.agent_resources[participant][ResourceType.REPUTATION]
                self.agent_resources[participant][ResourceType.REPUTATION] += agent_change
                self.agent_resources[participant][ResourceType.REPUTATION] = max(0, min(100,
                    self.agent_resources[participant][ResourceType.REPUTATION]))

                reputation_changes[participant] = agent_change

        # Store reputation change in memory
        self.memory_system.store_memory(
            agent_id="TavernEconomy",
            memory_type=MemoryType.EVENT,
            content=f"Reputation impact from {event_type}: {total_reputation_change:+.1f} points",
            importance=MemoryImportance.HIGH if abs(total_reputation_change) > 5 else MemoryImportance.MEDIUM,
            context={
                "event": event,
                "reputation_changes": reputation_changes,
                "old_tavern_reputation": old_reputation,
                "new_tavern_reputation": self.economic_state.reputation_score
            },
            tags=["reputation", "event_impact", event_type]
        )

        return reputation_changes

    def get_economic_summary(self) -> Dict[str, Any]:
        """Get comprehensive economic summary"""
        return {
            "tavern_state": asdict(self.economic_state),
            "market_prices": {rt.value: price for rt, price in self.market_prices.items()},
            "agent_wealth": {
                agent: self.get_agent_wealth_status(agent)
                for agent in self.agent_resources.keys()
            },
            "rumor_market": {
                "active_rumors": len(self.rumor_market["active_rumors"]),
                "total_rumor_value": sum(self.rumor_market["rumor_values"].values()),
                "top_traders": list(self.rumor_market["rumor_traders"].keys())[:5]
            },
            "recent_transactions": len([t for t in self.transaction_history if time.time() - t.timestamp < 3600]),
            "economic_metrics": {
                "total_wealth_in_circulation": sum(
                    sum(resources.values()) for resources in self.agent_resources.values()
                ),
                "average_reputation": sum(
                    resources[ResourceType.REPUTATION] for resources in self.agent_resources.values()
                ) / len(self.agent_resources),
                "market_activity": len(self.transaction_history)
            }
        }

# Global economy system instance
tavern_economy = TavernEconomySystem()

# Cleanup function for graceful shutdown
def cleanup_economy_system():
    """Save economic state before shutdown"""
    tavern_economy.memory_system.save_memories()
    print("💰 Economic state saved successfully")
