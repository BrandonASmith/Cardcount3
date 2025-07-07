import streamlit as st
import matplotlib.pyplot as plt

# Hi-Lo card values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
cards = list(hi_lo_values.keys())

# Betting advice logic
def get_bet_advice(tc):
    if tc <= 0.2:
        return "Chill 🧊"
    elif 0.21 <= tc < 1.8:
        return "More Juice 🍊"
    else:
        return "Extra Juicy 🧃"

# Heart-style card box
def render_card_html(card):
    return f"""
    <div style='
        display:inline-block;
        margin:2px;
        padding:6px;
        width:48px;
        height:70px;
        border:2px solid red;
        border-radius:6px;
        background:white;
        font-weight:bold;
        font-size:18px;
        color:red;
        text-align:center;
        line-height:1.2;
        font-family: Georgia, serif;
    '>
        ❤️<br>{card}
    </div>
    """

# Page config
st.set_page_config(page_title="JuiceBox", layout="centered")

# Theme & Sound Toggles
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "sound" not in st.session_state:
    st.session_state.sound = True

# CSS
dark_css = '''
<style>
.stApp { background-color: #1c2d24; padding-top: 5px; }
h1, .small-text { color: white; }
.stButton > button {
    background: white !important; color: black;
    font-size: 12px; border-radius: 6px;
    height: 50px; width: 50px; margin: 2px;
    border: 2px solid black; font-weight: bold;
}
</style>
'''
light_css = '''
<style>
.stApp { background-color: #f5f5f5; padding-top: 5px; }
h1, .small-text { color: black; }
.stButton > button {
    background: white !important; color: black;
    font-size: 12px; border-radius: 6px;
    height: 50px; width: 50px; margin: 2px;
    border: 2px solid black; font-weight: bold;
}
</style>
'''
st.markdown(dark_css if st.session_state.theme == "dark" else light_css, unsafe_allow_html=True)

# Top controls
colL, colM, colR = st.columns(3)
with colL:
    st.button("🌗 Theme", on_click=lambda: st.session_state.update(
        {"theme": "light" if st.session_state.theme == "dark" else "dark"}))
with colM:
    st.session_state.sound = st.toggle("🔊", value=st.session_state.sound, label_visibility="collapsed")
with colR:
    num_decks = st.selectbox("Decks", range(1, 9), index=5, label_visibility="collapsed")

# Title
st.markdown("<h1 style='font-size:24px; text-align:center;'>Juice🧃Box</h1>", unsafe_allow_html=True)

# Init state
if "count" not in st.session_state or st.session_state.get("num_decks") != num_decks:
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.num_decks = num_decks

# Reset buttons
col1, col2 = st.columns(2)
if col1.button("🔄 Shoe"):
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
if col2.button("♻️ Hand"):
    st.session_state.dealt = []
    st.session_state.history = []

# Count display
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
st.markdown(f"<div class='small-text'><strong>RC:</strong> {st.session_state.count} &nbsp;&nbsp; <strong>TC:</strong> {true_count} &nbsp;&nbsp; {get_bet_advice(true_count)}</div>", unsafe_allow_html=True)

# Card buttons in 2 rows
top = cards[:7]
bottom = cards[7:]
for row in [top, bottom]:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        remaining = st.session_state.card_counts[card]
        if cols[i].button(f"{card}\n({remaining})", key=f"{card}_btn"):
            if remaining > 0:
                st.session_state.card_counts[card] -= 1
                st.session_state.total_cards -= 1
                st.session_state.count += hi_lo_values[card]
                st.session_state.dealt.append(card)
                st.session_state.history.append(st.session_state.count)
                if st.session_state.sound:
                    st.audio("https://actions.google.com/sounds/v1/cartoon/wood_plank_flicks.ogg")
                st.rerun()

# Dealt card display
if st.session_state.dealt:
    st.markdown("<div class='small-text'>Dealt Cards:</div>", unsafe_allow_html=True)
    html = ''.join([render_card_html(card) for card in st.session_state.dealt])
    st.markdown(html, unsafe_allow_html=True)

# Graph in expander
if st.session_state.history:
    with st.expander("📈 Count Graph"):
        fig, ax = plt.subplots(figsize=(4, 1.5))
        ax.plot(st.session_state.history, marker='o')
        ax.set_xlabel("Cards")
        ax.set_ylabel("RC")
        st.pyplot(fig)
