# -*- coding: utf-8 -*-
# !/usr/bin/python

from flask import render_template, request, Blueprint, redirect, flash
from pymongo import MongoClient

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


@form_bp.route('/')
def index():
    db_connect()

    return redirect('/home')


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
    results = db_retrive_assignment_type()

    return render_template('view_database.html', results=results)


@form_bp.route('/delete_assignment_type', methods=['POST'])
def db_remove_assignment_type():

    if request.method =='POST':
        formInputs = request.form.to_dict()

    a_type = formInputs['delete_assignment_type']

    db = db_connect()
    db.assignmentType.remove({'assignment_type': a_type})

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
