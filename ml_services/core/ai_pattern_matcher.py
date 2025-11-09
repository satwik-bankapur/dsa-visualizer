import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from typing import Dict, List, Tuple, Any
import os

from models.internal_models import AlgorithmPattern
from core.ast_feature_extractor import ASTFeatureExtractor
from config.log_config import get_logger

logger = get_logger(__name__)

class AIPatternMatcher:
    """ML-based algorithm pattern recognition"""

    def __init__(self, model_path: str = "models/"):
        self.model_path = model_path
        self.feature_extractor = ASTFeatureExtractor()
        self.vectorizer = DictVectorizer(sparse=False)
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.is_trained = False

        # Ensure model directory exists
        os.makedirs(model_path, exist_ok=True)

        # Try to load pre-trained model
        self._try_load_model()

    def train(self, training_data: List[Tuple[str, str, AlgorithmPattern]]) -> Dict[str, float]:
        """Train the ML model on code samples

        Args:
            training_data: List of (code_ast_str, code_text, pattern_label) tuples
        """
        logger.info(f"Training AI pattern matcher on {len(training_data)} samples")

        # Extract features
        X_raw = []
        y = []

        for ast_code, code_text, pattern in training_data:
            try:
                # Parse AST from string if needed
                import ast
                if isinstance(ast_code, str):
                    tree = ast.parse(ast_code)
                else:
                    tree = ast_code

                # Extract features
                features = self.feature_extractor.extract_features(tree, code_text)
                X_raw.append(features)
                y.append(pattern.value)

            except Exception as e:
                logger.warning(f"Failed to extract features from sample: {e}")
                continue

        if len(X_raw) == 0:
            raise ValueError("No valid training samples found")

        # Vectorize features
        X = self.vectorizer.fit_transform(X_raw)
        y = np.array(y)

        # Split for validation
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Train classifier
        self.classifier.fit(X_train, y_train)

        # Validate
        y_pred = self.classifier.predict(X_val)
        accuracy = accuracy_score(y_val, y_pred)

        logger.info(f"Training completed. Validation accuracy: {accuracy:.3f}")
        print(f"Classification Report:\n{classification_report(y_val, y_pred)}")

        # Save model
        self._save_model()
        self.is_trained = True

        return {
            'accuracy': accuracy,
            'validation_samples': len(X_val),
            'training_samples': len(X_train)
        }

    def predict_pattern(self, code_ast, code_text: str = "") -> Tuple[AlgorithmPattern, float]:
        """Predict algorithm pattern for given code"""
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first or load pre-trained model.")

        try:
            # Extract features
            features = self.feature_extractor.extract_features(code_ast, code_text)

            # Vectorize
            X = self.vectorizer.transform([features])

            # Predict
            prediction = self.classifier.predict(X)[0]
            probabilities = self.classifier.predict_proba(X)[0]

            # Get confidence (max probability)
            confidence = np.max(probabilities)

            # Convert string prediction back to enum
            try:
                pattern = AlgorithmPattern(prediction)
            except ValueError:
                logger.warning(f"Unknown pattern predicted: {prediction}")
                return None, 0.0

            return pattern, confidence

        except Exception as e:
            logger.error(f"Error in pattern prediction: {e}")
            return None, 0.0

    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores"""
        if not self.is_trained:
            return {}

        feature_names = self.vectorizer.get_feature_names_out()
        importances = self.classifier.feature_importances_

        return dict(zip(feature_names, importances))

    def _save_model(self):
        """Save trained model and vectorizer"""
        try:
            joblib.dump(self.classifier, os.path.join(self.model_path, 'classifier.pkl'))
            joblib.dump(self.vectorizer, os.path.join(self.model_path, 'vectorizer.pkl'))
            logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Failed to save model: {e}")

    def _try_load_model(self):
        """Try to load pre-trained model"""
        try:
            classifier_path = os.path.join(self.model_path, 'classifier.pkl')
            vectorizer_path = os.path.join(self.model_path, 'vectorizer.pkl')

            if os.path.exists(classifier_path) and os.path.exists(vectorizer_path):
                self.classifier = joblib.load(classifier_path)
                self.vectorizer = joblib.load(vectorizer_path)
                self.is_trained = True
                logger.info("Pre-trained model loaded successfully")
            else:
                logger.info("No pre-trained model found")

        except Exception as e:
            logger.warning(f"Failed to load pre-trained model: {e}")
