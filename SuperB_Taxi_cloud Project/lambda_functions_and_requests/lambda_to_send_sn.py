import json
import boto3

def lambda_handler(event, context):
    # Initialize the SNS client
    sns = boto3.client('sns')
    
    # Specify the ARN of your SNS topic
    topic_arn = 'arn:aws:sns:us-east-1:366716511466:Superb_taxi'
    
    # Your message content
    message = 'Your Taxi Booked successfully!'
    
    # Publish the message to the SNS topic
    response = sns.publish(
        TopicArn=topic_arn,
        Message=message
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('SNS message sent successfully!'),
        'sns_response': response
    }
