import os
import tensorflow as tf
from .utils import load_class_names

class ModelManager:
    def __init__(self):
        self.model = None
        self.class_names = []
        
    def load_model_and_classes(self, model_path: str, class_names_path: str):
        print(f"Loading model from {model_path}...")
        if os.path.exists(model_path):
            from tensorflow.keras.layers import InputLayer, Dense
            
            class SafeInputLayer(InputLayer):
                def __init__(self, **kwargs):
                    kwargs.pop('batch_shape', None)
                    kwargs.pop('optional', None)
                    super().__init__(**kwargs)
                    
            class SafeDense(Dense):
                def __init__(self, **kwargs):
                    kwargs.pop('quantization_config', None)
                    super().__init__(**kwargs)
                    
            with tf.keras.utils.custom_object_scope({'InputLayer': SafeInputLayer, 'Dense': SafeDense}):
                self.model = tf.keras.models.load_model(model_path, compile=False)
            
            print("Model loaded successfully.")
        else:
            print(f"Model file not found at {model_path}")
            
        print(f"Loading class names from {class_names_path}...")
        self.class_names = load_class_names(class_names_path)
        print(f"Class names: {self.class_names}")
        
        # Cek apakah ada class unknown
        if "unknown" not in [c.lower() for c in self.class_names]:
            print("WARNING: 'unknown' is not in class_names.json. Expected class names: ['dura', 'pisifera', 'tenera', 'unknown']")
        
    def is_loaded(self) -> bool:
        return self.model is not None

model_manager = ModelManager()
