import random
import uuid
import copy
import json
from utils import grid_to_str, grid_to_html

COMMON_WORDS_FN = './data/common-words.txt'
VALID_WORDS_FN = './data/valid-words.txt'

def load_words():
    with open(VALID_WORDS_FN, 'r') as f:
        valid_words = f.read().splitlines()
    with open(COMMON_WORDS_FN, 'r') as f:
        common_words = f.read().splitlines()
    return {
        'valid':  [e.lower().strip()  for e in valid_words],
        'common': [e.lower().strip()  for e in common_words],
    }

class WordleGame:

    def __init__(self,
        word: str = None,         
        word_type: str = 'common',
        ) -> None:
        self.words = load_words()
        if word is not None:
            self.word = word.lower()
        else:
            self.word = random.choice(self.words[word_type])
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
            "grid": None if err else self.grid_state,
            "grid_formatted": grid_str,
            "grid_html": grid_html,
        }
        return info
        
    @staticmethod
    def check_win(result_states):
        return all([state == 'correct' for state in result_states])


def main():
    
    game = WordleGame(word="sails")
    print(game.word)

    info = game.play_round('about')
    state = game.grid_state
    # print(grid_to_str(state, formatted=True))
    
    info = game.play_round('other')
    state = game.grid_state
    # print(grid_to_str(state, formatted=True))
    # print(json.dumps(state, indent=2))
    # print(json.dumps(info, indent=2))
    print(info["grid_html"])

if __name__ == '__main__':
    main()