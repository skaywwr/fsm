import os
import random
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "football-ultra-sim-2026")

# БАЗА (FC 7E, Legends XI + 24 Клуба)
DEFAULT_CLUBS = {
    "FC 7E": [{"name": "Aibek", "pos": "GK", "rating": 88}, {"name": "Temirlan", "pos": "LB", "rating": 90}, {"name": "Edil", "pos": "CB", "rating": 88}, {"name": "Dastan", "pos": "CB", "rating": 90}, {"name": "Adilet", "pos": "CB", "rating": 85}, {"name": "Alishah", "pos": "RB", "rating": 88}, {"name": "Aidar", "pos": "CM", "rating": 90}, {"name": "Batyrhan", "pos": "CM", "rating": 88}, {"name": "Amir", "pos": "CM", "rating": 91}, {"name": "Baiel", "pos": "LW", "rating": 90}, {"name": "Bakai", "pos": "LW", "rating": 88}, {"name": "Timur", "pos": "ST", "rating": 91}, {"name": "Emir", "pos": "RW", "rating": 90}, {"name": "Adil", "pos": "RW", "rating": 89}],
    "Legends XI": [{"name": "Casillas", "pos": "GK", "rating": 89}, {"name": "Marcelo", "pos": "LB", "rating": 88}, {"name": "Puyol", "pos": "CB", "rating": 88}, {"name": "Maldini", "pos": "CB", "rating": 90}, {"name": "Alves", "pos": "RB", "rating": 88}, {"name": "Xavi", "pos": "CM", "rating": 89}, {"name": "Modric", "pos": "CM", "rating": 89}, {"name": "Zidane", "pos": "CM", "rating": 90}, {"name": "Cristiano Ronaldo", "pos": "LW", "rating": 91}, {"name": "Ronaldo", "pos": "ST", "rating": 89}, {"name": "Lionel Messi", "pos": "RW", "rating": 91}],
    "Real Madrid": [{"name": "Courtois", "pos": "GK", "rating": 90}, {"name": "Carvajal", "pos": "RB", "rating": 87}, {"name": "Militao", "pos": "CB", "rating": 87}, {"name": "Rudiger", "pos": "CB", "rating": 88}, {"name": "Mendy", "pos": "LB", "rating": 85}, {"name": "Valverde", "pos": "CM", "rating": 89}, {"name": "Bellingham", "pos": "CM", "rating": 90}, {"name": "Mbappe", "pos": "ST", "rating": 92}, {"name": "Vinicius Jr", "pos": "LW", "rating": 91}, {"name": "Rodrygo", "pos": "RW", "rating": 87}, {"name": "Modric", "pos": "CM", "rating": 84}],
    "Manchester City": [{"name": "Ederson", "pos": "GK", "rating": 88}, {"name": "Walker", "pos": "RB", "rating": 84}, {"name": "Dias", "pos": "CB", "rating": 89}, {"name": "Rodri", "pos": "CM", "rating": 91}, {"name": "De Bruyne", "pos": "CM", "rating": 90}, {"name": "Foden", "pos": "RW", "rating": 90}, {"name": "Haaland", "pos": "ST", "rating": 91}, {"name": "Gvardiol", "pos": "LB", "rating": 85}, {"name": "Bernardo", "pos": "CM", "rating": 88}, {"name": "Stones", "pos": "CB", "rating": 86}, {"name": "Gundogan", "pos": "CM", "rating": 87}],
    "Liverpool": [{"name": "Alisson", "pos": "GK", "rating": 89}, {"name": "Trent", "pos": "RB", "rating": 87}, {"name": "Van Dijk", "pos": "CB", "rating": 89}, {"name": "Mac Allister", "pos": "CM", "rating": 87}, {"name": "Salah", "pos": "RW", "rating": 90}, {"name": "Diaz", "pos": "LW", "rating": 86}, {"name": "Jota", "pos": "ST", "rating": 85}, {"name": "Szoboszlai", "pos": "CM", "rating": 85}, {"name": "Konate", "pos": "CB", "rating": 85}, {"name": "Robertson", "pos": "LB", "rating": 85}, {"name": "Nunez", "pos": "ST", "rating": 82}],
    "Barcelona": [{"name": "Ter Stegen", "pos": "GK", "rating": 89}, {"name": "Kounde", "pos": "RB", "rating": 85}, {"name": "Araujo", "pos": "CB", "rating": 86}, {"name": "Pedri", "pos": "CM", "rating": 87}, {"name": "Yamal", "pos": "RW", "rating": 85}, {"name": "Lewandowski", "pos": "ST", "rating": 88}, {"name": "Raphinha", "pos": "LW", "rating": 86}, {"name": "Gavi", "pos": "CM", "rating": 85}, {"name": "De Jong", "pos": "CM", "rating": 87}, {"name": "Olmo", "pos": "CM", "rating": 86}, {"name": "Balde", "pos": "LB", "rating": 81}],
    "Arsenal": [{"name": "Raya", "pos": "GK", "rating": 85}, {"name": "Saliba", "pos": "CB", "rating": 88}, {"name": "Rice", "pos": "CM", "rating": 88}, {"name": "Odegaard", "pos": "CM", "rating": 89}, {"name": "Saka", "pos": "RW", "rating": 89}, {"name": "Havertz", "pos": "ST", "rating": 84}, {"name": "Gabriel", "pos": "CB", "rating": 87}, {"name": "White", "pos": "RB", "rating": 84}, {"name": "Martinelli", "pos": "LW", "rating": 83}],
    "Bayern Munich": [{"name": "Neuer", "pos": "GK", "rating": 86}, {"name": "Kimmich", "pos": "RB", "rating": 87}, {"name": "Musiala", "pos": "CM", "rating": 89}, {"name": "Kane", "pos": "ST", "rating": 91}, {"name": "Sane", "pos": "LW", "rating": 85}, {"name": "Davies", "pos": "LB", "rating": 82}, {"name": "Upamecano", "pos": "CB", "rating": 82}, {"name": "Kim Min Jae", "pos": "CB", "rating": 83}, {"name": "Olise", "pos": "RW", "rating": 83}],
    "Inter Milan": [{"name": "Sommer", "pos": "GK", "rating": 87}, {"name": "Bastoni", "pos": "CB", "rating": 87}, {"name": "Barella", "pos": "CM", "rating": 88}, {"name": "Lautaro", "pos": "ST", "rating": 90}, {"name": "Calhanoglu", "pos": "CM", "rating": 86}, {"name": "Dimarco", "pos": "LB", "rating": 85}, {"name": "Thuram", "pos": "ST", "rating": 84}, {"name": "Pavard", "pos": "CB", "rating": 84}],
    "PSG": [{"name": "Donnarumma", "pos": "GK", "rating": 88}, {"name": "Marquinhos", "pos": "CB", "rating": 87}, {"name": "Dembele", "pos": "RW", "rating": 86}, {"name": "Hakimi", "pos": "RB", "rating": 85}, {"name": "Vitinha", "pos": "CM", "rating": 85}, {"name": "Barcola", "pos": "LW", "rating": 82}],
    "Bayer Leverkusen": [{"name": "Wirtz", "pos": "CM", "rating": 89}, {"name": "Grimaldo", "pos": "LB", "rating": 86}, {"name": "Xhaka", "pos": "CM", "rating": 86}, {"name": "Frimpong", "pos": "RB", "rating": 85}, {"name": "Tah", "pos": "CB", "rating": 84}],
    "Atletico Madrid": [{"name": "Griezmann", "pos": "ST", "rating": 88}, {"name": "Oblak", "pos": "GK", "rating": 87}, {"name": "Alvarez", "pos": "ST", "rating": 85}, {"name": "De Paul", "pos": "CM", "rating": 84}],
    "AC Milan": [{"name": "Leao", "pos": "LW", "rating": 87}, {"name": "Theo", "pos": "LB", "rating": 87}, {"name": "Maignan", "pos": "GK", "rating": 87}, {"name": "Pulisic", "pos": "RW", "rating": 84}],
    "Juventus": [{"name": "Bremer", "pos": "CB", "rating": 86}, {"name": "Vlahovic", "pos": "ST", "rating": 85}, {"name": "Koopmeiners", "pos": "CM", "rating": 85}],
    "Chelsea": [{"name": "Palmer", "pos": "CM", "rating": 86}, {"name": "Enzo", "pos": "CM", "rating": 84}, {"name": "Caicedo", "pos": "CM", "rating": 83}],
    "Man United": [{"name": "Bruno", "pos": "CM", "rating": 87}, {"name": "Onana", "pos": "GK", "rating": 84}, {"name": "De Ligt", "pos": "CB", "rating": 85}],
    "Dortmund": [{"name": "Kobel", "pos": "GK", "rating": 86}, {"name": "Brandt", "pos": "CM", "rating": 85}, {"name": "Schlotterbeck", "pos": "CB", "rating": 84}],
    "Spurs": [{"name": "Son", "pos": "LW", "rating": 87}, {"name": "Maddison", "pos": "CM", "rating": 85}, {"name": "Romero", "pos": "CB", "rating": 85}],
    "Napoli": [{"name": "Kvaratskhelia", "pos": "LW", "rating": 86}, {"name": "Lukaku", "pos": "ST", "rating": 82}, {"name": "Lobotka", "pos": "CM", "rating": 84}],
    "Aston Villa": [{"name": "Martinez", "pos": "GK", "rating": 87}, {"name": "Watkins", "pos": "ST", "rating": 84}, {"name": "Tielemans", "pos": "CM", "rating": 82}],
    "RB Leipzig": [{"name": "Simons", "pos": "CM", "rating": 85}, {"name": "Openda", "pos": "ST", "rating": 84}],
    "Sporting": [{"name": "Gyokeres", "pos": "ST", "rating": 86}, {"name": "Inacio", "pos": "CB", "rating": 81}],
    "Benfica": [{"name": "Di Maria", "pos": "RW", "rating": 83}, {"name": "Trubin", "pos": "GK", "rating": 82}],
    "Porto": [{"name": "Costa", "pos": "GK", "rating": 84}, {"name": "Galeno", "pos": "LW", "rating": 82}],
    "Roma": [{"name": "Dybala", "pos": "ST", "rating": 86}, {"name": "Pellegrini", "pos": "CM", "rating": 82}],
    "Girona": [{"name": "Tsygankov", "pos": "RW", "rating": 82}, {"name": "Blind", "pos": "CB", "rating": 80}]
}

def get_best_11(selected_names, user_clubs):
    pool = []
    for cn in selected_names:
        if cn in DEFAULT_CLUBS: pool.extend(DEFAULT_CLUBS[cn])
        if cn in user_clubs: pool.extend(user_clubs[cn]['players'])
    pool.sort(key=lambda x: x['rating'], reverse=True)
    schema = {'GK': 1, 'CB': 2, 'LB': 1, 'RB': 1, 'CM': 3, 'LW': 1, 'RW': 1, 'ST': 1}
    final_squad = []
    for player in pool:
        pos = player['pos']
        if pos in schema and schema[pos] > 0:
            final_squad.append(player)
            schema[pos] -= 1
    return final_squad

def get_weighted_player(team, position_type="attack"):
    # Веса для выбора игрока в зависимости от типа события
    if position_type == "attack":
        weights = {'ST': 45, 'LW': 20, 'RW': 20, 'CM': 10, 'LB': 2, 'RB': 2, 'CB': 0.5, 'GK': 0.5}
    elif position_type == "foul":
        weights = {'CB': 40, 'LB': 20, 'RB': 20, 'CM': 15, 'ST': 2, 'LW': 1, 'RW': 1, 'GK': 1}
    else:
        weights = {p['pos']: 10 for p in team}
    
    player_weights = [weights.get(p['pos'], 5) for p in team]
    return random.choices(team, weights=player_weights, k=1)[0]

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'my_clubs' not in session: session['my_clubs'] = {}
    if 'my_managers' not in session: session['my_managers'] = {}
    
    occupied_clubs = set()
    for m in session['my_managers'].values():
        for c in m['selected_clubs']: occupied_clubs.add(c)

    match_result = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create':
            m_name = request.form.get('manager_name').strip()
            new_selected = request.form.getlist('clubs')
            team = get_best_11(new_selected, session['my_clubs'])
            if len(team) >= 11:
                avg = sum(p['rating'] for p in team) / len(team)
                temp_managers = session['my_managers'].copy()
                temp_managers[m_name] = {"name": m_name, "rating": round(avg, 1), "team": team, "selected_clubs": new_selected}
                session['my_managers'] = temp_managers
                session.modified = True

        elif action == 'match':
            m1_n, m2_n = request.form.get('m1'), request.form.get('m2')
            mgrs = session['my_managers']
            if m1_n in mgrs and m2_n in mgrs:
                m1, m2 = mgrs[m1_n], mgrs[m2_n]
                chance = (m1['rating']**2.5 / (m1['rating']**2.5 + m2['rating']**2.5)) * 100
                log, s1, s2 = [], 0, 0
                
                # Генерируем 8 событий для насыщенности
                for m in sorted(random.sample(range(1, 91), 8)):
                    attacking_team_name = m1_n if random.uniform(0, 100) < chance else m2_n
                    defending_team_name = m2_n if attacking_team_name == m1_n else m1_n
                    atk_team = m1['team'] if attacking_team_name == m1_n else m2['team']
                    def_team = m2['team'] if attacking_team_name == m1_n else m1['team']
                    
                    event_type = random.choices(
                        ["goal", "save", "foul", "penalty", "miss", "injury"], 
                        weights=[20, 25, 25, 10, 15, 5], k=1)[0]
                    
                    prefix = f"[{attacking_team_name.upper()} АТАКУЕТ]"
                    
                    if event_type == "goal":
                        p = get_weighted_player(atk_team, "attack")
                        if attacking_team_name == m1_n: s1 += 1 
                        else: s2 += 1
                        log.append(f"{m}' — {prefix} ⚽ ГООООООООЛ!!! {p['name'].upper()} вколачивает мяч в сетку! Безумие на трибунах! ({s1}:{s2})")
                    
                    elif event_type == "save":
                        p_atk = get_weighted_player(atk_team, "attack")
                        p_gk = [p for p in def_team if p['pos'] == 'GK'][0]
                        log.append(f"{m}' — {prefix} 🧤 НЕВЕРОЯТНЫЙ СЕЙВ! {p_atk['name']} бил в упор, но {p_gk['name']} вытаскивает мертвый мяч!")
                    
                    elif event_type == "foul":
                        p_foul = get_weighted_player(def_team, "foul")
                        p_victim = get_weighted_player(atk_team, "attack")
                        card = random.choices(["", "🟨 Жёлтая карточка!", "🟥 КРАСНАЯ КАРТОЧКА! Удаление!"], weights=[60, 35, 5], k=1)[0]
                        log.append(f"{m}' — {prefix} ⚠️ Жесткий фол! {p_foul['name']} сносит {p_victim['name']}. {card}")
                    
                    elif event_type == "penalty":
                        p_shot = get_weighted_player(atk_team, "attack")
                        if random.random() > 0.3:
                            if attacking_team_name == m1_n: s1 += 1 
                            else: s2 += 1
                            log.append(f"{m}' — {prefix} 🎯 ПЕНАЛЬТИ! {p_shot['name']} подходит к точке... И ОН ТОЧЕН! ГОЛ! ({s1}:{s2})")
                        else:
                            log.append(f"{m}' — {prefix} ❌ ПЕНАЛЬТИ! {p_shot['name']} разбегается и... МИМО! Весь стадион в шоке!")
                    
                    elif event_type == "miss":
                        p = get_weighted_player(atk_team, "attack")
                        log.append(f"{m}' — {prefix} 💥 УДАР! {p['name']} мощно пробил издали... ШТАНГА! Мяч улетает в аут.")

                    elif event_type == "injury":
                        p = get_weighted_player(atk_team, "attack")
                        log.append(f"{m}' — {prefix} 🚑 Ой-ой-ой! {p['name']} лежит на газоне и держится за колено. Похоже, нужна замена.")

                match_result = {"score": f"{s1}:{s2}", "log": log, "winner": m1_n if s1>s2 else (m2_n if s2>s1 else "Ничья")}

    all_names = sorted(list(DEFAULT_CLUBS.keys()) + list(session['my_clubs'].keys()))
    return render_template('index.html', clubs=all_names, occupied=occupied_clubs, managers=session['my_managers'], match_result=match_result, full_database=DEFAULT_CLUBS)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
