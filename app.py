# app.py
from flask import Flask, render_template, redirect, url_for, session
from ai_logic import AttackAI, DefenseAI
import random
import json
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'supersecret'  # セッションのためのキー（何でもOK）

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start')
def start():
    # セッション初期化
    session['turn'] = 1
    session['score'] = 0
    session['attack_power'] = 100
    session['log'] = []
    session['attacker'] = AttackAI().__dict__
    session['defender'] = DefenseAI().__dict__
    return redirect(url_for('battle'))

@app.route('/battle')
def battle():
    # 最大ターン数
    MAX_TURN = 10
    WIN_SCORE = 100

    # セッションデータ取得
    turn = session.get('turn', 1)
    score = session.get('score', 0)
    attack_power = session.get('attack_power', 100)
    log = session.get('log', [])

    # AI初期化（セッションから）
    attacker = AttackAI()
    attacker.__dict__.update(session['attacker'])
    defender = DefenseAI()
    defender.__dict__.update(session['defender'])

    if turn > MAX_TURN or score >= WIN_SCORE or attack_power <= 0:
        return redirect(url_for('result'))

    attack = attacker.choose_attack()
    defense = defender.choose_defense()

    attack_success = attack['success_rate'] > random.random()
    defense_success = defense['success_rate'] > random.random()

    if attack_success and not defense_success:
        score += attack['score']
        result = "攻撃成功"
        result_icon = "🎯"
        result_type = "attack"
        color = "red"
    elif not attack_success and defense_success:
        attack_power -= 20
        result = "防御成功"
        result_icon = "🛡"
        result_type = "defense"
        color = "blue"
    else:
        result = "拮抗"
        result_icon = "⚔"
        result_type = "draw"
        color = "gray"

    log.append({
        "turn": turn,
        "attack": attack["name"],
        "defense": defense["name"],
        "result": result,
        "result_icon": result_icon,
        "result_type": result_type,
        "color": color,
        "score": score,
        "attack_power": attack_power
    })

    # 成長記録
    attacker.record_result(attack["name"], attack_success)
    defender.record_attack(attack["name"])
    if defense_success:
        defender.record_result(defense["name"], True)

    # セッション更新
    session['turn'] = turn + 1
    session['score'] = score
    session['attack_power'] = attack_power
    session['log'] = log
    session['attacker'] = attacker.__dict__
    session['defender'] = defender.__dict__

    return render_template("battle.html", log=log)

@app.route('/result')
def result():
    score = session.get('score', 0)
    attack_power = session.get('attack_power', 100)
    log = session.get('log', [])
    if score >= 100:
        final_result = "🎉 攻撃AIの勝利！"
    elif attack_power <= 0:
        final_result = "🛡 防御AIの勝利！（攻撃AI力尽きる）"
    else:
        final_result = "🕒 防御AIの勝利！（10ターン耐久）"
    save_battle_log(log, final_result)    
    return render_template("result.html", result=final_result)

def save_battle_log(log, final_result, filename="log.txt"):
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "battle_log": log,
        "final_result": final_result
    }
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False))
        f.write("\n")  # 1試合ごとに改行して追記

@app.route('/stats')
def stats():
    # ログを全件読み込む
    battles = []
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            for line in f:
                battles.append(json.loads(line))
    except FileNotFoundError:
        return render_template("stats.html", stats=None)

    # 集計処理
    total_games = len(battles)
    attack_wins = sum(1 for b in battles if "攻撃AI" in b["final_result"])
    defense_wins = total_games - attack_wins
    avg_score = sum(b["battle_log"][-1]["score"] for b in battles) / total_games

    stats = {
        "total_games": total_games,
        "attack_wins": attack_wins,
        "defense_wins": defense_wins,
        "avg_score": round(avg_score, 1)
    }
    return render_template("stats.html", stats=stats)

if __name__ == "__main__":
    app.run(debug=True)
