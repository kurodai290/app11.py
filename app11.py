import random
import time

def print_status(depth, hull, max_hull, oxygen, fuel, credits, torpedoes):
    print("\n" + "="*45)
    print(f" 🌊 深度: {depth}m / 1000m  |  💰 資金: {credits} Cr  |  🚀 魚雷: {torpedoes}発")
    print(f" ❤️ 船体: {hull}/{max_hull}% | 🫁 酸素: {oxygen}% | ⛽ 燃料: {fuel}%")
    print("="*45)

def shop_phase(hull, max_hull, oxygen, fuel, credits, torpedoes):
    print("\n🏪 【深海補給基地にドックインしました】 🏪")
    while True:
        print(f"\n現在の所持金: {credits} Cr")
        print(f"1: 🛠️ 船体修理 (30Cr) -> 耐久度+30 (現在: {hull}/{max_hull}%)")
        print(f"2: 🫁 酸素充填 (20Cr) -> 酸素+40 (現在: {oxygen}%)")
        print(f"3: ⛽ 燃料補給 (20Cr) -> 燃料+40 (現在: {fuel}%)")
        print(f"4: 🛡️ 装甲強化 (50Cr) -> 最大耐久度+20 (現在: {max_hull}%)")
        print(f"5: 🚀 魚雷購入 (25Cr) -> 魚雷+1発 (現在: {torpedoes}発)")
        print("6: 🚪 ショップを出て潜行を再開する")
        
        choice = input("購入する番号を入力 (1-6): ")
        
        if choice == '1' and credits >= 30:
            credits -= 30
            hull = min(max_hull, hull + 30)
            print("修理完了！")
        elif choice == '2' and credits >= 20:
            credits -= 20
            oxygen = min(100, oxygen + 40)
            print("酸素充填完了！")
        elif choice == '3' and credits >= 20:
            credits -= 20
            fuel = min(100, fuel + 40)
            print("燃料補給完了！")
        elif choice == '4' and credits >= 50:
            credits -= 50
            max_hull += 20
            hull += 20
            print("装甲強化完了！")
        elif choice == '5' and credits >= 25:
            credits -= 25
            torpedoes += 1
            print("魚雷を1発装填しました！")
        elif choice == '6':
            print("🚢 潜行を再開します。")
            break
        else:
            print("❌ クレジットが足りないか、無効な入力です。")
            
    return hull, max_hull, oxygen, fuel, credits, torpedoes

def battle_event(hull, fuel, torpedoes, credits):
    enemy = random.choice(["リュウグウノツカイ", "チョウチンアンコウ", "ダイオウグソクムシ"])
    print(f"\n⚠️ 警告！ 前方に敵モブ【{enemy}】を感知！")
    
    while True:
        print(f"どうする？ (魚雷残弾: {torpedoes}発)")
        print("1: 🚀 魚雷発射（魚雷-1、確実に撃破して報酬獲得）")
        print("2: 🏃 急速回避（燃料-15、50%の確率で無傷で逃亡）")
        
        choice = input("行動を選択 (1-2): ")
        
        if choice == '1':
            if torpedoes > 0:
                torpedoes -= 1
                reward = random.randint(20, 40)
                credits += reward
                print(f"💥 魚雷命中！【{enemy}】を撃破した！報酬 {reward} Cr 獲得。")
                break
            else:
                print("❌ 魚雷がありません！他の行動を選んでください。")
        elif choice == '2':
            fuel -= 15
            if random.random() < 0.5:
                print("💨 急速回避成功！ 敵を振り切った。")
            else:
                damage = random.randint(20, 35)
                hull -= damage
                print(f"💥 回避失敗！ 敵の体当たりを受け、船体に {damage}% のダメージ！")
            break
        else:
            print("❌ 無効な入力です。")
            
    return hull, fuel, torpedoes, credits

def boss_battle(hull, torpedoes):
    print("\n🚨 🚨 🚨 EMERGENCY 🚨 🚨 🚨")
    print("深度900m：巨大な影が潜水艦に迫る...！")
    print("深海の支配者【巨大ダイオウイカ】が出現！！")
    time.sleep(1.5)
    
    boss_hp = 3
    
    while boss_hp > 0 and hull > 0:
        print(f"\n🦑 ダイオウイカの残り体力: {'🔴' * boss_hp}")
        print(f"❤️ 潜水艦の耐久度: {hull}%  |  🚀 魚雷: {torpedoes}発")
        print("1: 🚀 魚雷で攻撃する（魚雷-1、ボスに1ダメージ）")
        print("2: 🛡️ 防御体勢をとる（受けるダメージを半減）")
        
        choice = input("行動を選択 (1-2): ")
        
        # ボスの攻撃準備
        boss_attack = random.choice(["💵 触手叩きつけ", "🌪️ 大うずまき"])
        print(f"\n🦑 ダイオウイカの 【{boss_attack}】！")
        
        base_damage = random.randint(20, 35)
        
        if choice == '1':
            if torpedoes > 0:
                torpedoes -= 1
                boss_hp -= 1
                hull -= base_damage
                print(f"🚀 魚雷命中！ ボスに1ダメージ！")
                print(f"💥 同時に攻撃を受け、船体に {base_damage}% のダメージ！")
            else:
                print("❌ 魚雷がない！ 攻撃できず、無防備に攻撃を喰らった！")
                hull -= base_damage
                print(f"💥 船体に {base_damage}% のダメージ！")
        elif choice == '2':
            reduced_damage = base_damage // 2
            hull -= reduced_damage
            print(f"🛡️ 防御成功！ ダメージを軽減し、船体に {reduced_damage}% のダメージ！")
        else:
            print("❌ 選択に迷い、直撃を受けた！")
            hull -= base_damage
            print(f"💥 船体に {base_damage}% のダメージ！")
            
        time.sleep(1)
        
    return hull, torpedoes, boss_hp <= 0

def main():
    print("🚢 【深海サバイバル：DEPTH 完全版】 🚢")
    print("魚雷を積み込み、敵モブを退け、900mに潜むボスを撃破せよ！")
    
    depth, max_hull, hull, oxygen, fuel, credits, torpedoes = 0, 100, 100, 100, 100, 30, 2
    shop_400, shop_800, boss_defeated = False, False, False
    
    while depth < 1000:
        # ショップ判定
        if depth >= 400 and not shop_400:
            hull, max_hull, oxygen, fuel, credits, torpedoes = shop_phase(hull, max_hull, oxygen, fuel, credits, torpedoes)
            shop_400 = True
        elif depth >= 800 and not shop_800:
            hull, max_hull, oxygen, fuel, credits, torpedoes = shop_phase(hull, max_hull, oxygen, fuel, credits, torpedoes)
            shop_800 = True

        # ボス戦判定
        if depth >= 900 and not boss_defeated:
            hull, torpedoes, success = boss_battle(hull, torpedoes)
            if success:
                print("\n🏆 奇跡だ！ 巨大ダイオウイカの撃破に成功した！ 最深部への道が開かれた！")
                boss_defeated = True
                depth = 900  # 深度を900mに固定して再開
            else:
                break # ループを抜けてゲームオーバーへ

        if hull <= 0 or oxygen <= 0 or fuel <= 0:
            break

        print_status(depth, hull, max_hull, oxygen, fuel, credits, torpedoes)
        print("行動を選択してください:")
        print("1: 通常潜行（燃料-10, 酸素-5, 深度+100m, +15Cr、敵遭遇率：中）")
        print("2: 急速潜行（燃料-20, 酸素-10, 深度+200m, +25Cr、敵遭遇率：高）")
        print("3: 資源探索（燃料-5, 酸素-15, 🕳️ノーリスク、アイテム発見チャンス）")
        
        choice = input("番号を入力 (1-3): ")
        
        if choice == '1':
            fuel, oxygen, depth, credits = fuel - 10, oxygen - 5, depth + 100, credits + 15
            event_chance, is_battle = 0.3, True
        elif choice == '2':
            fuel, oxygen, depth, credits = fuel - 20, oxygen - 10, depth + 200, credits + 25
            event_chance, is_battle = 0.6, True
        elif choice == '3':
            fuel, oxygen = fuel - 5, oxygen - 15
            event_chance, is_battle = 0.0, False
            
            search = random.choice(["treasure", "fuel", "nothing"])
            if search == "treasure":
                earn = random.randint(40, 70)
                credits += earn
                print(f"💎 沈没船を発見！ {earn} Cr を獲得！")
            elif search == "fuel":
                recover = random.randint(20, 40)
                fuel = min(100, fuel + recover)
                print(f"🔋 燃料タンクを発見！燃料が {recover}% 回復！")
            else:
                print("🕳️ 何も見つからなかった。")
        else:
            print("❌ 無効な入力です。酸素を浪費した（酸素-5）")
            oxygen -= 5
            continue

        # アクシデント・戦闘発生判定
        if event_chance > 0 and random.random() < event_chance:
            time.sleep(0.5)
            if is_battle and random.random() < 0.6:  # イベントの6割は戦闘
                hull, fuel, torpedoes, credits = battle_event(hull, fuel, torpedoes, credits)
            else:  # 残り4割は環境トラップ
                event = random.choice(["current", "leak"])
                if event == "current":
                    loss = random.randint(15, 25)
                    fuel -= loss
                    print(f"⚠️ 激しい熱水噴出流に遭遇！燃料を {loss}% 喪失！")
                elif event == "leak":
                    loss = random.randint(15, 25)
                    oxygen -= loss
                    print(f"⚠️ 酸素漏出発生！酸素が {loss}% 減少！")

        # ゲームオーバー判定
        if hull <= 0:
            print("\n💥 船体が圧壊した... GAME OVER")
            break
        if oxygen <= 0:
            print("\n💀 酸素が尽きた... GAME OVER")
            break
        if fuel <= 0:
            print("\n⚓ 燃料が尽き、沈没した... GAME OVER")
            break
            
        time.sleep(1)

    # クリア判定
    if depth >= 1000 and hull > 0 and oxygen > 0 and fuel > 0:
        print_status(depth, hull, max_hull, oxygen, fuel, credits, torpedoes)
        print("\n🎉 🎉 🎉 完全クリア！ 🎉 🎉 🎉")
        print("潜水艦は未知の深海1,000mを制覇し、無事に帰還した！")

if __name__ == "__main__":
    main()
