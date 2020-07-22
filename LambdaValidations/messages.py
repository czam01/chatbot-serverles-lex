import boto3
from boto3.dynamodb.conditions import Key

class DynamoAccessor:
    def __init__(self, dynamo_table):
        dynamo_db = boto3.resource('dynamodb')
        self.table = dynamo_db.Table(dynamo_table)

    def get_data_from_dynamo(self, dialectId):
        response = self.table.query(KeyConditionExpression=Key('dialectId').eq(dialectId))
        return response["Items"][0]["dialecto"] if any(response["Items"]) else None

    def put_dynamo_element(self, db_element):
        self.table.put_item(Item=db_element)
