
import random

# 攻撃AIクラス
class AttackAI:
    def __init__(self):
        self.attacks = [
            {"name": "ポートスキャン", "success_rate": 0.9, "score": 10},
            {"name": "ブルートフォース", "success_rate": 0.6, "score": 20},
            {"name": "SQLインジェクション", "success_rate": 0.7, "score": 30},
            {"name": "ゼロデイ攻撃", "success_rate": 0.4, "score": 50},
        ]
        self.history = []  # 攻撃履歴

    def choose_attack(self):
        if self.history:
            weights = []
            for atk in self.attacks:
                 success_count = sum(1 for h in self.history if h['name'] == atk['name'] and h['success'])
                 weights.append(success_count + 1)
            return random.choices(self.attacks, weights=weights)[0]
        return random.choice(self.attacks)

    def record_result(self, attack_name, success):
        self.history.append({"name": attack_name, "success": success})
        if success:
            for atk in self.attacks:
                if atk["name"] == attack_name:
                    atk["success_rate"] = min(atk["success_rate"] + 0.01, 0.99)

# 防御AIクラス
class DefenseAI:
    def __init__(self):
        self.defenses = [
            {"name": "ファイアウォール設定", "success_rate": 0.85, "counter": "ポートスキャン"},
            {"name": "ログ監視", "success_rate": 0.6, "counter": "SQLインジェクション"},
            {"name": "アカウントロック", "success_rate": 0.65, "counter": "ブルートフォース"},
            {"name": "アップデート適用", "success_rate": 0.3, "counter": "ゼロデイ攻撃"},
        ]
        self.attack_log = []

    def choose_defense(self):
        if self.attack_log:
            recent = self.attack_log[-1]
            for defense in self.defenses:
                if defense["counter"] == recent:
                    return defense
        return random.choice(self.defenses)

    def record_attack(self, attack_name):
        self.attack_log.append(attack_name)

    def record_result(self, defense_name, success):
        if success:
            for d in self.defenses:
                if d["name"] == defense_name:
                    d["success_rate"] = min(d["success_rate"] + 0.01, 0.99)    

