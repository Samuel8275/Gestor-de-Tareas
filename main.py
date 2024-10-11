from crypt import methods

from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

import db
from models import Tarea

app = Flask(__name__)

@app.route("/")
def home():
    todasLasTareas = db.session.query(Tarea).all()
    for i in todasLasTareas:
        print(i)
    return render_template("index.html", listaDeTareas = todasLasTareas)

@app.route("/crear-tarea", methods=["POST"])
def crear():
    tarea = Tarea(contenido=request.form["contenidoTarea"], hecha=False)
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/eliminar-tarea/<id>")
def eliminar(id):
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)
