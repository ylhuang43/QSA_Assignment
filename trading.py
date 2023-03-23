import json
import random
from typing import Dict, List
import logging

# Broker class definition
class Broker:
    def __init__(self, initial_positions, initial_aum: float):
        self.positions = initial_positions
        self.aum = initial_aum

    def get_live_price(self) -> Dict[str, float]:
        # Generate random prices for each asset in the position's universe
        prices = {asset: random.uniform(10, 30) for asset in self.positions.get_universe()}
        return prices

    def get_positions(self):
        return self.positions
    
    def execute_trades(self, excecution_positions) -> None:
        pass

# Positions class definition
class Positions:
    def __init__(self, positions: Dict[str, float]):
        self.pos = positions

    def get_universe(self) -> List[str]:
        return list(self.pos.keys())

# RebalancingSystem class definition
class RebalancingSystem:
    def __init__(self, broker: Broker):
        self.broker = broker
        logging.basicConfig(level=logging.INFO)

    def generate_trades(self, target_allocation: Dict[str, float]) -> Dict[str, int]:
        # Update the Broker's positions to include all assets from the target allocation
        for asset in target_allocation.keys():
            if asset not in self.broker.positions.pos:
                self.broker.positions.pos[asset] = 0

        # Get the live prices of the assets
        prices = self.broker.get_live_price()
        # Get the current positions of the assets
        current_positions = self.broker.get_positions().pos
        # Initialize an empty dictionary to store the trades
        trades = {}

        # Iterate over each asset and target allocation percentage
        # I have coded it this way so that it can handle situations where there is a stock in current position but not in the target
        for asset, current_unit in current_positions.items():
            # Calculate the current value of the asset
            current_value = current_unit * prices[asset]
            # Calculate the target value of the asset
            target_value = self.broker.aum * target_allocation.get(asset, 0)
            # Calculate the value difference to reach the target allocation
            trade_value = target_value - current_value
            # Calculate the number of units needed to be traded to reach the target allocation
            trade_units = trade_value / prices[asset]

            # Store the trade units in the trades dictionary
            trades[asset] = trade_units
            # Log the generated trade
            logging.info(f"Generated trade for {asset}: {trade_units} units")

        return trades

# Main function to run the rebalancing system
def main():
    # Initialize the initial positions and broker (AUM assumed to be 1,000,000)
    initial_positions = Positions({})
    broker = Broker(initial_positions, 1000000)
    rebalancing_system = RebalancingSystem(broker)

    # Read the target allocation from the input.json file
    with open("targetWeights_20230321.json", "r") as input_file:
        target_allocation = json.load(input_file)

    # Generate the trades to reach the target allocation
    trades = rebalancing_system.generate_trades(target_allocation)

    # Save the generated trades to the output.json file
    with open("executedTrades_20230321.json", "w") as output_file:
        json.dump(trades, output_file, indent=4)

if __name__ == "__main__":
    main()
