from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('text', required=True)
parser.add_argument('img_url', required=True)
parser.add_argument('read_time', required=True)

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('title')
edit_parser.add_argument('text')
edit_parser.add_argument('img_url')
edit_parser.add_argument('read_time')
