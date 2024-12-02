import grpc
from concurrent import futures
import time

# 导入生成的 gRPC 和消息代码
import connect_pb2
import connect_pb2_grpc


# 实现 Connect 服务
class ConnectServicer(connect_pb2_grpc.ConnectServicer):
    def TransmitMessage(self, request, context):
        # 处理传入的请求
        question = request.question
        print(f"Received question: {question}")

        # 创建一些 Context 对象作为响应
        context1 = connect_pb2.Context(page_content="This is the first page for rag_grpc", meta_data="First context_1")
        context2 = connect_pb2.Context(page_content="This is the second page, THIS is RAG!", meta_data="Second context_2")

        # 创建 Response 消息，并返回
        response = connect_pb2.Response(contexts=[context1, context2])
        return response


# 启动 gRPC 服务
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    connect_pb2_grpc.add_ConnectServicer_to_server(ConnectServicer(), server)

    # 在 50051 端口启动服务
    server.add_insecure_port('[::]:50051')
    print("Server started at port 50051...")
    server.start()

    try:
        # 保持服务一直运行
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

#
# if __name__ == '__main__':
#     serve()
