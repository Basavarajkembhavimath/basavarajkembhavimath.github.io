import boto3 # importing libraries
import os
import sys

"""
Plese run the config command before executing code
"""
# Creating S3 bucket instance 
my_s3 = boto3.resource("s3") # Actually we need to specify our key and secret id
my_s3_client = boto3.client("s3")

# Creating new bucket in AWS S3 storage
#my_s3_client.create_bucket(Bucket='mybucket', CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})

combination = ["",'-aws-s3','-aws-aws3','-awss3','-aws3-s3',
'-aws-s3-s3','-aws-ss3','-aws-sss3','-aws-aws','-aws-aws-s3']
my_iter = iter(combination)


global b_name

def get_new_name(): 
    new_name = b_name + next(my_iter)
    print("new_name :",new_name)
    return new_name

def delete_bct():
    for bucket in my_s3.buckets.all():
        if bucket.name != 'firstbucketb':
            my_s3_client.delete_bucket(Bucket= bucket.name)
    print("all buckets deleted successfully !!!")



def Create_s3_bucket(name):
    bucket_name = name
    while True:
        bucket_name = get_new_name()
        try :
            resp = my_s3_client.create_bucket(Bucket= bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
            #my_s3_client.delete_bucket(Bucket= bucket_name, CreateBucketConfiguration={'LocationConstraint': 'us-west-1'})
            print("bucket created successfull !!!!!!")
            #sys.exit()
            break
        except:
            print("got exciption errorss")
            continue
    return

def allbuckets():     
    bucket_list = []
    for bucket in my_s3.buckets.all():
        bucket_list.append(bucket.name)
    return bucket_list

#Create_s3_bucket(b_name)
#delete_bct()
#all_list = allbuckets()
#print(all_list)

print("We have some tasks to do for you")
print("if you want to create a bucket = create, or create_b")
print('if you want to delete a bucket = delete, or delete_b')
print('if you want to see all buckets = all_buckets, or buckets')
print('if you want to upload files to the particular bucket means = upload or up')
print('if you want to download files from the particular bucket means = download or dw')

while True:
    data = input("Tell me to do somthing : ")
    if not data:
        break
    
    if data == 'create' or data == 'create_b':
        b_name = input('Enter the bucket name here : ')
        Create_s3_bucket(b_name)

    if data == 'delete' or data == 'delete_b':
        delete_bct()
    if data == 'all_buckets' or data == 'buckets':
        all_list = allbuckets()
        print(all_list)

def upload_f():
    for file in os.listdir():
        if '.py' in file:
            upload_file_bucket = 'youtube-dummy-bucket'
            upload_file_key = 'python/' + str(file)
            client.upload_file(file, upload_file_bucket, upload_file_key)

