from aws_cdk import (
    Stack,
    aws_ec2 as _ec2,
    aws_ssm as _ssm
)

from constructs import Construct

class ArtifactsNetwork(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = _ec2.Vpc(
            self, 'vpc',
            ip_addresses = _ec2.IpAddresses.cidr('10.255.255.0/24'),
            ip_protocol = _ec2.IpProtocol.DUAL_STACK,
            enable_dns_hostnames = True,
            enable_dns_support = True,
            nat_gateways = 0,
            max_azs = 3,
            subnet_configuration = [
                _ec2.SubnetConfiguration(
                    cidr_mask = 26,
                    name = 'Public',
                    subnet_type = _ec2.SubnetType.PUBLIC
                )
            ],
            gateway_endpoints = {
                'DYNAMODB': _ec2.GatewayVpcEndpointOptions(
                    service = _ec2.GatewayVpcEndpointAwsService.DYNAMODB
                ),
                'S3': _ec2.GatewayVpcEndpointOptions(
                    service = _ec2.GatewayVpcEndpointAwsService.S3
                )
            }
        )

        vpcparameter = _ssm.StringParameter(
            self, 'vpcparameter',
            description = 'Public VPC ID',
            parameter_name = '/network/vpc',
            string_value = vpc.vpc_id,
            tier = _ssm.ParameterTier.STANDARD
        )

        sg = _ec2.SecurityGroup(
            self, 'sg',
            vpc = vpc,
            allow_all_outbound = True,
            allow_all_ipv6_outbound = True,
            description = 'Internet Access',
            security_group_name = 'Internet Access'
        )

        sgparameter = _ssm.StringParameter(
            self, 'sgparameter',
            description = 'Internet Access Security Group',
            parameter_name = '/network/sg',
            string_value = sg.security_group_id,
            tier = _ssm.ParameterTier.STANDARD
        )

        publicsubnets = []

        for subnet in vpc.public_subnets:
            subnetid = {}
            subnetid['subnet_id'] = subnet.subnet_id
            subnetid['availability_zone'] = subnet.availability_zone
            subnetid['route_table'] = subnet.route_table
            publicsubnets.append(subnetid)

        _ssm.StringParameter(
            self, 'publicsubnet0',
            description = 'Public Subnet ID',
            parameter_name = '/network/publicsubnet0',
            string_value = publicsubnets[0]['subnet_id'],
            tier = _ssm.ParameterTier.STANDARD
        )

        _ssm.StringParameter(
            self, 'publiczone0',
            description = 'Public Availability Zone',
            parameter_name = '/network/publiczone0',
            string_value = publicsubnets[0]['availability_zone'],
            tier = _ssm.ParameterTier.STANDARD
        )

        _ssm.StringParameter(
            self, 'publicroute0',
            description = 'Public Route ID',
            parameter_name = '/network/publicroute0',
            string_value = publicsubnets[0]['route_table'].route_table_id,
            tier = _ssm.ParameterTier.STANDARD
        )

        _ssm.StringParameter(
            self, 'publicsubnet1',
            description = 'Public Subnet ID',
            parameter_name = '/network/publicsubnet1',
            string_value = publicsubnets[1]['subnet_id'],
            tier = _ssm.ParameterTier.STANDARD
        )

        _ssm.StringParameter(
            self, 'publiczone1',
            description = 'Public Availability Zone',
            parameter_name = '/network/publiczone1',
            string_value = publicsubnets[1]['availability_zone'],
            tier = _ssm.ParameterTier.STANDARD
        )

        _ssm.StringParameter(
            self, 'publicroute1',
            description = 'Public Route ID',
            parameter_name = '/network/publicroute1',
            string_value = publicsubnets[1]['route_table'].route_table_id,
            tier = _ssm.ParameterTier.STANDARD
        )

        _ssm.StringParameter(
            self, 'publicsubnet2',
            description = 'Public Subnet ID',
            parameter_name = '/network/publicsubnet2',
            string_value = publicsubnets[2]['subnet_id'],
            tier = _ssm.ParameterTier.STANDARD
        )

        _ssm.StringParameter(
            self, 'publiczone2',
            description = 'Public Availability Zone',
            parameter_name = '/network/publiczone2',
            string_value = publicsubnets[2]['availability_zone'],
            tier = _ssm.ParameterTier.STANDARD
        )

        _ssm.StringParameter(
            self, 'publicroute2',
            description = 'Public Route ID',
            parameter_name = '/network/publicroute2',
            string_value = publicsubnets[2]['route_table'].route_table_id,
            tier = _ssm.ParameterTier.STANDARD
        )
