import joblib

pipe = joblib.load("best_model.joblib")
print(pipe)
print("\nPipeline steps:")
print(pipe.named_steps)
