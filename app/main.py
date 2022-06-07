from flask import Flask
from flask import jsonify
from flask_cors import CORS 
from flask import request

from swissdutch.dutch import DutchPairingEngine
from swissdutch.constants import FideTitle, Colour, FloatStatus
from app.utils import Player

app = Flask(__name__)
CORS(app)

def _top_seed_colour_selection_fn():
    return Colour.black

@app.route("/swiss", methods=['POST'])
def swiss():

    body = request.get_json()

    engine = DutchPairingEngine(top_seed_colour_selection_fn = _top_seed_colour_selection_fn )
    input_players = []

    for _player in body["players"]:
        input_players.append(Player(name=_player['name'],
                rating=_player['elo'],
                pairing_no=_player['orden'],
                score=_player['score'],
                opponents=_player['opponents'],
                colour_hist=_player['colors'],
                player_id=_player['player_id']))

    result_players = engine.pair_round(body["round"], input_players)

    response = []

    for r in result_players:
        response.append({
            "name": r.name,
            "rating": r.rating,
            "title": r.title,
            "pairing_no": r.pairing_no,
            "score": r.score,
            "float_status": r.float_status,
            "opponents": r.opponents,
            "colour_hist": r.colour_hist,
            "player_id": r.player_id,
        })

    return jsonify({"result": response})

