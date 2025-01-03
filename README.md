Celebrity Finder
Celebrity Finder is a FastAPI application designed to recognize celebrities in images using AWS Rekognition. It supports asynchronous task handling and provides endpoints to process images and retrieve recognition results.

Features
Upload an image to detect celebrities using AWS Rekognition.
Asynchronous task handling for scalable processing.
CloudFormation template for deployment on AWS EC2.
Docker support for local development.
RESTful API for managing tasks and fetching results.
Requirements
For Local Development
Python 3.8 or higher
Git
AWS CLI configured with appropriate credentials
Docker (optional)
For Deployment
AWS CLI configured with appropriate credentials.
An existing EC2 key pair for SSH access.
Prebuilt AMI (Amazon Machine Image) with the application installed.
Getting Started
1. Clone the Repository
bash
Copy code
git clone https://github.com/binarymachine01/celebrity-finder.git
cd celebrity-finder
2. Run Locally
Using Python
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Run the application:
bash
Copy code
uvicorn app.main:app --reload
Access the application at http://127.0.0.1:8000.
Using Docker
Build the Docker image:
bash
Copy code
docker build -t celebrity-finder .
Run the container:
bash
Copy code
docker run -d -p 8000:8000 celebrity-finder
Access the application at http://127.0.0.1:8000.
Deployment on AWS
1. Prepare AMI
Launch an EC2 instance with Amazon Linux 2.
Install Python, FastAPI, and the application dependencies.
Save the instance as a custom AMI.
2. Deploy with CloudFormation
Replace ami-xxxxxxxxxxxxxxxxx in the ec2-fastapi-template.yaml file with your AMI ID.
Deploy the stack:
bash
Copy code
aws cloudformation create-stack --stack-name celebrity-finder-stack --template-body file://ec2-fastapi-template.yaml --parameters ParameterKey=KeyName,ParameterValue=<your-key-name>
Retrieve the application URL from the stack outputs:
bash
Copy code
aws cloudformation describe-stacks --stack-name celebrity-finder-stack --query "Stacks[0].Outputs"
API Endpoints
1. Upload and Process an Image
URL: /process-image/
Method: POST
Description: Upload an image to recognize celebrities using AWS Rekognition.
Request:
File: An image file to upload.
Response:
json
Copy code
{
    "task_id": "12345",
    "message": "Processing started"
}
2. Get Task Status
URL: /process-image/{task_id}/status
Method: GET
Description: Fetch the status and result of an image processing task.
Response (If Task Exists):
json
Copy code
{
    "task_id": "12345",
    "status": "COMPLETED",
    "result": {
        "Celebrities": [
            {
                "Name": "Celebrity Name",
                "Confidence": 99.9,
                "Urls": ["http://example.com"]
            }
        ]
    }
}
Response (If Task Not Found):
json
Copy code
{
    "detail": "Task not found"
}
AWS Rekognition Integration
Requirements
Configure AWS credentials using the AWS CLI:
bash
Copy code
aws configure
Ensure the IAM role or user has the necessary permissions for Rekognition:
rekognition:RecognizeCelebrities
How It Works
Upload an image using the /process-image/ endpoint.
The image is processed asynchronously, and celebrities are recognized using AWS Rekognition.
Retrieve the results using the /process-image/{task_id}/status endpoint.