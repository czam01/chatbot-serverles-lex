import boto3
import botocore

GLUE =  boto3.client('glue')
S3 = boto3.client('s3')

def use_perkins_brain(intention_name,slots):
    if intention_name == 'Glue_control':
        glue_options = slots.get('glue_options')
        glue_command = slots.get('glue_command')
        glue_endpoint_name = slots.get('glue_endpoint_name') or '' # for optional slots
        
        if glue_options == 'listar' and glue_command == 'jobs' :
            message = GLUE.list_jobs()
            return 'estos son los jobs en la cuenta: '+ str(message['JobNames'])
        
        if glue_options == 'listar' and glue_command == 'crawlers' :
            message = GLUE.list_crawlers()
            return 'estos son los crawlers en la cuenta: '+ str(message['CrawlerNames'])
            
        if glue_options == 'listar' and glue_command == 'endpoints' :
            message = GLUE.list_dev_endpoints()
            return 'estos son los Dev endpoints activos: '+ str(message['DevEndpointNames']) if message['DevEndpointNames'] else 'No tiene endpoints Activos'
            
        if glue_options == 'iniciar' and glue_command == 'endpoints' and glue_endpoint_name:
            message = GLUE.create_dev_endpoint(EndpointName = glue_endpoint_name, RoleArn ="arn:aws:iam::136916740601:role/Glueadmin")
            return 'proceso de creacion de endpoint inciado con el nombre {} '.format(glue_endpoint_name)
            
        if glue_options == 'cerrar' and glue_command == 'endpoints' and glue_endpoint_name:
            message = GLUE.delete_dev_endpoint(EndpointName = glue_endpoint_name)
            return 'proceso de borrado de endpoint inciado con el nombre {} '.format(glue_endpoint_name)
    
    if intention_name == 'sss_control':
        se_initial_options = slots.get('se_initial_options')
        bucket_name_full = slots.get('bucket_name_full')
        
        if se_initial_options == 'listar':
            try:
                bucket_elements =  S3.list_objects(Bucket=bucket_name_full).get('Contents')
                if bucket_elements:
                    message = bucket_elements
                    bucket_objects = [key["Key"] for key in message]
                    return 'estos son los archivos en {}:  {}'.format(bucket_name_full,str(bucket_objects))
                else:
                    return 'El bucket no tiene elementos'
            except botocore.exceptions.ClientError as error:
                return 'tenemos un problema del tipo {}, por favor valide de nuevo la informacion. si desea adicionar el modulo por favor contacte con el desarrollador... gracias!'.format(error.response['Error']['Code'])
            
        
        if se_initial_options in ['crear', 'crear bucket']:
            message = S3.create_bucket(Bucket=bucket_name_full)
            return 'bucket {} creado! gracias por usar nuestro servicio!'.format(bucket_name_full)
        
    
        