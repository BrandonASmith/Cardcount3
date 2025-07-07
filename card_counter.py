import streamlit as st
import matplotlib.pyplot as plt
import base64
import os

# Hi-Lo values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}
cards = list(hi_lo_values.keys())

# Bet advice
def get_bet_advice(tc):
    if tc <= 0:
        return "🧊 Chill Out"
    elif 0 < tc < 1.5:
        return "🧃 More Juice"
    else:
        return "🔥 Foot on the Gas"

# Green felt background and styles
st.set_page_config(page_title="Hi-Lo Blackjack", layout="centered")
if os.path.exists("green_felt.png"):
    with open("green_felt.png", "rb") as f:
        bg_data = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg_data}");
            background-size: cover;
        }}
        .stButton > button {{
            background-color: white !important;
            color: black;
            border: 2px solid #000;
            font-size: 20px;
            font-weight: bold;
            border-radius: 12px;
            height: 100px;
            width: 80px;
            margin: 6px;
        }}
        .card-img {{
            display: inline-block;
            margin: 6px;
            width: 80px;
            height: 115px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Title
st.title("🃏 Hi-Lo Blackjack Counter")

# Deck selector
num_decks = st.selectbox("Number of decks:", range(1, 9), index=5)

# Init session state
if "count" not in st.session_state or st.session_state.get("num_decks") != num_decks:
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.num_decks = num_decks

# Reset buttons
col1, col2 = st.columns(2)
if col1.button("🔄 Reset Shoe"):
    st.session_state.count = 0
    st.session_state.total_cards = num_decks * 52
    st.session_state.card_counts = {card: num_decks * 4 for card in cards}
    st.session_state.dealt = []
    st.session_state.history = []

if col2.button("♻️ Reset Hand"):
    st.session_state.dealt = []
    st.session_state.history = []

# Show counts
true_count = round(st.session_state.count / (st.session_state.total_cards / 52), 2) if st.session_state.total_cards else 0
bet_advice = get_bet_advice(true_count)
st.markdown(f"#### Running Count: `{st.session_state.count}`")
st.markdown(f"#### True Count: `{true_count}`")
st.markdown(f"#### Bet Suggestion: **{bet_advice}**")

# Card buttons
st.markdown("### Tap a Card to Deal:")
half = len(cards) // 2
rows = [cards[:half], cards[half:]]
for row in rows:
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

# Show dealt cards as images
if st.session_state.dealt:
    st.markdown("### Dealt Cards:")
    dealt_html = ""
    for card in st.session_state.dealt:
        image_path = f"cards/{card}.png"
        if os.path.exists(image_path):
            with open(image_path, "rb") as img:
                encoded = base64.b64encode(img.read()).decode()
                dealt_html += f'<img class="card-img" src="data:image/png;base64,{encoded}"/>'
        else:
            dealt_html += f'<div class="card-img">{card}</div>'
    st.markdown(dealt_html, unsafe_allow_html=True)

# Graph
if st.session_state.history:
    st.markdown("### Running Count History:")
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(st.session_state.history, marker='o')
    ax.set_xlabel("Cards Dealt")
    ax.set_ylabel("Running Count")
    st.pyplot(fig)
