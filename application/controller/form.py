# -*- coding: utf-8 -*-
# !/usr/bin/python

from flask import render_template, request, Blueprint, redirect, flash
from pymongo import MongoClient
import numpy as np

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


def db_retrieve_assignments():
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
    assignments = db_retrieve_assignments()

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


def get_weights():
    db = db_connect();

    # store weights in list
    # [0] homework
    # [1] quiz
    # [2] exam

    # declare list of all weights
    weights = []

    # fetch all weights
    homework_weight_cursor = db.assignmentType.find(
        {'assignment_type': 'homework'}, {'assignment_weight': 1, '_id': 0})
    quiz_weight_cursor = db.assignmentType.find(
        {'assignment_type': 'quiz'}, {'assignment_weight': 1, '_id': 0})
    exam_weight_cursor = db.assignmentType.find(
        {'assignment_type': 'exam'}, {'assignment_weight': 1, '_id': 0})

    # add all weights to list
    if homework_weight_cursor.count() > 0:
        weights.append(int(list(homework_weight_cursor)[0]['assignment_weight']))
    else:
        weights.append(0);

    if quiz_weight_cursor.count() > 0:
        weights.append(int(list(quiz_weight_cursor)[0]['assignment_weight']))
    else:
        weights.append(0);

    if exam_weight_cursor.count() > 0:
        weights.append(int(list(exam_weight_cursor)[0]['assignment_weight']))
    else:
        weights.append(0);

    return weights


# right now this is hard coded to support only 3 categories, would be cool to support more..
@form_bp.route('/stats')
def render_stats():
    homework_scores = []
    quiz_scores = []
    exam_scores = []

    db = db_connect();

    # get the assignment table
    grades = db.assignment.find();

    # sum each category
    for item in grades:
        if item['type'] == 'homework':
            homework_scores.append(int(item['score']))
        elif item['type'] == 'quiz':
            quiz_scores.append(int(item['score']))
        elif item['type'] == 'exam':
            exam_scores.append(int(item['score']))

    # calculate average for each category
    homework_avg = np.mean(homework_scores)
    quiz_avg = np.mean(quiz_scores)
    exam_avg = np.mean(exam_scores)

    # if NaN, set to 0
    if np.isnan(homework_avg):
        homework_avg = 0
    if np.isnan(quiz_avg):
        quiz_avg = 0
    if np.isnan(exam_avg):
        exam_avg = 0

    weighted_avg = np.average([homework_avg, quiz_avg, exam_avg], weights=get_weights())

    return render_template('stats.html',
                           homework_avg=homework_avg,
                           quiz_avg=quiz_avg,
                           exam_avg=exam_avg,
                           weighted_avg=weighted_avg);


@form_bp.route('/destroy', methods=['POST'])
def destroy():
    db = db_connect()
    db.assignment.drop()
    db.assignmentType.drop()

    return redirect('/view_database')
