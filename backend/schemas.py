from marshmallow import fields, Schema

class UserSchema(Schema):
    id = fields.String(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.Str(required=True, load_only=True)
