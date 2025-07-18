# main.py
from ai_logic import AttackAI, DefenseAI
from colorama import Fore, Style, init
import random
import json

init(autoreset=True)

# 初期値
MAX_TURN = 10
WIN_SCORE = 100
turn = 1
score = 0
attack_power = 100

# ログリスト
battle_log = []

# AIインスタンス
attacker = AttackAI()
defender = DefenseAI()

print("=== セキュリティAIバトル・構造化ログ開始 ===\n")

while turn <= MAX_TURN and score < WIN_SCORE and attack_power > 0:
    print(f"\n--- 第{turn}ターン ---")
    
    attack = attacker.choose_attack()
    defense = defender.choose_defense()

    # 判定処理
    attack_success = attack['success_rate'] > random.random()
    defense_success = defense['success_rate'] > random.random()

    # 結果処理（独自ロジック含む）
    if attack_success and not defense_success:
        score += attack['score']
        result = "攻撃成功"
        result_icon = "🎯"
        print(Fore.RED + f"{result_icon} {result}！スコア +{attack['score']}（合計: {score}）")
    elif not attack_success and defense_success:
        attack_power -= 20
        result = "防御成功"
        result_icon = "🛡"
        print(Fore.BLUE + f"{result_icon} {result}！攻撃AIの攻撃力 -20（残り: {attack_power}）")
    else:
        result = "拮抗"
        result_icon = "⚔"
        print(Fore.YELLOW + f"{result_icon} 両者拮抗。状況変わらず。")

    # ログ辞書作成
    log = {
        "turn": turn,
        "attack_ai": attack['name'],
        "defense_ai": defense['name'],
        "result": result,
        "result_icon": result_icon,
        "result_type": "attack",
        "color": "red",  
        "score": score,
        "attack_power": attack_power
    }
    battle_log.append(log)

    # 学習履歴
    attacker.record_result(attack["name"], attack_success)
    defender.record_attack(attack["name"])

    turn += 1

# 勝敗判定
if score >= WIN_SCORE:
    final_result = "🎉 攻撃AIの勝利！重要情報を奪取！"
elif attack_power <= 0:
    final_result = "🛡 防御AIの勝利！攻撃者は力尽きた！"
else:
    final_result = "🕒 防御AIの勝利！全ターン守りきった！"

print("\n=== バトル終了 ===")
print(Style.BRIGHT + final_result)

# 最終ログに追加
battle_log.append({"final_result": final_result})

# バトルログをファイルに保存
def save_log(log_data, filename="log.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for entry in log_data:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")  # 1行ずつ書く形式（後で読みやすく）

# 最後にログ保存
save_log(battle_log)
print(Fore.GREEN + "📁 バトルログを log.txt に保存しました。")

# 成功時にスキル成長させる
if attack_success:
    attacker.record_result(attack["name"], True)
else:
    attacker.record_result(attack["name"], False)

if defense_success:
    defender.record_result(defense["name"], True)

