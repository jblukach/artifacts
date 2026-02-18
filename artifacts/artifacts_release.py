from aws_cdk import (
    Duration,
    RemovalPolicy,
    SecretValue,
    Size,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_secretsmanager as _secrets,
    aws_ssm as _ssm
)

from constructs import Construct

class ArtifactsRelease(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    ### SECRET MANAGER ###

        secret = _secrets.Secret(
            self, 'secret',
            secret_name = 'artifacts',
            secret_object_value = {
                "github": SecretValue.unsafe_plain_text("<EMPTY>")
            }
        )

    ### LAMBDA LAYERS ###

        requestslayer = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'requestslayer',
            parameter_name = '/layer/requests'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = requestslayer.string_value
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
                    's3:GetObject'
                ],
                resources = ['*']
            )
        )

        secret.grant_read(role)

    ### LAMBDA ###

        release = _lambda.Function(
            self, 'release',
            handler = 'release.handler',
            runtime = _lambda.Runtime.PYTHON_3_13,
            code = _lambda.Code.from_asset('release'),
            architecture = _lambda.Architecture.ARM_64,
            environment = dict(
                SECRET_MGR_ARN = secret.secret_arn
            ),
            timeout = Duration.seconds(900),
            ephemeral_storage_size = Size.gibibytes(4),
            memory_size = 4096,
            retry_attempts = 0,
            role = role,
            layers = [
                requests
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+release.function_name,
            retention = _logs.RetentionDays.ONE_MONTH,
            removal_policy = RemovalPolicy.DESTROY
        )

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '12',
                month = '*',
                week_day = 'SUN',
                year = '*'
            )
        )

        event.add_target(
            _targets.LambdaFunction(
                release
            )
        )
