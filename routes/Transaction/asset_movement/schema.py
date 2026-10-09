from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
  pass

class EssentialSchema(BaseModel):
  pass

class NoneSchema(BaseModel):
  pass

class Schema(BaseSchema, EssentialSchema, NoneSchema):
  pass

class CreateSchema(BaseSchema):
  pass

class UpdateSchema(NoneSchema):
  pass

class ReadSchema:
  pass

class ReadMultiSchema:
  pass

#! response

class ResponseSchema:
  pass

class CreateResponseSchema:
  pass

class UpdateResponseSchema:
  pass

class ReadResponseSchema:
  pass

class ReadMultiResponseSchema:
  pass


# query



