# 1. Import the library
import os
from dotenv import load_dotenv
from inference_sdk import InferenceHTTPClient

# Load environment variables
load_dotenv()

# 2. Connect to your local server
client = InferenceHTTPClient(
    api_url=os.getenv("API_URL"),
    api_key=os.getenv("API_KEY")
)

# 3. Run your workflow on an image
result = client.run_workflow(
    workspace_name=os.getenv("WORKSPACE_NAME"),
    workflow_id=os.getenv("WORKFLOW_ID"),
    images={
        "image": "test.png" # Path to your image file
    },
    use_cache=True # Speeds up repeated requests
)

# 4. Get your results
print(result)
