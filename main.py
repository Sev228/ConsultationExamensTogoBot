##----Fichier Main executant le bot selon votre plateforme
from telegram.ext import (
    ApplicationBuilder
)
from telegram import Update
from aiohttp import web
import os
import asyncio
from utils.globalUtils import log_me

#On importe les différents handlers crées
from utils.handlers import (
    bot_bepc,
    bot_help,
    bot_start,
    bot_bac1,
    bot_bac2,
    bot_number_only_handler,
    bot_unknown,
    bot_exam_handler,
    bot_legal,
    bac1_query_handler,
    bac2_query_handler
)
from dotenv import load_dotenv
load_dotenv()
#On recupere le TOKEN de notre bot directement depuis les variables d'environnement.
BOT_TOKEN = os.environ.get("BOT_TOKEN")

#-------------On recupere le port sur lequel sera exposé le Webhook
#--------A utiliser exclusivement si vous etes en hebergement sur serveur, en local vous en aurez pas besoin
PORT = int(os.environ.get("PORT", 8443))

#----Constante spécifiant l'environnement, True si on est sur serveur, False si on est en local
IS_PRODUCTION = False       #Fixer à False pour les tests en local


#----------Création de l'application (Le Bot Télégram)
app = ApplicationBuilder().token(BOT_TOKEN).build()

#------Ajouts des différents handlers
app.add_handler(bot_bac2)
app.add_handler(bot_bac1)
app.add_handler(bot_bepc)
app.add_handler(bot_help)
app.add_handler(bot_start)
app.add_handler(bot_number_only_handler)
app.add_handler(bac1_query_handler)
app.add_handler(bac2_query_handler)
app.add_handler(bot_exam_handler)
app.add_handler(bot_legal)
app.add_handler(bot_unknown)


#Interface Web pour voir le bon fonctionnement du code
#--------A utiliser exclusivement si vous etes en hebergement sur serveur, en local vous en aurez pas besoin
async def health_check(request):
    return web.Response(text="Bot Tourne bien !")

#Fonction qui recupere les updates reçus depuis le end-point du WebHook
#--------A utiliser exclusivement si vous etes en hebergement sur serveur, en local vous en aurez pas besoin
async def handle_webhook(request):
    if request.method == "POST":
        update_data = await request.json()
        update = Update.de_json(update_data, app.bot)
        await app.process_update(update)
        return web.Response(text="OK")
    return web.Response(text="Webhook endpoint")


#Fonction qui run le serveur Web, en utilisant les deux fonctions précédentes
#--------A utiliser exclusivement si vous etes en hebergement sur serveur, en local vous en aurez pas besoin
async def run_web_server():
    app_web = web.Application()
    app_web.router.add_get("/", health_check)
    app_web.router.add_get("/health", health_check)

    # Ajout du endpoint pour le webhook
    webhook_path = "/webhook"
    app_web.router.add_post(webhook_path, handle_webhook)
    app_web.router.add_get(webhook_path, handle_webhook)

    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()


# ─── Main asyncio ─────────────────────────────────────────────────────────
async def main():
    #Lancement du Bot
    await app.initialize()
    await app.start()

    # Configuration selon l'environnement
    if IS_PRODUCTION:
        #On recupere l'URL du Webhook directement depuis les variables d'environnement
        webhook_url = os.environ.get("WEBHOOK_URL")
        webhook_path = "/webhook"

        if webhook_url:
            # Supprimer tout webhook existant d'abord
            await app.bot.delete_webhook()
            # Configurer le nouveau webhook
            full_webhook_url = f"{webhook_url}{webhook_path}"
            await app.bot.set_webhook(full_webhook_url)
            print(f"Webhook configuré: {full_webhook_url}")
    else:
        # En local, on utilise le polling
        await app.bot.delete_webhook()
        await app.updater.start_polling()
        print("Polling démarré")

    # Démarrer le serveur web (obligatoire pour un environnement Serveur, négligeable en local)
    await run_web_server()

    print("Tout est prêt ✅")

    # Maintenir la boucle en vie
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:    #On lance le main en Asynchrone
        asyncio.run(main())
    except Exception as e:
        asyncio.run(log_me(f"Une erreur s'est produite lors de l'execution du bot: {e}", "MAIN THREAD"))    #Tres utile sur serveur
        print(f"Une erreur s'est produite lors de l'execution du bot: {e}")