# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: client/health/health.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='client/health/health.proto',
  package='health',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1a\x63lient/health/health.proto\x12\x06health\x1a\x1bgoogle/protobuf/empty.proto2D\n\x06Health\x12:\n\x06Health\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_HEALTH = _descriptor.ServiceDescriptor(
  name='Health',
  full_name='health.Health',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=67,
  serialized_end=135,
  methods=[
  _descriptor.MethodDescriptor(
    name='Health',
    full_name='health.Health.Health',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_HEALTH)

DESCRIPTOR.services_by_name['Health'] = _HEALTH

# @@protoc_insertion_point(module_scope)
