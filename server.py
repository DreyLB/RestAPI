from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text

conectar_db = create_engine('sqlite:///APIRestPython/db/exemplo.db')
app = Flask(__name__)
api = Api(app)


class Users(Resource):
    def get(self):
        conectar = conectar_db.connect()
        busca = conectar.execute(text("select * from user"))
        resultado = [dict(zip(tuple(busca.keys()), i)) for i in busca.cursor]
        return jsonify(resultado)

    def post(self):
        conn = conectar_db.connect()
        name = request.json['name']
        email = request.json['email']

        conn.execute(text(
            "insert into user values(null, '{0}','{1}')").format(name, email))

        query = conn.execute(text('select * from user order by id desc limit 1'))
        resultado = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(resultado)

    def put(self):
        conectar = conectar_db.connect()
        id = request.json['id']
        name = request.json['name']
        email = request.json['email']
        conectar.execute(
            text(f"update user set name =' {str(name)} ', email =' {str(email)} '  where id =%d  % {int(id)}"))
        query = conectar.execute(text(f"select * from user where id=%d  % {int(id)}"))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)


class UserById(Resource):
    def delete(self, id):
        conn = conectar_db.connect()
        conn.execute("delete from user where id=%d " % int(id))
        return {"status": "success"}

    def get(self, id):
        conn = conectar_db.connect()
        query = conn.execute("select * from user where id =%d " % int(id))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)


api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<id>')

if __name__ == '__main__':
    app.run()
