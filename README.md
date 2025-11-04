# scrabble-ai-research-srw-eacl2026
Supplementary materials for the paper "Optimizing Heuristic Decision-Making in a Stochastic Tile-Based Game Using a Tuned Risk-Tolerance Hyperparameter." Includes simulations, derivations, and algorithm implementation.

This project presents a novel approach to optimizing decision-making in stochastic, incomplete-information, tile-based word games. We formalize the game as a Markov Decision Process (MDP) and propose a heuristic-driven AI agent, the RiskAwareAgent. This agent evaluates all possible moves by calculating their true score and all potential future moves by their expected value. The probability of achieving a future move is derived from the multivariate hypergeometric distribution, which models the "sampling without replacement" nature of drawing tiles.

The agent's decision to play or gamble is governed by a tunable hyperparameter, $\lambda$ (risk-tolerance). We compare this agent against a baseline GreedyAgent that always selects the highest-scoring immediate move. This repository provides the simulation environment and experimentation scripts to replicate the paper's findings, demonstrating that an optimally tuned agent achieves a superior win rate over the greedy baseline.

Project Structure

scrabble-ai-research-srw-eacl2026/
├── data/
│   └── sowpods.txt         
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py   
│   │   ├── greedy_agent.py 
│   │   └── risk_aware_agent.py 
│   ├── utils/
│   │   ├── __init__.py
│   │   └── dictionary_loader.py 
│   ├── __init__.py
│   ├── constants.py        
│   ├── game_state.py       
│   └── move_evaluator.py   
├── analysis/
│   └── plot_results.py     
├── .gitignore
├── requirements.txt        
└── run_hyperparameter_sweep.py


Installation

Clone the repository:

git clone [https://github.com/your-username/scrabble-ai-research-eacl2026.git](https://github.com/your-username/scrabble-ai-research-eacl2026.git)
cd scrabble-ai-research-eacl2026


Create and activate a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate


Install the required dependencies:

pip install -r requirements.txt


Create the results directory:

mkdir results


Running the Experiment

To run the full hyperparameter sweep as described in the paper, execute the main script:

python run_hyperparameter_sweep.py


This script will iterate through a range of $\lambda$ (risk-tolerance) values. For each value, it will run a specified number of games in parallel, pitting the RiskAwareAgent against the GreedyAgent.

The results will be saved to results/hyperparameter_sweep_results.csv.

Visualizing Results

Once the sweep is complete, you can generate a plot of the results:

python analysis/plot_results.py


This will read the results/hyperparameter_sweep_results.csv file and generate a plot named results/risk_tolerance_vs_win_rate.png.
