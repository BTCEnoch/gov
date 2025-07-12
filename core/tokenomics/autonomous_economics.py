#!/usr/bin/env python3
"""
Enochian Cyphers: Autonomous Tokenomics System
Per expert guidance: Implement algorithmic supply-demand models with automatic burns, 
AMM-based trading, and anti-manipulation mechanisms.

Implements Rule 5: Autonomous Economics - self-regulating supply, dynamic pricing, liquidity pools.
"""

import json
import math
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import numpy as np

@dataclass
class LiquidityPool:
    """AMM-based liquidity pool for hypertoken trading"""
    token_a: str
    token_b: str
    reserve_a: float
    reserve_b: float
    total_liquidity: float
    fee_rate: float = 0.003  # 0.3% trading fee
    k_constant: float = 0.0  # Constant product (reserve_a * reserve_b)
    
    def __post_init__(self):
        self.k_constant = self.reserve_a * self.reserve_b

@dataclass
class MarketData:
    """Market data for autonomous price discovery"""
    token_id: str
    current_price: float
    volume_24h: float
    price_change_24h: float
    market_cap: float
    circulating_supply: float
    demand_pressure: float  # 0.0 to 1.0
    supply_pressure: float  # 0.0 to 1.0
    volatility_index: float
    last_updated: int

@dataclass
class SupplyAdjustment:
    """Supply adjustment event for anti-inflation"""
    timestamp: int
    adjustment_type: str  # mint, burn, stake_reward
    amount: float
    reason: str
    market_conditions: Dict[str, float]
    new_total_supply: float

class AutonomousEconomics:
    """
    Autonomous tokenomics system for Enochian Cyphers
    Self-regulating markets with anti-inflation and manipulation prevention
    """
    
    def __init__(self):
        self.liquidity_pools = {}
        self.market_data = {}
        self.supply_adjustments = []
        self.trading_history = []
        
        # Economic parameters (per expert guidance)
        self.inflation_threshold = 0.05  # 5% inflation trigger
        self.deflation_threshold = -0.02  # 2% deflation trigger
        self.max_daily_supply_change = 0.01  # 1% max daily supply change
        self.volatility_dampening = 0.8  # Volatility reduction factor
        self.manipulation_detection_threshold = 0.15  # 15% unusual activity
        
        # Initialize base economic state
        self._initialize_economic_parameters()
    
    def _initialize_economic_parameters(self):
        """Initialize base economic parameters"""
        self.base_token_supply = 21000000  # Bitcoin-inspired base supply
        self.staking_apy_base = 0.05  # 5% base staking APY
        self.burn_rate_base = 0.001  # 0.1% base burn rate
        self.liquidity_incentive_rate = 0.02  # 2% liquidity provider rewards
    
    def create_liquidity_pool(self, token_a: str, token_b: str, 
                            initial_a: float, initial_b: float) -> LiquidityPool:
        """
        Create AMM liquidity pool (per expert guidance: prefer AMM over order books)
        """
        pool_id = f"{token_a}_{token_b}"
        
        pool = LiquidityPool(
            token_a=token_a,
            token_b=token_b,
            reserve_a=initial_a,
            reserve_b=initial_b,
            total_liquidity=math.sqrt(initial_a * initial_b)  # Geometric mean
        )
        
        self.liquidity_pools[pool_id] = pool
        
        print(f"💧 Created liquidity pool: {pool_id}")
        print(f"   Initial reserves: {initial_a} {token_a}, {initial_b} {token_b}")
        print(f"   K constant: {pool.k_constant:.2f}")
        
        return pool
    
    def execute_amm_trade(self, pool_id: str, input_token: str, 
                         input_amount: float) -> Tuple[float, float]:
        """
        Execute AMM trade with constant product formula
        Includes manipulation prevention mechanisms
        """
        if pool_id not in self.liquidity_pools:
            raise ValueError(f"Pool {pool_id} not found")
        
        pool = self.liquidity_pools[pool_id]
        
        # Determine input/output tokens
        if input_token == pool.token_a:
            input_reserve = pool.reserve_a
            output_reserve = pool.reserve_b
            output_token = pool.token_b
        elif input_token == pool.token_b:
            input_reserve = pool.reserve_b
            output_reserve = pool.reserve_a
            output_token = pool.token_a
        else:
            raise ValueError(f"Token {input_token} not in pool")
        
        # Check for manipulation attempt
        if self._detect_manipulation(pool_id, input_amount, input_reserve):
            raise ValueError("Potential manipulation detected - trade rejected")
        
        # Calculate output amount with fees (constant product formula)
        input_with_fee = input_amount * (1 - pool.fee_rate)
        output_amount = (output_reserve * input_with_fee) / (input_reserve + input_with_fee)
        
        # Apply volatility dampening
        if self._is_high_volatility_trade(pool_id, output_amount, output_reserve):
            dampening_factor = self.volatility_dampening
            output_amount *= dampening_factor
            print(f"⚠️ Volatility dampening applied: {dampening_factor}")
        
        # Update pool reserves
        if input_token == pool.token_a:
            pool.reserve_a += input_amount
            pool.reserve_b -= output_amount
        else:
            pool.reserve_b += input_amount
            pool.reserve_a -= output_amount
        
        # Update K constant
        pool.k_constant = pool.reserve_a * pool.reserve_b
        
        # Record trade
        trade_record = {
            "timestamp": int(time.time()),
            "pool_id": pool_id,
            "input_token": input_token,
            "input_amount": input_amount,
            "output_token": output_token,
            "output_amount": output_amount,
            "price": output_amount / input_amount if input_amount > 0 else 0
        }
        self.trading_history.append(trade_record)
        
        return output_amount, trade_record["price"]
    
    def balance_supply(self, token_id: str, market_conditions: Dict[str, float]) -> SupplyAdjustment:
        """
        Autonomous supply balancing (per expert guidance: algorithmic supply control)
        """
        current_supply = market_conditions.get("circulating_supply", self.base_token_supply)
        demand_pressure = market_conditions.get("demand_pressure", 0.5)
        supply_pressure = market_conditions.get("supply_pressure", 0.5)
        inflation_rate = market_conditions.get("inflation_rate", 0.0)
        
        # Determine adjustment needed
        adjustment_amount = 0.0
        adjustment_type = "none"
        reason = "No adjustment needed"
        
        # Anti-inflation mechanism
        if inflation_rate > self.inflation_threshold:
            # Burn tokens to reduce supply
            burn_rate = min(self.max_daily_supply_change, inflation_rate * 0.5)
            adjustment_amount = -current_supply * burn_rate
            adjustment_type = "burn"
            reason = f"Anti-inflation burn: {inflation_rate:.3f} > {self.inflation_threshold}"
        
        # Anti-deflation mechanism
        elif inflation_rate < self.deflation_threshold:
            # Mint tokens for staking rewards
            mint_rate = min(self.max_daily_supply_change, abs(inflation_rate) * 0.3)
            adjustment_amount = current_supply * mint_rate
            adjustment_type = "stake_reward"
            reason = f"Anti-deflation mint: {inflation_rate:.3f} < {self.deflation_threshold}"
        
        # Demand-based adjustment
        elif demand_pressure > 0.8 and supply_pressure < 0.3:
            # High demand, low supply - mint small amount
            adjustment_amount = current_supply * 0.005  # 0.5% increase
            adjustment_type = "mint"
            reason = "High demand pressure adjustment"
        
        elif supply_pressure > 0.8 and demand_pressure < 0.3:
            # High supply, low demand - burn small amount
            adjustment_amount = -current_supply * 0.003  # 0.3% decrease
            adjustment_type = "burn"
            reason = "High supply pressure adjustment"
        
        # Create adjustment record
        adjustment = SupplyAdjustment(
            timestamp=int(time.time()),
            adjustment_type=adjustment_type,
            amount=adjustment_amount,
            reason=reason,
            market_conditions=market_conditions.copy(),
            new_total_supply=current_supply + adjustment_amount
        )
        
        self.supply_adjustments.append(adjustment)
        
        if adjustment_amount != 0:
            print(f"⚖️ Supply adjustment: {adjustment_type}")
            print(f"   Amount: {adjustment_amount:+.2f} tokens")
            print(f"   Reason: {reason}")
            print(f"   New supply: {adjustment.new_total_supply:.2f}")
        
        return adjustment
    
    def provide_liquidity_incentives(self, pool_id: str, provider_address: str, 
                                   liquidity_amount: float) -> float:
        """
        Calculate and provide liquidity incentives
        """
        if pool_id not in self.liquidity_pools:
            return 0.0
        
        pool = self.liquidity_pools[pool_id]
        
        # Calculate provider's share of pool
        provider_share = liquidity_amount / pool.total_liquidity
        
        # Calculate rewards based on trading volume and time
        base_reward = liquidity_amount * self.liquidity_incentive_rate
        volume_bonus = self._calculate_volume_bonus(pool_id)
        time_bonus = self._calculate_time_bonus(provider_address)
        
        total_reward = base_reward * (1 + volume_bonus + time_bonus)
        
        print(f"💰 Liquidity rewards for {provider_address}:")
        print(f"   Base reward: {base_reward:.4f}")
        print(f"   Volume bonus: {volume_bonus:.2%}")
        print(f"   Time bonus: {time_bonus:.2%}")
        print(f"   Total reward: {total_reward:.4f}")
        
        return total_reward
    
    def _detect_manipulation(self, pool_id: str, trade_amount: float, 
                           reserve_amount: float) -> bool:
        """
        Detect potential market manipulation attempts
        """
        # Check if trade is unusually large relative to pool
        trade_ratio = trade_amount / reserve_amount
        if trade_ratio > self.manipulation_detection_threshold:
            return True
        
        # Check for rapid successive trades (flash loan attacks)
        recent_trades = [t for t in self.trading_history 
                        if t["pool_id"] == pool_id and 
                        t["timestamp"] > time.time() - 60]  # Last minute
        
        if len(recent_trades) > 10:  # More than 10 trades per minute
            total_volume = sum(t["input_amount"] for t in recent_trades)
            if total_volume > reserve_amount * 0.5:  # 50% of reserve in 1 minute
                return True
        
        return False
    
    def _is_high_volatility_trade(self, pool_id: str, output_amount: float, 
                                output_reserve: float) -> bool:
        """
        Check if trade would cause high volatility
        """
        price_impact = output_amount / output_reserve
        return price_impact > 0.05  # 5% price impact threshold
    
    def _calculate_volume_bonus(self, pool_id: str) -> float:
        """
        Calculate volume-based bonus for liquidity providers
        """
        recent_trades = [t for t in self.trading_history 
                        if t["pool_id"] == pool_id and 
                        t["timestamp"] > time.time() - 86400]  # Last 24 hours
        
        total_volume = sum(t["input_amount"] for t in recent_trades)
        
        # Bonus scales with volume (max 50% bonus)
        volume_bonus = min(0.5, total_volume / 1000000)  # 1M volume = 50% bonus
        return volume_bonus
    
    def _calculate_time_bonus(self, provider_address: str) -> float:
        """
        Calculate time-based bonus for long-term liquidity providers
        """
        # Simplified time bonus calculation
        # In full implementation, would track provider history
        return 0.1  # 10% bonus for demonstration
    
    def get_market_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive market summary
        """
        summary = {
            "total_pools": len(self.liquidity_pools),
            "total_trades": len(self.trading_history),
            "total_supply_adjustments": len(self.supply_adjustments),
            "pools": {},
            "recent_adjustments": self.supply_adjustments[-5:] if self.supply_adjustments else []
        }
        
        # Pool summaries
        for pool_id, pool in self.liquidity_pools.items():
            recent_trades = [t for t in self.trading_history 
                           if t["pool_id"] == pool_id and 
                           t["timestamp"] > time.time() - 86400]
            
            volume_24h = sum(t["input_amount"] for t in recent_trades)
            
            summary["pools"][pool_id] = {
                "reserves": {pool.token_a: pool.reserve_a, pool.token_b: pool.reserve_b},
                "total_liquidity": pool.total_liquidity,
                "volume_24h": volume_24h,
                "trade_count_24h": len(recent_trades),
                "k_constant": pool.k_constant
            }
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    # Initialize autonomous economics system
    economics = AutonomousEconomics()
    
    print("🏛️ Enochian Cyphers Autonomous Economics System")
    print("=" * 50)
    
    # Create liquidity pools
    print("\n💧 Creating liquidity pools...")
    btc_gov_pool = economics.create_liquidity_pool("BTC", "GOVABR", 10.0, 1000000.0)
    gov_usdt_pool = economics.create_liquidity_pool("GOVABR", "USDT", 500000.0, 50000.0)
    
    # Execute some trades
    print("\n💱 Executing AMM trades...")
    try:
        output, price = economics.execute_amm_trade("BTC_GOVABR", "BTC", 0.5)
        print(f"Trade: 0.5 BTC → {output:.2f} GOVABR (price: {price:.2f})")
        
        output, price = economics.execute_amm_trade("GOVABR_USDT", "GOVABR", 10000.0)
        print(f"Trade: 10000 GOVABR → {output:.2f} USDT (price: {price:.4f})")
    except ValueError as e:
        print(f"Trade rejected: {e}")
    
    # Test supply balancing
    print("\n⚖️ Testing autonomous supply balancing...")
    market_conditions = {
        "circulating_supply": 15000000,
        "demand_pressure": 0.9,
        "supply_pressure": 0.2,
        "inflation_rate": 0.08  # 8% inflation - should trigger burn
    }
    
    adjustment = economics.balance_supply("GOVABR", market_conditions)
    
    # Test liquidity incentives
    print("\n💰 Testing liquidity incentives...")
    reward = economics.provide_liquidity_incentives("BTC_GOVABR", "user123", 50000.0)
    
    # Get market summary
    print("\n📊 Market Summary:")
    summary = economics.get_market_summary()
    print(json.dumps(summary, indent=2, default=str))
    
    print("\n🎉 Autonomous Economics Demo Complete!")
    print("✅ Anti-inflation mechanisms active")
    print("✅ AMM trading with manipulation prevention")
    print("✅ Liquidity incentives calculated")
    print("✅ Self-regulating supply adjustments")
