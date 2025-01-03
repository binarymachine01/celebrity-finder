
# **Celebrity Finder**

Celebrity Finder is a **FastAPI** application designed to recognize celebrities in images using **AWS Rekognition**. It supports asynchronous task handling and provides endpoints to process images and retrieve recognition results.

---

## **Features**

- Upload an image to detect celebrities using AWS Rekognition.
- Asynchronous task handling for scalable processing.
- CloudFormation template for deployment on AWS EC2.
- Docker support for local development.
- RESTful API for managing tasks and fetching results.

---

## **Requirements**

### **For Local Development**
- Python 3.8 or higher
- Git
- AWS CLI configured with appropriate credentials
- Docker (optional)

### **For Deployment**
- AWS CLI configured with appropriate credentials.
- An existing EC2 key pair for SSH access.
- Prebuilt AMI (Amazon Machine Image) with the application installed.

---

## **Getting Started**

### **1. Clone the Repository**
```bash
git clone https://github.com/binarymachine01/celebrity-finder.git
cd celebrity-finder
```

### **2. Run Locally**
#### **Using Python**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Access the application at `http://127.0.0.1:8000`.

#### **Using Docker**
1. Build the Docker image:
   ```bash
   docker build -t celebrity-finder .
   ```
2. Run the container:
   ```bash
   docker run -d -p 8000:8000 celebrity-finder
   ```
3. Access the application at `http://127.0.0.1:8000`.

---

## **Deployment on AWS**

### **1. Prepare AMI**
- Launch an EC2 instance with Amazon Linux 2.
- Install Python, FastAPI, and the application dependencies.
- Save the instance as a custom AMI.

### **2. Deploy with CloudFormation**
1. Replace `ami-xxxxxxxxxxxxxxxxx` in the `ec2-fastapi-template.yaml` file with your AMI ID.
2. Deploy the stack:
   ```bash
   aws cloudformation create-stack --stack-name celebrity-finder-stack --template-body file://ec2-fastapi-template.yaml --parameters ParameterKey=KeyName,ParameterValue=<your-key-name>
   ```
3. Retrieve the application URL from the stack outputs:
   ```bash
   aws cloudformation describe-stacks --stack-name celebrity-finder-stack --query "Stacks[0].Outputs"
   ```

---

## **API Endpoints**

### **1. Upload and Process an Image**
- **URL**: `/process-image/`
- **Method**: POST
- **Description**: Upload an image to recognize celebrities using AWS Rekognition.
- **Request**:
  - **File**: An image file to upload.
- **Response**:
  ```json
  {
      "task_id": "12345",
      "message": "Processing started"
  }
  ```

---

### **2. Get Task Status**
- **URL**: `/task-status/{task_id}`
- **Method**: GET
- **Description**: Fetch the status and result of an image processing task.
- **Response (If Task Exists)**:
  ```json
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
  ```
- **Response (If Task Not Found)**:
  ```json
  {
      "detail": "Task not found"
  }
  ```

---

## **AWS Rekognition Integration**

### **Requirements**
1. Configure AWS credentials using the AWS CLI:
   ```bash
   aws configure
   ```
2. Ensure the IAM role or user has the necessary permissions for Rekognition:
   - `rekognition:RecognizeCelebrities`

### **How It Works**
1. Upload an image using the `/process-image/` endpoint.
2. The image is processed asynchronously, and celebrities are recognized using AWS Rekognition.
3. Retrieve the results using the `/task-status/{task_id}` endpoint.

---

## **Project Structure**
```
celebrity-finder/
├── app/
│   ├── __init__.py
│   ├── auth.py          # Authentication logic
│   ├── main.py          # FastAPI application entry point
│   ├── tasks.py         # Task management logic
├── tests/
│   ├── __init__.py
│   ├── test_auth.py     # Unit tests for authentication
│   ├── test_main.py     # Unit tests for endpoints
│   ├── test_tasks.py    # Unit tests for task manager
├── ec2-fastapi-template.yaml  # CloudFormation template for EC2 deployment
├── Dockerfile           # Dockerfile for containerizing the application
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

