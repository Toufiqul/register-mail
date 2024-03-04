from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    password = fields.Str(required=True)