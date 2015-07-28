from flask import redirect, url_for, jsonify, request,make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from app import app,db
from .models import Controller,Element
from RF24Connector import updateController
api = Api(app)
element_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'status': fields.Integer,
    'controller_id':fields.Integer
#	'uri': fields.Url('controller')
}
controller_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'status': fields.Integer,
    'elements': fields.List(fields.Nested(element_fields)),
    'pipeRead': fields.String,
    'pipeWrite': fields.String
}


class ElementAPI(Resource):
    def __init__(self):
    #Will be used to parse our answers
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
        self.reqparse.add_argument('controller_id', type=int, location='json')
        super(ElementAPI, self).__init__()
    def put (self,element_id):
        args = self.reqparse.parse_args()
        element = Element.query.get(element_id)
        element.description = args['description']
        element.status = args['status']
        element.updateElement()
    def get(self,element_id):
        element = Element.query.get(element_id)
        return [marshal(element, element_fields)]


class ElementActionsAPI(Resource):
    def __init__(self):
     #Will be used to parse our answers
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
    def get(self,element_id,action):
        element = Element.query.get(element_id)
        if action == 'switch':
            element.switch()

class ElementListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
        self.reqparse.add_argument('controller_id', type=int, location='json')
    def get(self):
        elements = Element.query.all()
        return [marshal(element,element_fields) for element in elements]
    def post(self):
        args = self.reqparse.parse_args()
        element = Element(
            name= args['name'],
            description= args['description'],
            status= args['status'],
            controller_id = args['controller_id']
        )
        db.session.add(element)
        db.session.commit()
        return {'controller': marshal(element, element_fields)},201

class ControllerActionsAPI(Resource):
    def __init__(self):
     #Will be used to parse our answers
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
        self.reqparse.add_argument('pipeRead', type=str, location='json')
        self.reqparse.add_argument('pipeWrite', type=str, location='json')
    def get(self,controller_id,action):
        controller = Controller.query.get(controller_id)
        if action == 'switch':
            controller.switch()


class ControllerListAPI(Resource):
    def __init__(self):
        #Will be used to parse our answers
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json',required=True)
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
        self.reqparse.add_argument('pipeRead', type=str, location='json')
        self.reqparse.add_argument('pipeWrite', type=str, location='json')
        super(ControllerListAPI, self).__init__()
    def get(self):
        controllers = Controller.query.all()
        return [marshal(controller,controller_fields) for controller in controllers]
    def post(self):
        args = self.reqparse.parse_args()
        controller = Controller(
            name= args['name'],
            description= args['description'],
            status= args['status'],
            pipeRead = args['pipeRead'],
            pipeWrite = args['pipeWrite']
        )
        db.session.add(controller)
        db.session.commit()
        return {'controller': marshal(controller, controller_fields)},201

class ControllerAPI(Resource):
    def __init__(self):
    #Will be used to parse our answers
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
        self.reqparse.add_argument('pipeRead', type=str, location='json')
        self.reqparse.add_argument('pipeWrite', type=str, location='json')
        super(ControllerAPI, self).__init__()

    def get(self,controller_id):
        controller = Controller.query.get(controller_id)
        return [marshal(controller, controller_fields)]

    def put(self,controller_id):
        args = self.reqparse.parse_args()
        controller = Controller.query.get(controller_id)
        controller.name = args['name']
        controller.description = args['description']
        controller.status = args['status']
        controller.pipeRead = args['pipeRead']
        controller.pipeWrite = args['pipeWrite']
        print("Going to set the value of the controller to : %r" %(controller.status))
        for element in controller.elements:
            print(element)
        controller.updateController()
        #db.session.update(controller)
        db.session.commit()

    @staticmethod
    def delete(self,controller_id):
        controller = Controller.query.get(controller_id)
        db.session.delete(controller)
        db.session.commit()

api.add_resource(ControllerListAPI,'/api/controllers')
api.add_resource(ControllerAPI,'/api/controllers/<int:controller_id>',endpoint = 'controller')
api.add_resource(ControllerActionsAPI,'/api/controllers/<int:controller_id>/<string:action>',endpoint = 'controllerActions')
api.add_resource(ElementAPI,'/api/elements/<int:element_id>',endpoint = 'element')
api.add_resource(ElementListAPI,'/api/elements')
api.add_resource(ElementActionsAPI,'/api/elements/<int:element_id>/<string:action>',endpoint = 'elementActions')