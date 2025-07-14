from aiohttp import ClientSession

from constants import DEVELOPPER_ID, LOG_BOT

async def log_me(text : str, scope : str = "ResExamBot") -> None:
    """
    Fonction asynchrone pour se notifier sur le bon fonctionnement l'execution du code
    :param text: Texte à recevoir
    :type text: str
    :param scope: Scope dans lequel la fonction est executé afin de facilité le deboguage
    :return: Rien du tout, si l'envoi de la notification ne reussit pas on affiche l'erreur dans la console
    :rtype: None
    """
    url = f"https://api.telegram.org/bot{LOG_BOT}/sendMessage"
    payload = {
        "chat_id": DEVELOPPER_ID,
        "text": f"[{scope}] : {text}"
    }
    async with ClientSession() as session:
        try:
            async with session.post(url, data=payload) as response:
                if response.status != 200:
                    print("❌ Échec de la notification Telegram vers vous meme")
        except Exception as e:
            print(f"❌ Erreur notification: {e}\n\nErreur voulu envoyé : [{scope}] : {text}")