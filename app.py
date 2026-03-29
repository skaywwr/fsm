import os
import random
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mega-football-database-2026")

# ПОЛНАЯ БАЗА: 24 КЛУБА ПО 11-12 ИГРОКОВ В КАЖДОМ
DEFAULT_CLUBS = {
    "Real Madrid": [
        {"name": "Courtois", "pos": "GK", "rating": 90}, {"name": "Carvajal", "pos": "RB", "rating": 87},
        {"name": "Militao", "pos": "CB", "rating": 87}, {"name": "Rudiger", "pos": "CB", "rating": 88},
        {"name": "Mendy", "pos": "LB", "rating": 85}, {"name": "Valverde", "pos": "CM", "rating": 89},
        {"name": "Tchouameni", "pos": "CM", "rating": 86}, {"name": "Bellingham", "pos": "CM", "rating": 90},
        {"name": "Rodrygo", "pos": "RW", "rating": 87}, {"name": "Mbappe", "pos": "ST", "rating": 92},
        {"name": "Vinicius Jr", "pos": "LW", "rating": 91}, {"name": "Modric", "pos": "CM", "rating": 84}
    ],
    "Manchester City": [
        {"name": "Ederson", "pos": "GK", "rating": 88}, {"name": "Walker", "pos": "RB", "rating": 84},
        {"name": "Dias", "pos": "CB", "rating": 89}, {"name": "Stones", "pos": "CB", "rating": 86},
        {"name": "Gvardiol", "pos": "LB", "rating": 85}, {"name": "Rodri", "pos": "CM", "rating": 91},
        {"name": "Bernardo", "pos": "CM", "rating": 88}, {"name": "De Bruyne", "pos": "CM", "rating": 90},
        {"name": "Foden", "pos": "RW", "rating": 90}, {"name": "Haaland", "pos": "ST", "rating": 91},
        {"name": "Doku", "pos": "LW", "rating": 83}, {"name": "Gundogan", "pos": "CM", "rating": 87}
    ],
    "Liverpool": [
        {"name": "Alisson", "pos": "GK", "rating": 89}, {"name": "Trent", "pos": "RB", "rating": 87},
        {"name": "Konate", "pos": "CB", "rating": 85}, {"name": "Van Dijk", "pos": "CB", "rating": 89},
        {"name": "Robertson", "pos": "LB", "rating": 85}, {"name": "Mac Allister", "pos": "CM", "rating": 87},
        {"name": "Gravenberch", "pos": "CM", "rating": 82}, {"name": "Szoboszlai", "pos": "CM", "rating": 85},
        {"name": "Salah", "pos": "RW", "rating": 90}, {"name": "Jota", "pos": "ST", "rating": 85},
        {"name": "Diaz", "pos": "LW", "rating": 86}, {"name": "Nunez", "pos": "ST", "rating": 82}
    ],
    "Barcelona": [
        {"name": "Ter Stegen", "pos": "GK", "rating": 89}, {"name": "Kounde", "pos": "RB", "rating": 85},
        {"name": "Araujo", "pos": "CB", "rating": 86}, {"name": "Cubarsi", "pos": "CB", "rating": 80},
        {"name": "Balde", "pos": "LB", "rating": 81}, {"name": "De Jong", "pos": "CM", "rating": 87},
        {"name": "Pedri", "pos": "CM", "rating": 87}, {"name": "Olmo", "pos": "CM", "rating": 86},
        {"name": "Yamal", "pos": "RW", "rating": 85}, {"name": "Lewandowski", "pos": "ST", "rating": 88},
        {"name": "Raphinha", "pos": "LW", "rating": 86}, {"name": "Gavi", "pos": "CM", "rating": 85}
    ],
    "Arsenal": [
        {"name": "Raya", "pos": "GK", "rating": 85}, {"name": "White", "pos": "RB", "rating": 84},
        {"name": "Saliba", "pos": "CB", "rating": 88}, {"name": "Gabriel", "pos": "CB", "rating": 87},
        {"name": "Timber", "pos": "LB", "rating": 81}, {"name": "Rice", "pos": "CM", "rating": 88},
        {"name": "Odegaard", "pos": "CM", "rating": 89}, {"name": "Merino", "pos": "CM", "rating": 85},
        {"name": "Saka", "pos": "RW", "rating": 89}, {"name": "Havertz", "pos": "ST", "rating": 84},
        {"name": "Martinelli", "pos": "LW", "rating": 83}, {"name": "Trossard", "pos": "LW", "rating": 83}
    ],
    "Bayern Munich": [
        {"name": "Neuer", "pos": "GK", "rating": 86}, {"name": "Kimmich", "pos": "RB", "rating": 87},
        {"name": "Upamecano", "pos": "CB", "rating": 82}, {"name": "Kim Min Jae", "pos": "CB", "rating": 83},
        {"name": "Davies", "pos": "LB", "rating": 82}, {"name": "Palhinha", "pos": "CM", "rating": 85},
        {"name": "Laimer", "pos": "CM", "rating": 81}, {"name": "Musiala", "pos": "CM", "rating": 89},
        {"name": "Olise", "pos": "RW", "rating": 83}, {"name": "Kane", "pos": "ST", "rating": 91},
        {"name": "Sane", "pos": "LW", "rating": 85}, {"name": "Gnabry", "pos": "LW", "rating": 82}
    ],
    "Inter Milan": [
        {"name": "Sommer", "pos": "GK", "rating": 87}, {"name": "Pavard", "pos": "CB", "rating": 84},
        {"name": "Acerbi", "pos": "CB", "rating": 83}, {"name": "Bastoni", "pos": "CB", "rating": 87},
        {"name": "Darmian", "pos": "RB", "rating": 80}, {"name": "Dimarco", "pos": "LB", "rating": 85},
        {"name": "Barella", "pos": "CM", "rating": 88}, {"name": "Calhanoglu", "pos": "CM", "rating": 86},
        {"name": "Mkhitaryan", "pos": "CM", "rating": 83}, {"name": "Lautaro", "pos": "ST", "rating": 90},
        {"name": "Thuram", "pos": "ST", "rating": 84}, {"name": "Dumfries", "pos": "RW", "rating": 82}
    ],
    "PSG": [
        {"name": "Donnarumma", "pos": "GK", "rating": 88}, {"name": "Hakimi", "pos": "RB", "rating": 85},
        {"name": "Marquinhos", "pos": "CB", "rating": 87}, {"name": "Pacho", "pos": "CB", "rating": 81},
        {"name": "Mendes", "pos": "LB", "rating": 83}, {"name": "Vitinha", "pos": "CM", "rating": 85},
        {"name": "Zaire-Emery", "pos": "CM", "rating": 82}, {"name": "Fabian Ruiz", "pos": "CM", "rating": 82},
        {"name": "Dembele", "pos": "RW", "rating": 86}, {"name": "Barcola", "pos": "LW", "rating": 82},
        {"name": "Ramos", "pos": "ST", "rating": 81}, {"name": "Hernandez", "pos": "CB", "rating": 83}
    ],
    "Bayer Leverkusen": [
        {"name": "Hradecky", "pos": "GK", "rating": 81}, {"name": "Frimpong", "pos": "RB", "rating": 85},
        {"name": "Tah", "pos": "CB", "rating": 84}, {"name": "Tapsoba", "pos": "CB", "rating": 83},
        {"name": "Grimaldo", "pos": "LB", "rating": 86}, {"name": "Xhaka", "pos": "CM", "rating": 86},
        {"name": "Andrich", "pos": "CM", "rating": 82}, {"name": "Palacios", "pos": "CM", "rating": 81},
        {"name": "Wirtz", "pos": "CM", "rating": 89}, {"name": "Boniface", "pos": "ST", "rating": 82},
        {"name": "Schick", "pos": "ST", "rating": 80}, {"name": "Hincapie", "pos": "CB", "rating": 81}
    ],
    "Atletico Madrid": [
        {"name": "Oblak", "pos": "GK", "rating": 87}, {"name": "Gimenez", "pos": "CB", "rating": 83},
        {"name": "Le Normand", "pos": "CB", "rating": 82}, {"name": "Azpilicueta", "pos": "CB", "rating": 80},
        {"name": "Llorente", "pos": "RB", "rating": 82}, {"name": "Lino", "pos": "LB", "rating": 81},
        {"name": "De Paul", "pos": "CM", "rating": 84}, {"name": "Koke", "pos": "CM", "rating": 82},
        {"name": "Gallagher", "pos": "CM", "rating": 83}, {"name": "Griezmann", "pos": "ST", "rating": 88},
        {"name": "Alvarez", "pos": "ST", "rating": 85}, {"name": "Sorloth", "pos": "ST", "rating": 81}
    ],
    "AC Milan": [
        {"name": "Maignan", "pos": "GK", "rating": 87}, {"name": "Emerson", "pos": "RB", "rating": 78},
        {"name": "Tomori", "pos": "CB", "rating": 83}, {"name": "Pavlovic", "pos": "CB", "rating": 79},
        {"name": "Theo", "pos": "LB", "rating": 87}, {"name": "Fofana", "pos": "CM", "rating": 81},
        {"name": "Reijnders", "pos": "CM", "rating": 82}, {"name": "Loftus-Cheek", "pos": "CM", "rating": 80},
        {"name": "Pulisic", "pos": "RW", "rating": 84}, {"name": "Leao", "pos": "LW", "rating": 87},
        {"name": "Morata", "pos": "ST", "rating": 83}, {"name": "Abraham", "pos": "ST", "rating": 77}
    ],
    "Juventus": [
        {"name": "Di Gregorio", "pos": "GK", "rating": 82}, {"name": "Bremer", "pos": "CB", "rating": 86},
        {"name": "Gatti", "pos": "CB", "rating": 80}, {"name": "Kalulu", "pos": "CB", "rating": 78},
        {"name": "Cambiaso", "pos": "LB", "rating": 80}, {"name": "Locatelli", "pos": "CM", "rating": 80},
        {"name": "Douglas Luiz", "pos": "CM", "rating": 83}, {"name": "Koopmeiners", "pos": "CM", "rating": 85},
        {"name": "Gonzalez", "pos": "RW", "rating": 81}, {"name": "Vlahovic", "pos": "ST", "rating": 85},
        {"name": "Yildiz", "pos": "LW", "rating": 80}, {"name": "Thuram", "pos": "CM", "rating": 79}
    ],
    "Chelsea": [
        {"name": "Sanchez", "pos": "GK", "rating": 78}, {"name": "James", "pos": "RB", "rating": 83},
        {"name": "Colwill", "pos": "CB", "rating": 80}, {"name": "Fofana", "pos": "CB", "rating": 79},
        {"name": "Cucurella", "pos": "LB", "rating": 81}, {"name": "Caicedo", "pos": "CM", "rating": 83},
        {"name": "Enzo", "pos": "CM", "rating": 84}, {"name": "Palmer", "pos": "CM", "rating": 86},
        {"name": "Madueke", "pos": "RW", "rating": 80}, {"name": "Jackson", "pos": "ST", "rating": 80},
        {"name": "Neto", "pos": "LW", "rating": 81}, {"name": "Nkunku", "pos": "ST", "rating": 84}
    ],
    "Man United": [
        {"name": "Onana", "pos": "GK", "rating": 84}, {"name": "Mazraoui", "pos": "RB", "rating": 81},
        {"name": "De Ligt", "pos": "CB", "rating": 85}, {"name": "Martinez", "pos": "CB", "rating": 83},
        {"name": "Dalot", "pos": "LB", "rating": 81}, {"name": "Ugarte", "pos": "CM", "rating": 82},
        {"name": "Mainoo", "pos": "CM", "rating": 80}, {"name": "Bruno", "pos": "CM", "rating": 87},
        {"name": "Garnacho", "pos": "RW", "rating": 80}, {"name": "Hojlund", "pos": "ST", "rating": 79},
        {"name": "Rashford", "pos": "LW", "rating": 81}, {"name": "Casemiro", "pos": "CM", "rating": 82}
    ],
    "Dortmund": [
        {"name": "Kobel", "pos": "GK", "rating": 86}, {"name": "Ryerson", "pos": "RB", "rating": 79},
        {"name": "Sule", "pos": "CB", "rating": 81}, {"name": "Schlotterbeck", "pos": "CB", "rating": 84},
        {"name": "Bensebaini", "pos": "LB", "rating": 77}, {"name": "Can", "pos": "CM", "rating": 80},
        {"name": "Sabitzer", "pos": "CM", "rating": 82}, {"name": "Brandt", "pos": "CM", "rating": 85},
        {"name": "Malen", "pos": "RW", "rating": 81}, {"name": "Guirassy", "pos": "ST", "rating": 83},
        {"name": "Adeyemi", "pos": "LW", "rating": 80}, {"name": "Beier", "pos": "ST", "rating": 78}
    ],
    "Spurs": [
        {"name": "Vicario", "pos": "GK", "rating": 83}, {"name": "Porro", "pos": "RB", "rating": 82},
        {"name": "Romero", "pos": "CB", "rating": 85}, {"name": "Van de Ven", "pos": "CB", "rating": 82},
        {"name": "Udogie", "pos": "LB", "rating": 81}, {"name": "Bissouma", "pos": "CM", "rating": 80},
        {"name": "Sarr", "pos": "CM", "rating": 79}, {"name": "Maddison", "pos": "CM", "rating": 85},
        {"name": "Kulusevski", "pos": "RW", "rating": 81}, {"name": "Solanke", "pos": "ST", "rating": 81},
        {"name": "Son", "pos": "LW", "rating": 87}, {"name": "Werner", "pos": "LW", "rating": 77}
    ],
    "Napoli": [
        {"name": "Meret", "pos": "GK", "rating": 80}, {"name": "Di Lorenzo", "pos": "RB", "rating": 83},
        {"name": "Rrahmani", "pos": "CB", "rating": 81}, {"name": "Buongiorno", "pos": "CB", "rating": 81},
        {"name": "Olivera", "pos": "LB", "rating": 79}, {"name": "Lobotka", "pos": "CM", "rating": 84},
        {"name": "Anguissa", "pos": "CM", "rating": 82}, {"name": "McTominay", "pos": "CM", "rating": 80},
        {"name": "Politano", "pos": "RW", "rating": 79}, {"name": "Lukaku", "pos": "ST", "rating": 82},
        {"name": "Kvaratskhelia", "pos": "LW", "rating": 86}, {"name": "Neres", "pos": "RW", "rating": 80}
    ],
    "Aston Villa": [
        {"name": "Martinez", "pos": "GK", "rating": 87}, {"name": "Cash", "pos": "RB", "rating": 78},
        {"name": "Konsa", "pos": "CB", "rating": 81}, {"name": "Torres", "pos": "CB", "rating": 82},
        {"name": "Digne", "pos": "LB", "rating": 79}, {"name": "Onana", "pos": "CM", "rating": 80},
        {"name": "Tielemans", "pos": "CM", "rating": 82}, {"name": "McGinn", "pos": "CM", "rating": 81},
        {"name": "Bailey", "pos": "RW", "rating": 82}, {"name": "Watkins", "pos": "ST", "rating": 84},
        {"name": "Ramsey", "pos": "LW", "rating": 77}, {"name": "Maatsen", "pos": "LB", "rating": 79}
    ],
    "RB Leipzig": [
        {"name": "Gulacsi", "pos": "GK", "rating": 81}, {"name": "Henrichs", "pos": "RB", "rating": 79},
        {"name": "Orban", "pos": "CB", "rating": 82}, {"name": "Lukeba", "pos": "CB", "rating": 81},
        {"name": "Raum", "pos": "LB", "rating": 80}, {"name": "Haidara", "pos": "CM", "rating": 80},
        {"name": "Schlager", "pos": "CM", "rating": 81}, {"name": "Simons", "pos": "CM", "rating": 85},
        {"name": "Nusa", "pos": "RW", "rating": 77}, {"name": "Openda", "pos": "ST", "rating": 84},
        {"name": "Sesko", "pos": "ST", "rating": 81}, {"name": "Geertruida", "pos": "CB", "rating": 80}
    ],
    "Sporting": [
        {"name": "Israel", "pos": "GK", "rating": 76}, {"name": "Quaresma", "pos": "RB", "rating": 75},
        {"name": "Diomande", "pos": "CB", "rating": 80}, {"name": "Inacio", "pos": "CB", "rating": 81},
        {"name": "Reis", "pos": "LB", "rating": 77}, {"name": "Hjulmand", "pos": "CM", "rating": 81},
        {"name": "Morita", "pos": "CM", "rating": 79}, {"name": "Goncalves", "pos": "CM", "rating": 82},
        {"name": "Trincao", "pos": "RW", "rating": 80}, {"name": "Gyokeres", "pos": "ST", "rating": 86},
        {"name": "Edwards", "pos": "LW", "rating": 78}, {"name": "Debast", "pos": "CB", "rating": 78}
    ],
    "Benfica": [
        {"name": "Trubin", "pos": "GK", "rating": 82}, {"name": "Bah", "pos": "RB", "rating": 79},
        {"name": "Otamendi", "pos": "CB", "rating": 81}, {"name": "Silva", "pos": "CB", "rating": 80},
        {"name": "Beste", "pos": "LB", "rating": 78}, {"name": "Florentino", "pos": "CM", "rating": 79},
        {"name": "Aursnes", "pos": "CM", "rating": 81}, {"name": "Kokcu", "pos": "CM", "rating": 82},
        {"name": "Di Maria", "pos": "RW", "rating": 83}, {"name": "Pavlidis", "pos": "ST", "rating": 81},
        {"name": "Akturkoglu", "pos": "LW", "rating": 80}, {"name": "Barreiro", "pos": "CM", "rating": 78}
    ],
    "Porto": [
        {"name": "Costa", "pos": "GK", "rating": 84}, {"name": "Joao Mario", "pos": "RB", "rating": 78},
        {"name": "Otavio", "pos": "CB", "rating": 77}, {"name": "Perez", "pos": "CB", "rating": 77},
        {"name": "Moura", "pos": "LB", "rating": 76}, {"name": "Varela", "pos": "CM", "rating": 80},
        {"name": "Eustaquio", "pos": "CM", "rating": 77}, {"name": "Nico", "pos": "CM", "rating": 78},
        {"name": "Pepe", "pos": "RW", "rating": 80}, {"name": "Omorodion", "pos": "ST", "rating": 78},
        {"name": "Galeno", "pos": "LW", "rating": 82}, {"name": "Vieira", "pos": "CM", "rating": 77}
    ],
    "Roma": [
        {"name": "Svilar", "pos": "GK", "rating": 80}, {"name": "Celik", "pos": "RB", "rating": 75},
        {"name": "Mancini", "pos": "CB", "rating": 81}, {"name": "Ndicka", "pos": "CB", "rating": 80},
        {"name": "Angelino", "pos": "LB", "rating": 79}, {"name": "Cristante", "pos": "CM", "rating": 81},
        {"name": "Kone", "pos": "CM", "rating": 79}, {"name": "Pellegrini", "pos": "CM", "rating": 82},
        {"name": "Soule", "pos": "RW", "rating": 78}, {"name": "Dovbyk", "pos": "ST", "rating": 82},
        {"name": "Dybala", "pos": "LW", "rating": 86}, {"name": "Hermoso", "pos": "CB", "rating": 81}
    ],
    "Girona": [
        {"name": "Gazzaniga", "pos": "GK", "rating": 79}, {"name": "Arnau", "pos": "RB", "rating": 76},
        {"name": "Lopez", "pos": "CB", "rating": 79}, {"name": "Blind", "pos": "CB", "rating": 80},
        {"name": "Miguel", "pos": "LB", "rating": 81}, {"name": "Romeu", "pos": "CM", "rating": 78},
        {"name": "Herrera", "pos": "CM", "rating": 80}, {"name": "Martin", "pos": "CM", "rating": 80},
        {"name": "Tsygankov", "pos": "RW", "rating": 82}, {"name": "Abel Ruiz", "pos": "ST", "rating": 76},
        {"name": "Danjuma", "pos": "LW", "rating": 78}, {"name": "Asprilla", "pos": "RW", "rating": 76}
    ]
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'my_clubs' not in session: session['my_clubs'] = {}
    if 'my_managers' not in session: session['my_managers'] = {}
    
    match_result = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add_custom':
            c_name = request.form.get('club_name').strip()
            p_name = request.form.get('p_name').strip()
            p_pos = request.form.get('p_pos')
            p_rating = int(request.form.get('p_rating', 80))
            temp_clubs = session['my_clubs'].copy()
            if c_name not in temp_clubs: temp_clubs[c_name] = {"players": []}
            temp_clubs[c_name]["players"].append({"name": p_name, "pos": p_pos, "rating": p_rating})
            session['my_clubs'] = temp_clubs
            session.modified = True

        elif action == 'create':
            m_name = request.form.get('manager_name')
            selected_names = request.form.getlist('clubs')
            team = get_best_11(selected_names, session['my_clubs'])
            if len(team) >= 11:
                avg = sum(p['rating'] for p in team) / len(team)
                temp_m = session['my_managers'].copy()
                temp_m[m_name] = {"name": m_name, "rating": round(avg, 1), "team": team}
                session['my_managers'] = temp_m
                session.modified = True

        elif action == 'match':
            m1_n = request.form.get('m1')
            m2_n = request.form.get('m2')
            mgrs = session['my_managers']
            if m1_n in mgrs and m2_n in mgrs and m1_n != m2_n:
                m1, m2 = mgrs[m1_n], mgrs[m2_n]
                power = 2.5
                r1, r2 = m1['rating']**power, m2['rating']**power
                chance = (r1 / (r1 + r2)) * 100
                
                log = []
                s1, s2 = 0, 0
                minutes = sorted(random.sample(range(1, 91), 5))
                
                for minute in minutes:
                    if random.uniform(0, 100) < chance:
                        p_atk = random.choice(m1['team'])
                        p_def = random.choice(m2['team'])
                        if random.random() > 0.65:
                            s1 += 1
                            log.append(f"{minute}' — ⚽ ГОЛ! {p_atk['name']} обыгрывает {p_def['name']} и забивает! Счет {s1}:{s2}")
                        else:
                            log.append(f"{minute}' — {p_atk['name']} опасно пробил, но {p_def['name']} заблокировал удар.")
                    else:
                        p_atk = random.choice(m2['team'])
                        p_def = random.choice(m1['team'])
                        if random.random() > 0.65:
                            s2 += 1
                            log.append(f"{minute}' — ⚽ ГОЛ! {p_atk['name']} наносит точный удар! Счет {s1}:{s2}")
                        else:
                            log.append(f"{minute}' — Контратака! {p_atk['name']} упустил момент благодаря защите {p_def['name']}.")

                winner = m1_n if s1 > s2 else (m2_n if s2 > s1 else "Ничья")
                match_result = {"m1": m1_n, "m2": m2_n, "score": f"{s1}:{s2}", "log": log, "winner": winner, "chance": round(chance, 1)}

    all_names = sorted(list(DEFAULT_CLUBS.keys()) + list(session['my_clubs'].keys()))
    full_db = DEFAULT_CLUBS.copy()
    for uc, data in session['my_clubs'].items(): full_db[uc] = data['players']

    return render_template('index.html', clubs=all_names, managers=session['my_managers'], match_result=match_result, full_database=full_db)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
