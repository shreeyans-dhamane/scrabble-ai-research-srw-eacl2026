import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_FILE = 'results/hyperparameter_sweep_results.csv'
PLOT_FILE = 'results/risk_tolerance_vs_win_rate.png'

def plot_results():
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: Results file not found at {RESULTS_FILE}")
        print("Please run 'run_hyperparameter_sweep.py' first.")
        return

    df = pd.read_csv(RESULTS_FILE)
    
    df = df.sort_values(by='lambda')
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['lambda'], df['win_rate'] * 100, marker='o', linestyle='-')
    
    optimal_lambda = df.loc[df['win_rate'].idxmax()]
    plt.axvline(x=optimal_lambda['lambda'], color='r', linestyle='--', 
                label=f"Optimal $\lambda$ = {optimal_lambda['lambda']:.2f} (Win Rate: {optimal_lambda['win_rate']*100:.1f}%)")
    
    plt.title('Risk-Aware Agent Win Rate vs. Risk-Tolerance ($\lambda$)')
    plt.xlabel('Risk-Tolerance Hyperparameter ($\lambda$)')
    plt.ylabel('Win Rate vs. Greedy Agent (%)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.ylim(min(45, df['win_rate'].min() * 100 - 5), max(65, df['win_rate'].max() * 100 + 5))
    
    plt.savefig(PLOT_FILE)
    print(f"Plot saved to {PLOT_FILE}")

if __name__ == "__main__":
    plot_results()
