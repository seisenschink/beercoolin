import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def berechne_wärmeübergang_gesamt(h_innen, k_material, d, h_außen):
    return 1 / (1/h_innen + d/k_material + 1/h_außen)

def berechne_temperatur(t, T_start, T_umgebung, konstante):
    return T_umgebung + (T_start - T_umgebung) * np.exp(-konstante * t)

# Physikalische Grundlagen und Formeln in einer Infobox
if st.button('Zeige physikalische Grundlagen und Formeln'):
    st.markdown("""
    **Physikalische Grundlagen:**
    
    Das Modell basiert auf **Newtons Abkühlungsgesetz**, das besagt, dass die Änderungsrate der Temperatur eines Objekts proportional zur Differenz zwischen der aktuellen Temperatur des Objekts und der Umgebungstemperatur ist.
    
    **Formel:**
    \[
    \frac{dT(t)}{dt} = -k \cdot (T(t) - T_{\text{Umgebung}})
    \]
    - \( T(t) \) ist die Temperatur des Objekts zu einem Zeitpunkt \( t \).
    - \( T_{\text{Umgebung}} \) ist die konstante Umgebungstemperatur.
    - \( k \) ist die Abkühl- oder Erwärmungskonstante.
    
    Die Lösung dieser Differentialgleichung ergibt:
    \[
    T(t) = T_{\text{Umgebung}} + (T_{\text{Start}} - T_{\text{Umgebung}}) \cdot e^{-k \cdot t}
    \]
    
    **Wärmeübergangskoeffizient:**
    Der effektive Wärmeübergangskoeffizient \( h_{\text{gesamt}} \) berücksichtigt die Wärmeleitung durch das Gefäßmaterial und die Konvektion sowohl auf der Innen- als auch auf der Außenseite des Gefäßes.
    \[
    \frac{1}{h_{\text{gesamt}}} = \frac{1}{h_{\text{innen}}} + \frac{d}{k_{\text{Material}}} + \frac{1}{h_{\text{außen}}}
    \]
    - \( h_{\text{innen}} \) ist der Wärmeübergangskoeffizient zwischen Bier und Gefäßwand.
    - \( h_{\text{außen}} \) ist der Wärmeübergangskoeffizient zwischen der Außenseite des Gefäßes und der Umgebung.
    - \( d \) ist die Dicke des Gefäßes.
    - \( k_{\text{Material}} \) ist die Wärmeleitfähigkeit des Gefäßmaterials.
    """)

# Auswahl der Berechnungsmethode für k
berechnung_auswahl = st.sidebar.checkbox('k berechnen statt direkten Wert eingeben')

if berechnung_auswahl:
    # Auswahl der Gefäßmaterialien
    materialien = {
        "Glas": 1.0,   # Wärmeleitfähigkeit in W/m·K
        "Aluminium": 235.0,
        "Kunststoff": 0.2
    }

    material = st.sidebar.selectbox('Material des Gefäßes', list(materialien.keys()))
    k_material = materialien[material]

    # Eingabe für die Dicke des Gefäßes
    d = st.sidebar.number_input('Dicke des Gefäßes (m)', min_value=0.0001, max_value=0.1, value=0.003, step=0.0001)

    # Wärmeübergangskoeffizienten (könnten auch als Schieberegler hinzugefügt werden)
    h_innen = st.sidebar.number_input('Wärmeübergangskoeffizient innen (W/m²·K)', value=10.0)
    h_außen = st.sidebar.number_input('Wärmeübergangskoeffizient außen (W/m²·K)', value=25.0)

    # Berechnung des Gesamt-Wärmeübergangskoeffizienten
    h_gesamt = berechne_wärmeübergang_gesamt(h_innen, k_material, d, h_außen)

    # Berechnung der Abkühl-/Erwärmungskonstante k
    A = st.sidebar.number_input('Oberfläche der Flasche A (m²)', min_value=0.01, max_value=1.0, value=0.03)
    m = st.sidebar.number_input('Masse des Biers m (g)', min_value=100, max_value=2000, value=500)
    c = st.sidebar.number_input('Spezifische Wärmekapazität c (J/g·K)', min_value=1.0, max_value=10.0, value=4.18)

    k_berechnet = h_gesamt * A / (m * c)
    st.sidebar.write(f"Berechnete Abkühl-/Erwärmungskonstante k: {k_berechnet:.5f} min⁻¹")
else:
    # Direkte Eingabe eines k-Wertes
    k_berechnet = st.sidebar.number_input('Direkter k-Wert (min⁻¹)', min_value=0.0001, max_value=1.0, value=0.1, step=0.0001)

# Temperaturberechnung für die Simulation
T_start = st.slider('Anfangstemperatur des Biers (°C)', min_value=0, max_value=30, value=5)
T_umgebung = st.slider('Umgebungstemperatur (°C)', min_value=0, max_value=40, value=22)
zeit_end = 240  # Erhöhen der Zeit auf 240 Minuten
zeit = np.linspace(0, zeit_end, 1000)  # Mehr Berechnungspunkte, um niedrige k-Werte besser abzubilden

# Temperaturberechnung
temperatur = berechne_temperatur(zeit, T_start, T_umgebung, k_berechnet)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(zeit, temperatur, label='Biertemperatur')
plt.axhline(T_umgebung, color='red', linestyle='--', label='Umgebungstemperatur')
plt.title('Simulation der Biertemperatur über die Zeit')
plt.xlabel('Zeit (Minuten)')
plt.ylabel('Temperatur (°C)')
plt.legend()
plt.grid(True)
st.pyplot(plt)
