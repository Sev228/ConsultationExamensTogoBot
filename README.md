# ExamensTogoBot🤖

**ExamensTogoBot** est un bot Telegram non officiel qui permet aux utilisateurs de **consulter rapidement les résultats des examens nationaux du Togo** :
- ✅ BEPC
- ✅ BAC (général et technique)
- ✅ Probatoire

Ce projet interroge automatiquement le site officiel [de l'office du Bac](https://officedubactogo.net) pour récupérer les résultats en temps réel, sans stocker de données personnelles.

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Sev228/ConsultationExamensTogoBot.git
cd ConsultationExamensTogoBot
```
---

### 2.Créer un environnement virtuel pour le projet
```bash
python3 -m venv venv
source venv/bin/activate
```
---

### 3.Installer les dépendances
```bash
pip install -r requirements.txt
```
---


### 4. Créer les 2 bots directement depuis [Bot Father](https://telegram.me/BotFather/)
- Un Bot pour recevoir les logs
- Un Bot principal pour l'éxecution du code
---

### 5. Configurer les variables d’environnement

Crée un fichier .env en vous inspirant de .env.sample :
```
DEV_ID = VOTRE_ID_TELEGRAM

LOG_BOT = TOKEN_BOT_POUR_AVOIR_DES_LOGS

BOT_TOKEN = TOKEN_BOT_PRINCIPAL

------Utiliser coté serveur, en local inutile.
WEBHOOK_URL = URL_DE_VOTRE_WEBHOOK
```
---

## 🚀 Utilisation
## Lance le bot :
```bash
python3 main.py
```
### Puis, dans Telegram :

* Entrer dans le chat du Bot
* Tapez la commande `/start`
* Saisissez un numéro de table
* Choisissez un l'examen adéquat
* Vous recevrez le résultat recherché
---

## 🗂️ Structure du projet

```
.
├── main.py                  # Point d'entrée du bot
├── constants.py             # Constantes statiques
├── requirements.txt         # Dépendances Python
├── .env.sample              # Exemple de config .env
└── utils/
    ├── commands.py          # Commandes Telegram (/start, /help, etc.)
    ├── components.py        # Boutons et menus inline
    ├── fetchers.py          # Requêtes vers les site officiels
    ├── globalUtils.py       # Fonctions utilitaires diverses
    ├── handlers.py          # Logique de gestion des messages
    ├── messages.py          # Templates (messages) de réponses
    └── query_callbacks.py   # Réactions aux clics utilisateurs
```
---

## 🔐 Mentions légales

* Ce bot est **indépendant** du gouvernement togolais.
* Les résultats sont issus des site https://officedubactogo.net/ et https://resultats.gouv.tg/#/ 
* **Aucune donnée personnelle n’est stockée** ou exploitée à des fins commerciales.
---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.