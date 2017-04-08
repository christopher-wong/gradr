# -*- coding: utf-8 -*-
# !/usr/bin/python

from flask import Flask, render_template, request, Blueprint, redirect, flash

model_bp = Blueprint('model', __name__)
