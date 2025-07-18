# simulation.py
from ai_logic import AttackAI, DefenseAI
import random

def simulate_battle(verbose=False):
    MAX_TURN = 10
    WIN_SCORE = 100
    score = 0
    attack_power = 100
    turn = 1

    attacker = AttackAI()
    defender = DefenseAI()

    while turn <= MAX_TURN and score < WIN_SCORE and attack_power > 0:
        attack = attacker.choose_attack()
        defense = defender.choose_defense()

        attack_success = attack['success_rate'] > random.random()
        defense_success = defense['success_rate'] > random.random()

        if attack_success and not defense_success:
            score += attack['score']
            result = "attack_win"
            result_type = "attack"
            result_icon = "🎯"
            color = "red"
        elif not attack_success and defense_success:
            attack_power -= 20
            result = "defense_win"
            result_type = "defense"
            result_icon = "🛡" 
            color = "blue"
        else:
            result = "draw"
            result_type = "draw"
            result_icon = "⚔"
            color = "gray"

        attacker.record_result(attack["name"], attack_success)
        defender.record_attack(attack["name"])

        turn += 1

    if score >= WIN_SCORE:
        return "attack", score
    elif attack_power <= 0:
        return "defense", score
    else:
        return "defense", score

def run_simulation(trials=100):
    result_counter = {"attack": 0, "defense": 0}
    total_score = 0

    for i in range(trials):
        winner, score = simulate_battle()
        result_counter[winner] += 1
        total_score += score

    print("=== 結果 ===")
    print(f"試行回数: {trials}")
    print(f"攻撃AIの勝利: {result_counter['attack']}回")
    print(f"防御AIの勝利: {result_counter['defense']}回")
    print(f"攻撃AIの勝率: {result_counter['attack'] / trials * 100:.1f}%")
    print(f"平均スコア: {total_score / trials:.1f}")

if __name__ == "__main__":
    run_simulation(100)  # ← 回数は好きに変えてOK
