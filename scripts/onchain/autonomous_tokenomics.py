#!/usr/bin/env python3
"""
Enochian Cyphers Autonomous Tokenomics System

Implements self-regulating economic mechanisms with dynamic pricing and market 
balancing. Addresses expert feedback Gap #4: Autonomous Tokenomics & Market 
Balancing.

This system provides:
- Dynamic quest rarity pricing based on player demand
- Automatic token burns for failed attempts and inflation control
- Liquidity provisions for trading Governor hypertokens
- Volatility dampening for wisdom-based assets
- Utility-based valuation with tradition-weighted rarity
- Market makers via TAP pools for sustainable economics

Maintains structural care by placing in /onchain directory for Bitcoin L1 
integration components.
"""

import json
import math
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TokenMetrics:
    """Token economic metrics"""
    token_id: str
    current_price: float
    base_value: float
    demand_multiplier: float
    rarity_score: float
    utility_score: float
    volatility_index: float
    last_trade_timestamp: str

@dataclass
class MarketConditions:
    """Current market conditions"""
    total_supply: int
    circulating_supply: int
    burned_tokens: int
    average_price: float
    market_cap: float
    trading_volume_24h: float
    demand_pressure: float
    supply_pressure: float
    market_sentiment: str

@dataclass
class LiquidityPool:
    """Liquidity pool for token trading"""
    pool_id: str
    token_a: str
    token_b: str
    reserve_a: float
    reserve_b: float
    total_liquidity: float
    fee_rate: float
    last_update: str

@dataclass
class EconomicEvent:
    """Economic event affecting tokenomics"""
    event_id: str
    event_type: str
    impact_magnitude: float
    affected_tokens: List[str]
    timestamp: str
    auto_response: Dict[str, Any]

class AutonomousTokenomics:
    """Autonomous tokenomics system for Enochian Cyphers"""
    
    def __init__(self):
        self.token_metrics = {}
        self.market_conditions = None
        self.liquidity_pools = {}
        self.economic_events = {}
        
        # Economic parameters
        self.base_quest_price = 100.0  # Base price in tokens
        self.max_price_multiplier = 10.0
        self.min_price_multiplier = 0.1
        self.burn_rate_failed = 0.5  # 50% burn on failed quests
        self.inflation_target = 0.02  # 2% annual inflation target
        self.volatility_dampening = 0.8  # 80% volatility reduction
        
        # Tradition rarity weights (Enochian base = 1.0)
        self.tradition_weights = {
            'enochian_magic': 1.0,      # Base tradition
            'hermetic_qabalah': 1.2,    # High value
            'golden_dawn': 1.1,         # Moderate premium
            'chaos_magic': 1.3,         # High rarity
            'alchemy': 1.15,            # Moderate premium
            'taoism': 1.05,             # Slight premium
            'sufism': 1.25,             # High value
            'gnosticism': 1.2,          # High value
            'sacred_geometry': 1.1,     # Moderate premium
            'astrology': 0.9,           # Common
            'tarot': 0.85,              # Common
            'i_ching': 0.9              # Common
        }
    
    def calculate_dynamic_pricing(self, quest_data: Dict[str, Any], demand_metrics: Dict[str, float]) -> float:
        """Calculate dynamic quest pricing based on demand and rarity"""
        logger.info(f"Calculating dynamic pricing for quest {quest_data.get('quest_id', 'unknown')}")
        
        # Base price
        base_price = self.base_quest_price
        
        # Difficulty multiplier (1-30 scale)
        difficulty = quest_data.get('difficulty_level', 1)
        difficulty_multiplier = 1.0 + (difficulty - 1) * 0.1  # 10% per difficulty level
        
        # Tradition rarity multiplier
        traditions = quest_data.get('tradition_references', ['enochian_magic'])
        tradition_multiplier = 1.0
        for tradition in traditions:
            weight = self.tradition_weights.get(tradition, 1.0)
            tradition_multiplier *= weight
        
        # Normalize tradition multiplier for multiple traditions
        if len(traditions) > 1:
            tradition_multiplier = tradition_multiplier ** (1.0 / len(traditions))
        
        # Demand multiplier
        quest_demand = demand_metrics.get('quest_demand', 1.0)
        governor_popularity = demand_metrics.get('governor_popularity', 1.0)
        demand_multiplier = (quest_demand * governor_popularity) ** 0.5  # Square root to moderate impact
        
        # Supply scarcity multiplier
        quest_scarcity = demand_metrics.get('quest_scarcity', 1.0)
        scarcity_multiplier = 1.0 + (quest_scarcity - 1.0) * 0.5  # 50% of scarcity impact
        
        # Calculate final price
        dynamic_price = (base_price * 
                        difficulty_multiplier * 
                        tradition_multiplier * 
                        demand_multiplier * 
                        scarcity_multiplier)
        
        # Apply bounds
        max_price = base_price * self.max_price_multiplier
        min_price = base_price * self.min_price_multiplier
        dynamic_price = max(min_price, min(max_price, dynamic_price))
        
        logger.info(f"Dynamic price calculated: {dynamic_price:.2f} (base: {base_price}, multipliers: {difficulty_multiplier:.2f}x{tradition_multiplier:.2f}x{demand_multiplier:.2f}x{scarcity_multiplier:.2f})")
        return dynamic_price
    
    def calculate_utility_value(self, token_data: Dict[str, Any]) -> float:
        """Calculate utility-based token valuation"""
        # Base utility from wisdom level
        wisdom_level = token_data.get('wisdom_level', 1)
        base_utility = math.log(wisdom_level + 1) * 50  # Logarithmic scaling
        
        # Evolution stage bonus
        evolution_stages = {'initiate': 1.0, 'apprentice': 1.2, 'adept': 1.5, 'master': 2.0, 'transcendent': 3.0}
        evolution_stage = token_data.get('evolution_stage', 'initiate')
        evolution_bonus = evolution_stages.get(evolution_stage, 1.0)
        
        # Trait diversity bonus
        traits = token_data.get('traits', {})
        trait_count = sum(len(trait_list) if isinstance(trait_list, list) else 1 for trait_list in traits.values())
        diversity_bonus = 1.0 + (trait_count * 0.05)  # 5% per trait
        
        # Authenticity bonus
        authenticity_score = token_data.get('authenticity_score', 0.85)
        authenticity_bonus = authenticity_score * 1.2  # Up to 20% bonus
        
        utility_value = base_utility * evolution_bonus * diversity_bonus * authenticity_bonus
        
        logger.info(f"Utility value calculated: {utility_value:.2f}")
        return utility_value
    
    def balance_market_conditions(self, current_conditions: MarketConditions) -> Dict[str, Any]:
        """Balance market conditions through autonomous mechanisms"""
        logger.info("Balancing market conditions")
        
        balancing_actions = {
            'token_burns': 0,
            'liquidity_injections': 0,
            'price_stabilization': {},
            'supply_adjustments': {},
            'demand_incentives': {}
        }
        
        # Check inflation rate
        if current_conditions.demand_pressure > 1.5:  # High demand
            # Increase supply through quest generation incentives
            balancing_actions['supply_adjustments']['increase_quest_rewards'] = 0.2  # 20% increase
            balancing_actions['demand_incentives']['quest_completion_bonus'] = 0.1   # 10% bonus
        
        elif current_conditions.supply_pressure > 1.5:  # Oversupply
            # Reduce supply through increased burn rates
            balancing_actions['token_burns'] = int(current_conditions.circulating_supply * 0.05)  # 5% burn
            balancing_actions['supply_adjustments']['reduce_quest_generation'] = 0.15  # 15% reduction
        
        # Volatility dampening
        if current_conditions.average_price > 0:
            price_volatility = abs(current_conditions.trading_volume_24h / current_conditions.market_cap)
            if price_volatility > 0.1:  # High volatility
                # Inject liquidity to stabilize
                stabilization_amount = current_conditions.market_cap * 0.02  # 2% of market cap
                balancing_actions['liquidity_injections'] = stabilization_amount
                balancing_actions['price_stabilization']['volatility_reduction'] = self.volatility_dampening
        
        # Market sentiment adjustments
        if current_conditions.market_sentiment == 'bearish':
            # Incentivize holding and usage
            balancing_actions['demand_incentives']['holding_rewards'] = 0.05  # 5% holding rewards
            balancing_actions['demand_incentives']['quest_discounts'] = 0.1   # 10% quest discounts
        
        elif current_conditions.market_sentiment == 'bullish':
            # Moderate speculation
            balancing_actions['supply_adjustments']['speculation_tax'] = 0.02  # 2% speculation tax
        
        logger.info(f"Market balancing actions: {balancing_actions}")
        return balancing_actions
    
    def create_liquidity_pool(self, token_a: str, token_b: str, initial_a: float, initial_b: float) -> LiquidityPool:
        """Create liquidity pool for token trading"""
        pool_id = f"{token_a}_{token_b}_pool"
        logger.info(f"Creating liquidity pool: {pool_id}")
        
        # Calculate initial liquidity
        total_liquidity = math.sqrt(initial_a * initial_b)
        
        pool = LiquidityPool(
            pool_id=pool_id,
            token_a=token_a,
            token_b=token_b,
            reserve_a=initial_a,
            reserve_b=initial_b,
            total_liquidity=total_liquidity,
            fee_rate=0.003,  # 0.3% trading fee
            last_update=datetime.now().isoformat()
        )
        
        self.liquidity_pools[pool_id] = pool
        logger.info(f"Created liquidity pool {pool_id} with {total_liquidity:.2f} total liquidity")
        return pool
    
    def calculate_swap_price(self, pool_id: str, token_in: str, amount_in: float) -> Tuple[float, float]:
        """Calculate swap price using constant product formula"""
        if pool_id not in self.liquidity_pools:
            return 0.0, 0.0
        
        pool = self.liquidity_pools[pool_id]
        
        # Determine which token is being swapped
        if token_in == pool.token_a:
            reserve_in = pool.reserve_a
            reserve_out = pool.reserve_b
        else:
            reserve_in = pool.reserve_b
            reserve_out = pool.reserve_a
        
        # Apply trading fee
        amount_in_with_fee = amount_in * (1 - pool.fee_rate)
        
        # Constant product formula: x * y = k
        amount_out = (reserve_out * amount_in_with_fee) / (reserve_in + amount_in_with_fee)
        
        # Calculate price impact
        price_impact = amount_out / reserve_out
        
        return amount_out, price_impact
    
    def process_economic_event(self, event_type: str, event_data: Dict[str, Any]) -> EconomicEvent:
        """Process economic event and trigger autonomous responses"""
        event_id = f"{event_type}_{datetime.now().isoformat()}"
        logger.info(f"Processing economic event: {event_type}")
        
        auto_response = {}
        impact_magnitude = 0.0
        affected_tokens = []
        
        if event_type == 'quest_completion_surge':
            # High quest completion rate
            completion_rate = event_data.get('completion_rate', 1.0)
            impact_magnitude = completion_rate - 1.0
            
            if impact_magnitude > 0.5:  # 50% above normal
                # Increase quest difficulty and rewards
                auto_response['difficulty_adjustment'] = 0.1  # 10% increase
                auto_response['reward_adjustment'] = 0.15     # 15% increase
                affected_tokens = event_data.get('popular_quests', [])
        
        elif event_type == 'governor_popularity_spike':
            # Specific governor becomes very popular
            governor_name = event_data.get('governor_name', '')
            popularity_increase = event_data.get('popularity_increase', 1.0)
            impact_magnitude = popularity_increase
            
            if impact_magnitude > 2.0:  # 200% increase
                # Increase quest prices for this governor
                auto_response['price_multiplier'] = 1.5
                auto_response['quest_generation_boost'] = 0.2  # 20% more quests
                affected_tokens = [f"{governor_name}_quest_{i}" for i in range(1, 16)]
        
        elif event_type == 'market_crash':
            # General market downturn
            crash_severity = event_data.get('severity', 0.1)
            impact_magnitude = -crash_severity
            
            # Implement protective measures
            auto_response['emergency_liquidity'] = crash_severity * 10000  # Emergency liquidity
            auto_response['trading_halt'] = crash_severity > 0.3           # Halt if >30% crash
            auto_response['burn_reduction'] = 0.5                          # Reduce burn rate
            affected_tokens = ['all']
        
        economic_event = EconomicEvent(
            event_id=event_id,
            event_type=event_type,
            impact_magnitude=impact_magnitude,
            affected_tokens=affected_tokens,
            timestamp=datetime.now().isoformat(),
            auto_response=auto_response
        )
        
        self.economic_events[event_id] = economic_event
        logger.info(f"Processed economic event {event_id} with magnitude {impact_magnitude}")
        return economic_event
    
    def simulate_market_scenario(self, scenario_name: str, duration_days: int = 30) -> Dict[str, Any]:
        """Simulate market scenario for testing"""
        logger.info(f"Simulating market scenario: {scenario_name} for {duration_days} days")
        
        simulation_results = {
            'scenario_name': scenario_name,
            'duration_days': duration_days,
            'daily_metrics': [],
            'final_state': {},
            'autonomous_actions': []
        }
        
        # Initial conditions
        initial_supply = 1000000
        initial_price = 100.0
        current_supply = initial_supply
        current_price = initial_price
        
        for day in range(duration_days):
            # Simulate daily market changes based on scenario
            if scenario_name == 'steady_growth':
                price_change = 0.02  # 2% daily growth
                supply_change = 0.01  # 1% supply increase
            
            elif scenario_name == 'high_volatility':
                import random
                price_change = random.uniform(-0.1, 0.1)  # ±10% daily volatility
                supply_change = random.uniform(-0.02, 0.02)  # ±2% supply change
            
            elif scenario_name == 'bear_market':
                price_change = -0.03  # 3% daily decline
                supply_change = -0.005  # 0.5% supply decrease (burns)
            
            else:  # stable_market
                price_change = 0.001  # 0.1% daily change
                supply_change = 0.002  # 0.2% supply increase
            
            # Apply changes
            current_price *= (1 + price_change)
            current_supply *= (1 + supply_change)
            
            # Create market conditions
            market_conditions = MarketConditions(
                total_supply=int(current_supply),
                circulating_supply=int(current_supply * 0.9),
                burned_tokens=int(initial_supply - current_supply),
                average_price=current_price,
                market_cap=current_price * current_supply,
                trading_volume_24h=current_supply * 0.1,  # 10% daily volume
                demand_pressure=1.0 + price_change,
                supply_pressure=1.0 + supply_change,
                market_sentiment='neutral'
            )
            
            # Apply autonomous balancing
            balancing_actions = self.balance_market_conditions(market_conditions)
            simulation_results['autonomous_actions'].append({
                'day': day,
                'actions': balancing_actions
            })
            
            # Record daily metrics
            simulation_results['daily_metrics'].append({
                'day': day,
                'price': current_price,
                'supply': current_supply,
                'market_cap': market_conditions.market_cap,
                'price_change': price_change,
                'supply_change': supply_change
            })
        
        # Final state
        simulation_results['final_state'] = {
            'final_price': current_price,
            'final_supply': current_supply,
            'total_return': (current_price - initial_price) / initial_price,
            'supply_change': (current_supply - initial_supply) / initial_supply,
            'max_price': max(day['price'] for day in simulation_results['daily_metrics']),
            'min_price': min(day['price'] for day in simulation_results['daily_metrics']),
            'volatility': statistics.stdev([day['price_change'] for day in simulation_results['daily_metrics']])
        }
        
        logger.info(f"Simulation complete: {scenario_name}, final price: {current_price:.2f}, total return: {simulation_results['final_state']['total_return']:.2%}")
        return simulation_results
    
    def get_tokenomics_statistics(self) -> Dict[str, Any]:
        """Get comprehensive tokenomics statistics"""
        return {
            'total_tokens_tracked': len(self.token_metrics),
            'active_liquidity_pools': len(self.liquidity_pools),
            'economic_events_processed': len(self.economic_events),
            'base_quest_price': self.base_quest_price,
            'tradition_weights': self.tradition_weights,
            'economic_parameters': {
                'max_price_multiplier': self.max_price_multiplier,
                'min_price_multiplier': self.min_price_multiplier,
                'burn_rate_failed': self.burn_rate_failed,
                'inflation_target': self.inflation_target,
                'volatility_dampening': self.volatility_dampening
            }
        }
    
    def export_tokenomics_data(self, output_path: str = "onchain/autonomous_tokenomics_data.json"):
        """Export tokenomics data"""
        export_data = {
            'token_metrics': {token_id: asdict(metrics) for token_id, metrics in self.token_metrics.items()},
            'liquidity_pools': {pool_id: asdict(pool) for pool_id, pool in self.liquidity_pools.items()},
            'economic_events': {event_id: asdict(event) for event_id, event in self.economic_events.items()},
            'statistics': self.get_tokenomics_statistics(),
            'export_timestamp': datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported tokenomics data to {output_path}")

def main():
    """Test autonomous tokenomics system"""
    logger.info("Testing Autonomous Tokenomics System")
    
    # Create tokenomics system
    tokenomics = AutonomousTokenomics()
    
    # Test dynamic pricing
    test_quest = {
        'quest_id': 'ABRIOND_001',
        'difficulty_level': 15,
        'tradition_references': ['enochian_magic', 'hermetic_qabalah', 'chaos_magic'],
        'authenticity_score': 0.95
    }
    
    demand_metrics = {
        'quest_demand': 1.5,
        'governor_popularity': 2.0,
        'quest_scarcity': 1.3
    }
    
    dynamic_price = tokenomics.calculate_dynamic_pricing(test_quest, demand_metrics)
    
    # Test utility valuation
    token_data = {
        'wisdom_level': 10,
        'evolution_stage': 'adept',
        'traits': {'wisdom': ['analytical', 'strategic'], 'virtue': ['prudence']},
        'authenticity_score': 0.95
    }
    
    utility_value = tokenomics.calculate_utility_value(token_data)
    
    # Test liquidity pool
    pool = tokenomics.create_liquidity_pool('ENOCH', 'BTC', 10000, 1.0)
    swap_amount, price_impact = tokenomics.calculate_swap_price(pool.pool_id, 'ENOCH', 100)
    
    # Test economic event
    event_data = {'completion_rate': 1.8, 'popular_quests': ['ABRIOND_001', 'ABRIOND_002']}
    economic_event = tokenomics.process_economic_event('quest_completion_surge', event_data)
    
    # Test market simulation
    simulation = tokenomics.simulate_market_scenario('steady_growth', 30)
    
    # Display results
    stats = tokenomics.get_tokenomics_statistics()
    logger.info(f"\n=== AUTONOMOUS TOKENOMICS TEST RESULTS ===")
    logger.info(f"Dynamic Price: {dynamic_price:.2f} tokens")
    logger.info(f"Utility Value: {utility_value:.2f}")
    logger.info(f"Liquidity Pool: {pool.total_liquidity:.2f} total liquidity")
    logger.info(f"Swap Result: {swap_amount:.4f} output, {price_impact:.2%} impact")
    logger.info(f"Economic Event: {economic_event.event_type} with {economic_event.impact_magnitude:.2f} magnitude")
    logger.info(f"Simulation Final Return: {simulation['final_state']['total_return']:.2%}")
    logger.info(f"Statistics: {stats}")
    
    # Export data
    tokenomics.export_tokenomics_data()
    
    return tokenomics

if __name__ == "__main__":
    main()
