"""gRPC demo -- client code"""
import logging

import grpc

import demo_pb2
import demo_pb2_grpc


def demo_get_user_profile(stub):
    request = demo_pb2.UserProfileRequest(id=1)
    response = stub.GetUserProfile(request)
    print(f"""id: {response.id}""")
    print(f"""last_name: {response.last_name}""")
    print(f"""first_name: {response.first_name}""")
    print(f"""phone: {response.phone}""")
    print(f"""job_title: {response.job_title}""")
    print(f"""active: {response.active}""")


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.DemoServiceStub(channel)
        print("-------------- GetUserProfile --------------")
        demo_get_user_profile(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
