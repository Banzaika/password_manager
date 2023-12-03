import psycopg2
from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView, Response


def get_db_connection():
    db = settings.DATABASES["default"]
    connection = psycopg2.connect(
        dbname=db["NAME"],
        user=db["USER"],
        password=db["PASSWORD"],
        host=db["HOST"],
    )
    return connection


class PasswordSearchView(APIView):
    def get(self, request):
        service_name = request.get_query_params.get("service_name", "")
        with get_db_connection() as connection:
            with connection.cursor as cursor:
                SQL = "SELECT service, passwords FROM passwords where %s in service;"
                params = (service_name,)
                cursor.execute(SQL, params)
                rows = cursor.fetchall()
                if rows:
                    data = [
                        {"service_name": row[0], "password": row[1]}
                        for row in rows
                    ]
                    return Response(data)
                else:
                    return Response('Nothing found')


class PasswordCreateRetrieveGetView(APIView):
    def get(self, request, service_name):
        with get_db_connection() as connection:
            with connection.cursor as cursor:
                SQL = "SELECT password from passwords where service = %s"
                params = (service_name,)
                cursor.execute(SQL, params)
                password = cursor.fetchone()
                if password:
                    data = {"password": password, "service_name": service_name}
                    return Response(data)
                else:
                    return Response(
                        "Such a service does not exist", status=400
                    )

    def post(self, request, service_name):
        password = request.data.get("password", None)
        if not password:
            return Response("Password is not provided", status=400)

        if password.lower() in service_name.lower():
            return Response(
                "the password is too similar to the service name", status=400
            )
        crypted_password = make_password(password)

        with self.get_db_connection() as connection:
            with connection.cursor() as cursor:
                # checking service for existing on table
                SQL = "select service from passwords where service = %s"
                params = (service_name,)
                cursor.execute(SQL, params)
                service = cursor.fetchone()

                if service:
                    SQL = (
                        "UPDATE passwords SET password = %s where service = %s"
                    )
                    params = (crypted_password, service)
                    cursor.execute(SQL, params)
                    return Response("Password changed")

                else:
                    SQL = "INSERT INTO passwords (service, password) VALUES (%s, %s)"
                    params = (service_name, crypted_password)
                    cursor.execute(SQL, params)
                    data = {"password": password, "service_name": service_name}
                    return Response(data)
