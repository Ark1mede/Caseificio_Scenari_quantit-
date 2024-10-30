import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Imposta due colonne per la disposizione degli slider
col1, col2 = st.columns(2)

with col1:
    # Slider per lo Scenario A
    A_costo_Kg = st.slider("A Costo al Kg", 6, 15, 8, step=1, key="A_costo_Kg")
    A_vendita_Kg = st.slider("A Vendita €", 8, 40, 13, step=1, key="A_vendita_Kg")
    A_Spedizioni = st.slider("# spedizioni per settimana", 1, 7, 1, step=1, key="A_Spedizioni")
    A_Costo_Sped = st.slider("Costo Spedizione €", 2, 12, 5, step=1, key="A_Costo_Sped")
    A_Reso = st.slider("A Reso %", 0, 100, 0, step=10, key="A_Reso") / 100
    A_Ristoranti = st.slider("# A_Ristoranti", 1, 60, 30, step=1, key="A_Ristoranti")

with col2:
    # Slider per lo Scenario B
    B_costo_Kg = st.slider("B Costo al Kg", 6, 15, 11, step=1, key="B_costo_Kg")
    B_vendita_Kg = st.slider("B Vendita €", 8, 40, 23, step=1, key="B_vendita_Kg")
    B_Spedizioni = st.slider("# spedizioni per settimana", 1, 7, 5, step=1, key="B_Spedizioni")
    B_Costo_Sped = st.slider("Costo Spedizione €", 2, 12, 5, step=1, key="B_Costo_Sped")
    B_Reso = st.slider("B Reso %", 0, 100, 30, step=10, key="B_Reso") / 100
    B_Ristoranti = st.slider("# B_Ristoranti", 1, 60, 3, step=1, key="B_Ristoranti")

Profitto = st.slider("Profitto Target €", 0, 300, 50, step=10, key="Profitto_Target")

# Funzione profitto per ciascun scenario in funzione della quantità
def profit_scenario_A(Q):
    A_Vendita = A_vendita_Kg * Q * A_Spedizioni * (1 - A_Reso)
    A_Costo = (A_costo_Kg * Q * A_Spedizioni) + (A_Costo_Sped * A_Spedizioni)
    return A_Vendita - A_Costo

def profit_scenario_B(Q):
    B_Vendita = B_vendita_Kg * Q * B_Spedizioni * (1 - B_Reso)
    B_Costo = (B_costo_Kg * Q * B_Spedizioni) + (B_Costo_Sped * B_Spedizioni)
    return B_Vendita - B_Costo

# Quantità per spedizione (da 1 a 20)
quantities = np.arange(1, 21)
profits_A = [profit_scenario_A(q) for q in quantities]
profits_B = [profit_scenario_B(q) for q in quantities]

# Trova i punti di intersezione tra il profitto target e le curve di profitto
def find_intersection(profits, target):
    for i, profit in enumerate(profits):
        if profit >= target:
            return quantities[i]
    return None

# Calcolo delle quantità per i punti di intersezione
quantita_intersezione_A = find_intersection(profits_A, Profitto)
quantita_intersezione_B = find_intersection(profits_B, Profitto)

# Descrizione prima del grafico
st.markdown(f"<h3><strong>PROFITTO TARGET: {Profitto} €</strong></h3>", unsafe_allow_html=True)
st.write(f"<span style='color:blue'>Quantità per spedizione Scenario A:</span> {quantita_intersezione_A} Kg" if quantita_intersezione_A else "Nessuna intersezione per A", unsafe_allow_html=True)
st.write(f"<span style='color:green'>Quantità per spedizione Scenario B:</span> {quantita_intersezione_B} Kg" if quantita_intersezione_B else "Nessuna intersezione per B", unsafe_allow_html=True)

# Calcola profitto per ristorante e profitto annuo
profit_per_ristorante_A = [profit * A_Ristoranti for profit in profits_A]
profit_per_ristorante_B = [profit * B_Ristoranti for profit in profits_B]
profit_annuo_A = [profit * A_Ristoranti * 50 for profit in profits_A]
profit_annuo_B = [profit * B_Ristoranti * 50 for profit in profits_B]

# Aggiungi la colonna per la quantità per settimana
quantita_settimanale_A = [q * A_Spedizioni for q in quantities]
quantita_settimanale_B = [q * B_Spedizioni for q in quantities]

# Tabella per i valori A e B
table_data = {
    "Costo €/Kg": [A_costo_Kg, B_costo_Kg],
    "Vendita €/Kg": [A_vendita_Kg, B_vendita_Kg],
    "# spedizioni per settimana": [A_Spedizioni, B_Spedizioni],
    "Costo Spedizione (€)": [A_Costo_Sped, B_Costo_Sped],
    "Quantità per settimana": [f"{quantita_settimanale_A[-1]:,}".replace(",", "."),
                              f"{quantita_settimanale_B[-1]:,}".replace(",", ".")],
    "Reso %": [f"{int(A_Reso * 100)}%", f"{int(B_Reso * 100)}%"],
    "# Ristoranti": [A_Ristoranti, B_Ristoranti],
    "Profitto per Ristoranti (€)": [f"{int(profit_per_ristorante_A[-1]):,}".replace(",", "."),
                                     f"{int(profit_per_ristorante_B[-1]):,}".replace(",", ".")],  # Ultimo valore
    "Profitto Annuo (€)": [f"{int(profit_annuo_A[-1]):,}".replace(",", "."),
                           f"{int(profit_annuo_B[-1]):,}".replace(",", ".")]  # Ultimo valore
}

# Mostra la tabella centrata con intestazioni più piccole
st.write("<style> .streamlit-table th { font-size: 12px; } </style>", unsafe_allow_html=True)
st.table(table_data)

# Creazione del primo grafico
plt.figure(figsize=(10, 6))
plt.plot(quantities, profits_A, label='Scenario A', color='blue')
plt.plot(quantities, profits_B, label='Scenario B', color='green')

# Aggiungi i punti di intersezione
if quantita_intersezione_A is not None:
    plt.plot(quantita_intersezione_A, profit_scenario_A(quantita_intersezione_A), 'ro')  # Punto rosso per A
if quantita_intersezione_B is not None:
    plt.plot(quantita_intersezione_B, profit_scenario_B(quantita_intersezione_B), 'ro')  # Punto rosso per B

# Linea orizzontale per il profitto target
plt.axhline(y=Profitto, color="purple", linestyle="--")  # Senza la leggenda

# Aggiungi la leggenda
plt.legend(title='Scenari')

# Imposta limiti per gli assi
plt.xlim(1, 20)
plt.ylim(0, 300)  # Modifica dell'asse Y con un massimo di 300

# Trova il profitto minimo e massimo
min_profit = min(min(profits_A), min(profits_B), Profitto) - 50
max_profit = max(max(profits_A), max(profits_B), Profitto) + 50

# Etichette e titolo
plt.xlabel("Quantità per spedizione (Kg)")
plt.ylabel("Profitto €")
plt.title("Confronto Profitti: Scenario A vs Scenario B")
plt.grid(True)

# Mostra il grafico in Streamlit
st.pyplot(plt)
