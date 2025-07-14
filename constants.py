###---Fichier pour stocker des constantes directement depuis les variables d'environnements---

import os
from dotenv import load_dotenv
load_dotenv()

#Votre Id Telegram pour Recevoir les possibles bugs et Exceptions.
DEVELOPPER_ID = os.getenv("DEV_ID")

#--------------------------------------------------------------

#Bot pour recevoir les possibles bugs et Exceptions
LOG_BOT = os.getenv("LOG_BOT_ID")  #Vous devrez créer le bot en amont ave BotFather sur Telegram et passer le Token à cette variable d'environnement

#--------------------------------------------------------------