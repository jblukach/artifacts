from aws_cdk import (
    Stack,
    aws_ec2 as _ec2
)

from constructs import Construct

class ArtifactsNetwork(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = _ec2.Vpc(
            self, 'vpc',
            ip_addresses = _ec2.IpAddresses.cidr('10.255.255.0/24'),
            max_azs = 3,
            nat_gateways = 0,
            enable_dns_hostnames = True,
            enable_dns_support = True,
            subnet_configuration = [
                _ec2.SubnetConfiguration(
                    cidr_mask = 28,
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

        nacl = _ec2.NetworkAcl(
            self, 'nacl',
            vpc = vpc
        )

        nacl.add_entry(
            'ingress100',
            rule_number = 100,
            cidr = _ec2.AclCidr.ipv4('0.0.0.0/0'),
            traffic = _ec2.AclTraffic.all_traffic(),
            rule_action = _ec2.Action.ALLOW,
            direction = _ec2.TrafficDirection.INGRESS
        )

        nacl.add_entry(
            'egress100',
            rule_number = 100,
            cidr = _ec2.AclCidr.ipv4('0.0.0.0/0'),
            traffic = _ec2.AclTraffic.all_traffic(),
            rule_action = _ec2.Action.ALLOW,
            direction = _ec2.TrafficDirection.EGRESS
        )

        sg = _ec2.SecurityGroup(
            self, 'sg',
            vpc = vpc,
            allow_all_outbound = True,
            description = 'Internet Access',
            security_group_name = 'Internet Access'
        )
