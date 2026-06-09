import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
import tensorflow as tf
from .utils import load_class_names

class ModelManager:
    def __init__(self):
        self.model = None
        self.class_names = []
        
    def load_model_and_classes(self, model_path: str, class_names_path: str):
        print(f"Loading model from {model_path}...")
        if os.path.exists(model_path):
            from tensorflow.keras.layers import Dense, InputLayer, RandomFlip, RandomRotation, RandomZoom, Layer
            
            def sanitize_kwargs(kwargs):
                for k in ['batch_shape', 'optional', 'data_format', 'quantization_config']:
                    kwargs.pop(k, None)
                return kwargs

            class SafeDense(Dense):
                def __init__(self, units, **kwargs):
                    super().__init__(units, **sanitize_kwargs(kwargs))
                    
            class SafeInputLayer(InputLayer):
                def __init__(self, **kwargs):
                    super().__init__(**sanitize_kwargs(kwargs))
                    
            class SafeRandomFlip(RandomFlip):
                def __init__(self, mode="horizontal_and_vertical", seed=None, **kwargs):
                    super().__init__(mode=mode, seed=seed, **sanitize_kwargs(kwargs))
                    
            class SafeRandomRotation(RandomRotation):
                def __init__(self, factor, fill_mode="reflect", interpolation="bilinear", seed=None, fill_value=0.0, **kwargs):
                    super().__init__(factor=factor, fill_mode=fill_mode, interpolation=interpolation, seed=seed, fill_value=fill_value, **sanitize_kwargs(kwargs))
                    
            class SafeRandomZoom(RandomZoom):
                def __init__(self, height_factor, width_factor=None, fill_mode="reflect", interpolation="bilinear", seed=None, fill_value=0.0, **kwargs):
                    super().__init__(height_factor=height_factor, width_factor=width_factor, fill_mode=fill_mode, interpolation=interpolation, seed=seed, fill_value=fill_value, **sanitize_kwargs(kwargs))

            custom_objs = {
                'Dense': SafeDense,
                'InputLayer': SafeInputLayer,
                'RandomFlip': SafeRandomFlip,
                'RandomRotation': SafeRandomRotation,
                'RandomZoom': SafeRandomZoom
            }
            
            with tf.keras.utils.custom_object_scope(custom_objs):
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
