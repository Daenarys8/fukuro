import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import logging
from typing import List, Dict, Any, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or "models/isolation_forest.joblib"
        self.model = None
        self.initialize_model()

    def initialize_model(self):
        """Initialize or load the Isolation Forest model."""
        try:
            if os.path.exists(self.model_path):
                logger.info(f"Loading existing model from {self.model_path}")
                self.model = joblib.load(self.model_path)
            else:
                logger.info("Creating new Isolation Forest model")
                self.model = IsolationForest(
                    n_estimators=100,
                    contamination=0.1,
                    random_state=42,
                    n_jobs=-1
                )
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise

    def train(self, features: np.ndarray):
        """Train the Isolation Forest model."""
        try:
            logger.info("Training Isolation Forest model")
            self.model.fit(features)
            
            # Save the trained model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump(self.model, self.model_path)
            logger.info(f"Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            raise

    def detect(self, features: List[float]) -> Dict[str, Any]:
        """Detect anomalies in the input features."""
        try:
            # Reshape features for single sample prediction
            features_array = np.array(features).reshape(1, -1)
            
            # Get anomaly score (-1 for anomalies, 1 for normal samples)
            score = self.model.score_samples(features_array)[0]
            
            # Get prediction (-1 for anomalies, 1 for normal samples)
            is_anomaly = self.model.predict(features_array)[0] == -1
            
            # Convert score to a normalized anomaly score between 0 and 1
            normalized_score = 1 - (score - self.model.score_samples(features_array).min()) / \
                (self.model.score_samples(features_array).max() - self.model.score_samples(features_array).min())
            
            return {
                "is_anomaly": bool(is_anomaly),
                "anomaly_score": float(normalized_score),
                "raw_score": float(score)
            }
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            raise

    def bulk_detect(self, features_list: List[List[float]]) -> List[Dict[str, Any]]:
        """Detect anomalies in multiple samples."""
        try:
            features_array = np.array(features_list)
            scores = self.model.score_samples(features_array)
            predictions = self.model.predict(features_array)
            
            # Normalize scores
            normalized_scores = 1 - (scores - scores.min()) / (scores.max() - scores.min())
            
            results = []
            for i in range(len(features_list)):
                results.append({
                    "is_anomaly": bool(predictions[i] == -1),
                    "anomaly_score": float(normalized_scores[i]),
                    "raw_score": float(scores[i])
                })
            
            return results
        except Exception as e:
            logger.error(f"Error in bulk anomaly detection: {str(e)}")
            raise