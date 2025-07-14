###---Fichier pour stocker lees composants de générations de claviers cliquables et autres---

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


## -------------KEYBOARDS -------------------##
def gen_bac1_keyboard(candidate_number: int | str) -> InlineKeyboardMarkup:
    """
    Cette fonction génère un clavier pour la consultation des examens du Bac-1
    L'utilisateur dispose de deux boutons afin de choisir la filiere pour laquelle il veut consulter le résultat.
    :param candidate_number: Numéro de table du candidat
    :type candidate_number: int | str
    :return: Retourne le clavier adéquat
    :rtype: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓GENERAL", callback_data=f"bac1_gen_{candidate_number}")],
        [InlineKeyboardButton("🎓TECHNIQUE", callback_data=f"bac1_tech_{candidate_number}")]
    ])


def gen_bac2_keyboard(candidate_number: int | str) -> InlineKeyboardMarkup:
    """
    Cette fonction génère un clavier pour la consultation des examens du Bac-2
    L'utilisateur dispose de deux boutons afin de choisir la filiere pour laquelle il veut consulter le résultat.
    :param candidate_number: Numéro de table du candidat
    :type candidate_number: int | str
    :return: Retourne le clavier adéquat
    :rtype: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓GENERAL", callback_data=f"bac2_gen_{candidate_number}")],
        [InlineKeyboardButton("🎓TECHNIQUE", callback_data=f"bac2_tech_{candidate_number}")]
    ])


def gen_guess_keyboard(candidate_number: int | str) -> InlineKeyboardMarkup:
    """
    Fonction pour générer un clavier permettant à l'utilisateur de choisir un examen pour lequel il veut consulter
    :param candidate_number: Numero de table du candidat
    :type candidate_number: str | int
    :return: Retourne le clavier adéquat
    :rtype: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓BAC", callback_data=f"Nbac2_{candidate_number}")],
        [InlineKeyboardButton("🎓PROBA", callback_data=f"Nbac1_{candidate_number}")],
        [InlineKeyboardButton("🎓BEPC", callback_data=f"bepc_{candidate_number}")]
    ])
