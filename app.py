import os
import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# База данных прямо в коде
ALL_CLUBS_DATA = {
    "Real Madrid": [{"name": "Mbappe", "pos": "ST", "rating": 92}, {"name": "Vinicius Jr", "pos": "LW", "rating": 91}, {"name": "Bellingham", "pos": "CM", "rating": 90}, {"name": "Courtois", "pos": "GK", "rating": 90}, {"name": "Rudiger", "pos": "CB", "rating": 88}],
    "Manchester City": [{"name": "Haaland", "pos": "ST", "rating": 91}, {"name": "Rodri", "pos": "CM", "rating": 91}, {"name": "De Bruyne", "pos": "CM", "rating": 90}, {"name": "Foden", "pos": "RW", "rating": 90}, {"name": "Dias", "pos": "CB", "rating": 89}],
    "Liverpool": [{"name": "Salah", "pos": "RW", "rating": 90}, {"name": "Van Dijk", "pos": "CB", "rating": 89}, {"name": "Alisson", "pos": "GK", "rating": 89}, {"name": "Mac Allister", "pos": "CM", "rating": 87}],
    "Barcelona": [{"name": "Lewandowski", "pos": "ST", "rating": 88}, {"name": "Yamal", "pos": "RW", "rating": 85}, {"name": "Pedri", "pos": "CM", "rating": 87}],
    "Arsenal": [{"name": "Odegaard", "pos": "CM", "rating": 89}, {"name": "Saka", "pos": "RW", "rating": 89}, {"name": "Saliba", "pos": "CB", "rating": 88}],
    "Bayern Munich": [{"name": "Kane", "pos": "ST", "rating": 91}, {"name": "Musiala", "pos": "CM", "rating": 89}],
    "Inter Milan": [{"name": "Lautaro", "pos": "ST", "rating": 90}, {"name": "Barella", "pos": "CM", "rating": 88}],
    "PSG": [{"name": "Donnarumma", "pos": "GK", "rating": 88}, {"name": "Marquinhos", "pos": "CB", "rating": 87}],
    "AC Milan": [{"name": "Leao", "pos": "LW", "rating": 87}, {"name": "Theo", "pos": "LB", "rating": 87}],
    "Chelsea": [{"name": "Palmer", "pos": "CM", "rating": 86}],
    "Man United": [{"name": "Bruno", "pos": "CM", "rating": 87}],
    "Roma": [{"name": "Dybala", "pos": "ST", "rating": 86}]
}

SAVED_MANAGERS = {}

def get_best_11(selected_clubs):
    pool = []
    for club in selected_clubs:
        if club in ALL_CLUBS_DATA:
            pool.extend(ALL_CLUBS_DATA[club])
    pool.sort(key=lambda x: x['rating'], reverse=True)
    schema = {'GK': 1, 'CB': 2, 'LB': 1, 'RB': 1, 'CM': 3, 'LW': 1, 'RW': 1, 'ST': 1}
    final_squad = []
    for player in pool:
        pos = player['pos']
        if pos in schema and schema[pos] > 0:
            final_squad.append(player)
            schema[pos] -= 1
    return final_squad

@app.route('/', methods=['GET', 'POST'])
def index():
    match_result = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            name = request.form.get('manager_name')
            clubs = request.form.getlist('clubs')
            team = get_best_11(clubs)
            if team:
                avg_rating = sum(p['rating'] for p in team) / len(team)
                SAVED_MANAGERS[name] = {'name': name, 'clubs': clubs, 'team': team, 'rating': round(avg_rating, 1)}
        elif action == 'match':
            m1_name = request.form.get('manager1')
            m2_name = request.form.get('manager2')
            if m1_name in SAVED_MANAGERS and m2_name in SAVED_MANAGERS:
                m1, m2 = SAVED_MANAGERS[m1_name], SAVED_MANAGERS[m2_name]
                win_chance = (m1['rating'] / (m1['rating'] + m2['rating'])) * 100
                winner = m1['name'] if random.uniform(0, 100) < win_chance else m2['name']
                match_result = {'m1': m1['name'], 'm2': m2['name'], 'chance': round(win_chance, 1), 'winner': winner}
    return render_template('index.html', clubs=sorted(ALL_CLUBS_DATA.keys()), managers=SAVED_MANAGERS, match_result=match_result)

if __name__ == '__main__':
    # Настройка порта для Northflank
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
