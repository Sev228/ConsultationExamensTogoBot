##---Fichier contenant les handlers de toutes les fonctions utilisées dans le projet
from telegram.ext import CallbackQueryHandler, MessageHandler, CommandHandler, filters
from utils.query_callbacks import bac1_handler, bac2_handler
from utils.commands import bepc, proba, bac, start, help, legal, unknown_command, exam_handler, number_handler


##----Callback Query Handlers

bac1_query_handler = CallbackQueryHandler(bac1_handler, pattern=r"^bac1")
bac2_query_handler = CallbackQueryHandler(bac2_handler, pattern=r"^bac2")
bot_exam_handler = CallbackQueryHandler(exam_handler, pattern=r"^(Nbac1|Nbac2|bepc)_\d+$")


##----Commands Handlers

bot_bepc = CommandHandler("bepc", bepc, filters.ChatType.PRIVATE)
bot_bac1 = CommandHandler("proba", proba, filters.ChatType.PRIVATE)
bot_bac2 = CommandHandler("bac", bac, filters.ChatType.PRIVATE)
bot_start = CommandHandler("start", start, filters.ChatType.PRIVATE)
bot_help = CommandHandler("help", help, filters.ChatType.PRIVATE)
bot_legal = CommandHandler("legal", legal, filters.ChatType.PRIVATE)


#-----Messages Handlers

bot_number_only_handler = MessageHandler(filters.Regex(r"^\d{5,}$") & filters.ChatType.PRIVATE, number_handler)
bot_unknown = MessageHandler(filters.COMMAND, unknown_command, filters.ChatType.PRIVATE)
