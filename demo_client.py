"""gRPC demo -- client code"""
import logging

import grpc

import demo_pb2
import demo_pb2_grpc


def demo_get_user_profile(stub, user_id):
    print(f"""Requesting profile for user with id {user_id}""")
    print()
    request = demo_pb2.UserProfileRequest(id=user_id)
    try:
        response = stub.GetUserProfile(request)
    except grpc.RpcError as e:
        status_code = e.code()
        print(f"""Server returned error {status_code.name}""")
        print(f"""Error message: {e.details()}""")
        # print(status_code.value)
        # if grpc.StatusCode.NOT_FOUND == status_code:
        #         print(f"""Perhaps {user_id} is not a valid id?""")
        return

    print(f"""id: {response.id}""")
    print(f"""last_name: {response.last_name}""")
    print(f"""first_name: {response.first_name}""")
    print(f"""phone: {response.phone}""")
    print(f"""job_title: {response.job_title}""")
    print(f"""active: {response.active}""")
    print()


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.DemoServiceStub(channel)
        print("-------------- GetUserProfile --------------")
        demo_get_user_profile(stub, 1)
        demo_get_user_profile(stub, 2)


if __name__ == '__main__':
    logging.basicConfig()
    run()
