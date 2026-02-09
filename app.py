#!/usr/bin/env python3
import os

import aws_cdk as cdk

from artifacts.artifacts_database import ArtifactsDatabase
from artifacts.artifacts_stack import ArtifactsStack
from artifacts.artifacts_storage import ArtifactsStorage

app = cdk.App()

ArtifactsDatabase(
    app, 'ArtifactsDatabase',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

ArtifactsStack(
    app, 'ArtifactsStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

ArtifactsStorage(
    app, 'ArtifactsStorage',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

cdk.Tags.of(app).add('Alias','artifacts')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/artifacts')
cdk.Tags.of(app).add('Org','lukach.io')

app.synth()