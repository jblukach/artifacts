#!/usr/bin/env python3
import os

import aws_cdk as cdk

from artifacts.artifacts_database import ArtifactsDatabase
from artifacts.artifacts_gtfobins import ArtifactsGtfobins
from artifacts.artifacts_layers import ArtifactsLayers
from artifacts.artifacts_lolbas import ArtifactsLolbas
from artifacts.artifacts_loobins import ArtifactsLoobins
from artifacts.artifacts_network import ArtifactsNetwork
from artifacts.artifacts_process import ArtifactsProcess
from artifacts.artifacts_search import ArtifactsSearch
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

ArtifactsGtfobins(
    app, 'ArtifactsGtfobins',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

ArtifactsLayers(
    app, 'ArtifactsLayers',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

ArtifactsLolbas(
    app, 'ArtifactsLolbas',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

ArtifactsLoobins(
    app, 'ArtifactsLoobins',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

ArtifactsNetwork(
    app, 'ArtifactsNetwork',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

ArtifactsProcess(
    app, 'ArtifactsProcess',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = 'us-east-2'
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = 'lukach'
    )
)

ArtifactsSearch(
    app, 'ArtifactsSearch',
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