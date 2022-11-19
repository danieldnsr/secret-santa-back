import json
import random
from django.conf import settings
from django.core.mail import send_mail
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

def order_players(players : list):
    players_to_assign = players.copy()
    players_to_recive = players.copy()
    result = {}
    for player in players:
        while True:
            secret_player = random.choice(players_to_assign)
            if player["name"] != secret_player["name"]:
                result[player["name"]] = secret_player
                break
            else: 
                continue
        index_assigned = players_to_assign.index(secret_player)
        players_to_assign.pop(index_assigned)
    return result


class sendEmail(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        #print(request.body)
        jd = json.loads(request.body)
        print(jd)
        admin_data = jd["admin"]
        players = jd["players"]
        email_from = settings.EMAIL_HOST_USER
        subject = "Amigo secreto"
        result_game = order_players(players)
        msm_admin = "Resultado juego: \n\n"
        for player in result_game:
            mail_player = [f"{result_game[player]['mail']}"]
            msm_player = f"Estimado {result_game[player]['name']} su amigo secreto es {player}."
            msm_admin += f"El jugador {result_game[player]['name']} con correo {result_game[player]['mail']} tiene de amigo secreto a {player}.\n"
            send_mail(subject, msm_player, email_from, mail_player)
            print(msm_player)
        if admin_data["name"] != "" and admin_data["mail"] != "":
            mail_admin = [admin_data["mail"]]
            send_mail(subject, msm_admin, email_from, mail_admin)
        mail_player = []
        mail_admin = []
        msm_player = ""
        msm_admin = ""
        return JsonResponse({"message" : "Success"})
