from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_s3 as _s3
)

from constructs import Construct

class ArtifactsStorage(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        matchmetabackup = _s3.Bucket(
            self, 'matchmetabackup',
            bucket_name = 'matchmetabackup',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = False,
            enforce_ssl = True,
            versioned = False
        )

        matchmetadata = _s3.Bucket(
            self, 'matchmetadata',
            bucket_name = 'matchmetadata',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = False,
            enforce_ssl = True,
            versioned = False
        )

        matchmetaoutput = _s3.Bucket(
            self, 'matchmetaoutput',
            bucket_name = 'matchmetaoutput',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        matchmetaoutput.add_lifecycle_rule(
            expiration = Duration.days(1),
            noncurrent_version_expiration = Duration.days(1)
        )

        matchmetastaged = _s3.Bucket(
            self, 'matchmetastaged',
            bucket_name = 'matchmetastaged',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        matchmetatemporary = _s3.Bucket(
            self, 'matchmetatemporary',
            bucket_name = 'matchmetatemporary',
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            enforce_ssl = True,
            versioned = False
        )

        matchmetatemporary.add_lifecycle_rule(
            expiration = Duration.days(1),
            noncurrent_version_expiration = Duration.days(1)
        )
