from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_glue_alpha as _glue,
    aws_s3 as _s3
)

from constructs import Construct

class ArtifactsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### S3 BUCKETS ###

        matchmeta = _s3.Bucket.from_bucket_name(
            self, 'matchmeta',
            bucket_name = 'matchmeta'
        )

        metaout = _s3.Bucket(
            self, 'metaout',
            bucket_name = 'metaout',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        metaout.add_lifecycle_rule(
            expiration = Duration.days(1),
            noncurrent_version_expiration = Duration.days(1)
        )

        tempmeta = _s3.Bucket(
            self, 'tempmeta',
            bucket_name = 'tempmeta',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        tempmeta.add_lifecycle_rule(
            expiration = Duration.days(1),
            noncurrent_version_expiration = Duration.days(1)
        )

    ### DATABASE ###

        database = _glue.Database(
            self, 'database',
            database_name = 'matchmeta'
        )

    ### TABLE - AmazonLinux2023arm ###

        amazonlinux2023arm =  _glue.Table(
            self, 'amazonlinux2023arm',
            bucket = matchmeta,
            s3_prefix = 'AmazonLinux2023arm/',
            database = database,
            table_name = 'amazonlinux2023arm',
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

    ### TABLE - AmazonLinux2023x86 ###

        amazonlinux2023x86 =  _glue.Table(
            self, 'amazonlinux2023x86',
            bucket = matchmeta,
            s3_prefix = 'AmazonLinux2023x86/',
            database = database,
            table_name = 'amazonlinux2023x86',
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

    ### TABLE - AmazonLinux2arm ###

        amazonlinux2arm =  _glue.Table(
            self, 'amazonlinux2arm',
            bucket = matchmeta,
            s3_prefix = 'AmazonLinux2arm/',
            database = database,
            table_name = 'amazonlinux2arm',
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

    ### TABLE - AmazonLinux2x86 ###

        amazonlinux2x86 =  _glue.Table(
            self, 'amazonlinux2x86',
            bucket = matchmeta,
            s3_prefix = 'AmazonLinux2x86/',
            database = database,
            table_name = 'amazonlinux2x86',
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

    ### TABLE - AppleSequoia15arm ###

        applesequoia15arm =  _glue.Table(
            self, 'applesequoia15arm',
            bucket = matchmeta,
            s3_prefix = 'AppleSequoia15arm/',
            database = database,
            table_name = 'applesequoia15arm',
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

    ### TABLE - AppleSonoma14arm ###

        applesonoma14arm =  _glue.Table(
            self, 'applesonoma14arm',
            bucket = matchmeta,
            s3_prefix = 'AppleSonoma14arm/',
            database = database,
            table_name = 'applesonoma14arm',
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

    ### TABLE - AppleVentura13arm ###

        appleventura13arm =  _glue.Table(
            self, 'appleventura13arm',
            bucket = matchmeta,
            s3_prefix = 'AppleVentura13arm/',
            database = database,
            table_name = 'appleventura13arm',
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

    ### TABLE - MicrosoftWin2k16x86 ###

        microsoftwin2k16x86 =  _glue.Table(
            self, 'microsoftwin2k16x86',
            bucket = matchmeta,
            s3_prefix = 'MicrosoftWin2k16x86/',
            database = database,
            table_name = 'microsoftwin2k16x86',
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

    ### TABLE - MicrosoftWin2k19x86 ###

        microsoftwin2k19x86 =  _glue.Table(
            self, 'microsoftwin2k19x86',
            bucket = matchmeta,
            s3_prefix = 'MicrosoftWin2k19x86/',
            database = database,
            table_name = 'microsoftwin2k19x86',
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

    ### TABLE - MicrosoftWin2k22x86 ###

        microsoftwin2k22x86 =  _glue.Table(
            self, 'microsoftwin2k22x86',
            bucket = matchmeta,
            s3_prefix = 'MicrosoftWin2k22x86/',
            database = database,
            table_name = 'microsoftwin2k22x86',
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

    ### TABLE - MicrosoftWin2k25x86 ###

        microsoftwin2k25x86 =  _glue.Table(
            self, 'microsoftwin2k25x86',
            bucket = matchmeta,
            s3_prefix = 'MicrosoftWin2k25x86/',
            database = database,
            table_name = 'microsoftwin2k25x86',
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

    ### TABLE - UbuntuLinux18arm ###

        ubuntulinux18arm =  _glue.Table(
            self, 'ubuntulinux18arm',
            bucket = matchmeta,
            s3_prefix = 'UbuntuLinux18arm/',
            database = database,
            table_name = 'ubuntulinux18arm',
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

    ### TABLE - UbuntuLinux18x86 ###

        ubuntulinux18x86 =  _glue.Table(
            self, 'ubuntulinux18x86',
            bucket = matchmeta,
            s3_prefix = 'UbuntuLinux18x86/',
            database = database,
            table_name = 'ubuntulinux18x86',
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

    ### TABLE - UbuntuLinux20arm ###

        ubuntulinux20arm =  _glue.Table(
            self, 'ubuntulinux20arm',
            bucket = matchmeta,
            s3_prefix = 'UbuntuLinux20arm/',
            database = database,
            table_name = 'ubuntulinux20arm',
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

    ### TABLE - UbuntuLinux20x86 ###

        ubuntulinux20x86 =  _glue.Table(
            self, 'ubuntulinux20x86',
            bucket = matchmeta,
            s3_prefix = 'UbuntuLinux20x86/',
            database = database,
            table_name = 'ubuntulinux20x86',
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

    ### TABLE - UbuntuLinux22arm ###

        ubuntulinux22arm =  _glue.Table(
            self, 'ubuntulinux22arm',
            bucket = matchmeta,
            s3_prefix = 'UbuntuLinux22arm/',
            database = database,
            table_name = 'ubuntulinux22arm',
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

    ### TABLE - UbuntuLinux22x86 ###

        ubuntulinux22x86 =  _glue.Table(
            self, 'ubuntulinux22x86',
            bucket = matchmeta,
            s3_prefix = 'UbuntuLinux22x86/',
            database = database,
            table_name = 'ubuntulinux22x86',
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

    ### TABLE - UbuntuLinux24arm ###

        ubuntulinux24arm =  _glue.Table(
            self, 'ubuntulinux24arm',
            bucket = matchmeta,
            s3_prefix = 'UbuntuLinux24arm/',
            database = database,
            table_name = 'ubuntulinux24arm',
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

    ### TABLE - UbuntuLinux24x86 ###

        ubuntulinux24x86 =  _glue.Table(
            self, 'ubuntulinux24x86',
            bucket = matchmeta,
            s3_prefix = 'UbuntuLinux24x86/',
            database = database,
            table_name = 'ubuntulinux24x86',
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
