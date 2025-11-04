from src.agents.base_agent import BaseAgent

class GreedyAgent(BaseAgent):
    def __init__(self):
        super().__init__("GreedyAgent")

    def choose_move(self, playable_goals, future_goals, bag_size, log_func):
        log_func("GreedyAgent analysis: Looking for the best *fully playable word*.")
        if playable_goals:
            return max(playable_goals, key=lambda g: g['score'])
        return None
