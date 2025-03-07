# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from python_pachyderm.proto.v2.proxy import proxy_pb2 as python__pachyderm_dot_proto_dot_v2_dot_proxy_dot_proxy__pb2


class APIStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Listen = channel.unary_stream(
                '/proxy.API/Listen',
                request_serializer=python__pachyderm_dot_proto_dot_v2_dot_proxy_dot_proxy__pb2.ListenRequest.SerializeToString,
                response_deserializer=python__pachyderm_dot_proto_dot_v2_dot_proxy_dot_proxy__pb2.ListenResponse.FromString,
                )


class APIServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Listen(self, request, context):
        """Listen streams database events. 
        It signals that it is internally set up by sending an initial empty ListenResponse.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_APIServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Listen': grpc.unary_stream_rpc_method_handler(
                    servicer.Listen,
                    request_deserializer=python__pachyderm_dot_proto_dot_v2_dot_proxy_dot_proxy__pb2.ListenRequest.FromString,
                    response_serializer=python__pachyderm_dot_proto_dot_v2_dot_proxy_dot_proxy__pb2.ListenResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proxy.API', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class API(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Listen(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/proxy.API/Listen',
            python__pachyderm_dot_proto_dot_v2_dot_proxy_dot_proxy__pb2.ListenRequest.SerializeToString,
            python__pachyderm_dot_proto_dot_v2_dot_proxy_dot_proxy__pb2.ListenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
