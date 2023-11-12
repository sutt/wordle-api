import random
import uuid
import copy
from utils import grid_to_str, grid_to_html
from words import WORDS


class WordleGame:

    def __init__(self) -> None:
        self.word = random.choice(WORDS).lower()
        self.current_row = 0
        self.grid_state = [
            [('empty', '') for _ in range(5)]
            for _ in range(6)
        ]
        self.b_win = False
        self.uuid = str(uuid.uuid4())

    def check_input(self, word):
        word = word.lower()
        result = []
        for i, letter in enumerate(word):
            if letter == self.word[i]:
                result.append('correct')
            elif letter in self.word:
                result.append('present')
            else:
                result.append('absent')
        return result
    
    def play_round(self, word):
        err = None
        try:
            result_states = self.check_input(word)
            self.b_win = self.check_win(result_states)
            results_tuple = [
                (state, letter) 
                for state, letter in zip(result_states, list(word))
            ]
            self.grid_state[self.current_row] = results_tuple
            self.current_row += 1
            grid_str = grid_to_str(self.grid_state, formatted=True)
            grid_html = grid_to_html(self.grid_state)
        except Exception as e:
            err = str(e)
        info = {
            "word": word,
            "current_row": self.current_row - 1,
            "error": True if err else False,
            "error_text": err if err else None,
            "win": self.b_win,
            "results": None if err else result_states,
            "grid_formatted": grid_str,
            "grid_html": grid_html,
        }
        return info
        
    @staticmethod
    def check_win(result_states):
        return all([state == 'correct' for state in result_states])


def main():
    
    game = WordleGame()
    print(game.word)

    game.play_round('about')
    state = game.grid_state
    print(grid_to_str(state, formatted=True))
    
    game.play_round('other')
    state = game.grid_state
    print(grid_to_str(state, formatted=True))

if __name__ == '__main__':
    main()