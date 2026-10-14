import random
import time


class Agent:
    ident = 0

    def __init__(self):
        self.id = Agent.ident
        Agent.ident += 1

    def get_chosen_action(self, state, max_depth):
        pass


class RandomAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        return actions[random.randint(0, len(actions) - 1)]


class GreedyAgent(Agent):
    def get_chosen_action(self, state, max_depth):
        time.sleep(0.5)
        actions = state.get_legal_actions()
        best_score, best_action = None, None
        for action in actions:
            new_state = state.generate_successor_state(action)
            score = new_state.get_score(state.get_on_move_chr())
            if (best_score is None and best_action is None) or score > best_score:
                best_action = action
                best_score = score
        return best_action


class MaxNAgent(Agent):
    def get_chosen_action(self, state, max_depth):

        def get_scores(s):
            return tuple(s.get_score(chr(ord('A') + i)) for i in range(s.get_num_of_players()))

        def recurse(s, depth):
            if depth == 0 or s.is_goal_state():
                return get_scores(s)

            moves = s.get_legal_actions()
            if not moves:
                return get_scores(s)

            current = s.get_on_move_ord()
            best = None
            for mv in moves:
                child = s.generate_successor_state(mv)
                result = recurse(child, depth - 1)
                if best is None or result[current] > best[current]:
                    best = result
            return best

        moves = state.get_legal_actions()
        if not moves:
            return None

        me = state.get_on_move_ord()
        chosen = None
        best_score = None
        for mv in moves:
            child = state.generate_successor_state(mv)
            score_tuple = recurse(child, max_depth - 1)
            if best_score is None or score_tuple[me] > best_score:
                best_score = score_tuple[me]
                chosen = mv

        return chosen


class MinimaxAgent(Agent):
    def get_chosen_action(self, state, max_depth):

        if state.get_num_of_players() != 2:
            raise ValueError("Minimax radi samo sa 2 igraca")

        me = state.get_on_move_ord()

        def diff_score(s):
            return s.get_score(chr(ord('A') + me)) - s.get_score(chr(ord('A') + (1 - me)))

        def minimax_search(s, depth, is_max):
            if depth == 0 or s.is_goal_state():
                return diff_score(s)

            actions = s.get_legal_actions()
            if not actions:
                return diff_score(s)

            if is_max:
                best_val = -float('inf')
                for mv in actions:
                    val = minimax_search(s.generate_successor_state(mv), depth - 1, False)
                    best_val = max(best_val, val)
                return best_val
            else:
                worst_val = float('inf')
                for mv in actions:
                    val = minimax_search(s.generate_successor_state(mv), depth - 1, True)
                    worst_val = min(worst_val, val)
                return worst_val

        best_move = None
        best_value = -float('inf')
        for act in state.get_legal_actions():
            val = minimax_search(state.generate_successor_state(act), max_depth - 1, False)
            if val > best_value:
                best_value = val
                best_move = act

        return best_move


class MinimaxABAgent(Agent):
    def get_chosen_action(self, state, max_depth):

        if state.get_num_of_players() != 2:
            raise ValueError("MinimaxAB radi samo sa 2 igraca")

        me = state.get_on_move_ord()

        def score_diff(s):
            return s.get_score(chr(ord('A') + me)) - s.get_score(chr(ord('A') + (1 - me)))

        def alphabeta(s, depth, alpha, beta, maximizing):
            if depth == 0 or s.is_goal_state():
                return score_diff(s)

            actions = s.get_legal_actions()
            if not actions:
                return score_diff(s)

            if maximizing:
                value = alpha
                for mv in actions:
                    value = max(value, alphabeta(s.generate_successor_state(mv), depth - 1, value, beta, False))
                    if value >= beta:
                        break
                return value
            else:
                value = beta
                for mv in actions:
                    value = min(value, alphabeta(s.generate_successor_state(mv), depth - 1, alpha, value, True))
                    if value <= alpha:
                        break
                return value

        best_action = None
        best_score = -float('inf')
        for act in state.get_legal_actions():
            val = alphabeta(state.generate_successor_state(act), max_depth - 1, -float('inf'), float('inf'), False)
            if val > best_score:
                best_score = val
                best_action = act

        return best_action
