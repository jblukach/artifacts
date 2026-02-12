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

class ArtifactsLolbas(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    ### LAMBDA LAYERS ###

        requestslayer = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'requestslayer',
            parameter_name = '/layer/requests'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = requestslayer.string_value
        )

    ### DYNAMODB ###

        lolbas = _dynamodb.Table(
            self, 'lolbas',
            table_name = 'lolbas',
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

        lolba = _lambda.Function(
            self, 'lolba',
            handler = 'lolbas.handler',
            runtime = _lambda.Runtime.PYTHON_3_13,
            code = _lambda.Code.from_asset('lolbas'),
            architecture = _lambda.Architecture.ARM_64,
            environment = dict(
                LOLBAS_TABLE = lolbas.table_name
            ),
            timeout = Duration.seconds(900),
            memory_size = 512,
            retry_attempts = 0,
            role = role,
            layers = [
                requests
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+lolba.function_name,
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
                lolba
            )
        )
