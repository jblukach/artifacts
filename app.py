#!/usr/bin/env python3
import os

import aws_cdk as cdk

from artifacts.artifacts_gtfobins import ArtifactsGtfobins
from artifacts.artifacts_lolbas import ArtifactsLolbas
from artifacts.artifacts_search import ArtifactsSearch
from artifacts.artifacts_stack import ArtifactsStack

app = cdk.App()

ArtifactsGtfobins(
    app, 'ArtifactsGtfobins',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

ArtifactsLolbas(
    app, 'ArtifactsLolbas',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

ArtifactsSearch(
    app, 'ArtifactsSearch',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

ArtifactsStack(
    app, 'ArtifactsStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('Alias','MatchMeta')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/artifacts')

app.synth()