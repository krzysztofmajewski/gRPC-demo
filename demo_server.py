"""gRPC demo -- server code"""
from concurrent import futures

import logging

import grpc

import demo_pb2
import demo_pb2_grpc


# Create a database of user profiles
def init_users():
    chris = dict()
    chris['last_name'] = 'Majewski'
    chris['first_name'] = 'Chris'
    chris['phone'] = '514-754-0182'
    chris['job_title'] = 'Junior gRPC Developer'
    chris['active'] = True
    return {1: chris}


# Subclass the Servicer
class DemoServiceServicer(demo_pb2_grpc.DemoServiceServicer):
    def __init__(self):
        self.users = init_users()

    # Server business logic :)
    def GetUserProfile(self, request, context):
        try:
            user = self.users[request.id]
        except KeyError as ke:
            context.set_details(f"""No user found for id {request.id}""")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return demo_pb2.UserProfileResponse()

        # TODO: what happens if id not set in response?
        return demo_pb2.UserProfileResponse(last_name=user['last_name'],
                                            first_name=user['first_name'],
                                            phone=user['phone'],
                                            job_title=user['job_title'],
                                            active=user['active'],
                                            id=request.id)


# Server plumbing
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    demo_pb2_grpc.add_DemoServiceServicer_to_server(
        DemoServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
