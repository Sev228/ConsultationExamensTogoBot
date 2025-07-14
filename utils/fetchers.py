##--- Fichier contenant des class pour chaque examens ainsi que leurs methodes appropriées
#Les methodes sont ensentiellement basées sur du scrap(Appel vers API externes)

import aiohttp  #Pour Faire les requetes API en asynchrone, utiliser requests si vous etes plus alaise avec
import asyncio
import json

from utils.globalUtils import log_me

SLEEP = 0.5  #Constante pour les sleep dans les fonctions afin d'éviter de saturer les serveurs


class Bepc:
    """
    Class pour les consultations du BEPC 
    """
    def __init__(self, num_table: str | int):
        """
        Constructeur de la class, prend en parametre le numero de table du candidat recherché
        :param num_table: Numéro de table du candidat recheché
        :type num_table: str | int
        """
        self.num_table = num_table
        self.url = None         #Vous verrez à quoi cela servira 
        self.session = None     #Attribut pour stocker la session AioHttp avec laquelle les requetes seront faite
        self.data = None        #Attribut pour sytocker les données du resultat

    async def check_num_table(self) -> bool:
        """
        Méthode pour checker si tous les parametres sont bons
        :return: Booléen : True si tout est en ordre, False sinon
        :rtype: bool
        """
        return f"{self.num_table}".isdigit()

    async def get_token_url(self) -> bool:
        """
        Fonction qui recupere le token pour le numero de table donné
        :returns: Retourne le token
        :rtype: str
        """
        if not self.session:
            return False
        payload_post = {"num_table": f"{self.num_table}"}
        
        #Point API depuis lequel on genere un token securisé, ce token servira ensuite pour recuperer les données.
        api_post = "https://resultats.gouv.tg/api/examens/generate-url/bepc"
        
        headers_post = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://resultats.gouv.tg/",
            #On Usurpe un navigateur normal pour contrer les restrictions
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
        }
        
        response = await self.session.post(api_post, json=payload_post, headers=headers_post)
        
        try:
            data = await response.json()
            url = data["url"]
            self.url = url
        except KeyError:
            if self.session:
                await self.session.close()
            return False
        except aiohttp.ClientResponseError:
            if self.session:
                await self.session.close()
            await log_me("❌ Erreur de réponse du serveur lors de la récupération du token pour le numéro de table.",
                         "BEPC")
            return False
        except Exception as e:
            if self.session:
                await self.session.close()
            await log_me(
                f"❌ Une erreur inconnue s'est produite lors de la récupération du token pour le numéro de table : {e}",
                "BEPC")
            return False
        else:
            return True

    async def get_result_data(self) -> bool:
        """
        Fonction qui recupere les resultats BEPC d'un eleve précis grace à son numéro de table
        :returns: Retourne un boolean indiquant si la récupération des données a réussi ou non
        :rtype: bool
        """
        if not self.url or not self.session:
            return False
        headers_get = {
            "Accept": "application/json",
            "Referer": "https://resultats.gouv.tg/"
        }
        #Point API pour recuperer finalement les resultats dans un format Json
        api_get = f"https://resultats.gouv.tg/api/examens/bepc/{self.url}"
        response = await self.session.get(api_get, headers=headers_get)
        try:
            data = await response.json()
            self.data = data[0]
        except aiohttp.ClientResponseError:
            await log_me("❌ Erreur de réponse du serveur lors de la récupération des résultats BEPC.",
                         "BEPC")
            return False
        except IndexError:
            return False
        except Exception as e:
            await log_me(f"❌ Une erreur inconnue s'est produite lors de la récupération des résultats BEPC : {e}",
                         "BEPC")
            return False
        else:
            return True
        finally:
            if self.session:
                await self.session.close()

    async def get_bepc_result(self) -> bool:
        """
        Fonction principale qui recupere les resultats BEPC d'un eleve précis grace à son numéro de table
        :returns: Retourne un boolean indiquant si la récupération des données a réussi ou non
        :rtype: bool
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
        except aiohttp.ClientError:
            await log_me("❌ Erreur lors de la création de la session aiohttp pour récupérer les résultats BEPC.",
                         "BEPC")
            return False
        else:
            try:
                if not await self.get_token_url():
                    return False
                return await self.get_result_data()
            except Exception as e:
                await log_me(
                    f"❌ Une erreur inconnue s'est produite dans la fonction principale de récupération des résultats BEPC : {e}",
                    "BEPC")
                return False
        finally:
            if self.session:
                await self.session.close()

    async def affichage_formatte(self) -> str:
        """
        Fonction qui affiche les resultats de l'eleve de manière formatée
        :returns: Retourne une chaine de caractere contenant les resultats formatés en HTML
        :rtype: str
        """
        dico = self.data
        if not dico:
            return "❌Aucun résultat trouvé pour ce numéro de table."
        formatted_data = f"""<u>EXAMEN DU BEPC 2024-2025</u>
👤 Nom et Prénom : <b>{dico.get("nom_prenom", "Inconnu")}</b>

🚻 Sexe : <b>{dico.get("sexe", "Pas de Sexe")}</b>

🆔 Numéro de Table : <b>{dico.get("num_table", "Pas trouvé")}</b>

🌍 Région : <b>{dico.get("region", "Pas de Région")}</b>

🎓 Décision : <b>{dico.get("mention", "Pas trouvé")}</b>

📊 Moyenne : <b>{dico.get("moyenne", "Pas trouvé")}</b>

<b>🤖By @Resultats_Examens_Tg_Bot</b>
"""
        return formatted_data


class Bac1:
    def __init__(self, num_table: str | int, enseignement: str):
        """
        Constructeur de la class, prend en parametre le numero de table du candidat recherché et sa filiere d'enseignement
        :param num_table: Numéro de table du candidat
        :param enseignement: Filiere d'enseignement du candidat (GENERAL ou TECHNIQUE, autre que ces deux ne passe pas)
        """
        self.num_table = num_table
        #Meme Logique que pour la class Bepc
        self.url = None
        self.session = None     
        self.data = None
        self.enseignement = enseignement

    async def check(self) -> bool:
        """
        Fonction pour voir si tous les attributs sont bons
        :return: boolean : True si tout est bon, False sinon
        :rtype: bool
        """
        return f"{self.num_table}".isdigit() and self.enseignement in ["TECHNIQUE", "GENERAL"]

    # Les autres méthodes pour Bac1 seraient similaires à celles de Bepc, adaptées pour le Bac 1.

    async def get_token_url(self) -> bool:
        """
        Fonction qui recupere le token pour le numero de table donné
        :returns: Retourne le token
        :rtype: str
        """
        if not self.session:
            return False
        payload_post = {"num_table": f"{self.num_table}", "type_enseignement": f"{self.enseignement}"}
        api_post = "https://resultats.gouv.tg/api/examens/generate-url/bac1"
        headers_post = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://resultats.gouv.tg/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
        }
        try:
            response = await self.session.post(api_post, json=payload_post, headers=headers_post)
            data = await response.json()
            url = data["url"]
            self.url = url
        except KeyError:
            if self.session:
                await self.session.close()
            return False
        except aiohttp.ClientResponseError:
            if self.session:
                await self.session.close()
            await log_me("❌ Erreur de réponse du serveur lors de la récupération du token pour le numéro de table.",
                         "BAC1")
            return False
        except Exception as e:
            if self.session:
                await self.session.close()
            await log_me(
                f"❌ Une erreur inconnue s'est produite lors de la récupération du token pour le numéro de table : {e}",
                "BAC1")
            return False
        else:
            return True

    async def get_result_data(self) -> bool:
        """
        Fonction qui recupere les resultats de BAC1 d'un eleve précis grace à son numéro de table
        :returns: Retourne un boolean indiquant si la récupération des données a réussi ou non
        :rtype: bool
        """
        if not self.url or not self.session:
            return False
        headers_get = {
            "Accept": "application/json",
            "Referer": "https://resultats.gouv.tg/"
        }
        api_get = f"https://resultats.gouv.tg/api/examens/bac1/{self.url}"
        try:
            response = await self.session.get(api_get, headers=headers_get)
            data = await response.json()
            self.data = data[0]
        except aiohttp.ClientResponseError:
            await log_me("❌ Erreur de réponse du serveur lors de la récupération des résultats BAC1.", "BAC1")
            return False
        except IndexError:
            return False
        except Exception as e:
            await log_me(f"❌ Une erreur inconnue s'est produite lors de la récupération des résultats BAC1 : {e}",
                         "BAC1")
            return False
        else:
            return True
        finally:
            if self.session:
                await self.session.close()

    async def get_bac1_result(self) -> bool:
        """
        Fonction principale qui recupere les resultats BAC1 d'un eleve précis grace à son numéro de table
        :returns: Retourne un boolean indiquant si la récupération des données a réussi ou non
        :rtype: bool
        """
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
        except aiohttp.ClientError:
            await log_me("❌ Erreur lors de la création de la session aiohttp pour récupérer les résultats BAC1.",
                         "BAC1")
            return False
        else:
            try:
                if not await self.get_token_url():
                    return False
                return await self.get_result_data()
            except Exception as e:
                await log_me(
                    f"❌ Une erreur inconnue s'est produite dans la fonction principale de récupération des résultats BAC1 : {e}",
                    "BAC1")
                return False
        finally:
            if self.session:
                await self.session.close()

    async def affichage_formatte(self) -> str:
        """
        Fonction qui affiche les resultats de l'eleve de manière formatée
        :returns: Retourne une chaine de caractere contenant les resultats formatés en HTML
        :rtype: str
        """
        dico = self.data
        if not dico:
            formatted_data = "Aucun résultat trouvé pour ce numéro de table."
        else:
            decision = (dico.get("decision", "Pas trouvé")).lower()
            moyenne = dico.get("moyenne")
            ajout = "Amégan l'année prochaine aussi🤣" if decision == "ajourne" else "Félicitations pour votre réussite ! 🎉"
            txt_moyenne = f"\n\n📊 Moyenne : <b>{moyenne}</b>" if moyenne else ""
            formatted_data = f"""<u>EXAMEN DU BAC-1 2024-2025</u>
👤Nom et Prénom : <b>{dico.get("nom_prenom", "Inconnu")}</b>

🚻Sexe : <b>{dico.get("sexe", "Pas de Sexe")}</b>

🏫Centre d'écrit : <b>{dico.get("centre_decrit", "Pas trouvé")}</b>

🎓Série :  <b>{dico.get("serie_filiere", "Pas de Série")}</b>

🆔Numéro de Table : <b>{dico.get("num_table", "Pas trouvé")}</b>

👀Décision : <b>{dico.get("mention", "Pas trouvé")}</b>{txt_moyenne}

{ajout}
<b>🤖By @Resultats_Examens_Tg_Bot</b>
"""
        return formatted_data


class Bac2:
    """Class pour les consultation du Bac 2"""
    def __init__(self, num_table: int | str, enseignement: str):
        """
        Constructeur de la class BAC2
        :param num_table: Numéro de table de l'étudiant recheché
        :param enseignement: Filiere d'enseignement, ce parametre est vain car l'API ne le prends plus en copte
        """
        self.num_table = num_table
        self.enseignement = "general"
        self.data = None
        
    #Fonction de check plus trop utile mais gardé
    
    async def check(self) -> bool:
        return f"{self.num_table}".isdigit() and self.enseignement == "general"

    async def get_bac2_result(self) -> bool:
        """
        Fonction unique pour recuperer les resultats d'un candidat de Bac2
        :return: Retourne True si la requete a reussi, False autrement
        :rtype: bool
        """
        data = {"year": 2025, "type": self.enseignement, "numTable": self.num_table}

        headers = {
            "Accept": "*/*",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://officedubactogo.net/Views/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
        }

        api_url = "https://officedubactogo.net/Views/Async/check-result.php"

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, headers=headers,
                                        data=data) as response:  #Remplacer data par json en cas d'échec de la requete
                    data_text = await response.text()
                    data = json.loads(data_text)  #Essayer de changer l'encodage du formattage Json en cas d'échec
                    self.data = data["data"]
            except aiohttp.ClientResponseError:
                await log_me("❌ Erreur de réponse du serveur lors de la récupération des résultats BAC2.",
                             "BAC2")
                return False
            except KeyError:
                return False
            except Exception as e:
                await log_me(f"❌ Une erreur inconnue s'est produite lors de la récupération des résultats BAC1 : {e}",
                             "BAC2")
                return False
            else:
                return True

    async def affichage_formatte(self) -> str:
        """
        Fonction pour obtenir une chaine formattée lisible en HTML
        :return: Chaine de caractère formattée du resultat
        :rtype: str
        """
        dico = self.data
        if not dico:
            return "Aucun résultat trouvé pour ce numéro de table❌"

        #Dictionnaire pour matcher les données fournies par l'API
        matcher = {"AJ": "Ajournée", "Adss": "Admissible", "ADM": "Admis(e)"}

        nom_prenoms = f"{dico.get("nom")} {dico.get("prenoms")}"
        sexe = dico.get("sexe", "")
        naissance = f"{dico.get("dateDeNaissance", "00-00-0000")} à {dico.get("lieuDeNaissance", "XX")}"
        serie = dico.get("serie_filiere")
        num_table = f"{dico.get("numTable", "Pas trouvé")}"
        jury = f"{dico.get("jury", "Pas trouvé")}"
        decision = (dico.get("decision", "Pas trouvé"))
        dec = f"🎓Décision : <b>{matcher.get(decision, "?    ")} {dico.get("mention", " ")}</b>\n\n"
        moyenne = dico.get("moyenne")
        ajout = "Amégan l'année prochaine aussi🤣" if decision == "AJ" else "Félicitations pour votre réussite !🎉"
        txt_moyenne = f"📊 Moyenne : <b>{moyenne}</b>\n\n" if moyenne else ""

        #Un peut spaghetti, a refactoriser à votre gout.....
        return f"""<u>EXAMEN DU BAC-2 2024-2025</u>

👤Nom et Prénoms : <b>{nom_prenoms}</b>

{f"🚻Sexe : <b>{sexe}</b>\n\n" if sexe else ""}{f"🤱🏽Date de Naissance : <b>{naissance}</b>\n\n"}{f"🎒Série : <b>{serie}</b>\n\n" if serie else ""}{f"🆔Numéro de Table : <b>{num_table}</b>\n\n"}{f"Jury : <b>{jury}</b>\n\n"}{dec}{txt_moyenne}{ajout}
<b>🤖By @Resultats_Examens_Tg_Bot</b>
"""

#Fonction main pour tester les differentes class
async def main():
    bac2 = Bac2("42750", "general")  # Remplacez 123456 par le numéro de table que vous souhaitez tester
    if await bac2.check():
        await bac2.get_bac2_result()
        formatted_result = await bac2.affichage_formatte()
        print(formatted_result)
    else:
        print("Enseignement invalide.")


if __name__ == '__main__':
    asyncio.run(main())
