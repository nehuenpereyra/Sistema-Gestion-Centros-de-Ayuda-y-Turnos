from datetime import date, timedelta, datetime
from flask import request, abort, Response, jsonify
from flask import abort

from app.models.turn import Turn
from app.models.help_center import HelpCenter
from app.helpers.forms.TurnForm import TurnForm
import json


def quantity_turns_last():
    """Returns a json with the number of shifts reserved in a week for each day. 
    """
    return jsonify(Turn.get_quantity_turns_last())


def free_time(id):
    """Returns a json with the times of the available shifts.

    Keyword arguments:
    id -- integer help center id  
    """

    # Se comprueba que el centro exista
    center = HelpCenter.query.get(id)
    if not center:
        abort(404)

    # Si el centro no esta aceptado retorna error 400
    if not center.is_in_accepted_state():
        abort(404)

    # Se establece la fecha actual para buscar turnos libres
    search_date = date.today()

    # Si se envia una fecha por parametro se la establece para buscar turnos libres
    if request.args.get('fecha'):
        try:
            search_date = datetime.strptime(
                request.args.get('fecha'), '%d-%m-%Y').date()
        except ValueError:
            abort(500)

    send_data = json.loads(Turn.all_free_time_json(id, search_date))
    send_data["centro"] = HelpCenter.get(id).name

    return Response(response=json.dumps(send_data), status=200, mimetype="application/json")


def reserved(id):
    """Allows you to book an appointment for a help center
    Returns a json with the data sent for the reservation or if the reservation could not be made an about 400. 

    Keyword arguments:
    id -- integer help center id  
    """

    data = request.json
    print(request.json)

    try:
        # Se comprueba que el centro exista
        center = HelpCenter.query.get(data["centro_id"])
        if not center or (data["centro_id"] != id):
            abort(400)

        # Si el centro no esta aceptado retorna error 400
        if not center.is_in_accepted_state():
            abort(400)

        # Se realiza la conversion de string a datetime
        data_time_init = datetime.strptime(
            f"{data['fecha']} - {data['hora_inicio']}:00", '%Y-%m-%d - %H:%M:%S')
        data_time_end = datetime.strptime(
            f"{data['fecha']} - {data['hora_fin']}:00", '%Y-%m-%d - %H:%M:%S')

        # Se comprueba que la diferencia sea de media hora
        if ((data_time_end-data_time_init).total_seconds() / 60) != 30:
            abort(400)

        # Se establece el campo de telefono de donante en una cadena vacia por si no envio ese campo
        donor_phone_number = ""
        if 'telefono_donante' in data:
            donor_phone_number = data['telefono_donante']

        # Se crea uns instancia del formulario con los datos recibidos
        form = TurnForm(id=None, day_hour=data_time_init,
                        center_id=id, email=data['email_donante'],
                        donor_phone_number=donor_phone_number, meta={
                            'csrf': False},
                        name=data['nombre'], surname=data['apellido'])

        # Se validan los datos recibidos
        if form.validate_on_submit():
            Turn(help_center=center,
                 email=form.email.data,
                 donor_phone_number=form.donor_phone_number.data,
                 day_hour=form.day_hour.data,
                 name=form.name.data,
                 surname=form.surname.data).save()

            # Respuesta que se le entrega al cliente
            # Si envia campos demas no seran utilizados en la respuesta
            response = {
                "atributos":
                {
                    "centro_id": data["centro_id"],
                    "email_donante": data["email_donante"],
                    "hora_inicio": data["hora_inicio"],
                    "hora_fin": data["hora_fin"],
                    "fecha": data["fecha"],
                    "nombre": data["nombre"],
                    "apellido": data["apellido"]
                }
            }
            if 'telefono_donante' in data:
                response["atributos"]["telefono_donante"] = data["telefono_donante"]

            return jsonify(response)
        else:
            # Si no cumple con alguna de las validaciones
            print("El fomulario es Incorrecto o ya esta cargado")
            abort(400)

    except Exception as e:
        # Si existe alguna excepción imprime la excepción
        print(f"Excepción: {e}")
        abort(400)
