import json, urllib, boto3, csv
from datetime import datetime
from decimal import Decimal

# Connect to AWS S3 and DynamoDB
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Connect to SNS 
sns = boto3.client('sns') 
alertTopic = 'proy-sns' 
snsTopicArn = [t['TopicArn'] for t in sns.list_topics()['Topics'] 
                if t['TopicArn'].lower().endswith(':' + alertTopic.lower())][0] 

# Connect to the DynamoDB table
stats_table = dynamodb.Table('proy-stats')

def lambda_handler(event, context):
    # Show the incoming event in the debug log 
    print('Event received by Lambda: ' + json.dumps(event, indent=2))
    

    # Extract the bucket name and object key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    local_filename = '/tmp/stats.csv'

    # Download the file from S3 to the local filesystem
    try:
        s3.meta.client.download_file(bucket, key, local_filename)
    except Exception as e:
        print(e)
        print(f'Error retrieving object {key} from bucket {bucket}. Ensure it exists and is in the same region as this function.')
        raise e

    # Process the CSV file
    row_count = 0
    try:
        with open(local_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                row_count += 1

                #Validate and process each row
                try:
                    date_str = row['Fecha']
                    mean = Decimal(row['Medias'])
                    deviation = Decimal(row['Desviaciones'])

                    if deviation > 0.5:
                        #Message:
                        message = (f"Alert: Weekly temperature deviation exceeded threshold with {deviation} deviation, in {date_str}")
                        
                        print(f"Sending email alert for record on {date_str}")

                        # Send message to SNS 
                        sns.publish( 
                            TopicArn=snsTopicArn, 
                            Message=message, 
                            Subject='Temperature Alert!', 
                            MessageStructure='raw' 
                        )

                    # Convert the date and calculate YearMonth and Day
                    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
                    year_month = 100 * date_obj.year + date_obj.month
                    day = date_obj.day

                    # Insert into the DynamoDB table
                    stats_table.put_item(
                        Item={
                            'YearMonth': year_month,
                            'Day': day,
                            'Mean': mean,
                            'Deviation': deviation
                        }
                    )
                except Exception as e:
                    print(f'Error processing row: {row}. Details: {e}')

    except Exception as e:
        print(f'Error reading or processing the CSV file: {e}')
        raise e

    # Finished
    print(f'{row_count} rows processed and inserted into the DynamoDB table.')
