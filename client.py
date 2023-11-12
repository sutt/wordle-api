import time
import requests

# Main Client Functions

def mini_new_game(base_url='http://localhost:5000'):
    r = requests.post(f'{base_url}/new_game')
    data = r.json()
    return data.get('id', None)

def mini_play_word(word, game_id, base_url='http://localhost:5000'):
    data = {'word': word, 'id': game_id}
    r = requests.post(f'{base_url}/play_word', json=data)
    return r.json()

def nyt_new_game(base_url='http://localhost:5000'):
    r = requests.post(f'{base_url}/nyt/new_game')
    data = r.json()
    return data.get('id', None)

def nyt_play_word(word, game_id, base_url='http://localhost:5000'):
    data = {'word': word, 'id': game_id}
    r = requests.post(f'{base_url}/nyt/play_word', json=data)
    return r.json()


# Compound Action Demo Functions

def play_two_mini_games():

    game_id = mini_new_game()
    print(game_id)

    game_id_2 = mini_new_game()
    print(game_id_2)

    base_url = 'http://localhost:5000'
    r = requests.get(f'{base_url}/get_games')
    print(r.json())
    
    info = mini_play_word('about', game_id)
    print(info.get('info', {}).get('grid_formatted', None))
    print(info.get('info', {}).get('grid_html', None))
    
    info = mini_play_word('sales', game_id)
    print(info.get('info', {}).get('grid_formatted', None))
    print(info.get('info', {}).get('grid_html', None))

    info = mini_play_word('skate', game_id_2)
    print(info.get('info', {}).get('grid_formatted', None))

    info = mini_play_word('flame', game_id)
    print(info.get('info', {}).get('grid_formatted', None))


def play_one_nyt_game():

    game_id = nyt_new_game()
    print(game_id)

    time.sleep(2)

    info = nyt_play_word('meals', game_id)
    print(info.get('info', {}).get('grid_formatted', None))

    time.sleep(2)

    info = nyt_play_word('silky', game_id)
    print(info.get('info', {}).get('grid_formatted', None))

    time.sleep(2)
    info = nyt_play_word('meant', game_id)
    print(info.get('info', {}).get('grid_formatted', None))


if __name__ == '__main__':
    
    play_two_mini_games()
    # play_one_nyt_game()