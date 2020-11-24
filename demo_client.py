"""gRPC demo -- client code"""
import logging
import queue
import sys

import grpc

import demo_pb2
import demo_pb2_grpc


def demo_get_user_profile(stub, user_id, timeout=None):
    print()
    print(f"""Requesting profile for user with id {user_id}""")

    request = demo_pb2.UserProfileRequest(id=user_id)
    try:
        response = stub.GetUserProfile(request, timeout=timeout)
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


def prep_chat_messages(client_name):
    messages = [
        "First message",
        "Second message",
        "Third message",
        "Fourth message",
        "Fifth message"
    ]
    q = queue.Queue()
    for msg in messages:
        q.put(demo_pb2.ChatMessage(message=msg, client_name=client_name))
    return q


def generate_messages(q, buffer_size):
    num_generated = 0
    while num_generated < buffer_size:
        yield q.get()
        num_generated += 1
        if num_generated >= buffer_size or q.empty():
            return


def demo_chat(stub, buffer_size=None, client_name="client0"):
    q = prep_chat_messages(client_name)
    if buffer_size is None:
        buffer_size = q.qsize()
    print()
    print(f"""Sending {q.qsize()} messages, {buffer_size} messages at a time""")
    while not q.empty():
        responses = stub.Chat(generate_messages(q, buffer_size))
        print("Sent message(s)")
        for response in responses:
            print(f"""Received message: {response.message} ({response.client_name})""")


def run(client_name):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = demo_pb2_grpc.DemoServiceStub(channel)
        # demo_get_user_profile(stub, 1, timeout=1)
        # demo_get_user_profile(stub, 2, timeout=1)
        # demo_get_user_profile(stub, 1)
        demo_chat(stub, client_name=client_name)
        demo_chat(stub, buffer_size=1, client_name=client_name)
        demo_chat(stub, buffer_size=2, client_name=client_name)


if __name__ == '__main__':
    name = "client0"
    if len(sys.argv) > 1:
        name = sys.argv[1]
    logging.basicConfig()
    run(name)
