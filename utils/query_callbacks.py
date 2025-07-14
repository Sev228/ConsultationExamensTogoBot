##---Fichier contenant les fonctions repondant aux Callbacks Querys

from telegram.ext import ContextTypes
from telegram import Update
from telegram.constants import ParseMode
from utils.fetchers import Bac1, Bac2
from utils.globalUtils import log_me

#Dictionnaire pour matcher les alias aux vrais fillieres
bac1_matcher = {"gen": "GENERAL","tech": "TECHNIQUE"}
bac2_matcher = {"gen": "GENERAL","tech": "TECHNIQUE"}
async def bac1_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        query = update.callback_query
        await query.answer()
        data = query.data
        chat_id = query.from_user.id
        d = data.split("_")
        filiere = bac1_matcher[d[1]]
        candidate_number = d[2]
        res = Bac1(candidate_number, filiere)
        if not await res.check():
            await query.edit_message_text(
                text="❌Ce Numéro de table n'est pas valide.",
            )
            return
        if not await res.get_bac1_result():
            await query.edit_message_text(
                text="❌Ce Numéro de table n'est pas valide.",
            )
            return
        message = await res.affichage_formatte()
        try:
            await query.edit_message_text(
                text=message,
                parse_mode=ParseMode.HTML,
            )
        except TypeError:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
    except Exception as e:      #Si une exception innatendue est levée, on se la notifie
        await log_me(f"Une exception inconnue est survenue : {e}", "BAC1 Query Handler")


async def bac2_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        query = update.callback_query
        await query.answer()
        data = query.data
        chat_id = query.from_user.id
        d = data.split("_")
        filiere = bac2_matcher[d[1]]
        candidate_number = d[2]
        res = Bac2(candidate_number, filiere)
        if not await res.get_bac2_result():
            await query.edit_message_text(
                text="❌Ce Numéro de table n'est pas valide.",
            )
            return
        message = await res.affichage_formatte()
        try:
            await query.edit_message_text(
                text=message,
                parse_mode=ParseMode.HTML,
            )
        except TypeError:
            await context.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode=ParseMode.HTML
            )
    except Exception as e:       #Si une exception innatendue est levée, on se la notifie
        await log_me(f"Une exception inconnue est survenue : {e}", "BAC2 Query Handler")