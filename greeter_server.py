# Implement the Greeter service defined in the .proto file.
# // The service definition.
# service Greeter {
#   // A simple RPC (Unary) that takes a name and returns a greeting.
#   rpc SayHello (HelloRequest) returns (HelloReply) {}
# }
import grpc
import time
from concurrent import futures

# Import the generated files.
import greet_pb2_grpc
import greet_pb2

# Define the service class inheriting from the generated base class
class GreeterService(greet_pb2_grpc.GreeterServicer):

    # Implement the SayHello RPC method
    def SayHello(self, request, context):
        print(f"Server received request: {request.name}")
        # Construct the response message
        return greet_pb2.HelloReply(message=f"Hello, {request.name}! Greetings from the gRPC server.")

def serve():
    # 1. Create a gRPC server with a thread pool executor
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 2. Add the implementation service to the server
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)

    # 3. Bind the server to an address and port
    server.add_insecure_port('[::]:12345')

    # 4. Start the server
    server.start()
    print('gRPC server started on port 1234. Press Ctrl C to stop.')

    try:
        # Keep the main thread alive until terminated
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
