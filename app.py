import os
import random
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fc26-secret-key-999")

# Начальный список клубов (Глобальный)
GLOBAL_CLUBS = {
    "Real Madrid": [{"name": "Mbappe", "pos": "ST", "rating": 92}, {"name": "Vinicius Jr", "pos": "LW", "rating": 91}, {"name": "Bellingham", "pos": "CM", "rating": 90}],
    "Manchester City": [{"name": "Haaland", "pos": "ST", "rating": 91}, {"name": "Rodri", "pos": "CM", "rating": 91}, {"name": "De Bruyne", "pos": "CM", "rating": 90}],
    "Barcelona": [{"name": "Lewandowski", "pos": "ST", "rating": 88}, {"name": "Yamal", "pos": "RW", "rating": 85}, {"name": "Pedri", "pos": "CM", "rating": 87}],
    "Liverpool": [{"name": "Salah", "pos": "RW", "rating": 90}, {"name": "Van Dijk", "pos": "CB", "rating": 89}, {"name": "Alisson", "pos": "GK", "rating": 89}]
}

def get_best_11(selected_clubs):
    pool = []
    for club in selected_clubs:
        if club in GLOBAL_CLUBS:
            pool.extend(GLOBAL_CLUBS[club])
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
    if 'my_managers' not in session:
        session['my_managers'] = {}
    
    match_result = None
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        # КОМАНДА: ДОБАВИТЬ НОВЫЙ КЛУБ (ДЛЯ ВСЕХ)
        if action == 'add_club':
            club_name = request.form.get('new_club_name')
            player_name = request.form.get('player_name')
            player_pos = request.form.get('player_pos')
            player_rating = int(request.form.get('player_rating', 80))
            
            if club_name not in GLOBAL_CLUBS:
                GLOBAL_CLUBS[club_name] = []
            
            GLOBAL_CLUBS[club_name].append({
                "name": player_name, 
                "pos": player_pos, 
                "rating": player_rating
            })

        # КОМАНДА: СОЗДАТЬ МЕНЕДЖЕРА (ТОЛЬКО ДЛЯ СЕБЯ)
        elif action == 'create':
            name = request.form.get('manager_name')
            clubs = request.form.getlist('clubs')
            team = get_best_11(clubs)
            if team:
                avg_rating = sum(p['rating'] for p in team) / len(team)
                temp = session['my_managers'].copy()
                temp[name] = {'name': name, 'rating': round(avg_rating, 1)}
                session['my_managers'] = temp
                session.modified = True
                
        elif action == 'match':
            m1_name = request.form.get('manager1')
            m2_name = request.form.get('manager2')
            managers = session.get('my_managers', {})
            if m1_name in managers and m2_name in managers:
                m1, m2 = managers[m1_name], managers[m2_name]
                win_chance = (m1['rating'] / (m1['rating'] + m2['rating'])) * 100
                winner = m1['name'] if random.uniform(0, 100) < win_chance else m2['name']
                match_result = {'m1': m1['name'], 'm2': m2['name'], 'chance': round(win_chance, 1), 'winner': winner}

    return render_template('index.html', 
                           clubs=sorted(GLOBAL_CLUBS.keys()), 
                           managers=session.get('my_managers', {}), 
                           match_result=match_result)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
