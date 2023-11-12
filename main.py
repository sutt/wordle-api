from flask import Flask, jsonify, request
from mini import WordleGame

# requires selenium libraries to be installed
# can still play mini games without this installed
b_nyt_enabled = False
try:
    from nyt import NYTWordleGame
    b_nyt_enabled = True
except:
    print('not able to import NYTWordleGame; selenium likely not installed')

nyt_games = {}
mini_games = {}

app = Flask(__name__)

def validate_word(word):
    if not(word):
        return {'error': 'No word provided'}
    if not(isinstance(word, str)):
        return {'error': 'Word must be a string'}
    if len(word) != 5:
        return {'error': 'Word must be 5 letters'}
    if not(word.isalpha()):
        return {'error': 'Word must be all letters'}
    return None

def validate_game(game):
    if game is None:
        return {'error': 'Game not initialized'}
    if game.current_row >= 6:
        return {'error': 'Game already finished'}
    return None

@app.route('/get_games', methods=['GET'])
def get_games_route():
    return jsonify(list(mini_games.keys()))

@app.route('/new_game', methods=['POST'])
def new_game_route():
    global mini_games
    try:
        game = WordleGame()
        mini_games[game.uuid] = game
        return jsonify({'status': 'success', 'id': game.uuid})
    except Exception as e:
        return jsonify({'status': 'failure', 'error': str(e)})

@app.route('/play_word', methods=['POST'])
def play_word_route():
    global mini_games
    data = request.get_json()
    
    input_word = data.get('word', None)
    invalid_word = validate_word(input_word)
    if invalid_word:
        return jsonify({'status': 'failure', **invalid_word})
    
    game_id = data.get('id', None)
    game = mini_games.get(game_id, None)
    invalid_game = validate_game(game)
    if invalid_game:
        return jsonify({'status': 'failure', **invalid_game})
    
    info = game.play_round(input_word)
    return jsonify({'status': 'success', 'info': info})


@app.route('/nyt/new_game', methods=['POST'])
def nyt_new_game_route():
    global nyt_games
    try:
        game = NYTWordleGame()
        nyt_games[game.uuid] = game
        return jsonify({'status': 'success', 'id': game.uuid})
    except Exception as e:
        return jsonify({'status': 'failure', 'error': str(e)})

@app.route('/nyt/play_word', methods=['POST'])
def nyt_play_word_route():
    data = request.get_json()
    
    input_word = data.get('word', None)
    invalid_word = validate_word(input_word)
    if invalid_word:
        return jsonify({'status': 'failure', **invalid_word})
    
    game_id = data.get('id', None)
    game = nyt_games.get(game_id, None)
    invalid_game = validate_game(game)
    if invalid_game:
        return jsonify({'status': 'failure', **invalid_game})
    
    info = game.play_round(input_word)
    return jsonify({'status': 'success', 'info': info})


if __name__ == "__main__":
    
    # import argparse
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--debug', action='store_true')
    # parser.add_argument('--test', action='store_true')
    # # TODO - add port/host args
    # args = parser.parse_args()
    
    app.run(debug=False)
    # app.run(debug=args.debug)
    # main()

    '''
    curl -X POST -H "Content-Type: application/json" -d "{\"word\":\"fjoRD\"}" http://localhost:5000/play_word
    '''


        

