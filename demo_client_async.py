"""gRPC demo -- client code"""
import logging
import asyncio

import grpc

import demo_pb2
import demo_pb2_grpc


async def demo_get_user_profile(stub, user_id, timeout=None):
    print()
    print(f"""Requesting profile for user with id {user_id}""")

    request = demo_pb2.UserProfileRequest(id=user_id)
    try:
        response = await stub.GetUserProfile(request, timeout=timeout)
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


async def run():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.DemoServiceStub(channel)
        task1 = asyncio.create_task(demo_get_user_profile(stub, 1, timeout=1))
        task2 = asyncio.create_task(demo_get_user_profile(stub, 2))
        task3 = asyncio.create_task(demo_get_user_profile(stub, 1))
        await task1
        await task2
        await task3


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(run())
