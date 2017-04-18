# -*- coding: utf-8 -*-
# !/usr/bin/python

from flask import render_template, request, Blueprint, redirect, flash
from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps

form_bp = Blueprint('form_controller', __name__)


# Controller

def db_connect():
    client = MongoClient("mongodb://127.0.0.1:27017")

    db = client.gradr

    return db


def db_insert_assignment_type(formInputs):
    db = db_connect()

    a_type = "assignment_type"
    weight = "assignment_weight"

    results = db_retrive_assignment_type()

    s = set()

    for document in results:
        s.add(document['assignment_type'])

    if formInputs['assignment_type'] in s:
        flash("This Assignment Type already exists")

    elif a_type in formInputs and weight in formInputs:

        try:
            db.assignmentType.insert({
                a_type: formInputs[a_type],
                weight: formInputs[weight]
            })
            flash("Insert successful!")
        except Exception as e:
            flash(e)
            flash("Insert failed!")


def db_retrive_assignment_type():
    db = db_connect();

    cursor = db.assignmentType.find();

    results = []

    for document in cursor:
        results.append(document)

    return results


def db_retrive_assignments():
    db = db_connect();

    cursor = db.assignment.find();

    results = []

    for document in cursor:
        results.append(document)

    return results


@form_bp.route('/')
def index():
    return render_template('login.html')


@form_bp.route('/home')
def home():
    updatedWeight = db_get_total_weight()
    return render_template('index.html', updatedWeight=updatedWeight)


@form_bp.route('/submit', methods=['POST'])
def submit():
    originalWeight = db_get_total_weight()

    # get inputs from form as dict
    if request.method == 'POST':
        formInputs = request.form.to_dict()

    projectedWeight = originalWeight + int(formInputs['assignment_weight'])

    if projectedWeight <= 100:
        db_insert_assignment_type(formInputs)
    else:
        flash("Sum of Weights Cannot Exceed 100")

    updatedWeight = db_get_total_weight()

    return render_template('index.html', updatedWeight=updatedWeight)


@form_bp.route('/view_database')
def view_database():
    assignment_weight_table = db_retrive_assignment_type()
    assignments = db_retrive_assignments()

    return render_template('view_database.html',
                           assignment_weight_table=assignment_weight_table,
                           assignments=assignments)


@form_bp.route('/delete_assignment_type', methods=['POST'])
def db_remove_assignment_type():
    if request.method == 'POST':
        formInputs = request.form.to_dict()

    a_type = formInputs['delete_assignment_type']

    db = db_connect()
    db.assignmentType.remove({'assignment_type': a_type})

    return redirect('/view_database')


@form_bp.route('/delete_assignment', methods=['POST'])
def db_remove_assignment():
    if request.method == 'POST':
        formInputs = request.form.to_dict()

    a_name = formInputs['delete_assignment']
    print(formInputs)

    db = db_connect()
    db.assignment.remove({'name': a_name})

    return redirect('/view_database')


@form_bp.route('/update_assignment_type', methods=['POST'])
def db_update_assignment_weight():
    if request.method == 'POST':
        formInputs = request.form.to_dict()

    typeToUpdate = formInputs['update_assignment_type']
    weightToUpdate = formInputs['assignment_weight']

    db = db_connect()

    type = db_retrive_assignment_type()

    for document in type:
        if document['assignment_type'] == typeToUpdate:
            old = document['assignment_weight']

    difference = int(weightToUpdate) - int(old)
    totalWeight = db_get_total_weight() + difference

    if totalWeight <= 100:
        db.assignmentType.update({'assignment_type': typeToUpdate}, {'$set': {'assignment_weight': weightToUpdate}})
    else:
        flash("Total Weight Cannot Exceed 100")

    return redirect('/view_database')


def db_get_total_weight():
    results = db_retrive_assignment_type()

    originalWeight = 0

    for document in results:
        # originalWeight = originalWeight + document.assignment_weight
        originalWeight = originalWeight + int((document['assignment_weight']))

    return originalWeight


@form_bp.route('/view_raw', methods=["POST"])
def db_view_raw():
    results = db_retrive_assignment_type()

    # for item in results:
    #     print (results)

    return render_template('raw_data.html', results=results)


@form_bp.route('/return', methods=['POST'])
def return_post():
    return redirect('/view_database')


@form_bp.route('/add_assignment', methods=['POST'])
def add_assignment():
    if request.method == 'POST':
        formInputs = request.form.to_dict()

    db = db_connect();
    db.assignment.insert({
        'user_id': '0001',
        'name': formInputs['assignment_name'],
        'type': formInputs['assignment_type'],
        'score': formInputs['assignment_score']
    })

    flash("Assignment insert successful")

    return redirect('/home')


@form_bp.route('/stats')
def render_stats():
    db = db_connect();

    categories = db_retrive_assignment_type()

    # get the assignment table
    results = db.assignment.find();

    # get count for each category
    homework_count = db.assignment.find({'type': 'homework'}).count()
    quiz_count = db.assignment.find({'type': 'quiz'}).count()
    exam_count = db.assignment.find({'type': 'exam'}).count()

    homework_total = 0
    quiz_total = 0;
    exam_total = 0

    # sum each category
    for item in results:
        if item['type'] == 'homework':
            homework_total += item['score']
        elif item['type'] == 'quiz':
            quiz_total += item['score']
        elif item['type'] == 'exam':
            exam_total += item['score']

    homework_avg = homework_total / homework_count
    quiz_avg = quiz_total / quiz_count
    exam_avg = exam_total / exam_count

    print(categories)

    return render_template('stats.html');


@form_bp.route('/destroy', methods=['POST'])
def destroy():
    db = db_connect()
    db.assignment.drop()
    db.assignmentType.drop()

    return redirect('/view_database')
