#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_vpcendpoint.cdk_vpcendpoint_stack import CdkVpcendpointStack
app = cdk.App()
CdkVpcendpointStack(app, "CdkVpcendpointStack",
                    env=cdk.Environment( 
                        account='642252392942', 
                        region='us-east-1')
                    )


app.synth()
