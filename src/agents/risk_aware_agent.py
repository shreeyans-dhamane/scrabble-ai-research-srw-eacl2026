from src.agents.base_agent import BaseAgent

class RiskAwareAgent(BaseAgent):
    def __init__(self, lambda_risk_tolerance=1.8):
        super().__init__("RiskAwareAgent")
        self.lambda_risk_tolerance = lambda_risk_tolerance

    def choose_move(self, playable_goals, future_goals, bag_size, log_func):
        best_playable_goal = None
        best_playable_score = -1
        if playable_goals:
            best_playable_goal = max(playable_goals, key=lambda g: g['score'])
            best_playable_score = best_playable_goal['score']

        best_future_goal = None
        best_future_expected_score = -1
        if future_goals:
            best_future_goal = max(future_goals, key=lambda g: g['expected_score'])
            best_future_expected_score = best_future_goal['expected_score']

        log_func("--- RiskAwareAgent Analysis ---")
        log_func(f"Best Playable Word: '{best_playable_goal['word'] if best_playable_goal else 'None'}', Guaranteed Score: {best_playable_score}")
        log_func(f"Best Future Goal: '{best_future_goal['word'] if best_future_goal else 'None'}', Expected Score: {best_future_expected_score:.2f}")

        if (best_future_expected_score > (best_playable_score * self.lambda_risk_tolerance)) and best_future_goal is not None:
            log_func(f"AI: The future goal's potential ({best_future_expected_score:.2f}) is > {self.lambda_risk_tolerance}x the guaranteed play ({best_playable_score}). GAMBLE!")
            return best_future_goal
        else:
            log_func("AI: The guaranteed word is better (or equal) to a gamble.")
            return best_playable_goal
