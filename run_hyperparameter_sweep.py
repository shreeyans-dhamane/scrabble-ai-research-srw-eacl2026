import numpy as np
import pandas as pd
from multiprocessing import Pool, cpu_count
import time
import os
from tqdm import tqdm

from src.game_state import TileGuesserGame
from src.agents.risk_aware_agent import RiskAwareAgent
from src.agents.greedy_agent import GreedyAgent
from src.utils.dictionary_loader import load_dictionary
from src.constants import TILE_BAG_TEMPLATE, LETTER_SCORES, RACK_SIZE

LAMBDA_VALUES = np.linspace(0.5, 5.0, 10)
GAMES_PER_LAMBDA = 500
DICTIONARY_PATH = 'data/sowpods.txt'
RESULTS_DIR = 'results'
RESULTS_FILE = os.path.join(RESULTS_DIR, 'hyperparameter_sweep_results.csv')

def run_simulation(args):
    lambda_val, num_games, dictionary = args
    wins = 0
    ties = 0
    
    for _ in range(num_games):
        player1 = RiskAwareAgent(lambda_risk_tolerance=lambda_val)
        player2 = GreedyAgent()
        
        game = TileGuesserGame(
            player1=player1,
            player2=player2,
            dictionary=dictionary,
            tile_bag_template=TILE_BAG_TEMPLATE,
            letter_scores=LETTER_SCORES,
            rack_size=RACK_SIZE,
            silent=True
        )
        
        winner_name = game.run_game()
        
        if winner_name == player1.name:
            wins += 1
        elif winner_name == "TIE":
            ties += 1
            
    win_rate = wins / num_games
    return lambda_val, win_rate, wins, ties, num_games

if __name__ == "__main__":
    if not os.path.exists(DICTIONARY_PATH):
        print(f"Error: Dictionary file not found at {DICTIONARY_PATH}")
        exit()
        
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created directory: {RESULTS_DIR}")

    print("Loading dictionary...")
    valid_dictionary = load_dictionary(DICTIONARY_PATH)
    
    num_cores = cpu_count()
    print(f"Starting hyperparameter sweep on {num_cores} cores.")
    print(f"Lambda values: {LAMBDA_VALUES}")
    print(f"Games per lambda: {GAMES_PER_LAMBDA}")
    
    tasks = [(val, GAMES_PER_LAMBDA, valid_dictionary) for val in LAMBDA_VALUES]
    
    results = []
    
    start_time = time.time()
    
    with Pool(processes=num_cores) as pool:
        for result in tqdm(pool.imap_unordered(run_simulation, tasks), total=len(tasks)):
            results.append(result)
            
    end_time = time.time()
    
    print(f"\nSweep finished in {end_time - start_time:.2f} seconds.")
    
    results.sort()
    
    df = pd.DataFrame(results, columns=['lambda', 'win_rate', 'wins', 'ties', 'total_games'])
    df.to_csv(RESULTS_FILE, index=False)
    
    print("\nResults:")
    print(df)
    print(f"\nResults saved to {RESULTS_FILE}")
