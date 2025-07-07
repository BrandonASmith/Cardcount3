import streamlit as st
import matplotlib.pyplot as plt

# Hi-Lo values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
cards = list(hi_lo_values.keys())

def get_bet_advice(tc):
    if tc <= .2:
        return "Chill 🧊"
    elif .21 < tc < 1.8:
        return "More Juice 🍊"
    else:
        return "Extra Juicy 🧃"

def render_card_html(card):
    return f"""
    <div style='
        display:inline-block;
        margin:4px;
        padding:8px;
        width:50px;
        height:70px;
        border:3px solid red;
        border-radius:6px;
        background:white;
        font-weight:bold;
        font-size:18px;
        color:red;
        text-align:center;
        line-height:1.3;
        font-family: Georgia, serif;
    '>
        ❤️<br>{card}
    </div>
    """

st.set_page_config(page_title="JuiceBox", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #204420;
        padding: 5px;
    }
    .stButton > button {
        background-color: white !important;
        color: black;
        font-weight: bold;
        font-family: Georgia, serif;
        border: 2px solid black;
        font-size: 14px;
        border-radius: 10px;
        height: 55px;
        width: 55px;
        padding: 4px;
        margin: 2px;
    }
    .small-text {
        font-size: 16px;
        font-weight: bold;
        color: white;
        padding-bottom: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Juice🧃Box</h2>", unsafe_allow_html=True)

num_decks = st.selectbox("Number of decks:", range(1, 9), index=5)

# State init
if "count" not in st.session_state or st.session_state.get("num_decks") != num_decks:
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.num_decks = num_decks

# Reset Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Shoe"):
        st.session_state.count = 0
        st.session_state.total_cards = num_decks * 52
        st.session_state.card_counts = {card: num_decks * 4 for card in cards}
        st.session_state.dealt = []
        st.session_state.history = []
with col2:
    if st.button("♻️ Hand"):
        st.session_state.dealt = []
        st.session_state.history = []

# Counts & advice
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
bet_advice = get_bet_advice(true_count)

st.markdown(f"<div class='small-text'>RC: {st.session_state.count} &nbsp;&nbsp; TC: {true_count} &nbsp;&nbsp; {bet_advice}</div>", unsafe_allow_html=True)

# Card Buttons — 2 rows
half = (len(cards) + 1) // 2
for row in [cards[:half], cards[half:]]:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        remaining = st.session_state.card_counts[card]
        if cols[i].button(f"{card} ({remaining})", key=f"{card}_btn"):
            if remaining > 0:
                st.session_state.card_counts[card] -= 1
                st.session_state.total_cards -= 1
                st.session_state.count += hi_lo_values[card]
                st.session_state.dealt.append(card)
                st.session_state.history.append(st.session_state.count)

# Dealt cards
if st.session_state.dealt:
    st.markdown("<div class='small-text'>Dealt Cards:</div>", unsafe_allow_html=True)
    dealt_html = ''.join([render_card_html(card) for card in st.session_state.dealt])
    st.markdown(dealt_html, unsafe_allow_html=True)

# History Graph
if st.session_state.history:
    st.markdown("<div class='small-text'>Count Graph:</div>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(4, 1.5))
    ax.plot(st.session_state.history, marker='o')
    ax.set_xlabel("Cards")
    ax.set_ylabel("RC")
    st.pyplot(fig)
