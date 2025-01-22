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
    aws_ssm as _ssm
)

from constructs import Construct

class ArtifactsGtfobins(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAYERS ###

        extensions = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'extensions',
            parameter_name = '/extensions/account'
        )

        beautifulsoup4 = _lambda.LayerVersion.from_layer_version_arn(
            self, 'beautifulsoup4',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:beautifulsoup4:4'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:requests:7'
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
            point_in_time_recovery = True,
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
                AWS_ACCOUNT = account,
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

        gtfologs = _logs.LogGroup(
            self, 'gtfologs',
            log_group_name = '/4n6ir/lambda/'+gtfobin.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        gtfoevent = _events.Rule(
            self, 'gtfoevent',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '10',
                month = '*',
                week_day = 'SUN',
                year = '*'
            )
        )

        gtfoevent.add_target(
            _targets.LambdaFunction(
                gtfobin
            )
        )
