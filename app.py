from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__, template_folder="pages", static_folder="css")

# Database configuration (replace with your actual credentials)
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'biblio'
}

@app.route('/')
def index():
    return render_template('index.html')

# Route to add a book
@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if request.method == 'POST':
        isbn = request.form['isbnLivre']
        titre = request.form['titreLivre']
        auteur = request.form['auteurLivre']
        annee_edition = request.form['anneeEdition']
        prix = request.form['prixLivre']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO livre (isbn, titre, auteur, annee_edition, prix)
            VALUES (%s, %s, %s, %s, %s)
        """, (isbn, titre, auteur, annee_edition, prix))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('ajouter_livre.html')

# Route to register a subscriber
@app.route('/inscrire_abonne', methods=['GET', 'POST'])
def inscrire_abonne():
    if request.method == 'POST':
        nom = request.form['nomAbonne']
        prenom = request.form['prenomAbonne']
        telephone = request.form['telephoneAbonne']
        email = request.form['emailAbonne']
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO abonne (nom, prenom, telephone, Email)
            VALUES (%s, %s, %s, %s)
        """, (nom, prenom, telephone, email))
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('inscrire_abonne.html')

@app.route('/emprunter_livre', methods=['GET', 'POST'])
def emprunter_livre():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch all abonnés and livres
    cursor.execute("SELECT id, nom, prenom FROM abonne")
    abonnes = cursor.fetchall()
    cursor.execute("SELECT id, titre FROM livre")
    livres = cursor.fetchall()

    if request.method == 'POST':
        # Retrieve form data
        id_abonne = request.form.get('idAbonne')
        id_livre = request.form.get('idLivre')
        date_emrpunt = request.form['dateEmrpunt']
        date_retour = request.form['dateRetour']

        # Debugging: Print the values
        print(f"Received Abonné ID: {id_abonne}, Livre ID: {id_livre}")

        # Check if the abonné and livre exist
        cursor.execute("SELECT id FROM abonne WHERE id = %s", (id_abonne,))
        abonne_exists = cursor.fetchone()
        
        cursor.execute("SELECT id FROM livre WHERE id = %s", (id_livre,))
        livre_exists = cursor.fetchone()

        if not abonne_exists:
            print("Erreur : L'abonné n'existe pas dans la table abonne.")
            return "Erreur : Abonné introuvable", 400

        if not livre_exists:
            print("Erreur : Le livre n'existe pas dans la table livre.")
            return "Erreur : Livre introuvable", 400

        # Insert into emprunt table if both abonné and livre exist
        cursor.execute("""
            INSERT INTO emprunt (id_livre, id_abonne, date_emrpunt, date_retour)
            VALUES (%s, %s, %s, %s)
        """, (id_livre, id_abonne, date_emrpunt, date_retour))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('emprunter_livre.html', abonnes=abonnes, livres=livres)

@app.route('/rechercher_abonne', methods=['GET'])
# Route for searching a subscriber by name or first name
def rechercher_abonne():
    terme = request.args.get('terme', '')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nom, prenom FROM abonne WHERE nom LIKE %s OR prenom LIKE %s", 
                   (f"%{terme}%", f"%{terme}%"))
    resultats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultats)

@app.route('/rechercher_livre', methods=['GET'])
def rechercher_livre():
    terme = request.args.get('terme', '')
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, titre FROM livre WHERE titre LIKE %s", (f"%{terme}%",))
    resultats = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(resultats)

if __name__ == '__main__':
    app.run(debug=True)
