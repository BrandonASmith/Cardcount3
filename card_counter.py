import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="JuiceBox", layout="centered")

# Hi-Lo values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
cards = list(hi_lo_values.keys())

def get_bet_advice(tc):
    if tc <= .2:
        return "🧊 Chill"
    elif .21 < tc < 1.8:
        return "🍊 More Juice"
    else:
        return "🧃 Extra Juicy"

def render_card_html(card):
    return f"""
    <div style='
        display:inline-block;
        margin:3px;
        padding:6px;
        width:45px;
        height:65px;
        border:2px solid red;
        border-radius:6px;
        background:white;
        font-weight:bold;
        font-size:16px;
        color:red;
        text-align:center;
        line-height:1.2;
        font-family: Georgia, serif;
    '>
        ❤️<br>{card}
    </div>
    """

# Style overrides for tight mobile layout
st.markdown("""
    <style>
    .stApp {
        background-color: #1c2d24;
        padding: 0.5rem;
    }
    .stButton > button {
        background-color: white !important;
        color: black;
        font-weight: bold;
        font-size: 14px;
        border-radius: 6px;
        height: 45px;
        width: 55px;
        padding: 0;
        margin: 2px;
    }
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h4 style='text-align:center;'>Juice🧃Box</h4>", unsafe_allow_html=True)

num_decks = st.selectbox("Decks", range(1, 9), index=5)

# Initialize session state
if "count" not in st.session_state or st.session_state.get("num_decks") != num_decks:
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.num_decks = num_decks

col1, col2 = st.columns(2)
if col1.button("Shoe"):
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []

if col2.button("Hand"):
    st.session_state.dealt = []
    st.session_state.history = []

# Show count values
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
bet_advice = get_bet_advice(true_count)

st.markdown(f"<div style='text-align:center;font-size:14px;'>RC: {st.session_state.count} &nbsp;&nbsp; TC: {true_count} &nbsp;&nbsp; {bet_advice}</div>", unsafe_allow_html=True)

# Card buttons in 2 rows (7 + 6)
rows = [cards[:7], cards[7:]]
for row in rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        remaining = st.session_state.card_counts[card]
        if cols[i].button(f"{card}\n({remaining})", key=card):
            if remaining > 0:
                st.session_state.card_counts[card] -= 1
                st.session_state.total_cards -= 1
                st.session_state.count += hi_lo_values[card]
                st.session_state.dealt.append(card)
                st.session_state.history.append(st.session_state.count)
            st.experimental_rerun()  # ensure immediate update

# Display dealt cards horizontally
if st.session_state.dealt:
    st.markdown("<div style='text-align:center;'>Dealt:</div>", unsafe_allow_html=True)
    html = ''.join([render_card_html(card) for card in st.session_state.dealt])
    st.markdown(f"<div style='text-align:center;'>{html}</div>", unsafe_allow_html=True)

# Optional history graph
if st.session_state.history:
    st.markdown("### Count Graph:")
    fig, ax = plt.subplots(figsize=(4, 1.5))
    ax.plot(st.session_state.history, marker='o')
    ax.set_xlabel("Cards")
    ax.set_ylabel("RC")
    st.pyplot(fig)
