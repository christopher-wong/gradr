# -*- coding: utf-8 -*-
# !/usr/bin/python

from flask import render_template, request, Blueprint, redirect

about_bp = Blueprint('about', __name__)


# Views

@about_bp.route('/about')
def about():
    return render_template('about.html')
