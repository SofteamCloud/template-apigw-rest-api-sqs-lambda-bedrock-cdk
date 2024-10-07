import json
import boto3 

modelId = "anthropic.claude-3-haiku-20240307-v1:0:48k"

def invoke_bedrock(prompt_data):
    body = json.dumps({
        'prompt': f'Human:{prompt_data}\n\nAssistant:', 
        'max_tokens_to_sample': 1028,
        'temperature': 1,
        'top_k': 250,
        'top_p': 0.999,
        'stop_sequences': ['\n\nHuman:']
    })

    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        body=body, modelId=modelId, contentType="application/json",
        accept="*/*"
    )
    return json.loads(response["body"].read().decode("utf-8"))

def lambda_handler(event, context):
    responses = []
    for record in event['Records']:
        print(record)
        request = json.loads(record["body"])
        print(request)
        prompt_data = request["prompt"]
        
        response = invoke_bedrock(prompt_data)
        responses.append(response)
        print(response)

    return {
        'statusCode': 200,
        'body': json.dumps(responses)
    }

        #### Publish response to websocket, IoT Core topic


