

import streamlit as st
import matplotlib.pyplot as plt

hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

if 'running_count' not in st.session_state:
    st.session_state.running_count = 0
    st.session_state.cards_seen = 0
    st.session_state.num_decks = 6
    st.session_state.true_count_history = []
    st.session_state.player_hand = []
    st.session_state.dealer_hand = []

def render_card(card):
    return f"<span style='display:inline-block;border:2px solid black;border-radius:8px;padding:10px;margin:6px;font-size:24px;background:white;color:red;width:48px;text-align:center;'>{card}♥</span>"

def plot_graph(history):
    fig, ax = plt.subplots()
    ax.plot(history, marker='o')
    ax.set_title("True Count Over Time")
    ax.set_xlabel("Cards Played")
    ax.set_ylabel("True Count")
    st.pyplot(fig)

# Apply background styling
st.markdown("""
<style>
    .stApp {
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/7/70/Casino_table_texture.jpg');
        background-size: cover;
        background-attachment: fixed;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🃏 Blackjack Card Counter</h1>", unsafe_allow_html=True)
st.markdown("### 🎴 Select number of decks")
st.session_state.num_decks = st.selectbox("", [1, 2, 4, 6, 8], index=3)
total_cards = st.session_state.num_decks * 52

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_rows = [cards[i:i+4] for i in range(0, len(cards), 4)]

# Dealer buttons
st.markdown("## 🧑‍⚖️ Dealer Hand")
for row in card_rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        if cols[i].button("Dealer: " + card + "♥"):
            st.session_state.running_count += hi_lo_values[card]
            st.session_state.cards_seen += 1
            st.session_state.dealer_hand.append(card)
            decks_remaining = max((total_cards - st.session_state.cards_seen) / 52, 1)
            true_count = round(st.session_state.running_count / decks_remaining, 2)
            st.session_state.true_count_history.append(true_count)

# Player buttons
st.markdown("## 🙋 Player Hand")
for row in card_rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        if cols[i].button("Player: " + card + "♥"):
            st.session_state.running_count += hi_lo_values[card]
            st.session_state.cards_seen += 1
            st.session_state.player_hand.append(card)
            decks_remaining = max((total_cards - st.session_state.cards_seen) / 52, 1)
            true_count = round(st.session_state.running_count / decks_remaining, 2)
            st.session_state.true_count_history.append(true_count)

# Display hands
if st.session_state.dealer_hand:
    st.markdown("### 🧑‍⚖️ Dealer Cards")
    st.markdown("".join([render_card(c) for c in st.session_state.dealer_hand]), unsafe_allow_html=True)

if st.session_state.player_hand:
    st.markdown("### 🙋 Player Cards")
    st.markdown("".join([render_card(c) for c in st.session_state.player_hand]), unsafe_allow_html=True)

# Count and metrics
decks_remaining = max((total_cards - st.session_state.cards_seen) / 52, 1)
true_count = round(st.session_state.running_count / decks_remaining, 2)

def bet_suggestion(tc):
    if tc <= 0:
        return "Minimum Bet"
    elif tc == 1:
        return "1× Base Bet"
    elif tc == 2:
        return "2× Base Bet"
    else:
        return "4× (Max Aggressive)"

st.markdown("---")
st.metric("Running Count", st.session_state.running_count)
st.metric("True Count", true_count)
st.metric("Cards Seen", st.session_state.cards_seen)
st.metric("💸 Suggested Bet", bet_suggestion(true_count))

# Reset buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("♻️ Reset Player Hand"):
        st.session_state.player_hand = []
with col2:
    if st.button("♻️ Reset Dealer Hand"):
        st.session_state.dealer_hand = []
with col3:
    if st.button("❌ Reset Count & Hands"):
        st.session_state.running_count = 0
        st.session_state.cards_seen = 0
        st.session_state.true_count_history = []
        st.session_state.player_hand = []
        st.session_state.dealer_hand = []

if st.session_state.true_count_history:
    st.markdown("### 📈 True Count Over Time")
    plot_graph(st.session_state.true_count_history)
