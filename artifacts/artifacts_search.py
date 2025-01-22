from aws_cdk import (
    Stack,
    aws_ssm as _ssm
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
            for b3type in b3types:
                
                parameter = _ssm.StringParameter(
                    self, 'parameter'+ostype.lower()+b3type.lower(),
                    description = ostype.lower()+'-'+b3type.lower(),
                    parameter_name = '/artifacts/'+ostype.lower()+'/'+b3type.lower(),
                    string_value = 'EMPTY',
                    tier = _ssm.ParameterTier.STANDARD,
                )
