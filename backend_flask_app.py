from flask import Flask,render_template,request,send_file,send_from_directory
import mysql.connector
import os
import json

class Database():
    def __init__(s,host,username,password,db_name):
        s.db = mysql.connector.connect( host = host , user = username , password = password , database = db_name)
        s.cursor = s.db.cursor()
    def get_vote(s,author_name):
        query = "SELECT votes FROM authors WHERE name = '{0}'".format(author_name)
        s.cursor.execute(query)
        votes = s.cursor.fetchall()[0][0]
        return votes
    def update_vote(s,author_name):
        old_votes = s.get_vote(author_name)
        new_votes = old_votes + 1
        query = "UPDATE authors SET votes = '{0}' WHERE name = '{1}'".format(new_votes,author_name)
        s.cursor.execute(query)
        s.db.commit()
    def get_votes(s):
        query = "SELECT * FROM authors"
        s.cursor.execute(query)
        result_sets = [ list(each) for each in s.cursor.fetchall()]
        result_sets.sort(key=lambda t : t[0])
        result_sets = [each[1] for each in result_sets]
        return result_sets



app = Flask(__name__,template_folder = os.getcwd() )

@app.route("/")
def home():
    return render_template('favorite_author.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    selected_name = request.form['author']
    db = Database('localhost','root','','author_preference')
    db.update_vote(selected_name)
    auth_votes =  db.get_votes()
    return render_template('results.html',auth_votes = json.dumps(auth_votes))

if __name__ == "__main__":
    app.run(debug=True)
