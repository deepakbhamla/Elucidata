import json
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import time
import pyqrcode 
import png 
from pyqrcode import QRCode 
import qrcode
from Crypto import Random
import ast
from Crypto.Cipher import PKCS1_OAEP
import random

from logging import basicConfig, getLogger, INFO
from botocore.exceptions import ClientError
from pyqldb.driver.qldb_driver import QldbDriver
from amazon.ion.simpleion import dumps, loads

from pyqldbsamples.constants import Constants

hash = hashlib.sha1()
logger = getLogger(__name__)
basicConfig(level=INFO)
table_name = "i8labs"


##################################################### QLDB CONNECTION ################################################################
def create_qldb_driver(ledger_name=table_name, region_name=None, endpoint_url=None, boto3_session=None):
    qldb_driver = QldbDriver(ledger_name=ledger_name, region_name=region_name, endpoint_url=endpoint_url,
                             boto3_session=boto3_session)
    return qldb_driver
######################################################################################################################################

################################################ INSERT DATA INTO QLDB ################################################################
def convert_object_to_ion(py_object):
    ion_object = loads(dumps(py_object))
    return ion_object

def get_document_ids_from_dml_results(result):
    ret_val = list(map(lambda x: x.get('documentId'), result))
    return ret_val

def insert_documents(transaction_executor, table_name, documents):
    logger.info('Inserting some documents in the {} table...'.format(table_name))
    statement = 'INSERT INTO {} ?'.format(table_name)
    cursor = transaction_executor.execute_statement(statement, convert_object_to_ion(documents))
    list_of_document_ids = get_document_ids_from_dml_results(cursor)

    return list_of_document_ids

def update_and_insert_documents(transaction_executor, qr_code_data):
    cursor = insert_documents(transaction_executor,Constants.I8LABS_CONSENT_TABLE_NAME, qr_code_data)
    print(cursor)
######################################################################################################################################



def lambda_handler(event=None, context=None):
    ############################################################ USER ID GENERATION ######################################################
    data = {
        "name": "satyam anand",
        "aadharNumber": "725335304104",
        "phoneNumber": "9513868175",
        "age": "22"
        }
    hash.update(str(time.time()).encode('utf-8'))
    hash.update(data["name"].encode('utf-8'))
    hash.update(data["aadharNumber"].encode('utf-8'))
    hash.update(data["phoneNumber"].encode('utf-8'))
    hash.update(data["age"].encode('utf-8'))
    userId = hash.hexdigest()
    print(hash.hexdigest())
    ######################################################################################################################################
      
    ###################################################### GENERATING KEY PAIR ############################################################
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)

    publickey = key.publickey()
    print("Public Key : ", publickey)
    ######################################################################################################################################

    #################################################### DATA ENCRYPTION USING PUBLIC KEY ################################################
    encryptor = PKCS1_OAEP.new(publickey)
    decryptor = PKCS1_OAEP.new(key)
    data = json.dumps(data)
    data = bytes(data, 'utf-8')
    encrypted = encryptor.encrypt(data)
    print('encrypted :', encrypted)
    ######################################################################################################################################
    qr_code_data = {
        "Publickey": str(publickey.export_key()),
        "signature": str(encrypted),
        "User_Id": str(userId)
    }
    try:
        with create_qldb_driver() as driver:
            driver.execute_lambda(lambda executor: update_and_insert_documents(executor, qr_code_data),
                                   lambda retry_attempt: logger.info('Retrying due to OCC conflict...'))
            logger.info('Documents inserted successfully!')
    except Exception:
        logger.exception('Error inserting or updating documents.')
    
    ##################################################### QR CODE GENERATION #############################################################
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )
    
    qr.add_data(qr_code_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save('qrcode_test.png')
    ######################################################################################################################################

    ##################################################### OTP GENERATION #################################################################
    otp = random.randint(1000,9999)
    print(otp)
    encryptedOTP = encryptor.encrypt(bytes(str(otp), 'utf-8'))
    print(f"ecrypted otp = {encryptedOTP}")
    ######################################################################################################################################

    #################################################### OTP VERIFICATION ################################################################
    decryptedOTP = decryptor.decrypt(ast.literal_eval(str(encryptedOTP)))
    print('Decrypted otp', decryptedOTP.decode('utf-8'))
    ######################################################################################################################################

    ####################################################### USER DATA RETREIVAL ##########################################################
    decrypted = decryptor.decrypt(ast.literal_eval(str(encrypted)))
    print('Decrypted : ', decrypted.decode('utf-8'))
    ######################################################################################################################################

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == '__main__':
    lambda_handler()