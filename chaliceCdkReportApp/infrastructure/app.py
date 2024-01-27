#!/usr/bin/env python3
try:
    from aws_cdk import core as cdk
except ImportError:
    import aws_cdk as cdk
from stacks.chaliceapp import ChaliceApp

app = cdk.App()
env_USA = cdk.Environment(account="642252392942", region="us-east-1")


ChaliceApp(app, 'chaliceCdkReportApp',env = env_USA)

app.synth()
