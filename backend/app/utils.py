import json

def load_class_names(path: str) -> list[str]:
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading class names: {e}")
        # Fallback default
        return ["dura", "pisifera", "tenera"]

def get_description(label: str) -> str:
    descriptions = {
        "dura": "Dura memiliki cangkang yang tebal dan mesocarp yang relatif lebih tipis. Jenis ini biasanya memiliki kandungan minyak lebih rendah dibanding Tenera.",
        "pisifera": "Pisifera umumnya memiliki cangkang sangat tipis atau hampir tidak memiliki cangkang. Jenis ini sering digunakan sebagai induk jantan dalam persilangan.",
        "tenera": "Tenera adalah hasil persilangan Dura dan Pisifera. Jenis ini memiliki cangkang tipis, mesocarp lebih tebal, dan umum digunakan untuk produksi komersial."
    }
    return descriptions.get(label.lower(), "Deskripsi tidak tersedia.")
