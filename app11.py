import random
import streamlit as st

# アプリのタイトル
st.title("🚢 【深海サバイバル：DEPTH 完全版】")
st.caption("資源を管理し、補給基地で潜水艦を強化しながら1,000mの底を目指せ！")

# セッション状態（ゲームデータ）の初期化
if "game_over" not in st.session_state:
    st.session_state.depth = 0
    st.session_state.max_hull = 100
    st.session_state.hull = 100
    st.session_state.oxygen = 100
    st.session_state.fuel = 100
    st.session_state.credits = 30
    st.session_state.torpedoes = 2
    st.session_state.shop_400 = False
    st.session_state.shop_800 = False
    st.session_state.boss_defeated = False
    st.session_state.game_over = False
    st.session_state.game_clear = False
    st.session_state.log = ["ゲームを開始しました。"]
    st.session_state.mode = "action" # action, shop, battle, boss
    st.session_state.current_enemy = ""
    st.session_state.boss_hp = 3

# リセットボタン
if st.button("ゲームをリセット"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ステータス表示
st.sidebar.header("📊 潜水艦ステータス")
st.sidebar.metric("🌊 深度", f"{st.session_state.depth}m / 1000m")
st.sidebar.metric("💰 資金", f"{st.session_state.credits} Cr")
st.sidebar.metric("🚀 魚雷", f"{st.session_state.torpedoes} 発")
st.sidebar.progress(max(0, min(100, int(st.session_state.hull / st.session_state.max_hull * 100))), f"❤️ 船体: {st.session_state.hull}/{st.session_state.max_hull}%")
st.sidebar.progress(max(0, min(100, st.session_state.oxygen)), f"🫁 酸素: {st.session_state.oxygen}%")
st.sidebar.progress(max(0, min(100, st.session_state.fuel)), f"⛽ 燃料: {st.session_state.fuel}%")

# ゲームオーバー・クリア判定
if st.session_state.hull <= 0 and not st.session_state.game_over:
    st.session_state.log.append("💥 船体が圧壊した... GAME OVER")
    st.session_state.game_over = True
if st.session_state.oxygen <= 0 and not st.session_state.game_over:
    st.session_state.log.append("💀 酸素が尽きた... GAME OVER")
    st.session_state.game_over = True
if st.session_state.fuel <= 0 and not st.session_state.game_over:
    st.session_state.log.append("⚓ 燃料が尽き、沈没した... GAME OVER")
    st.session_state.game_over = True
if st.session_state.depth >= 1000 and not st.session_state.game_over:
    st.session_state.game_clear = True

# メイン画面の処理分岐
if st.session_state.game_over:
    st.error("💀 ゲームオーバー")
elif st.session_state.game_clear:
    st.success("🎉 完全クリア！潜水艦は未知の深海1,000mを制覇し、無事に帰還した！")
else:
    # 深度イベントチェック
    if st.session_state.depth >= 400 and not st.session_state.shop_400:
        st.session_state.mode = "shop"
    elif st.session_state.depth >= 800 and not st.session_state.shop_800:
        st.session_state.mode = "shop"
    elif st.session_state.depth >= 900 and not st.session_state.boss_defeated:
        st.session_state.mode = "boss"

    # --- モード1: 通常アクション ---
    if st.session_state.mode == "action":
        st.subheader("現在の行動を選択してください")
        
        col1, col2, col3 = st.columns(3)
        if col1.button("通常潜行\n(燃料-10,酸素-5,深度+100m)"):
            st.session_state.fuel -= 10
            st.session_state.oxygen -= 5
            st.session_state.depth += 100
            st.session_state.credits += 15
            st.session_state.log.append("🚢 通常潜行しました。(深度+100m)")
            if random.random() < 0.3:
                if random.random() < 0.6:
                    st.session_state.mode = "battle"
                    st.session_state.current_enemy = random.choice(["リュウグウノツカイ", "チョウチンアンコウ", "ダイオウグソクムシ"])
                else:
                    event = random.choice(["current", "leak"])
                    if event == "current":
                        loss = random.randint(15, 25)
                        st.session_state.fuel -= loss
                        st.session_state.log.append(f"⚠️ 熱水噴出流に遭遇！燃料を {loss}% 喪失！")
                    else:
                        loss = random.randint(15, 25)
                        st.session_state.oxygen -= loss
                        st.session_state.log.append(f"⚠️ 酸素漏出発生！酸素が {loss}% 減少！")
            st.rerun()

        if col2.button("急速潜行\n(燃料-20,酸素-10,深度+200m)"):
            st.session_state.fuel -= 20
            st.session_state.oxygen -= 10
            st.session_state.depth += 200
            st.session_state.credits += 25
            st.session_state.log.append("🚀 急速潜行しました。(深度+200m)")
            if random.random() < 0.6:
                if random.random() < 0.6:
                    st.session_state.mode = "battle"
                    st.session_state.current_enemy = random.choice(["リュウグウノツカイ", "チョウチンアンコウ", "ダイオウグソクムシ"])
                else:
                    # トラップイベント
                    loss = random.randint(15, 25)
                    st.session_state.fuel -= loss
                    st.session_state.log.append(f"⚠️ トラップ遭遇！燃料を {loss}% 喪失！")
            st.rerun()

        if col3.button("資源探索\n(燃料-5,酸素-15,ノーリスク)"):
            st.session_state.fuel -= 5
            st.session_state.oxygen -= 15
            search = random.choice(["treasure", "fuel", "nothing"])
            if search == "treasure":
                earn = random.randint(40, 70)
                st.session_state.credits += earn
                st.session_state.log.append(f"💎 沈没船を発見！ {earn} Cr を獲得！")
            elif search == "fuel":
                recover = random.randint(20, 40)
                st.session_state.fuel = min(100, st.session_state.fuel + recover)
                st.session_state.log.append(f"🔋 燃料タンクを発見！燃料が {recover}% 回復！")
            else:
                st.session_state.log.append("🕳️ 何も見つからなかった。")
            st.rerun()

    # --- モード2: ショップ ---
    elif st.session_state.mode == "shop":
        st.subheader("🏪 深海補給基地にドックインしました")
        st.write(f"所持金: {st.session_state.credits} Cr")
        
        c1, c2, c3, c4, c5 = st.columns(5)
        if c1.button("船体修理 (30Cr)") and st.session_state.credits >= 30:
            st.session_state.credits -= 30
            st.session_state.hull = min(st.session_state.max_hull, st.session_state.hull + 30)
            st.rerun()
        if c2.button("酸素充填 (20Cr)") and st.session_state.credits >= 20:
            st.session_state.credits -= 20
            st.session_state.oxygen = min(100, st.session_state.oxygen + 40)
            st.rerun()
        if c3.button("燃料補給 (20Cr)") and st.session_state.credits >= 20:
            st.session_state.credits -= 20
            st.session_state.fuel = min(100, st.session_state.fuel + 40)
            st.rerun()
        if c4.button("装甲強化 (50Cr)") and st.session_state.credits >= 50:
            st.session_state.credits -= 50
            st.session_state.max_hull += 20
            st.session_state.hull += 20
            st.rerun()
        if c5.button("魚雷購入 (25Cr)") and st.session_state.credits >= 25:
            st.session_state.credits -= 25
            st.session_state.torpedoes += 1
            st.rerun()
            
        if st.button("🚪 ショップを出て潜行を再開する"):
            if st.session_state.depth >= 800:
                st.session_state.shop_800 = True
            else:
                st.session_state.shop_400 = True
            st.session_state.mode = "action"
            st.rerun()

    # --- モード3: 敵モブ戦 ---
    elif st.session_state.mode == "battle":
        st.subheader(f"⚠️ 敵モブ【{st.session_state.current_enemy}】が出現！")
        
        if st.button("🚀 魚雷発射 (魚雷-1)"):
            if st.session_state.torpedoes > 0:
                st.session_state.torpedoes -= 1
                reward = random.randint(20, 40)
                st.session_state.credits += reward
                st.session_state.log.append(f"💥 魚雷命中！【{st.session_state.current_enemy}】を撃破！ 報酬 {reward} Cr")
                st.session_state.mode = "action"
                st.rerun()
            else:
                st.warning("魚雷がありません！")
                
        if st.button("🏃 急速回避 (燃料-15, 確率50%)"):
            st.session_state.fuel -= 15
            if random.random() < 0.5:
                st.session_state.log.append("💨 急速回避成功！ 敵を振り切った。")
            else:
                damage = random.randint(20, 35)
                st.session_state.hull -= damage
                st.session_state.log.append(f"💥 回避失敗！ 船体に {damage}% のダメージ！")
            st.session_state.mode = "action"
            st.rerun()

    # --- モード4: ボス戦 ---
    elif st.session_state.mode == "boss":
        st.subheader("🚨 EMERGENCY: 深海の支配者【巨大ダイオウイカ】襲来！")
        st.write(f"ボスの残り体力: {'🔴' * st.session_state.boss_hp}")
        
        b1, b2 = st.columns(2)
        if b1.button("🚀 魚雷で攻撃する (魚雷-1)"):
            base_damage = random.randint(20, 35)
            if st.session_state.torpedoes > 0:
                st.session_state.torpedoes -= 1
                st.session_state.boss_hp -= 1
                st.session_state.hull -= base_damage
                st.session_state.log.append(f"🚀 魚雷命中！ボスに1ダメ。反撃で {base_damage}% ダメージを受けた。")
            else:
                st.session_state.hull -= base_damage
                st.session_state.log.append(f"❌ 魚雷がない！無防備な状態で {base_damage}% の直撃を受けた。")
            
            if st.session_state.boss_hp <= 0:
                st.session_state.boss_defeated = True
                st.session_state.mode = "action"
                st.session_state.log.append("🏆 巨大ダイオウイカの撃破に成功した！")
            st.rerun()
            
        if b2.button("🛡️ 防御体勢をとる"):
            base_damage = random.randint(20, 35) // 2
            st.session_state.hull -= base_damage
            st.session_state.log.append(f"🛡️ 防御成功！ダメージを軽減し、船体に {base_damage}% のダメージ。")
            st.rerun()

# ログ表示
st.write("---")
st.subheader("📜 航海ログ")
for msg in reversed(st.session_state.log):
    st.write(msg)
