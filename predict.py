"""
Standalone Prediction Script
Script untuk prediksi bug tanpa API (CLI atau integration)
"""
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Union
import sys

class BugPredictor:
    """Class untuk melakukan prediksi bug"""
    
    def __init__(self, model_path='best_model.joblib', features_path='feature_names.joblib'):
        """
        Initialize predictor dengan load model
        
        Args:
            model_path: Path ke model .joblib file
            features_path: Path ke feature names .joblib file
        """
        try:
            self.model = joblib.load(model_path)
            self.feature_names = joblib.load(features_path)
            print(f"✅ Model loaded: {len(self.feature_names)} features")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            sys.exit(1)
    
    def predict_single(self, metrics: Dict[str, int]) -> Dict:
        """
        Prediksi untuk single file
        
        Args:
            metrics: Dictionary dengan keys sesuai feature_names
                    {
                        'radon_total_complexity': int,
                        'radon_num_items': int,
                        'pylint_msgs_count': int,
                        'pylint_rc': int,
                        'bandit_issues_count': int,
                        'bandit_rc': int
                    }
        
        Returns:
            Dictionary dengan prediction results
        """
        # Validasi input
        missing = set(self.feature_names) - set(metrics.keys())
        if missing:
            raise ValueError(f"Missing features: {missing}")
        
        # Prepare input
        X = np.array([[metrics[feat] for feat in self.feature_names]])
        
        # Prediction
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        return {
            'is_bug': bool(prediction),
            'confidence': float(max(probabilities) * 100),
            'probability_no_bug': float(probabilities[0]),
            'probability_bug': float(probabilities[1]),
            'input_metrics': metrics
        }
    
    def predict_from_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Batch prediction dari pandas DataFrame
        
        Args:
            df: DataFrame dengan columns sesuai feature_names
        
        Returns:
            DataFrame dengan added prediction columns
        """
        # Validasi columns
        missing = set(self.feature_names) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        
        # Prepare input
        X = df[self.feature_names].values
        
        # Predictions
        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)
        
        # Add results to dataframe
        result_df = df.copy()
        result_df['is_bug'] = predictions
        result_df['confidence'] = np.max(probabilities, axis=1) * 100
        result_df['probability_no_bug'] = probabilities[:, 0]
        result_df['probability_bug'] = probabilities[:, 1]
        
        return result_df
    
    def predict_from_csv(self, input_csv: str, output_csv: str = None):
        """
        Batch prediction dari CSV file
        
        Args:
            input_csv: Path ke input CSV file
            output_csv: Path ke output CSV file (optional)
        
        Returns:
            DataFrame dengan results
        """
        # Load CSV
        df = pd.read_csv(input_csv)
        print(f"📁 Loaded {len(df)} records from {input_csv}")
        
        # Predict
        result_df = self.predict_from_dataframe(df)
        
        # Save if output path provided
        if output_csv:
            result_df.to_csv(output_csv, index=False)
            print(f"💾 Results saved to {output_csv}")
        
        # Print summary
        bug_count = result_df['is_bug'].sum()
        print(f"\n📊 Summary:")
        print(f"   Total files: {len(result_df)}")
        print(f"   Predicted bugs: {bug_count} ({bug_count/len(result_df)*100:.1f}%)")
        print(f"   No bugs: {len(result_df) - bug_count} ({(len(result_df)-bug_count)/len(result_df)*100:.1f}%)")
        
        return result_df


def main():
    """Main function untuk CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Bug Prediction CLI')
    parser.add_argument('--csv', type=str, help='Input CSV file untuk batch prediction')
    parser.add_argument('--output', type=str, help='Output CSV file (optional)')
    parser.add_argument('--single', action='store_true', help='Single prediction mode')
    
    args = parser.parse_args()
    
    # Initialize predictor
    predictor = BugPredictor()
    
    if args.csv:
        # Batch prediction dari CSV
        predictor.predict_from_csv(args.csv, args.output)
    
    elif args.single:
        # Single prediction (interactive)
        print("\n🔍 Single Prediction Mode")
        print("Enter code metrics:\n")
        
        metrics = {}
        for feature in predictor.feature_names:
            value = int(input(f"  {feature}: "))
            metrics[feature] = value
        
        result = predictor.predict_single(metrics)
        
        print("\n" + "="*50)
        print("📊 PREDICTION RESULT")
        print("="*50)
        print(f"Bug Detected: {'YES ⚠️' if result['is_bug'] else 'NO ✅'}")
        print(f"Confidence: {result['confidence']:.2f}%")
        print(f"Probability (Bug): {result['probability_bug']:.4f}")
        print(f"Probability (No Bug): {result['probability_no_bug']:.4f}")
        print("="*50)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
