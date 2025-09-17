

from flask import Flask, render_template_string, request, redirect, url_for
import numpy as np

app = Flask(__name__)


# Classes
# -------------------
class Etudiant:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age
        self.matieres = []

    def ajouter_matiere(self, matiere, note):
        self.matieres.append((matiere, note))

    def retirer_matiere(self, matiere):
        self.matieres = [m for m in self.matieres if m[0] != matiere]

    def moyenne(self):
        notes = [note for (_, note) in self.matieres]
        return np.mean(notes) if notes else 0

class GestionEtudiants:
    def __init__(self):
        self.etudiants = []

    def ajouter_etudiant(self, etudiant):
        self.etudiants.append(etudiant)

    def chercher_etudiant(self, nom):
        for e in self.etudiants:
            if e.nom.lower() == nom.lower():
                return e
        return None

    def moyenne_par_matiere(self):
        matieres_dict = {}
        for e in self.etudiants:
            for mat, note in e.matieres:
                if mat not in matieres_dict:
                    matieres_dict[mat] = []
                matieres_dict[mat].append(note)
        return {m: np.mean(notes) for m, notes in matieres_dict.items()}

    def liste_etudiants(self):
        return self.etudiants

# -------------------
# Instance de gestion
# -------------------
gestion = GestionEtudiants()

# -------------------
# Flask routes
# -------------------
@app.route("/")
def index():
    moyennes_globales = {e.nom: e.moyenne() for e in gestion.liste_etudiants()}
    moyennes_matieres = gestion.moyenne_par_matiere()
    
    template = """ 
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Gestion des Étudiants</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
    <div class="container py-5">
        <h1 class="text-center text-primary mb-4">📚 Gestion des Étudiants (OOP)</h1>

        <div class="card shadow-sm p-4 mb-4">
            <h3>Ajouter un étudiant</h3>
            <form method="POST" action="/ajouter">
                <div class="row g-2">
                    <div class="col-md-6"><input class="form-control" name="nom" placeholder="Nom" required></div>
                    <div class="col-md-6"><input type="number" class="form-control" name="age" placeholder="Âge" required></div>
                </div>
                <hr>
                <h5>Matières & Notes</h5>
                {% for i in range(1,6) %}
                <div class="row g-2 mb-2">
                    <div class="col-md-6"><input class="form-control" name="matiere{{i}}" placeholder="Matière {{i}}"></div>
                    <div class="col-md-6"><input type="number" step="0.01" class="form-control" name="note{{i}}" placeholder="Note"></div>
                </div>
                {% endfor %}
                <button class="btn btn-success mt-3" type="submit">Ajouter</button>
            </form>
        </div>

        <div class="card shadow-sm p-4 mb-4">
            <h3>Liste des étudiants</h3>
            <table class="table table-striped">
                <thead><tr><th>Nom</th><th>Âge</th><th>Moyenne</th><th>Matières</th></tr></thead>
                <tbody>
                    {% for e in gestion.liste_etudiants() %}
                    <tr>
                        <td>{{ e.nom }}</td>
                        <td>{{ e.age }}</td>
                        <td><strong>{{ "%.2f"|format(e.moyenne()) }}</strong></td>
                        <td>
                            {% for mat, note in e.matieres %}
                                <span class="badge bg-primary">{{ mat }}: {{ note }}</span>
                            {% endfor %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <div class="card shadow-sm p-4">
            <h3>Moyenne par matière</h3>
            <ul class="list-group">
                {% for m, moyenne in moyennes_matieres.items() %}
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    {{ m }} <span class="badge bg-info">{{ "%.2f"|format(moyenne) }}</span>
                </li>
                {% endfor %}
            </ul>
        </div>
    </div>
    </body>
    </html>
    """
    return render_template_string(template, gestion=gestion, moyennes_matieres=moyennes_matieres)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    nom = request.form.get("nom")
    age = int(request.form.get("age"))
    etudiant = Etudiant(nom, age)
    for i in range(1,6):
        mat = request.form.get(f"matiere{i}")
        note = request.form.get(f"note{i}")
        if mat and note:
            etudiant.ajouter_matiere(mat, float(note))
    gestion.ajouter_etudiant(etudiant)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




# from flask import Flask, render_template_string, request, redirect, url_for
# import numpy as np

# app = Flask(__name__)

# # -------------------
# # Classes
# # -------------------
# class Etudiant:
#     def __init__(self, nom, age):
#         self.nom = nom
#         self.age = age
#         self.matieres = []

#     def ajouter_matiere(self, matiere, note):
#         self.matieres.append((matiere, note))

#     def retirer_matiere(self, matiere):
#         self.matieres = [m for m in self.matieres if m[0] != matiere]

#     def moyenne(self):
#         notes = [note for (_, note) in self.matieres]
#         return np.mean(notes) if notes else 0

# class GestionEtudiants:
#     def __init__(self):
#         self.etudiants = []

#     def ajouter_etudiant(self, etudiant):
#         self.etudiants.append(etudiant)

#     def moyenne_par_matiere(self):
#         matieres_dict = {}
#         for e in self.etudiants:
#             for mat, note in e.matieres:
#                 if mat not in matieres_dict:
#                     matieres_dict[mat] = []
#                 matieres_dict[mat].append(note)
#         return {m: np.mean(notes) for m, notes in matieres_dict.items()}

#     def liste_etudiants(self):
#         return self.etudiants

# # -------------------
# # Instance
# # -------------------
# gestion = GestionEtudiants()

# # -------------------
# # Flask routes
# # -------------------
# @app.route("/")
# def index():
#     moyennes_globales = {e.nom: e.moyenne() for e in gestion.liste_etudiants()}
#     moyennes_matieres = gestion.moyenne_par_matiere()
    
#     template = """
#     <!DOCTYPE html>
#     <html lang="fr">
#     <head>
#         <meta charset="UTF-8">
#         <title>Gestion des Étudiants</title>
#         <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
#         <style>
#             body { background-color: #f2f7ff; font-family: 'Segoe UI', sans-serif; }
#             h1 { font-weight: bold; }
#             .card { border-radius: 15px; }
#             .badge { font-size: 0.9rem; margin: 2px; }
#             .table-striped > tbody > tr:nth-of-type(odd) { background-color: #e9f0ff; }
#         </style>
#     </head>
#     <body>
#         <div class="container py-5">
#             <h1 class="text-center text-primary mb-5">📘 Gestion des Étudiants</h1>

#             <!-- Formulaire -->
#             <div class="card shadow-sm p-4 mb-5">
#                 <h3 class="mb-4">Ajouter un étudiant</h3>
#                 <form method="POST" action="/ajouter">
#                     <div class="row g-3 mb-3">
#                         <div class="col-md-6"><input class="form-control" name="nom" placeholder="Nom" required></div>
#                         <div class="col-md-6"><input type="number" class="form-control" name="age" placeholder="Âge" required></div>
#                     </div>
#                     <h5>Matières & Notes</h5>
#                     {% for i in range(1,6) %}
#                     <div class="row g-3 mb-2">
#                         <div class="col-md-6"><input class="form-control" name="matiere{{i}}" placeholder="Matière {{i}}"></div>
#                         <div class="col-md-6"><input type="number" step="0.01" class="form-control" name="note{{i}}" placeholder="Note"></div>
#                     </div>
#                     {% endfor %}
#                     <button class="btn btn-primary mt-3 w-100">Ajouter l'étudiant</button>
#                 </form>
#             </div>

#             <!-- Liste des étudiants -->
#             <div class="card shadow-sm p-4 mb-5">
#                 <h3 class="mb-4">Liste des étudiants</h3>
#                 <div class="table-responsive">
#                     <table class="table table-hover align-middle">
#                         <thead class="table-dark">
#                             <tr><th>Nom</th><th>Âge</th><th>Moyenne</th><th>Matières</th></tr>
#                         </thead>
#                         <tbody>
#                             {% for e in gestion.liste_etudiants() %}
#                             <tr>
#                                 <td>{{ e.nom }}</td>
#                                 <td>{{ e.age }}</td>
#                                 <td><strong>{{ "%.2f"|format(e.moyenne()) }}</strong></td>
#                                 <td>
#                                     {% for mat, note in e.matieres %}
#                                         <span class="badge bg-success">{{ mat }}: {{ note }}</span>
#                                     {% endfor %}
#                                 </td>
#                             </tr>
#                             {% endfor %}
#                         </tbody>
#                     </table>
#                 </div>
#             </div>

#             <!-- Moyenne par matière -->
#             <div class="card shadow-sm p-4">
#                 <h3 class="mb-4">Moyenne par matière</h3>
#                 <ul class="list-group list-group-flush">
#                     {% for m, moyenne in moyennes_matieres.items() %}
#                     <li class="list-group-item d-flex justify-content-between align-items-center">
#                         {{ m }} <span class="badge bg-warning text-dark">{{ "%.2f"|format(moyenne) }}</span>
#                     </li>
#                     {% endfor %}
#                 </ul>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     return render_template_string(template, gestion=gestion, moyennes_matieres=moyennes_matieres)

# @app.route("/ajouter", methods=["POST"])
# def ajouter():
#     nom = request.form.get("nom")
#     age = int(request.form.get("age"))
#     etudiant = Etudiant(nom, age)
#     for i in range(1,6):
#         mat = request.form.get(f"matiere{i}")
#         note = request.form.get(f"note{i}")
#         if mat and note:
#             etudiant.ajouter_matiere(mat, float(note))
#     gestion.ajouter_etudiant(etudiant)
#     return redirect(url_for("index"))

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
























# from flask import Flask, render_template, request, redirect, url_for
# import numpy as np

# app = Flask(__name__)

# etudiants = []

# def ajouter_etudiant(nom, age, matieres):
#     etudiant = {"nom": nom, "age": age, "matieres": matieres}
#     etudiants.append(etudiant)

# def calculer_moyenne(etudiant):
#     notes = [note for (_, note) in etudiant["matieres"]]
#     return np.mean(notes) if notes else 0

# def moy_par_matiere():
#     matieres_dict = {}
#     for e in etudiants:
#         for matiere, note in e["matieres"]:
#             if matiere not in matieres_dict:
#                 matieres_dict[matiere] = []
#             matieres_dict[matiere].append(note)
#     return {m: np.mean(notes) for m, notes in matieres_dict.items()}

# @app.route("/")
# def index():
#     moyennes_globales = {e["nom"]: calculer_moyenne(e) for e in etudiants}
#     moyennes_matieres = moy_par_matiere()
#     return render_template("index.html", etudiants=etudiants, moyennes=moyennes_globales, moyennes_matieres=moyennes_matieres)

# @app.route("/ajouter", methods=["POST"])
# def ajouter():
#     nom = request.form.get("nom")
#     age = int(request.form.get("age"))
#     matieres = []
#     for i in range(1,6):
#         matiere = request.form.get(f"matiere{i}")
#         note = request.form.get(f"note{i}")
#         if matiere and note:
#             matieres.append((matiere, float(note)))
#     ajouter_etudiant(nom, age, matieres)
#     return redirect(url_for("index"))

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
