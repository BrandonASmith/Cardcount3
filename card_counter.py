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

def get_bet_advice(tc):
    if tc <= 0:
        return "🧊 Chill Out"
    elif 0 < tc < 1.5:
        return "🧃 More Juice"
    else:
        return "🔥 Foot on the Gas"

st.set_page_config(page_title="Hi‑Lo Blackjack", layout="centered")

# Green felt background
if os.path.exists("green_felt.png"):
    import base64
    with open("green_felt.png","rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
        }}
        .stButton>button {{
            border:2px solid #000; border-radius:12px;
            background:white; color:black;
            height:80px; width:60px; font-size:18px; margin:4px;
        }}
        .card-img {{
            display:inline-block; margin:4px;
            width:60px; height:90px;
        }}
        </style>
    ''', unsafe_allow_html=True)

st.title("🃏 Hi‑Lo Blackjack Counter")

num_decks = st.selectbox("Number of decks:", range(1,9), index=5)

if "count" not in st.session_state or st.session_state.get("num_decks")!=num_decks:
    st.session_state.count = 0
    st.session_state.total = num_decks*52
    st.session_state.card_counts = {c: num_decks*4 for c in cards}
    st.session_state.dealt = []
    st.session_state.history = []
    st.session_state.num_decks = num_decks

col1,col2 = st.columns(2)
if col1.button("🔄 Reset Shoe"):
    st.session_state.count=0
    st.session_state.total=num_decks*52
    st.session_state.card_counts={c:num_decks*4 for c in cards}
    st.session_state.dealt=[]
    st.session_state.history=[]
if col2.button("♻️ Reset Hand"):
    st.session_state.dealt=[]
    st.session_state.history=[]

true_count = round(st.session_state.count/(st.session_state.total/52),2) if st.session_state.total else 0
bet = get_bet_advice(true_count)
st.markdown(f"#### Running Count: `{st.session_state.count}`")
st.markdown(f"#### True Count: `{true_count}`")
st.markdown(f"#### Bet Suggestion: {bet}")

st.markdown("### Tap a card:")
half = len(cards)//2
for row in [cards[:half], cards[half:]]:
    cols = st.columns(len(row))
    for i,c in enumerate(row):
        rem = st.session_state.card_counts[c]
        if cols[i].button(f"{c}\n({rem})",key=c):
            if rem>0:
                st.session_state.card_counts[c] -=1
                st.session_state.total -=1
                st.session_state.count += hi_lo_values[c]
                st.session_state.dealt.append(c)
                st.session_state.history.append(st.session_state.count)

if st.session_state.dealt:
    st.markdown("### Dealt Cards:")
    html=""
    for c in st.session_state.dealt:
        path=f"cards/{c}.png"
        if os.path.exists(path):
            with open(path,"rb") as f:
                enc=base64.b64encode(f.read()).decode()
            html += f'<img class="card-img" src="data:image/png;base64,{enc}"/>'
        else:
            html += f'<div class="card-img">{c}</div>'
    st.markdown(html,unsafe_allow_html=True)

if st.session_state.history:
    st.markdown("### Running Count History:")
    fig,ax=plt.subplots(figsize=(4,2))
    ax.plot(st.session_state.history,marker='o')
    ax.set_xlabel("Dealt")
    ax.set_ylabel("Count")
    st.pyplot(fig)
