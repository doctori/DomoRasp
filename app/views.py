from flask import redirect, url_for, jsonify, request,make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from app import app,db
from .models import Controller,Element
from RF24Connector import updateController
api = Api(app)
controller_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'status': fields.Integer,
#	'uri': fields.Url('controller')
}
class ControllerAPI(Resource):
    def __init__(self):
    #Will be used to parse our answers
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
        super(ControllerAPI, self).__init__()
    def get(self,controller_id):
        controller = Controller.query.get(controller_id)
        return [marshal(controller, controller_fields)]

    def put (self,controller_id):
        args = self.reqparse.parse_args()
        controller = Controller.query.get(controller_id)
        controller.name = args['name']
        controller.description = args['description']
        controller.status = args['status']
        print("Going to set the value of the controller to : %r" %(controller.status))
        controller.updateController()
        #db.session.update(controller)
        db.session.commit()

    def delete(self,controller_id):
        controller = Controller.query.get(controller_id)
        db.session.delete(controller)
        db.session.commit()
class ControllerActionsAPI(Resource):
    def __init__(self):
     #Will be used to parse our answers
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
    def get(self,controller_id,action):
        controller = Controller.query.get(controller_id)

class ControllerListAPI(Resource):
    def __init__(self):
        #Will be used to parse our answers
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json',required=True)
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('status', type=int, location='json')
        super(ControllerListAPI, self).__init__()
    def get(self):
        controllers = Controller.query.all()
        return [marshal(controller,controller_fields) for controller in controllers]
    def post(self):
        args = self.reqparse.parse_args()
        controller = Controller(
            name= args['name'],
            description= args['description'],
            status= args['status']
        )
        db.session.add(controller)
        db.session.commit()
        return {'controller': marshal(controller, controller_fields)},201


api.add_resource(ControllerListAPI,'/api/controllers')
api.add_resource(ControllerAPI,'/api/controllers/<int:controller_id>',endpoint = 'controller')
api.add_resource(ControllerActionsAPI,'/api/controllers/<int:controller_id>/<string:action>',endpoint = 'controllerActions')
