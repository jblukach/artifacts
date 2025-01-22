import cdk_nag

from aws_cdk import (
    Aspects,
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

    ### CDK NAG ###

        Aspects.of(self).add(
            cdk_nag.AwsSolutionsChecks()
        )

        Aspects.of(self).add(
            cdk_nag.HIPAASecurityChecks()    
        )

        Aspects.of(self).add(
            cdk_nag.NIST80053R5Checks()
        )

        Aspects.of(self).add(
            cdk_nag.PCIDSS321Checks()
        )

        cdk_nag.NagSuppressions.add_stack_suppressions(
            self, suppressions = [
               {"id":"AwsSolutions-S1","reason":"The S3 Bucket has server access logs disabled."},
                {"id":"AwsSolutions-S2","reason":"The S3 Bucket does not have public access restricted and blocked."},
                {"id":"AwsSolutions-S5","reason":"The S3 static website bucket either has an open world bucket policy or does not use a CloudFront Origin Access Identity (OAI) in the bucket policy for limited getObject and/or putObject permissions."},
                {"id":"AwsSolutions-S10","reason":"The S3 Bucket or bucket policy does not require requests to use SSL."},
                {"id":"NIST.800.53.R5-S3BucketLevelPublicAccessProhibited","reason":"The S3 bucket does not prohibit public access through bucket level settings - (Control IDs: AC-2(6), AC-3, AC-3(7), AC-4(21), AC-6, AC-17b, AC-17(1), AC-17(1), AC-17(4)(a), AC-17(9), AC-17(10), MP-2, SC-7a, SC-7b, SC-7c, SC-7(2), SC-7(3), SC-7(7), SC-7(9)(a), SC-7(11), SC-7(20), SC-7(21), SC-7(24)(b), SC-7(25), SC-7(26), SC-7(27), SC-7(28), SC-25)."},
                {"id":"NIST.800.53.R5-S3BucketLoggingEnabled","reason":"The S3 Buckets does not have server access logs enabled - (Control IDs: AC-2(4), AC-3(1), AC-3(10), AC-4(26), AC-6(9), AU-2b, AU-3a, AU-3b, AU-3c, AU-3d, AU-3e, AU-3f, AU-6(3), AU-6(4), AU-6(6), AU-6(9), AU-8b, AU-10, AU-12a, AU-12c, AU-12(1), AU-12(2), AU-12(3), AU-12(4), AU-14a, AU-14b, AU-14b, AU-14(3), CA-7b, CM-5(1)(b), CM-6a, CM-9b, IA-3(3)(b), MA-4(1)(a), PM-14a.1, PM-14b, PM-31, SC-7(9)(b), SI-1(1)(c), SI-3(8)(b), SI-4(2), SI-4(17), SI-4(20), SI-7(8), SI-10(1)(c))."},
                {"id":"NIST.800.53.R5-S3BucketPublicReadProhibited","reason":"The S3 Bucket does not prohibit public read access through its Block Public Access configurations and bucket ACLs - (Control IDs: AC-2(6), AC-3, AC-3(7), AC-4(21), AC-6, AC-17b, AC-17(1), AC-17(1), AC-17(4)(a), AC-17(9), AC-17(10), CM-6a, CM-9b, MP-2, SC-7a, SC-7b, SC-7c, SC-7(2), SC-7(3), SC-7(7), SC-7(9)(a), SC-7(11), SC-7(12), SC-7(16), SC-7(20), SC-7(21), SC-7(24)(b), SC-7(25), SC-7(26), SC-7(27), SC-7(28), SC-25)."},
                {"id":"NIST.800.53.R5-S3BucketPublicWriteProhibited","reason":"The S3 Bucket does not prohibit public write access through its Block Public Access configurations and bucket ACLs - (Control IDs: AC-2(6), AC-3, AC-3(7), AC-4(21), AC-6, AC-17b, AC-17(1), AC-17(1), AC-17(4)(a), AC-17(9), AC-17(10), CM-6a, CM-9b, MP-2, SC-7a, SC-7b, SC-7c, SC-7(2), SC-7(3), SC-7(7), SC-7(9)(a), SC-7(11), SC-7(12), SC-7(16), SC-7(20), SC-7(21), SC-7(24)(b), SC-7(25), SC-7(26), SC-7(27), SC-7(28), SC-25)."},
                {"id":"NIST.800.53.R5-S3BucketReplicationEnabled","reason":"The S3 Bucket does not have replication enabled - (Control IDs: AU-9(2), CM-6a, CM-9b, CP-1(2), CP-2(5), CP-6a, CP-6(1), CP-6(2), CP-9a, CP-9b, CP-9c, CP-10, CP-10(2), SC-5(2), SI-13(5))."},
                {"id":"NIST.800.53.R5-S3BucketSSLRequestsOnly","reason":"The S3 Bucket or bucket policy does not require requests to use SSL - (Control IDs: AC-4, AC-4(22), AC-17(2), AC-24(1), AU-9(3), CA-9b, CM-6a, CM-9b, IA-5(1)(c), PM-11b, PM-17b, SC-7(4)(b), SC-7(4)(g), SC-8, SC-8(1), SC-8(2), SC-8(3), SC-8(4), SC-8(5), SC-13a, SC-16(1), SC-23, SI-1a.2, SI-1a.2, SI-1c.2)."},
                {"id":"NIST.800.53.R5-S3BucketVersioningEnabled","reason":"The S3 Bucket does not have versioning enabled - (Control IDs: AU-9(2), CP-1(2), CP-2(5), CP-6a, CP-6(1), CP-6(2), CP-9a, CP-9b, CP-9c, CP-10, CP-10(2), PM-11b, PM-17b, SC-5(2), SC-16(1), SI-1a.2, SI-1a.2, SI-1c.2, SI-13(5))."},
                {"id":"NIST.800.53.R5-S3DefaultEncryptionKMS","reason":"The S3 Bucket is not encrypted with a KMS Key by default - (Control IDs: AU-9(3), CP-9d, CP-9(8), SC-8(3), SC-8(4), SC-13a, SC-28(1), SI-19(4))."},
                {"id":"HIPAA.Security-S3BucketLevelPublicAccessProhibited","reason":"The S3 bucket does not prohibit public access through bucket level settings - (Control IDs: 164.308(a)(3)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(C), 164.312(a)(1), 164.312(e)(1))."},
                {"id":"HIPAA.Security-S3BucketLoggingEnabled","reason":"The S3 Bucket does not have server access logs enabled - (Control IDs: 164.308(a)(3)(ii)(A), 164.312(b))."},
                {"id":"HIPAA.Security-S3BucketPublicReadProhibited","reason":"The S3 Bucket does not prohibit public read access through its Block Public Access configurations and bucket ACLs - (Control IDs: 164.308(a)(3)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(C), 164.312(a)(1), 164.312(e)(1))."},
                {"id":"HIPAA.Security-S3BucketPublicWriteProhibited","reason":"The S3 Bucket does not prohibit public write access through its Block Public Access configurations and bucket ACLs - (Control IDs: 164.308(a)(3)(i), 164.308(a)(4)(ii)(A), 164.308(a)(4)(ii)(C), 164.312(a)(1), 164.312(e)(1))."},
                {"id":"HIPAA.Security-S3BucketReplicationEnabled","reason":"The S3 Bucket does not have replication enabled - (Control IDs: 164.308(a)(7)(i), 164.308(a)(7)(ii)(A), 164.308(a)(7)(ii)(B))."},
                {"id":"HIPAA.Security-S3BucketSSLRequestsOnly","reason":"The S3 Bucket or bucket policy does not require requests to use SSL - (Control IDs: 164.312(a)(2)(iv), 164.312(c)(2), 164.312(e)(1), 164.312(e)(2)(i), 164.312(e)(2)(ii))."},
                {"id":"HIPAA.Security-S3BucketVersioningEnabled","reason":"The S3 Bucket does not have versioning enabled - (Control IDs: 164.308(a)(7)(i), 164.308(a)(7)(ii)(A), 164.308(a)(7)(ii)(B), 164.312(c)(1), 164.312(c)(2))."},
                {"id":"HIPAA.Security-S3DefaultEncryptionKMS","reason":"The S3 Bucket is not encrypted with a KMS Key by default - (Control IDs: 164.312(a)(2)(iv), 164.312(e)(2)(ii))."},
                {"id":"PCI.DSS.321-S3BucketLevelPublicAccessProhibited","reason":"The S3 bucket does not prohibit public access through bucket level settings - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 1.3.6, 2.2.2)."},
                {"id":"PCI.DSS.321-S3BucketLoggingEnabled","reason":"The S3 Buckets does not have server access logs enabled - (Control IDs: 2.2, 10.1, 10.2.1, 10.2.2, 10.2.3, 10.2.4, 10.2.5, 10.2.7, 10.3.1, 10.3.2, 10.3.3, 10.3.4, 10.3.5, 10.3.6)."},
                {"id":"PCI.DSS.321-S3BucketPublicReadProhibited","reason":"The S3 Bucket does not prohibit public read access through its Block Public Access configurations and bucket ACLs - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 1.3.6, 2.2, 2.2.2)."},
                {"id":"PCI.DSS.321-S3BucketPublicWriteProhibited","reason":"The S3 Bucket does not prohibit public write access through its Block Public Access configurations and bucket ACLs - (Control IDs: 1.2, 1.2.1, 1.3, 1.3.1, 1.3.2, 1.3.4, 1.3.6, 2.2, 2.2.2)."},
                {"id":"PCI.DSS.321-S3BucketReplicationEnabled","reason":"The S3 Bucket does not have replication enabled - (Control IDs: 2.2, 10.5.3)."},
                {"id":"PCI.DSS.321-S3BucketSSLRequestsOnly","reason":"The S3 Bucket or bucket policy does not require requests to use SSL - (Control IDs: 2.2, 4.1, 8.2.1)."},
                {"id":"PCI.DSS.321-S3BucketVersioningEnabled","reason":"The S3 Bucket does not have versioning enabled - (Control ID: 10.5.3)."},
                {"id":"PCI.DSS.321-S3DefaultEncryptionKMS","reason":"The S3 Bucket is not encrypted with a KMS Key by default - (Control IDs: 3.4, 8.2.1, 10.5)."},
            ]
        )

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

        #metaout.add_lifecycle_rule(
        #    expiration = Duration.days(1),
        #    noncurrent_version_expiration = Duration.days(1)
        #)

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

        #tempmeta.add_lifecycle_rule(
        #    expiration = Duration.days(1),
        #    noncurrent_version_expiration = Duration.days(1)
        #)

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
