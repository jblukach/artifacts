from aws_cdk import (
    Duration,
    RemovalPolicy,
    Size,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_ssm as _ssm
)

from constructs import Construct

class ArtifactsProcess(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### LAYERS ###

        extensions = _ssm.StringParameter.from_string_parameter_attributes(
            self, 'extensions',
            parameter_name = '/extensions/account'
        )

        requests = _lambda.LayerVersion.from_layer_version_arn(
            self, 'requests',
            layer_version_arn = 'arn:aws:lambda:'+region+':'+extensions.string_value+':layer:requests:7'
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
                    's3:GetBucketLocation',
                    's3:GetObject',
                    's3:ListBucket',
                    's3:PutObject',
                    'ssm:GetParameter'
                ],
                resources = ['*']
            )
        )

    ### LAMBDA ###

        process = _lambda.Function(
            self, 'process',
            handler = 'process.handler',
            runtime = _lambda.Runtime.PYTHON_3_13,
            code = _lambda.Code.from_asset('process'),
            architecture = _lambda.Architecture.ARM_64,
            environment = dict(
                AWS_ACCOUNT = account
            ),
            timeout = Duration.seconds(900),
            ephemeral_storage_size = Size.gibibytes(4),
            memory_size = 8192,
            retry_attempts = 0,
            role = role,
            layers = [
                requests
            ]
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/aws/lambda/'+process.function_name,
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
                process
            )
        )
