import perkins_brain


def handler(event, context):
    print('fulfillment event:')
    print(event)


    message_fulfillment = perkins_brain.use_perkins_brain(event['currentIntent']['name'],event['currentIntent']['slots'])
    
    
    response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": message_fulfillment
            }
        }
    }
    
    
    return response