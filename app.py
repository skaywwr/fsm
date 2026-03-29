import os
import random
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ultra-football-manager-2026")

# ГЛОБАЛЬНАЯ БАЗА: 24 КЛУБА (ПО 12-15 ИГРОКОВ В КАЖДОМ)
GLOBAL_CLUBS = {
    "Real Madrid": [
        {"name": "Mbappe", "pos": "ST", "rating": 92}, {"name": "Vinicius Jr", "pos": "LW", "rating": 91},
        {"name": "Bellingham", "pos": "CM", "rating": 90}, {"name": "Courtois", "pos": "GK", "rating": 90},
        {"name": "Valverde", "pos": "CM", "rating": 89}, {"name": "Rudiger", "pos": "CB", "rating": 88},
        {"name": "Rodrygo", "pos": "RW", "rating": 87}, {"name": "Militao", "pos": "CB", "rating": 87},
        {"name": "Carvajal", "pos": "RB", "rating": 87}, {"name": "Tchouameni", "pos": "CM", "rating": 86},
        {"name": "Camavinga", "pos": "CM", "rating": 85}, {"name": "Mendy", "pos": "LB", "rating": 85},
        {"name": "Modric", "pos": "CM", "rating": 84}, {"name": "Alaba", "pos": "CB", "rating": 85}
    ],
    "Manchester City": [
        {"name": "Haaland", "pos": "ST", "rating": 91}, {"name": "Rodri", "pos": "CM", "rating": 91},
        {"name": "De Bruyne", "pos": "CM", "rating": 90}, {"name": "Foden", "pos": "RW", "rating": 90},
        {"name": "Dias", "pos": "CB", "rating": 89}, {"name": "Ederson", "pos": "GK", "rating": 88},
        {"name": "Bernardo", "pos": "CM", "rating": 88}, {"name": "Gundogan", "pos": "CM", "rating": 87},
        {"name": "Stones", "pos": "CB", "rating": 86}, {"name": "Gvardiol", "pos": "LB", "rating": 85},
        {"name": "Walker", "pos": "RB", "rating": 84}, {"name": "Ake", "pos": "CB", "rating": 84},
        {"name": "Doku", "pos": "LW", "rating": 83}, {"name": "Savinho", "pos": "RW", "rating": 82}
    ],
    "Liverpool": [
        {"name": "Salah", "pos": "RW", "rating": 90}, {"name": "Van Dijk", "pos": "CB", "rating": 89},
        {"name": "Alisson", "pos": "GK", "rating": 89}, {"name": "Mac Allister", "pos": "CM", "rating": 87},
        {"name": "Trent", "pos": "RB", "rating": 87}, {"name": "Diaz", "pos": "LW", "rating": 86},
        {"name": "Jota", "pos": "ST", "rating": 85}, {"name": "Konate", "pos": "CB", "rating": 85},
        {"name": "Szoboszlai", "pos": "CM", "rating": 85}, {"name": "Robertson", "pos": "LB", "rating": 85},
        {"name": "Nunez", "pos": "ST", "rating": 82}, {"name": "Gakpo", "pos": "LW", "rating": 83}
    ],
    "Arsenal": [
        {"name": "Odegaard", "pos": "CM", "rating": 89}, {"name": "Saka", "pos": "RW", "rating": 89},
        {"name": "Saliba", "pos": "CB", "rating": 88}, {"name": "Rice", "pos": "CM", "rating": 88},
        {"name": "Gabriel", "pos": "CB", "rating": 87}, {"name": "Raya", "pos": "GK", "rating": 85},
        {"name": "Havertz", "pos": "ST", "rating": 84}, {"name": "White", "pos": "RB", "rating": 84},
        {"name": "Timber", "pos": "CB", "rating": 81}, {"name": "Martinelli", "pos": "LW", "rating": 83},
        {"name": "Merino", "pos": "CM", "rating": 85}, {"name": "Trossard", "pos": "LW", "rating": 83}
    ],
    "Barcelona": [
        {"name": "Lewandowski", "pos": "ST", "rating": 88}, {"name": "Yamal", "pos": "RW", "rating": 85},
        {"name": "Pedri", "pos": "CM", "rating": 87}, {"name": "De Jong", "pos": "CM", "rating": 87},
        {"name": "Raphinha", "pos": "LW", "rating": 86}, {"name": "Gavi", "pos": "CM", "rating": 85},
        {"name": "Ter Stegen", "pos": "GK", "rating": 89}, {"name": "Araujo", "pos": "CB", "rating": 86},
        {"name": "Kounde", "pos": "RB", "rating": 85}, {"name": "Balde", "pos": "LB", "rating": 81},
        {"name": "Cubarsi", "pos": "CB", "rating": 80}, {"name": "Olmo", "pos": "CM", "rating": 86},
        {"name": "Ferran", "pos": "LW", "rating": 82}
    ],
    "Bayern Munich": [
        {"name": "Kane", "pos": "ST", "rating": 91}, {"name": "Musiala", "pos": "CM", "rating": 89},
        {"name": "Kimmich", "pos": "RB", "rating": 87}, {"name": "Neuer", "pos": "GK", "rating": 86},
        {"name": "Sane", "pos": "RW", "rating": 85}, {"name": "Coman", "pos": "LW", "rating": 84},
        {"name": "Palhinha", "pos": "CM", "rating": 85}, {"name": "Upamecano", "pos": "CB", "rating": 82},
        {"name": "Kim Min Jae", "pos": "CB", "rating": 83}, {"name": "Davies", "pos": "LB", "rating": 82},
        {"name": "Olise", "pos": "RW", "rating": 83}, {"name": "Muller", "pos": "CM", "rating": 82},
        {"name": "Gnabry", "pos": "LW", "rating": 82}
    ],
    "Bayer Leverkusen": [
        {"name": "Wirtz", "pos": "CM", "rating": 89}, {"name": "Grimaldo", "pos": "LB", "rating": 86},
        {"name": "Xhaka", "pos": "CM", "rating": 86}, {"name": "Frimpong", "pos": "RB", "rating": 85},
        {"name": "Tah", "pos": "CB", "rating": 84}, {"name": "Tapsoba", "pos": "CB", "rating": 83},
        {"name": "Boniface", "pos": "ST", "rating": 82}, {"name": "Hradecky", "pos": "GK", "rating": 81},
        {"name": "Schick", "pos": "ST", "rating": 80}, {"name": "Andrich", "pos": "CM", "rating": 82},
        {"name": "Hincapie", "pos": "CB", "rating": 81}, {"name": "Palacios", "pos": "CM", "rating": 81}
    ],
    "Inter Milan": [
        {"name": "Lautaro", "pos": "ST", "rating": 90}, {"name": "Barella", "pos": "CM", "rating": 88},
        {"name": "Bastoni", "pos": "CB", "rating": 87}, {"name": "Sommer", "pos": "GK", "rating": 87},
        {"name": "Calhanoglu", "pos": "CM", "rating": 86}, {"name": "Dimarco", "pos": "LB", "rating": 85},
        {"name": "Pavard", "pos": "CB", "rating": 84}, {"name": "Thuram", "pos": "ST", "rating": 84},
        {"name": "Dumfries", "pos": "RB", "rating": 82}, {"name": "Acerbi", "pos": "CB", "rating": 83},
        {"name": "Mkhitaryan", "pos": "CM", "rating": 83}, {"name": "Zielinski", "pos": "CM", "rating": 83}
    ],
    "PSG": [
        {"name": "Donnarumma", "pos": "GK", "rating": 88}, {"name": "Marquinhos", "pos": "CB", "rating": 87},
        {"name": "Dembele", "pos": "RW", "rating": 86}, {"name": "Hakimi", "pos": "RB", "rating": 85},
        {"name": "Vitinha", "pos": "CM", "rating": 85}, {"name": "Barcola", "pos": "LW", "rating": 82},
        {"name": "Nuno Mendes", "pos": "LB", "rating": 83}, {"name": "Hernandez", "pos": "CB", "rating": 83},
        {"name": "Zaire-Emery", "pos": "CM", "rating": 82}, {"name": "Fabian Ruiz", "pos": "CM", "rating": 82},
        {"name": "Ramos", "pos": "ST", "rating": 81}, {"name": "Pacho", "pos": "CB", "rating": 81}
    ],
    "Atletico Madrid": [
        {"name": "Griezmann", "pos": "ST", "rating": 88}, {"name": "Oblak", "pos": "GK", "rating": 87},
        {"name": "Alvarez", "pos": "ST", "rating": 85}, {"name": "De Paul", "pos": "CM", "rating": 84},
        {"name": "Koke", "pos": "CM", "rating": 82}, {"name": "Gimenez", "pos": "CB", "rating": 83},
        {"name": "Gallagher", "pos": "CM", "rating": 83}, {"name": "Le Normand", "pos": "CB", "rating": 82},
        {"name": "Llorente", "pos": "RB", "rating": 82}, {"name": "Sorloth", "pos": "ST", "rating": 81},
        {"name": "Lino", "pos": "LW", "rating": 81}, {"name": "Azpilicueta", "pos": "CB", "rating": 80}
    ],
    "AC Milan": [
        {"name": "Leao", "pos": "LW", "rating": 87}, {"name": "Theo", "pos": "LB", "rating": 87},
        {"name": "Maignan", "pos": "GK", "rating": 87}, {"name": "Pulisic", "pos": "RW", "rating": 84},
        {"name": "Morata", "pos": "ST", "rating": 83}, {"name": "Reijnders", "pos": "CM", "rating": 82},
        {"name": "Tomori", "pos": "CB", "rating": 83}, {"name": "Bennacer", "pos": "CM", "rating": 81},
        {"name": "Chukwueze", "pos": "RW", "rating": 80}, {"name": "Fofana", "pos": "CM", "rating": 81},
        {"name": "Pavlovic", "pos": "CB", "rating": 79}, {"name": "Emerson", "pos": "RB", "rating": 78}
    ],
    "Juventus": [
        {"name": "Bremer", "pos": "CB", "rating": 86}, {"name": "Vlahovic", "pos": "ST", "rating": 85},
        {"name": "Koopmeiners", "pos": "CM", "rating": 85}, {"name": "Douglas Luiz", "pos": "CM", "rating": 83},
        {"name": "Di Gregorio", "pos": "GK", "rating": 82}, {"name": "Yildiz", "pos": "CM", "rating": 80},
        {"name": "Cambiaso", "pos": "LB", "rating": 80}, {"name": "Danilo", "pos": "CB", "rating": 81},
        {"name": "Nico Gonzalez", "pos": "RW", "rating": 81}, {"name": "Locatelli", "pos": "CM", "rating": 80},
        {"name": "Thuram", "pos": "CM", "rating": 79}, {"name": "Kalulu", "pos": "CB", "rating": 78}
    ],
    "Chelsea": [
        {"name": "Palmer", "pos": "CM", "rating": 86}, {"name": "Enzo", "pos": "CM", "rating": 84},
        {"name": "Caicedo", "pos": "CM", "rating": 83}, {"name": "James", "pos": "RB", "rating": 83},
        {"name": "Nkunku", "pos": "ST", "rating": 84}, {"name": "Jackson", "pos": "ST", "rating": 80},
        {"name": "Cucurella", "pos": "LB", "rating": 81}, {"name": "Colwill", "pos": "CB", "rating": 80},
        {"name": "Neto", "pos": "RW", "rating": 81}, {"name": "Felix", "pos": "LW", "rating": 80},
        {"name": "Sanchez", "pos": "GK", "rating": 78}, {"name": "Fofana", "pos": "CB", "rating": 79}
    ],
    "Man United": [
        {"name": "Bruno", "pos": "CM", "rating": 87}, {"name": "De Ligt", "pos": "CB", "rating": 85},
        {"name": "Onana", "pos": "GK", "rating": 84}, {"name": "Rashford", "pos": "LW", "rating": 81},
        {"name": "Mainoo", "pos": "CM", "rating": 80}, {"name": "Garnacho", "pos": "RW", "rating": 80},
        {"name": "Hojlund", "pos": "ST", "rating": 79}, {"name": "Lisandro", "pos": "CB", "rating": 83},
        {"name": "Mazraoui", "pos": "RB", "rating": 81}, {"name": "Dalot", "pos": "LB", "rating": 81},
        {"name": "Ugarte", "pos": "CM", "rating": 82}, {"name": "Yoro", "pos": "CB", "rating": 78}
    ],
    "Dortmund": [
        {"name": "Kobel", "pos": "GK", "rating": 86}, {"name": "Brandt", "pos": "CM", "rating": 85},
        {"name": "Schlotterbeck", "pos": "CB", "rating": 84}, {"name": "Guirassy", "pos": "ST", "rating": 83},
        {"name": "Sabitzer", "pos": "CM", "rating": 82}, {"name": "Malen", "pos": "RW", "rating": 81},
        {"name": "Adeyemi", "pos": "LW", "rating": 80}, {"name": "Sule", "pos": "CB", "rating": 81},
        {"name": "Ryerson", "pos": "RB", "rating": 79}, {"name": "Can", "pos": "CM", "rating": 80},
        {"name": "Bynoe-Gittens", "pos": "LW", "rating": 78}, {"name": "Anton", "pos": "CB", "rating": 81}
    ],
    "Spurs": [
        {"name": "Son", "pos": "LW", "rating": 87}, {"name": "Maddison", "pos": "CM", "rating": 85},
        {"name": "Romero", "pos": "CB", "rating": 85}, {"name": "Vicario", "pos": "GK", "rating": 83},
        {"name": "Porro", "pos": "RB", "rating": 82}, {"name": "Van de Ven", "pos": "CB", "rating": 82},
        {"name": "Kulusevski", "pos": "RW", "rating": 81}, {"name": "Solanke", "pos": "ST", "rating": 81},
        {"name": "Bissouma", "pos": "CM", "rating": 80}, {"name": "Udogie", "pos": "LB", "rating": 81},
        {"name": "Sarr", "pos": "CM", "rating": 79}, {"name": "Bentancur", "pos": "CM", "rating": 79}
    ],
    "Napoli": [
        {"name": "Kvaratskhelia", "pos": "LW", "rating": 86}, {"name": "Lukaku", "pos": "ST", "rating": 82},
        {"name": "Di Lorenzo", "pos": "RB", "rating": 83}, {"name": "Lobotka", "pos": "CM", "rating": 84},
        {"name": "Anguissa", "pos": "CM", "rating": 82}, {"name": "Rrahmani", "pos": "CB", "rating": 81},
        {"name": "Meret", "pos": "GK", "rating": 80}, {"name": "McTominay", "pos": "CM", "rating": 80},
        {"name": "Neres", "pos": "RW", "rating": 80}, {"name": "Olivera", "pos": "LB", "rating": 79},
        {"name": "Buongiorno", "pos": "CB", "rating": 81}, {"name": "Politano", "pos": "RW", "rating": 79}
    ],
    "Aston Villa": [
        {"name": "Martinez", "pos": "GK", "rating": 87}, {"name": "Watkins", "pos": "ST", "rating": 84},
        {"name": "Tielemans", "pos": "CM", "rating": 82}, {"name": "Bailey", "pos": "RW", "rating": 82},
        {"name": "McGinn", "pos": "CM", "rating": 81}, {"name": "Konsa", "pos": "CB", "rating": 81},
        {"name": "Torres", "pos": "CB", "rating": 82}, {"name": "Onana", "pos": "CM", "rating": 80},
        {"name": "Digne", "pos": "LB", "rating": 79}, {"name": "Maatsen", "pos": "LB", "rating": 79},
        {"name": "Cash", "pos": "RB", "rating": 78}, {"name": "Rogers", "pos": "CM", "rating": 77}
    ],
    "RB Leipzig": [
        {"name": "Simons", "pos": "CM", "rating": 85}, {"name": "Openda", "pos": "ST", "rating": 84},
        {"name": "Orban", "pos": "CB", "rating": 82}, {"name": "Gulacsi", "pos": "GK", "rating": 81},
        {"name": "Raum", "pos": "LB", "rating": 80}, {"name": "Lukeba", "pos": "CB", "rating": 81},
        {"name": "Haidara", "pos": "CM", "rating": 80}, {"name": "Henrichs", "pos": "RB", "rating": 79},
        {"name": "Sesko", "pos": "ST", "rating": 81}, {"name": "Schlager", "pos": "CM", "rating": 81},
        {"name": "Geertruida", "pos": "CB", "rating": 80}, {"name": "Nusa", "pos": "LW", "rating": 77}
    ],
    "Sporting": [
        {"name": "Gyokeres", "pos": "ST", "rating": 86}, {"name": "Goncalves", "pos": "CM", "rating": 82},
        {"name": "Hjulmand", "pos": "CM", "rating": 81}, {"name": "Inacio", "pos": "CB", "rating": 81},
        {"name": "Diomande", "pos": "CB", "rating": 80}, {"name": "Trincao", "pos": "RW", "rating": 80},
        {"name": "Quenda", "pos": "RW", "rating": 75}, {"name": "Debast", "pos": "CB", "rating": 78},
        {"name": "Catamo", "pos": "RB", "rating": 77}, {"name": "Israel", "pos": "GK", "rating": 76},
        {"name": "Morita", "pos": "CM", "rating": 79}, {"name": "Harder", "pos": "ST", "rating": 74}
    ],
    "Benfica": [
        {"name": "Di Maria", "pos": "RW", "rating": 83}, {"name": "Pavlidis", "pos": "ST", "rating": 81},
        {"name": "Kokcu", "pos": "CM", "rating": 82}, {"name": "Otamendi", "pos": "CB", "rating": 81},
        {"name": "Trubin", "pos": "GK", "rating": 82}, {"name": "Aursnes", "pos": "CM", "rating": 81},
        {"name": "Silva", "pos": "CB", "rating": 80}, {"name": "Bah", "pos": "RB", "rating": 79},
        {"name": "Akturkoglu", "pos": "LW", "rating": 80}, {"name": "Florentino", "pos": "CM", "rating": 79},
        {"name": "Beste", "pos": "LB", "rating": 78}, {"name": "Barreiro", "pos": "CM", "rating": 78}
    ],
    "Porto": [
        {"name": "Diogo Costa", "pos": "GK", "rating": 84}, {"name": "Galeno", "pos": "LW", "rating": 82},
        {"name": "Varela", "pos": "CM", "rating": 80}, {"name": "Omorodion", "pos": "ST", "rating": 78},
        {"name": "Nico", "pos": "CM", "rating": 78}, {"name": "Pepe", "pos": "RW", "rating": 80},
        {"name": "Otavio", "pos": "CB", "rating": 77}, {"name": "Moura", "pos": "LB", "rating": 76},
        {"name": "Nehuen Perez", "pos": "CB", "rating": 77}, {"name": "Joao Mario", "pos": "RB", "rating": 78},
        {"name": "Grujic", "pos": "CM", "rating": 76}, {"name": "Eustaquio", "pos": "CM", "rating": 77}
    ],
    "Roma": [
        {"name": "Dybala", "pos": "ST", "rating": 86}, {"name": "Pellegrini", "pos": "CM", "rating": 82},
        {"name": "Mancini", "pos": "CB", "rating": 81}, {"name": "Svilar", "pos": "GK", "rating": 80},
        {"name": "Cristante", "pos": "CM", "rating": 81}, {"name": "Ndicka", "pos": "CB", "rating": 80},
        {"name": "Angelino", "pos": "LB", "rating": 79}, {"name": "Dovbyk", "pos": "ST", "rating": 82},
        {"name": "Soule", "pos": "RW", "rating": 78}, {"name": "Hermoso", "pos": "CB", "rating": 81},
        {"name": "Kone", "pos": "CM", "rating": 79}, {"name": "Saelemaekers", "pos": "RW", "rating": 77}
    ],
    "Girona": [
        {"name": "Tsygankov", "pos": "RW", "rating": 82}, {"name": "Miguel", "pos": "LB", "rating": 81},
        {"name": "Blind", "pos": "CB", "rating": 80}, {"name": "Gazzaniga", "pos": "GK", "rating": 79},
        {"name": "Yangel Herrera", "pos": "CM", "rating": 80}, {"name": "Ivan Martin", "pos": "CM", "rating": 80},
        {"name": "Misehouy", "pos": "CM", "rating": 74}, {"name": "Asprilla", "pos": "RW", "rating": 76},
        {"name": "Danjuma", "pos": "LW", "rating": 78}, {"name": "Romeu", "pos": "CM", "rating": 78},
        {"name": "David Lopez", "pos": "CB", "rating": 79}, {"name": "Abel Ruiz", "pos": "ST", "rating": 76}
    ]
}

def get_best_11(selected_clubs):
    pool = []
    for club in selected_clubs:
        if club in GLOBAL_CLUBS:
            pool.extend(GLOBAL_CLUBS[club])
    
    # Сортировка по убыванию рейтинга
    pool.sort(key=lambda x: x['rating'], reverse=True)
    
    # Схема состава
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
        
        # Добавление игрока в ОБЩУЮ базу
        if action == 'add_player':
            club_name = request.form.get('new_club_name')
            p_name = request.form.get('p_name')
            p_pos = request.form.get('p_pos')
            p_rating = int(request.form.get('p_rating', 80))
            
            if club_name not in GLOBAL_CLUBS:
                GLOBAL_CLUBS[club_name] = []
            GLOBAL_CLUBS[club_name].append({"name": p_name, "pos": p_pos, "rating": p_rating})

        # Создание менеджера ТОЛЬКО для себя
        elif action == 'create':
            name = request.form.get('manager_name')
            clubs = request.form.getlist('clubs')
            team = get_best_11(clubs)
            if team:
                avg = sum(p['rating'] for p in team) / len(team)
                temp = session['my_managers'].copy()
                temp[name] = {'name': name, 'rating': round(avg, 1)}
                session['my_managers'] = temp
                session.modified = True
                
        # Матч между менеджерами из СВОЕГО списка
        elif action == 'match':
            m1_name = request.form.get('manager1')
            m2_name = request.form.get('manager2')
            managers = session.get('my_managers', {})
            if m1_name in managers and m2_name in managers and m1_name != m2_name:
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
