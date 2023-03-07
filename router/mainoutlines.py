from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields

import feeds
from api import api


ns = api.namespace("mainoutlines", description="TODO operations")

@ns.route("/")
class MainOutlineList(Resource):
    """Shows a list of main outlines"""
    def get(self):
        """List all main outlines"""
        main_outlines = []
        for main_outline_title in feeds.global_main_outlines:
            main_outlines.append({
            'index': list(feeds.global_main_outlines.keys()).index(main_outline_title),
            'title': main_outline_title,
            })
        return main_outlines