import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#  Fonction pour charger les données depuis le fichier CSV local
@st.cache_data
def load_data():
    try:
        # Chargement des données depuis le fichier 'data.csv' local
        df = pd.read_csv('BeansDataSet.csv')  # Assurez-vous que 'data.csv' est dans le même dossier que votre script
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

#  Interface Streamlit
st.title(" Analyse des Ventes de Beans & Pods")

# Chargement des données
df = load_data()

if not df.empty:
    # Afficher un aperçu des données
    st.subheader(" Aperçu des données")
    st.dataframe(df.head())

    #  Vérification des types de colonnes
    if "Channel" in df.columns:
        df["Channel"] = df["Channel"].astype(str)

    if "Region" in df.columns:
        df["Region"] = df["Region"].astype(str)
    
    # Vérification et conversion des ventes en numériques
    vente_columns = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    for col in vente_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    #  Statistiques de base
    st.subheader(" Statistiques de base")
    total_ventes = df[vente_columns].sum().sum()
    moyenne_ventes = df[vente_columns].mean().mean()
    mediane_ventes = df[vente_columns].median().mean()
    max_ventes = df[vente_columns].max().max()
    min_ventes = df[vente_columns].min().min()

    st.write(f"**Total des ventes :** {total_ventes:.2f} ")
    st.write(f"**Moyenne des ventes :** {moyenne_ventes:.2f} ")
    st.write(f"**Médiane des ventes :** {mediane_ventes:.2f} ")
    st.write(f"**Vente max :** {max_ventes:.2f} ")
    st.write(f"**Vente min :** {min_ventes:.2f} ")

    #  Graphique des ventes par produit (Robusta, Arabica, etc.)
    st.subheader(" Ventes par produit")
    vente_par_produit = df[vente_columns].sum()
    fig, ax = plt.subplots()
    vente_par_produit.plot(kind='bar', ax=ax)
    ax.set_ylabel('Total des ventes ')
    ax.set_title('Ventes totales par produit')
    st.pyplot(fig)

    #  Tendance des ventes au fil du temps
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df_sorted = df.sort_values("Date")

        st.subheader(" Tendance des ventes dans le temps")
        fig, ax = plt.subplots()
        sns.lineplot(data=df_sorted, x="Date", y="Robusta", label="Robusta", ax=ax)
        sns.lineplot(data=df_sorted, x="Date", y="Arabica", label="Arabica", ax=ax)
        sns.lineplot(data=df_sorted, x="Date", y="Espresso", label="Espresso", ax=ax)
        sns.lineplot(data=df_sorted, x="Date", y="Lungo", label="Lungo", ax=ax)
        sns.lineplot(data=df_sorted, x="Date", y="Latte", label="Latte", ax=ax)
        sns.lineplot(data=df_sorted, x="Date", y="Cappuccino", label="Cappuccino", ax=ax)
        ax.set_xlabel('Date')
        ax.set_ylabel('Ventes ')
        ax.set_title('Évolution des ventes dans le temps')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    #  Ventes par canal (Store vs Online)
    if "Channel" in df.columns:
        st.subheader(" Ventes par canal")
        ventes_par_canal = df.groupby("Channel")[vente_columns].sum()
        fig, ax = plt.subplots()
        ventes_par_canal.plot(kind='bar', stacked=True, ax=ax)
        ax.set_ylabel('Total des ventes ')
        ax.set_title('Ventes totales par canal (Store vs Online)')
        st.pyplot(fig)

    #  Ventes par région
    if "Region" in df.columns:
        st.subheader(" Ventes par région")
        ventes_par_region = df.groupby("Region")[vente_columns].sum()
        fig, ax = plt.subplots()
        ventes_par_region.plot(kind='bar', stacked=True, ax=ax)
        ax.set_ylabel('Total des ventes ')
        ax.set_title('Ventes totales par région')
        st.pyplot(fig)

    #  Recommandations
    st.subheader(" Recommandations")
    st.write("""
    1. **Concentrer les efforts marketing sur les produits les plus populaires**: 
    En fonction des ventes totales par produit, Beans & Pods devrait concentrer ses efforts marketing sur les produits qui génèrent le plus de revenus (par exemple, Robusta et Arabica).
    
    2. **Cibler les régions à forte demande**: 
    Identifier les régions avec les meilleures ventes et concentrer les campagnes publicitaires dans ces zones.
    
    3. **Optimiser les ventes en ligne**: 
    Étant donné que la vente en ligne est probablement une partie clé de l'expansion, Beans & Pods devrait investir davantage dans des stratégies pour augmenter les ventes en ligne.
    """)

else:
    st.error("Le fichier CSV est vide ou mal formaté.")
