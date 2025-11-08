# Create a connection to the server and calls the method
import grpc
import greet_pb2
import greet_pb2_grpc

def run():
    # 1. Create communication channel to the server
    with grpc.insecure_channel('localhost:12345') as channel:
        # 2. Create a stub (client interface) using the channel
        stub = greet_pb2_grpc.GreeterStub(channel)

        print("Sending request to  server ...")

        # 3. Call the remote RPC method (SayHello)
        try:
            response = stub.SayHello(greet_pb2.HelloRequest(name="Huan map dep trai"))

            # 4. Print the response
            print("Client received: " + response.message)

        except grpc.RpcError as e:
            print(f"Could not connect to server: {e.details()}")

if __name__ == '__main__':
    run()
