from datetime import date
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="AL CHAZEAU Section pétanque", page_icon="🤾", layout="wide"
)

# --- CLASSES / MODÈLES DE DONNÉES ---


class Membre:

  def __init__(
      self,
      id: int,
      nom: str,
      prenom: str,
      type_adhesion: str,
      telephone: str,
      num_licence: str = None,
  ):
    self.id = id
    self.nom = nom
    self.prenom = prenom
    self.type_adhesion = type_adhesion
    self.telephone = telephone
    self.num_licence = num_licence
    self.points_challenge = 0
    self.parties_jouees = 0
    self.victoires = 0


# Initialisation des données dans la session Streamlit
if "membres" not in st.session_state:
  st.session_state.membres = [
      Membre(1, "Dupont", "Jean", "Licencié", "06 12 34 56 78", "123456A"),
      Membre(2, "Martin", "Claire", "Licencié", "06 98 76 54 32", "654321B"),
      Membre(3, "Durand", "Michel", "Loisir", "06 11 22 33 44"),
      Membre(4, "Bernard", "Sarah", "Licencié", "06 55 44 33 22", "789101C"),
  ]

if "concours" not in st.session_state:
  st.session_state.concours = [
      {
          "id": 1,
          "titre": "Concours de Rentrée (Doublette formée)",
          "date": "2026-10-18",
          "type": "Doublette",
      },
      {
          "id": 2,
          "titre": "Mêlée Tournante du Mois",
          "date": "2026-10-25",
          "type": "Mêlée",
      },
  ]

if "buvette" not in st.session_state:
  st.session_state.buvette = [
      {"id": 1, "poste": "Tenue Buvette - Matin", "benevole": "Jean Dupont"},
      {
          "id": 2,
          "poste": "Préparation des terrains",
          "benevole": "Non attribué",
      },
      {"id": 3, "poste": "Table de marque", "benevole": "Claire Martin"},
  ]

if "photos" not in st.session_state:
  st.session_state.photos = [
      {
          "titre": "Concours d'ouverture 2026",
          "date": "15/09/2026",
          "url": "https://picsum.photos/seed/petanque1/600/400",
      },
      {
          "titre": "Remise des prix du Challenge",
          "date": "02/07/2026",
          "url": "https://picsum.photos/seed/petanque2/600/400",
      },
      {
          "titre": "Journée convivialité & Barbecue",
          "date": "20/06/2026",
          "url": "https://picsum.photos/seed/petanque3/600/400",
      },
  ]

# --- EN-TÊTE DE L'APPLICATION ---
st.title("AL CHAZEAU — Section pétanque 🎯")
st.caption("Gestion du club, des concours, de la photothèque et de la buvette")

# --- ONGLETS FIXES PRINCIPAUX ---
tab_accueil, tab_membres, tab_concours, tab_photos, tab_buvette = st.tabs([
    "🏠 Tableau de bord",
    "📇 Membres & Challenge",
    "🏆 Concours & Parties",
    "📸 Photothèque",
    "🍺 Buvette & Bénévolat",
])

# --- 1. TABLEAU DE BORD ---
with tab_accueil:
  st.header("Vue d'ensemble")

  col1, col2, col3 = st.columns(3)
  col1.metric("Membres Actifs", len(st.session_state.membres))
  col2.metric("Concours à venir", len(st.session_state.concours))
  col3.metric("Parties jouées cette saison", "48")

  st.divider()

  st.subheader("📌 Prochains Événements")
  for c in st.session_state.concours:
    st.info(f"📅 **{c['titre']}** — Prévu le {c['date']} (Type: {c['type']})")

  st.subheader("🏆 Top 3 du Challenge Interne (Provisoire)")
  membres_tries = sorted(
      st.session_state.membres, key=lambda x: x.points_challenge, reverse=True
  )
  for i, m in enumerate(membres_tries[:3], 1):
    st.write(
        f"**#{i}** : {m.prenom} {m.nom} — **{m.points_challenge} pts**"
        f" ({m.victoires} victoires)"
    )

# --- 2. MEMBRES & CHALLENGE ---
with tab_membres:
  st.header("Gestion des Membres & Classement")

  sub_tab1, sub_tab2 = st.tabs(["Annuaire des Joueurs", "Ajouter un Membre"])

  with sub_tab1:
    st.subheader("Liste des membres du club")
    data = []
    for m in st.session_state.membres:
      data.append({
          "Nom": m.nom,
          "Prénom": m.prenom,
          "Type": m.type_adhesion,
          "Licence": m.num_licence if m.num_licence else "N/A",
          "Téléphone": m.telephone,
          "Points Challenge": m.points_challenge,
      })
    st.dataframe(data, use_container_width=True)

  with sub_tab2:
    st.subheader("Enregistrer un nouveau joueur")
    with st.form("form_membre"):
      nom = st.text_input("Nom")
      prenom = st.text_input("Prénom")
      type_adh = st.selectbox("Type d'adhésion", ["Licencié", "Loisir"])
      tel = st.text_input("Téléphone")
      licence = st.text_input("Numéro de licence (si licencié)")

      submitted = st.form_submit_button("Ajouter le membre")
      if submitted and nom and prenom:
        nouvel_id = len(st.session_state.membres) + 1
        nouveau = Membre(nouvel_id, nom, prenom, type_adh, tel, licence)
        st.session_state.membres.append(nouveau)
        st.success(f"Membre {prenom} {nom} ajouté avec succès !")
        st.rerun()

# --- 3. CONCOURS & PARTIES ---
with tab_concours:
  st.header("Gestion des Concours & Tournois")

  st.subheader("Créer un nouveau concours")
  with st.form("form_concours"):
    titre_c = st.text_input("Nom du concours (ex: Challenge d'automne)")
    date_c = st.date_input("Date du concours", value=date.today())
    type_c = st.selectbox(
        "Format de jeu",
        ["Mêlée tournante", "Doublette formée", "Triplette formée"],
    )
    submit_c = st.form_submit_button("Créer le concours")
    if submit_c and titre_c:
      st.session_state.concours.append({
          "id": len(st.session_state.concours) + 1,
          "titre": titre_c,
          "date": str(date_c),
          "type": type_c,
      })
      st.success("Concours créé !")
      st.rerun()

  st.divider()
  st.subheader("Simulateur de Saisie de Partie")
  noms_membres = [f"{m.prenom} {m.nom}" for m in st.session_state.membres]
  if len(noms_membres) >= 2:
    col1, col2 = st.columns(2)
    with col1:
      j1 = st.selectbox("Équipe 1 - Joueur 1", noms_membres, index=0)
      score1 = st.number_input("Score Équipe 1", 0, 13, 13)
    with col2:
      j2 = st.selectbox(
          "Équipe 2 - Joueur 2",
          noms_membres,
          index=1 if len(noms_membres) > 1 else 0,
      )
      score2 = st.number_input("Score Équipe 2", 0, 13, 8)

    if st.button("Enregistrer le résultat de la partie"):
      for m in st.session_state.membres:
        if f"{m.prenom} {m.nom}" == j1:
          m.parties_jouees += 1
          if score1 > score2:
            m.victoires += 1
            m.points_challenge += 3
        elif f"{m.prenom} {m.nom}" == j2:
          m.parties_jouees += 1
          if score2 > score1:
            m.victoires += 1
            m.points_challenge += 3
      st.success(
          "Partie enregistrée ! Les points du challenge ont été mis à jour."
      )

# --- 4. PHOTOTHÈQUE ---
with tab_photos:
  st.header("Photothèque du Club 📸")

  sub_tab_galerie, sub_tab_ajout = st.tabs(
      ["Galerie Photos", "Ajouter une nouvelle photo"]
  )

  with sub_tab_galerie:
    st.subheader("Albums & Souvenirs de AL CHAZEAU Section pétanque")
    cols = st.columns(3)

    for idx, photo in enumerate(st.session_state.photos):
      with cols[idx % 3]:
        st.image(photo["url"], caption=f"{photo['titre']} ({photo['date']})")

  with sub_tab_ajout:
    st.subheader("Ajouter une photo à l'album")
    uploaded_file = st.file_uploader(
        "Choisissez une photo", type=["png", "jpg", "jpeg"]
    )
    titre_photo = st.text_input("Titre ou description de la photo")

    if st.button("Publier la photo"):
      if uploaded_file and titre_photo:
        st.session_state.photos.append({
            "titre": titre_photo,
            "date": date.today().strftime("%d/%m/%Y"),
            "url": uploaded_file,
        })
        st.success("Photo ajoutée à la galerie avec succès !")
        st.rerun()
      else:
        st.warning("Veuillez importer une image et saisir un titre.")

# --- 5. BUVETTE & BÉNÉVOLAT ---
with tab_buvette:
  st.header("Planning Buvette & Bénévolat 🍻")

  st.subheader("Inscriptions aux créneaux pour le prochain concours")

  for item in st.session_state.buvette:
    col_a, col_b, col_c = st.columns([3, 2, 2])
    col_a.write(f"📌 **{item['poste']}**")
    col_b.write(f"Assigné à : *{item['benevole']}*")

    with col_c:
      if st.button("M'inscrire", key=f"btn_{item['id']}"):
        item["benevole"] = "Moi (Admin)"
        st.success("Inscrit avec succès !")
        st.rerun()    
