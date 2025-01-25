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
    aws_sns as _sns
)

from constructs import Construct

class ArtifactsMonitor(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### SNS TOPIC ###

        topic = _sns.Topic.from_topic_arn(
            self, 'topic',
            topic_arn = 'arn:aws:sns:'+region+':'+account+':athena-query-failure'
        )

    ### DYNAMODB ###

        athena = _dynamodb.Table(
            self, 'athena',
            table_name = 'athena',
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
                    'athena:ListQueryExecutions',
                    'athena:GetQueryExecution',
                    'dynamodb:PutItem',
                    'dynamodb:Query',
                    'iam:PassRole',
                    'sns:Publish'
                ],
                resources = ['*']
            )
        )

    ### LAMBDA ###

        monitor = _lambda.Function(
            self, 'monitor',
            handler = 'monitor.handler',
            runtime = _lambda.Runtime.PYTHON_3_13,
            code = _lambda.Code.from_asset('monitor'),
            architecture = _lambda.Architecture.ARM_64,
            environment = dict(
                AWS_ACCOUNT = account,
                ATHEANA_TABLE = athena.table_name,
                SNS_TOPIC = topic.topic_arn
            ),
            timeout = Duration.seconds(900),
            memory_size = 512,
            retry_attempts = 0,
            role = role
        )

        logs = _logs.LogGroup(
            self, 'logs',
            log_group_name = '/4n6ir/lambda/'+monitor.function_name,
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
                monitor
            )
        )
