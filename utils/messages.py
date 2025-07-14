###---Fichier pour stocker les messages qui seront affichés en Front dans le bot---

#Tout les messages sont formattés en HTML pour un beau effet visuel. Vous pouvez changer en Markdown si vous etes plus alaise avec
#Vous pouvez les ajuster selon vos préferences


#Message de bienvenue, apparait quand l'utilisateur lance la commande /start
welcome = """<b>🇹🇬Bienvenue sur le bot de consultation des résultats du examens nationaux {}🇹🇬</b>

📚 Pour consulter vos résultats, veuillez suivre les étapes suivantes :

<b>🚨Pour les candidats du BAC2 :</b>
    👉🏽Tapez /bac suivi de votre numéro de table, par exemple : <code>/bac 123456789</code>

<b>🚨Pour les candidats du BAC1(PROBA) :</b>
    👉🏽Tapez /proba suivi de votre numéro de table, par exemple : <code>/proba 123456789</code>

<b>🚨Pour les candidats du BEPC :</b>
    👉🏽Tapez /bepc suivi de votre numéro de table, par exemple : <code>/bepc 123456789</code>


⚠️Ce bot n’est pas un service officiel du gouvernement togolais, il vous facilite seulement l'acces a vos résultat via les résultats fournis par le site officiel du <a href="https://resultats.gouv.tg">Gouvernement Togolais</a> sans stocker vos données.
"""


#Message de droits et confdentialté, apparait quand l'utilisateur lance la commande /legal
legal_policy = """<b>⚠️Les résultats sont fournis par le site officiel du <a href="https://resultats.gouv.tg">Gouvernement Togolais</a>.

⚠️Evitez toute utilisation abusive de ce service afin de ne pas le surcharger.

⚠️Ce bot n'est pas un service officiel du gouvernement togolais, il vous facilite seulement l'accès à vos résultats sans stocker vos données.

⚠️Ce service est indépendant et non affilié à l’État togolais.</b>
"""


#Message d'aide sur les différentes commandes disponibles dans le bot et leurs utilisations, apparait quand l'utilisateur lance la commande /help
help_text = """<b>🇹🇬Aide pour le bot de consultation des résultats du examens nationaux🇹🇬</b>

<b>🚨Pour les candidats du BAC2 :</b>
    👉🏽Tapez /bac suivi de votre numéro de table, par exemple : <code>/bac 123456789</code>

<b>🚨Pour les candidats du PROBA :</b>
    👉🏽Tapez /proba suivi de votre numéro de table, par exemple : <code>/proba 123456789</code>

<b>🚨Pour les candidats du BEPC :</b>
    👉🏽Tapez /bepc suivi de votre numéro de table, par exemple : <code>/bepc 123456789</code>

⚠️Ce bot n’est pas un service officiel du gouvernement togolais, il vous facilite seulement l'acces a vos résultat via les résultats fournis par le site officiel du <a href="https://resultats.gouv.tg">Gouvernement Togolais</a> sans stocker vos données.
    """

#Message indiquant de fournir un numéro de tables, à formatter selon l'examen
no_num_table = "🤦🏾‍♂️Veuillez fournir votre numéro de table après la commande {}"

#Message indiquant qu'un numéro de table invalide, à formatter avec la raison
invalid_num_table = "🤦🏾‍♂️Le numéro de table fournit n'est pas valide car : {}"

#Message indiquant à l'utilisateur de choisir la filiere pour laquellle il veut consulter
choose_filiar = "🤖{} : Veuillez choisir la filière pour le candidat {}👇🏽" #On formattera avec le type d'examen et le numéro de table en amont.

#Message indiquant qu'une commande inconnue a été reçue
unknown_command = "🤖Commande inconnue. Utilisez /help pour voir les commandes disponibles"

#Message notifiant la réception directe d'un message contenant un numéro de table valide, à formatter avec le numéro de table

number_handler = "🤖Vous avez entré le numéro de table : <b>{}</b>, veuillez choisir l'examen à consulter👇🏽"