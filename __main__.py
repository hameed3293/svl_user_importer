import pulumi
import pulumi_aws as aws
import json

table = aws.dynamodb.Table("my-table",
    attributes=[
        {
            "name": "id",
            "type": "S",
        }
    ],
    hash_key="id",
    billing_mode="PAY_PER_REQUEST"
)

role = aws.iam.Role("lambda-exec-role",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                }
            }
        ]
    }"""
)

role_policy = aws.iam.RolePolicy("lambda-policy",
    role=role.id,
    policy=table.arn.apply(lambda arn: json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "dynamodb:PutItem",
                    "dynamodb:GetItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:DeleteItem"
                ],
                "Resource": arn
            },
            {
                "Effect": "Allow",
                "Action": "logs:*",
                "Resource": "arn:aws:logs:*:*:*"
            }
        ]
    }))
)

lambda_function = aws.lambda_.Function("my-lambda",

    runtime="python3.11",
    role=role.arn,
    handler="handler.handler",
    code=pulumi.AssetArchive({
        ".": pulumi.FileArchive("./build"),
    }),
    environment={
        "variables": {
            "TABLE_NAME": table.name,
        },
    },
)

pulumi.export("table_name", table.name)
pulumi.export("lambda_function_name", lambda_function.name)