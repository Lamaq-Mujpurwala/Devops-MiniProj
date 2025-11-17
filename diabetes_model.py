
import pandas as pd
from pycaret.classification import setup, compare_models, save_model
from pycaret.datasets import get_data

print("Starting model training...")

    # Load the diabetes dataset from PyCaret's data repository
    # This dataset is small and good for a demo
diabetes_data = get_data('diabetes')
    
print("Dataset loaded.")

    # Initialize the PyCaret environment
    # 'Class variable' is the name of the target column (1 = has diabetes, 0 = no diabetes)
    # We use silent=True to avoid manual prompts
clf_setup = setup(data=diabetes_data, target='Class variable', session_id=123)
    
print("PyCaret setup complete.")

    # Compare all models and find the best one
best_model = compare_models()
    
print(f"Best model found: {best_model}")

    # Save the best model
    # The saved file will be named 'diabetes_model.pkl'
save_model(best_model, 'diabetes_model')
    
print("Model training complete and 'diabetes_model.pkl' has been saved.")