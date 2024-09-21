import pandas as pd
from sklearn.neighbors import NearestNeighbors
import boto3
import io

def load_data_from_s3(bucket_name, file_key, aws_access_key, aws_secret_key):
    # Connect to S3 and download dataset
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    return df

def train_knn_model(ratings_df):
    # Pivot the data into a user-item matrix
    book_matrix = ratings_df.pivot_table(index='user_id', columns='book_id', values='rating').fillna(0)
    
    # Use KNN with cosine similarity
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(book_matrix.values)
    
    return knn, book_matrix

def recommend_books(user_id, model, book_matrix, n_neighbors=5):
    distances, indices = model.kneighbors([book_matrix.loc[user_id].values], n_neighbors=n_neighbors+1)
    
    recommended_books = []
    for idx in indices[0][1:]:
        book_id = book_matrix.columns[idx]
        recommended_books.append(book_id)
        
    return recommended_books
