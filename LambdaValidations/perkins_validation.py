from messages import DynamoAccessor




def validate_slots_glue(slots):
    """
    validates the currentIntent Glue values and elements
    """
    
    dynamo_db = DynamoAccessor('perkinsDialects')
    glue_command = slots.get('glue_command') or ''
    glue_options = slots.get('glue_options') or ''
    glue_endpoint_name = slots.get('glue_endpoint_name') or ''

    
    """
    ask for one element per iteration building the process logic
    the precedence of the variables is important on the element creation.
    """
    if glue_command.lower() == 'help':
        return [False, 'glue_command', dynamo_db.get_data_from_dynamo("glue_help_message")]
    if glue_command.lower() not in ['endpoints', 'workflows', 'jobs', 'crawlers']:
        return [False, 'glue_command', dynamo_db.get_data_from_dynamo("glue_alert_help_message")]
    if glue_options and glue_options.lower() not in ['listar', 'iniciar', 'cerrar']:
        return [False, 'glue_options', dynamo_db.get_data_from_dynamo("glue_options_message")]
    
    if glue_options in ['iniciar','cerrar'] and glue_command.lower() == 'endpoints' and not glue_endpoint_name:
        return [False, 'glue_endpoint_name', dynamo_db.get_data_from_dynamo("glue_init_endpoint")]
        
    return [True]


def validate_slots_s3(slots):
    """
    validates the currentIntent S3 values and elements
    """
    
    dynamo_db = DynamoAccessor('perkinsDialects')
    se_initial_options = slots.get('se_initial_options') or ''
    bucket_name_full = slots.get('bucket_name_full') or ''


    """
    ask for one element per iteration building the process logic
    the precedence of the variables is important on the element creation.
    """
    if se_initial_options.lower() == 'help':
        return [False, 'se_initial_options', dynamo_db.get_data_from_dynamo("s3_help_message")]
    if se_initial_options.lower() not in ['listar', 'crear', 'crear bucket', 'ultimo update']:
        return [False, 'se_initial_options', dynamo_db.get_data_from_dynamo("s3_initial_options_message")]
    if se_initial_options and not bucket_name_full:
        return [False, 'bucket_name_full', dynamo_db.get_data_from_dynamo("s3_bucker_name_message")]
    return [True]
    

def validate(event, context):
    """
    the logic can be used on other element handlers, at the moment the main event discriminant can be obtained from the intentName
    """
    print (event)
    if event['sessionAttributes'] is not None:
        session_attributes = event['sessionAttributes']
    else:
        session_attributes = {}
    slots = event['currentIntent']['slots']

    if "Glue_control" == event['currentIntent']['name']:
        val_result = validate_slots_glue(slots)
    elif "sss_control" == event['currentIntent']['name']:
        val_result = validate_slots_s3(slots)

    if val_result[0]:
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate',
                'slots': slots,

            }
        }
    else:
        return {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'intentName': event['currentIntent']['name'],
                'slots': slots,
                'slotToElicit': val_result[1],
                'message': {'contentType': 'PlainText', 'content': val_result[2]}
            }
        }

