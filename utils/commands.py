from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram import Update
from utils.fetchers import Bepc
import utils.components as components
import utils.messages as messages
from utils.globalUtils import log_me


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui traite la commande /start
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """
    chat_id = update.effective_chat.id
    f_name = update.effective_chat.full_name
    message = messages.welcome.format(f_name)
    await context.bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

async def proba(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui traite la commande /proba pour les resultats du Bac 1
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """
    try:
        chat_id = update.effective_chat.id
        if len(context.args) == 0:      #On vérifie si l'utilisateur a fourni un numéro de table
            msg = messages.no_num_table.format("/proba")
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg,
            )
            return
        try:        #Bloc de code vérifiant la validité du numéro de table fourni
            candidate_number = int(context.args[0])
            if len(context.args[0]) < 5:
                msg = messages.invalid_num_table.format("Le numero de table doit dépasser 5 caractères.")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=msg
                )
                return
        except ValueError:
            msg = messages.invalid_num_table.format("Le numéro de table doit etre un nombre entier.")
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg
            )
            return
        else:
            #Si tout est bon, on génère le clavier et on l'envoi à l'utilisateur
            keyboard = components.gen_bac1_keyboard(candidate_number)
            msg = messages.choose_filiar.format("BAC1", candidate_number)
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg,
                reply_markup=keyboard
            )
    except Exception as e:
        await log_me(
            f"Une exception est survenue dans la fonction /proba {e}"
            "Fonction /proba"
        )

async def bac(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui traite la commande /bac pour les resultats du Bac 2
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """

    #Exactement la meme logique que pour la fonction précédente, seuls les messages en Front changent
    try:
        chat_id = update.effective_chat.id
        if len(context.args) == 0:
            msg = messages.no_num_table.format("/bac")
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg,
            )
            return
        try:
            candidate_number = int(context.args[0])
            if len(context.args[0]) < 5:
                msg = messages.invalid_num_table.format("Le numero de table doit dépasser 5 caractères.")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                )
                return
        except ValueError:
            msg = messages.invalid_num_table.format("Le numéro de table doit etre un nombre entier.")
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg
            )
            return
        else:
            keyboard = components.gen_bac2_keyboard(candidate_number)
            msg = messages.choose_filiar.format("BAC2", candidate_number)
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg,
                reply_markup=keyboard
            )
    except Exception as e:
        await log_me(
            f"Une exception est survenue dans la fonction /bac : {e}"
            "Fonction /bac"
        )

async def bepc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui traite la commande /bepc pour les resultats du Bepc
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """
    try:
        chat_id = update.effective_chat.id
        if len(context.args) == 0:
            msg = messages.no_num_table.format("/bepc")
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg
            )
            return
        try:
            candidate_number = int(context.args[0])
            if len(context.args[0]) < 5:
                msg = messages.invalid_num_table.format("Le numero de table doit dépasser 5 caractères.")
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=msg
                )
                return
        except ValueError:
            msg = messages.invalid_num_table.format("Le numéro de table doit etre un nombre entier.")
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg
            )
            return

        #Si tout est bon, on crée une instance de la class Bepc pour traiter les informations
        result = Bepc(candidate_number)
        if not await result.get_bepc_result():      #Si la méthode renvoie False, c'est qu'il y'a pas de correspondance pour le numéro de table donné dans la bd.
            msg = messages.invalid_num_table.format("n'existe pas.")
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg,
            )
            return
        #Si tout se passe bien, on continue
        result_text = await result.affichage_formatte()     #Methode pour avoir une chaine de caractère formattée en HTML agréable à visionner
        #On envoie le resultat à l'utilisateur
        await context.bot.send_message(
            chat_id=chat_id,
            text=result_text,
            parse_mode=ParseMode.HTML       #On parse le message en HTML pour avoir le resulat voulu
        )
    except Exception as e:
        await log_me(
            f"Une exception est survenue dans la fonction /bepc : {e}"
            "Fonction /bepc"
        )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui traite la commande /help pour fournir les différentes commandes disponibles dans le bot et leurs utilisations
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """
    chat_id = update.effective_chat.id
    help_text = messages.help_text
    await context.bot.send_message(
        chat_id=chat_id,
        text=help_text,
        parse_mode=ParseMode.HTML
    )

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui traite toutes les commandes inconnues.
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """
    chat_id = update.effective_chat.id
    msg = messages.unknown_command
    await context.bot.send_message(
        chat_id=chat_id,
        text=msg
    )

async def number_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui traite la reception directe d'un message contenant un numéro de table valide
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """
    try:
        chat_id = update.effective_chat.id
        try:
            candidate_number = int(update.message.text)
            msg = messages.number_handler.format(candidate_number)
        except ValueError:
            msg = messages.invalid_num_table.format("Le numéro de table doit etre un nombre entier.")
            await context.bot.send_message(
                chat_id=chat_id,
                text=msg
            )
            return
        keyboard = components.gen_guess_keyboard(candidate_number)
        await context.bot.send_message(
            chat_id=chat_id,
            text=msg,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await log_me(
            f"Une exception est survenue dans la fonction number_handler : {e}"
            "Fonction number_handler"
        )

async def exam_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui recupere l'examen choisit à la fonction précédente.
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """
    try:
        query = update.callback_query
        await query.answer()
        data = query.data
        chat_id = query.from_user.id
        d = data.split("_")
        exam_type = d[0]
        candidate_number = d[1]
        if exam_type == "bepc":
            result = Bepc(candidate_number)
            if not await result.check_num_table():

                await query.edit_message_text(
                    text=messages.invalid_num_table.format("Le numéro de table doit etre un nombre entier.")
                )
                return
            if not await result.get_bepc_result():
                await query.edit_message_text(
                    text=messages.invalid_num_table.format("n'existe pas.")
                )
                return
            result_text = await result.affichage_formatte()
            try:
                await query.edit_message_text(text=result_text, parse_mode=ParseMode.HTML)
                return
            except TypeError:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=result_text,
                    parse_mode=ParseMode.HTML
                )
                return

        keyboard = None
        msg = ""
        if exam_type == "Nbac1":
            keyboard = components.gen_bac1_keyboard(candidate_number)
            msg = messages.choose_filiar.format("BAC1", candidate_number)
        elif exam_type == "Nbac2":
            keyboard = components.gen_bac2_keyboard(candidate_number)
            msg = messages.choose_filiar.format("BAC2", candidate_number)
        if keyboard and msg:
            #On essaye de modifier l'ancien message direcement sans en envoyer un nouveau
            try:
                await query.edit_message_text(text=msg, reply_markup=keyboard)
            except TypeError:
                #Si cela échoue on envoie simplement le message
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=msg,
                    reply_markup=keyboard
                )
    except Exception as e:
        await log_me(
            f"Une exception est survenue dans la fonction exam_handler : {e}"
            "Fonction exam_handler"
        )

async def legal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fonction qui traite la commande /legal pour afficher les messages de confidentialités
    :param update: Objet Update fournit par Telegram
    :param context: Objet context convrant les différentes méthodes du Bot
    :return: Rien du tout
    """
    chat_id = update.effective_chat.id
    legal_text = messages.legal_policy
    await context.bot.send_message(
        chat_id=chat_id,
        text=legal_text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )