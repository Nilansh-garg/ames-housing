import pickle
import os
import sys 
import pandas as pd
from sklearn.compose import ColumnTransformer

# Add a simple custom exception handler for robustness
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        self.error_message = f"Error: {error_message}"
        super().__init__(self.error_message)

# NOTE: You MUST import any custom transformers used in your pipeline here.

def load_object(file_path):
    """Loads a pickled object from a given file path."""
    try:
        print(f"DEBUG: Trying to open file at absolute path: {os.path.abspath(file_path)}")
        
        with open(file_path, "rb") as file_obj:
            loaded_object = pickle.load(file_obj)
            print("DEBUG: File opened and object successfully loaded.")
            return loaded_object
            
    except FileNotFoundError:
        print(f"❌ ERROR: File not found at path: {os.path.abspath(file_path)}")
        return None
    except Exception as e:
        # Catch issues like permission errors or corrupt pickle data
        raise CustomException(f"Error loading object from {file_path}: {e}", sys)

def get_preprocessor_feature_names(preprocessor_path):
    """
    Loads the preprocessor and attempts to extract the feature names 
    it was trained on.
    """
    print(f"\n--- Starting Feature Extraction ---")
    
    # 1. Load the preprocessor object
    preprocessor = load_object(preprocessor_path)

    if preprocessor is None:
        print("DEBUG: Preprocessor object is None, skipping extraction.")
        return []

    print(f"DEBUG: Successfully loaded object of type: {type(preprocessor)}")

    feature_names = []
    
    try:
        # 2. Check if it's a ColumnTransformer (most common case for CCDS)
        if hasattr(preprocessor, 'transformers_'):
            print("DEBUG: Processor appears to be a Scikit-learn ColumnTransformer.")
            
            for name, transformer, features in preprocessor.transformers_:
                if isinstance(features, (list, tuple, pd.Index)):
                    feature_names.extend(features)
                
        elif hasattr(preprocessor, 'feature_names_in_'):
            feature_names = list(preprocessor.feature_names_in_)
            print("DEBUG: Using 'feature_names_in_' attribute.")

        else:
            print("DEBUG: Could not automatically determine feature names.")
            
    except Exception as e:
        print(f"❌ ERROR: An error occurred during feature name extraction logic: {e}")
        return []

    return sorted(list(set(feature_names)))

# --- EXECUTION ---
# IMPORTANT: Choose only ONE path option below, based on your terminal location.

# Option A: If you run this script from the project's root folder
PREPROCESSOR_FILE = os.path.join('models', 'preprocessor.pkl') 

# Option B: If you run this script from a folder like src/ or src/pipeline/
# PREPROCESSOR_FILE = os.path.join('../..', 'models', 'processor.pkl') # Assumes running from src/pipeline

all_features = get_preprocessor_feature_names(PREPROCESSOR_FILE)

if all_features:
    print("\n" + "="*50)
    print("✨ REQUIRED FEATURE LIST FOR PREDICTION ✨")
    print("="*50)
    for i, feature in enumerate(all_features):
        print(f"{i+1:2d}. {feature}")
    print("="*50)
    print(f"\nTotal Features Found: {len(all_features)}")
else:
    print("\n⚠️ Feature list extraction finished, but the final list is empty.")
    print("   This means either the file was not found (check the ERROR/DEBUG messages above) ")
    print("   or the structure of the preprocessor is not a standard ColumnTransformer.")
