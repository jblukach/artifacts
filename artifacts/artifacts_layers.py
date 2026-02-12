import datetime

from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_ssm as _ssm
)

from constructs import Construct

class ArtifactsLayers(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        year = datetime.datetime.now().strftime('%Y')
        month = datetime.datetime.now().strftime('%m')
        day = datetime.datetime.now().strftime('%d')

    ### LAMBDA LAYER ###

        packages = _s3.Bucket.from_bucket_name(
            self, 'packages',
            bucket_name = 'packages-use2-lukach-io'
        )

        beautifulsoup4 = _lambda.LayerVersion(
            self, 'beautifulsoup4',
            layer_version_name = 'beautifulsoup4',
            description = str(year)+'-'+str(month)+'-'+str(day)+' deployment',
            code = _lambda.Code.from_bucket(
                bucket = packages,
                key = 'beautifulsoup4.zip'
            ),
            compatible_architectures = [
                _lambda.Architecture.ARM_64
            ],
            compatible_runtimes = [
                _lambda.Runtime.PYTHON_3_13
            ],
            removal_policy = RemovalPolicy.DESTROY
        )

        beautifulsoup4parameter = _ssm.StringParameter(
            self, 'beautifulsoup4parameter',
            parameter_name = '/layer/beautifulsoup4',
            string_value = beautifulsoup4.layer_version_arn,
            description = 'BeautifulSoup4 Lambda Layer ARN',
            tier = _ssm.ParameterTier.STANDARD
        )

        requests = _lambda.LayerVersion(
            self, 'requests',
            layer_version_name = 'requests',
            description = str(year)+'-'+str(month)+'-'+str(day)+' deployment',
            code = _lambda.Code.from_bucket(
                bucket = packages,
                key = 'requests.zip'
            ),
            compatible_architectures = [
                _lambda.Architecture.ARM_64
            ],
            compatible_runtimes = [
                _lambda.Runtime.PYTHON_3_13
            ],
            removal_policy = RemovalPolicy.DESTROY
        )

        requestsparameter = _ssm.StringParameter(
            self, 'requestsparameter',
            parameter_name = '/layer/requests',
            string_value = requests.layer_version_arn,
            description = 'Requests Lambda Layer ARN',
            tier = _ssm.ParameterTier.STANDARD
        )
