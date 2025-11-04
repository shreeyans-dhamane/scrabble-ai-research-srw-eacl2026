class BaseAgent:
    def __init__(self, name="Agent"):
        self.name = name

    def choose_move(self, playable_goals, future_goals, bag_size, log_func):
        if playable_goals:
            return max(playable_goals, key=lambda g: g['score'])
        return None
