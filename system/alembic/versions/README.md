# Migration Order and Dependencies

1. `1a2b3c4d5e6f_base_schema.py` - Base schema that creates all tables using string/varchar types

Note: All columns use standard SQL types (VARCHAR, INTEGER, etc.) rather than custom enum types to simplify the schema and improve flexibility. String constants in the models.py file define the valid values.