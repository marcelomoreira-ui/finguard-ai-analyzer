import boto3
import json

def nova_lite_test():
    bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-west-2')
    response = bedrock_client.invoke_model(
        modelId='us.amazon.nova-lite-v1:0',
        body=json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": "Diga 'Teste OK'"}]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 50,
                "temperature": 0
            }
        }),
        contentType='application/json',
        accept='application/json'
    )

    response_body = json.loads(response['body'].read())
    print(response_body["output"]["message"]["content"][0]["text"])