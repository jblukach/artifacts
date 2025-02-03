from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs
)

from constructs import Construct

class ArtifactsSearch(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region

    ### ATHENA SEARCH ###

        b3types = []
        b3types.append('b3dir')
        b3types.append('b3hash')
        b3types.append('b3lol')
        b3types.append('b3name')
        b3types.append('b3path')

        ostypes = []
    ### Amazon Linux ###
        ostypes.append('AmazonLinux2023arm')
        ostypes.append('AmazonLinux2023x86')
        ostypes.append('AmazonLinux2arm')
        ostypes.append('AmazonLinux2x86')
    ### Apple macOS ###
        ostypes.append('AppleVentura13arm')
        ostypes.append('AppleSonoma14arm')
        ostypes.append('AppleSequoia15arm')
    ### Microsoft Windows ###
        ostypes.append('MicrosoftWin2k16x86')
        ostypes.append('MicrosoftWin2k19x86')
        ostypes.append('MicrosoftWin2k22x86')
        ostypes.append('MicrosoftWin2k25x86')
    ### Ubuntu Linux ###
        ostypes.append('UbuntuLinux18arm')
        ostypes.append('UbuntuLinux18x86')
        ostypes.append('UbuntuLinux20arm')
        ostypes.append('UbuntuLinux20x86')
        ostypes.append('UbuntuLinux22arm')
        ostypes.append('UbuntuLinux22x86')
        ostypes.append('UbuntuLinux24arm')
        ostypes.append('UbuntuLinux24x86')

        for ostype in ostypes:

            role = _iam.Role(
                self, 'role'+ostype.lower(), 
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
                        'athena:CreateWorkGroup',
                        'athena:DeleteWorkGroup',
                        'athena:GetWorkGroup',
                        'athena:ListEngineVersions',
                        'athena:StartQueryExecution',
                        'athena:StopQueryExecution',
                        'athena:UpdateWorkGroup',
                        'dynamodb:Query',
                        'glue:GetDatabase',
                        'glue:GetDatabases',
                        'glue:GetTable',
                        'glue:GetTables',
                        'glue:GetPartition',
                        'glue:GetPartitions',
                        'glue:BatchGetPartition',
                        'iam:PassRole',
                        's3:GetBucketLocation',
                        's3:GetObject',
                        's3:ListBucket',
                        's3:ListBucketMultipartUploads',
                        's3:ListMultipartUploadParts',
                        's3:AbortMultipartUpload',
                        's3:PutObject'
                    ],
                    resources = ['*']
                )
            )

            search = _lambda.Function(
                self, 'search'+ostype.lower(),
                handler = 'search.handler',
                runtime = _lambda.Runtime.PYTHON_3_13,
                code = _lambda.Code.from_asset('search'),
                architecture = _lambda.Architecture.ARM_64,
                environment = dict(
                    AWS_ACCOUNT = account
                ),
                timeout = Duration.seconds(900),
                memory_size = 128,
                retry_attempts = 0,
                role = role
            )

            logs = _logs.LogGroup(
                self, 'logs'+ostype.lower(),
                log_group_name = '/4n6ir/lambda/'+search.function_name,
                retention = _logs.RetentionDays.ONE_MONTH,
                removal_policy = RemovalPolicy.DESTROY
            )

            for b3type in b3types:

                event = _events.Rule(
                    self, 'event'+ostype.lower()+b3type.lower(),
                    schedule = _events.Schedule.cron(
                        minute = '0',
                        hour = '11',
                        month = '*',
                        week_day = 'SUN',
                        year = '*'
                    )
                )

                event.add_target(
                    _targets.LambdaFunction(
                        search,
                        event = _events.RuleTargetInput.from_object(
                            {
                                "name": ostype,
                                "category": b3type
                            }
                        )
                    )
                )
