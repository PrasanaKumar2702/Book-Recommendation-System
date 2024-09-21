## Installation

### Requirements

- Python 3.8+
- AWS account with access to S3, RDS, and EC2
- PostgreSQL database (for RDS)

### Step-by-step Instructions

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/book-recommender.git
    cd book-recommender
    ```

2. **Install Dependencies**

    Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

    Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. **AWS Setup**

    Ensure you have AWS credentials and resources ready:
    
    - Upload your dataset (e.g., ratings.csv) to S3.
    - Set up an RDS instance with the book metadata.
    
    Configure the following environment variables:

    ```bash
    export AWS_ACCESS_KEY=your_aws_access_key
    export AWS_SECRET_KEY=your_aws_secret_key
    export S3_BUCKET_NAME=your_s3_bucket_name
    export RDS_HOST=your_rds_host
    export RDS_USER=your_rds_user
    export RDS_PASSWORD=your_rds_password
    export RDS_DB=your_rds_db
    ```

4. **Run the Application**

    Start the Flask web server:

    ```bash
    python app.py
    ```

    The app will be available at `http://localhost:5000`. If hosted on EC2, use your instance's public IP to access the app.

## Usage

- Enter a user ID on the web interface to get a list of recommended books based on that user's previous ratings.

## Future Improvements

- Add more sophisticated recommendation algorithms (e.g., matrix factorization).
- Enhance the web interface with more filtering options (genres, ratings, etc.).
- Implement user login and profiles.

