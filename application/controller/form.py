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
        print(len(s))

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

    return redirect('/home')


@form_bp.route('/home')
def home():
    originalWeight = db_get_total_weight()
    return render_template('index.html', originalWeight=originalWeight)


@form_bp.route('/submit', methods=['POST'])
def submit():
    originalWeight = db_get_total_weight()


    # get inputs from form as dict
    if request.method == 'POST':
        formInputs = request.form.to_dict()

    updatedWeight = originalWeight + int(formInputs['assignment_weight'])

    print(updatedWeight)

    if updatedWeight <= 100:
        db_insert_assignment_type(formInputs)
    else:
        flash("Sum of Weights Cannot Exceed 100")

    return render_template('index.html', originalWeight=originalWeight)


@form_bp.route('/view_database')
def view_database():
    results = db_retrive_assignment_type()

    return render_template('view_database.html', results=results)


@form_bp.route('/delete_assignment_type', methods=['POST'])
def db_remove_assignment_type():

    if request.method =='POST':
        formInputs = request.form.to_dict()

    print(formInputs)
    a_type = formInputs['delete_assignment_type']

    db = db_connect()
    db.assignmentType.remove({'assignment_type': a_type})

    return redirect('/view_database')


def db_get_total_weight():
    results = db_retrive_assignment_type()

    originalWeight = 0

    for document in results:
        # originalWeight = originalWeight + document.assignment_weight
        originalWeight = originalWeight + int((document['assignment_weight']))

    return originalWeight
