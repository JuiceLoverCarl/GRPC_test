import grpc
from concurrent import futures
import time

# 导入生成的rag的gRPC 和消息代码
import rag_pb2
import rag_pb2_grpc

#实现 RagService 服务
class RagServicer(rag_pb2_grpc.RagServiceServicer):
    def ExecuteTask(self, request, context):
        question = request.question
        print(f"Received question: {question}")

        # 创建一些 Context 对象作为响应
        context1 = rag_pb2.Context(page_content="this is Lab1201's RAG!", meta_data="this is first test_data!")
        context2 = rag_pb2.Context(meta_data="this is second test_data!")

        # 创建 Response 消息，并返回
        response = rag_pb2.Response(contexts=[context1, context2])
        return response

# 启动 gRPC 服务
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rag_pb2_grpc.add_RagServiceServicer_to_server(RagServicer(), server)

    # 在 50051 端口启动服务
    server.add_insecure_port('[::]:50051')
    print("RAG_Server started at port 50051...")
    server.start()

    try:
        # 保持服务一直运行
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

