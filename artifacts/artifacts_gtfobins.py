import datetime

from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_dynamodb as _dynamodb,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3
)

from constructs import Construct

class ArtifactsGtfobins(Stack):

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

    ### DYNAMODB ###

        gtfobins = _dynamodb.Table(
            self, 'gtfobins',
            table_name = 'gtfobins',
            partition_key = {
                'name': 'pk',
                'type': _dynamodb.AttributeType.STRING
            },
            sort_key = {
                'name': 'sk',
                'type': _dynamodb.AttributeType.STRING
            },
            billing_mode = _dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy = RemovalPolicy.DESTROY,
            point_in_time_recovery_specification = _dynamodb.PointInTimeRecoverySpecification(
                point_in_time_recovery_enabled = True
            ),
            deletion_protection = False
        )

    ### IAM ROLE ###

        role = _iam.Role(
            self, 'role', 
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    'dynamodb:DeleteItem',
                    'dynamodb:PutItem',
                    'dynamodb:Query'
                ],
                resources = ['*']
            )
        )

    ### LAMBDA ###

        gtfobin = _lambda.Function(
            self, 'gtfobin',
            handler = 'gtfobins.handler',
            runtime = _lambda.Runtime.PYTHON_3_13,
            code = _lambda.Code.from_asset('gtfobins'),
            architecture = _lambda.Architecture.ARM_64,
            environment = dict(
                GTFO_TABLE = gtfobins.table_name
            ),
            timeout = Duration.seconds(900),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                beautifulsoup4,
                requests
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+gtfobin.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '10',
                month = '*',
                week_day = 'SUN',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(
                gtfobin
            )
        )
