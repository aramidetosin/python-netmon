from flask import Flask, request


def create_app():
    app = Flask(__name__.split('.')[0])
    return app


quokka_app = create_app()

from db_apis import get_all_hosts, set_host
from db_apis import get_all_devices, set_device
from db_apis import get_all_services, set_service


@quokka_app.route("/hosts", methods=["GET", "PUT"])
def hosts():

    if request.method == "GET":
        return get_all_hosts()

    elif request.method == "PUT":
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on PUT", 400

        host = request.get_json()
        set_host(host)
        return {}, 204


@quokka_app.route("/devices", methods=["GET", "PUT"])
def devices():

    if request.method == "GET":
        return get_all_devices()

    elif request.method == "PUT":
        name = request.args.get("name")
        if not name:
            return "must provide name on PUT", 400

        device = request.get_json()
        set_device(device)
        return {}, 204


@quokka_app.route("/services", methods=["GET", "PUT"])
def services():

    if request.method == "GET":
        return get_all_services()

    elif request.method == "PUT":
        name = request.args.get("name")
        if not name:
            return "must provide name on PUT", 400

        service = request.get_json()
        set_service(service)
        return {}, 204