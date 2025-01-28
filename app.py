#!/usr/bin/env python3
import os

import aws_cdk as cdk

from artifacts.artifacts_blog import ArtifactsBlog
from artifacts.artifacts_gtfobins import ArtifactsGtfobins
from artifacts.artifacts_lolbas import ArtifactsLolbas
from artifacts.artifacts_monitor import ArtifactsMonitor
from artifacts.artifacts_process import ArtifactsProcess
from artifacts.artifacts_readme import ArtifactsReadme
from artifacts.artifacts_release import ArtifactsRelease
from artifacts.artifacts_search import ArtifactsSearch
from artifacts.artifacts_stack import ArtifactsStack

app = cdk.App()

ArtifactsBlog(
    app, 'ArtifactsBlog',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

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

ArtifactsMonitor(
    app, 'ArtifactsMonitor',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

ArtifactsProcess(
    app, 'ArtifactsProcess',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

ArtifactsReadme(
    app, 'ArtifactsReadme',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

ArtifactsRelease(
    app, 'ArtifactsRelease',
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