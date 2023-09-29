from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text, select
from flask_cors import CORS

conectar_db = create_engine('sqlite:///db/exemplo.db')
app = Flask(__name__)
api = Api(app)
CORS(app, origins='http://localhost:5173')


class Users(Resource):
    def get(self):
        print("entrei")
        conectar = conectar_db.connect()
        busca = conectar.execute(text("select * from user"))
        resultado = [dict(zip(tuple(busca.keys()), i)) for i in busca.cursor]
        return jsonify(resultado)

    def post(self):
        conectar = conectar_db.connect()
        name = request.json['name']
        email = request.json['email']

        conectar.execute(text(
            "insert into user values(null, '{0}','{1}')").format(name, email))

        busca = conectar.execute(text('select * from user order by id desc limit 1'))
        resultado = [dict(zip(tuple(busca.keys()), i)) for i in busca]
        return jsonify(resultado)

    def put(self):
        conectar = conectar_db.connect()
        id = request.json['id']
        name = request.json['name']
        email = request.json['email']
        conectar.execute(
            text(f"update user set name =' {str(name)} ', email =' {str(email)} '  where id =%d  % {int(id)}"))
        busca = conectar.execute(text(f"select * from user where id=%d  % {int(id)}"))
        result = [dict(zip(tuple(busca.keys()), i)) for i in busca]
        return jsonify(result)


class UserById(Resource):
    def delete(self, id):
        conectar = conectar_db.connect()
        conectar.execute(text("delete from user where id=%d " % int(id)))
        return {"status": "success"}

    def get(self, id):
        conectar = conectar_db.connect()
        busca = conectar.execute(text("select * from user where id =%d" % int(id)))
        result = [dict(zip(tuple(busca.keys()), i)) for i in busca]
        return jsonify(result)


api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<id>')

if __name__ == '__main__':
    app.run()
