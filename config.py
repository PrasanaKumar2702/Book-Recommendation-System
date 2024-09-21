import os

class Config:
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
    S3_BUCKET = os.getenv('S3_BUCKET_NAME')
    RDS_HOST = os.getenv('RDS_HOST')
    RDS_PORT = os.getenv('RDS_PORT', 5432)
    RDS_USER = os.getenv('RDS_USER')
    RDS_PASSWORD = os.getenv('RDS_PASSWORD')
    RDS_DB = os.getenv('RDS_DB')
