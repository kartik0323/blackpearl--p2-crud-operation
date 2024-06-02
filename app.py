from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__, template_folder='templates')

# Connect to MongoDB
client = MongoClient('mongodb+srv://kartikpoojary8:kartik@kartik.p9a2qyy.mongodb.net/user?retryWrites=true&w=majority&appName=kartik')
db = client['school']
users_collection = db['users']

# Routes for CRUD operations

@app.route('/')
def index():
    users = users_collection.find()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        roll_no = request.form['roll_no']
        marks = request.form['marks']
        user_data = {'username': username, 'roll_no': roll_no, 'marks': marks}
        users_collection.insert_one(user_data)
    return redirect(url_for('index'))

@app.route('/update/<user_id>', methods=['POST'])
def update_user(user_id):
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_roll_no = request.form['new_roll_no']
        new_marks = request.form['new_marks']
        users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'username': new_username, 'roll_no': new_roll_no, 'marks': new_marks}})
    return redirect(url_for('index'))

@app.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    users_collection.delete_one({'_id': ObjectId(user_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
