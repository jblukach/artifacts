from aws_cdk import (
    Stack,
    aws_glue_alpha as _glue,
    aws_s3 as _s3
)

from constructs import Construct

class ArtifactsDatabase(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = _s3.Bucket.from_bucket_name(
            self, 'bucket',
            bucket_name = 'matchmetadata'
        )

        database = _glue.Database(
            self, 'database',
            database_name = 'artifacts'
        )

        amazon =  _glue.Table(
            self, 'amazon',
            bucket = bucket,
            database = database,
            table_name = 'amazon',
            s3_prefix = 'amazon/',
            columns = [
                _glue.Column(
                    name = 'amiid',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fpath',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fname',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fsize',
                    type = _glue.Schema.BIG_INT
                ),
                _glue.Column(
                    name = 'b3hash',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3name',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3path',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3dir',
                    type = _glue.Schema.STRING
                )
            ],
            data_format = _glue.DataFormat(
                input_format = _glue.InputFormat.PARQUET,
                output_format = _glue.OutputFormat.PARQUET,
                serialization_library = _glue.SerializationLibrary.PARQUET
            )
        )

        microsoft =  _glue.Table(
            self, 'microsoft',
            bucket = bucket,
            database = database,
            table_name = 'microsoft',
            s3_prefix = 'microsoft/',
            columns = [
                _glue.Column(
                    name = 'amiid',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fpath',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fname',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fsize',
                    type = _glue.Schema.BIG_INT
                ),
                _glue.Column(
                    name = 'b3hash',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3name',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3path',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3dir',
                    type = _glue.Schema.STRING
                )
            ],
            data_format = _glue.DataFormat(
                input_format = _glue.InputFormat.PARQUET,
                output_format = _glue.OutputFormat.PARQUET,
                serialization_library = _glue.SerializationLibrary.PARQUET
            )
        )

        ubuntu =  _glue.Table(
            self, 'ubuntu',
            bucket = bucket,
            database = database,
            table_name = 'ubuntu',
            s3_prefix = 'ubuntu/',
            columns = [
                _glue.Column(
                    name = 'amiid',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fpath',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fname',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'fsize',
                    type = _glue.Schema.BIG_INT
                ),
                _glue.Column(
                    name = 'b3hash',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3name',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3path',
                    type = _glue.Schema.STRING
                ),
                _glue.Column(
                    name = 'b3dir',
                    type = _glue.Schema.STRING
                )
            ],
            data_format = _glue.DataFormat(
                input_format = _glue.InputFormat.PARQUET,
                output_format = _glue.OutputFormat.PARQUET,
                serialization_library = _glue.SerializationLibrary.PARQUET
            )
        )
