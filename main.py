import streamlit as st
import tensorflow as tf
import numpy as np
import time
from PIL import Image
import base64
from io import BytesIO
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input as mobile_preprocess, decode_predictions

# Page configuration
st.set_page_config(
    page_title="KHASYAPIX - AI Plant Disease Detection",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for KHASYAPIX - Vibrant Dark Theme
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        padding-top: 2rem;
    }
    
    /* KHASYAPIX Vibrant Dark Theme Variables */
    :root {
        --primary-color: #00ff88;
        --secondary-color: #ff0080;
        --accent-color: #00d4ff;
        --neon-purple: #8b5cf6;
        --neon-orange: #ff6b35;
        --neon-green: #39ff14;
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --bg-primary: #0a0a0a;
        --bg-secondary: #1a1a1a;
        --bg-tertiary: #2a2a2a;
        --border-color: #333333;
        --shadow: 0 0 20px rgba(0, 255, 136, 0.3);
        --shadow-hover: 0 0 30px rgba(0, 255, 136, 0.5);
        --shadow-purple: 0 0 20px rgba(139, 92, 246, 0.3);
        --shadow-pink: 0 0 20px rgba(255, 0, 128, 0.3);
        --border-radius: 15px;
        --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        --gradient-primary: linear-gradient(135deg, #00ff88, #00d4ff);
        --gradient-secondary: linear-gradient(135deg, #ff0080, #8b5cf6);
        --gradient-accent: linear-gradient(135deg, #ff6b35, #39ff14);
    }
    
    /* Apply KHASYAPIX theme to body */
    .stApp {
        background: radial-gradient(ellipse at center, #1a1a2e 0%, #0a0a0a 100%);
        color: var(--text-primary);
        font-family: 'Exo 2', sans-serif;
        transition: var(--transition);
        min-height: 100vh;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--bg-secondary), var(--bg-tertiary));
        border-right: 2px solid var(--primary-color);
        box-shadow: var(--shadow);
    }
    
    .css-1d391kg .css-1v0mbdj {
        color: var(--text-primary);
        font-family: 'Exo 2', sans-serif;
    }
    
    /* KHASYAPIX Logo Header */
    .khasyapix-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border: 2px solid var(--primary-color);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow), inset 0 0 50px rgba(0, 255, 136, 0.1);
        animation: slideInDown 1s ease-out, glow 2s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .khasyapix-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, var(--primary-color), transparent);
        animation: rotate 4s linear infinite;
        opacity: 0.1;
    }
    
    .khasyapix-logo {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
        animation: pulse 2s ease-in-out infinite alternate;
        position: relative;
        z-index: 1;
    }
    
    .khasyapix-tagline {
        font-size: 1.4rem;
        margin: 1rem 0 0 0;
        color: var(--accent-color);
        font-weight: 500;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .khasyapix-subtitle {
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
        color: var(--text-secondary);
        position: relative;
        z-index: 1;
    }
    
    /* KHASYAPIX Card Styling */
    .card {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border: 2px solid var(--primary-color);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow), inset 0 0 20px rgba(0, 255, 136, 0.05);
        transition: var(--transition);
        animation: fadeInUp 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 136, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .card:hover {
        box-shadow: var(--shadow-hover), var(--shadow-purple);
        transform: translateY(-5px) scale(1.02);
        border-color: var(--accent-color);
    }
    
    .card:hover::before {
        left: 100%;
    }
    
    /* KHASYAPIX Button Styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: var(--bg-primary);
        border: 2px solid var(--primary-color);
        border-radius: var(--border-radius);
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        font-family: 'Exo 2', sans-serif;
        transition: var(--transition);
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: var(--shadow-hover), var(--shadow-purple);
        background: var(--gradient-secondary);
        border-color: var(--secondary-color);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
        box-shadow: var(--shadow);
    }
    
    /* File Uploader Styling */
    .stFileUploader > div {
        border: 2px dashed var(--border-color);
        border-radius: var(--border-radius);
        padding: 2rem;
        text-align: center;
        transition: var(--transition);
        background: var(--bg-secondary);
    }
    
    .stFileUploader > div:hover {
        border-color: var(--primary-color);
        background: var(--bg-primary);
    }
    
    /* Image Display */
    .image-container {
        text-align: center;
        margin: 2rem 0;
        animation: fadeIn 0.8s ease-out;
    }
    
    .image-container img {
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        max-width: 100%;
        height: auto;
    }
    
    /* Prediction Result */
    .prediction-result {
        background: linear-gradient(135deg, #E8F5E8, #F0F8F0);
        border: 2px solid var(--primary-color);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 2rem 0;
        animation: slideInUp 0.8s ease-out;
    }
    
    .prediction-result h3 {
        color: var(--secondary-color);
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .prediction-result p {
        color: var(--text-primary);
        line-height: 1.6;
        margin: 0;
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }
    
    /* Theme Toggle */
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: var(--shadow);
        transition: var(--transition);
    }
    
    .theme-toggle:hover {
        box-shadow: var(--shadow-hover);
        transform: scale(1.1);
    }
    
    /* KHASYAPIX Animations */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
    
    @keyframes pulse {
        0% {
            text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
        }
        100% {
            text-shadow: 0 0 50px rgba(0, 255, 136, 0.8), 0 0 80px rgba(0, 212, 255, 0.3);
        }
    }
    
    @keyframes glow {
        0% {
            box-shadow: var(--shadow), inset 0 0 50px rgba(0, 255, 136, 0.1);
        }
        100% {
            box-shadow: var(--shadow-hover), inset 0 0 80px rgba(0, 255, 136, 0.2);
        }
    }
    
    @keyframes rotate {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    
    @keyframes neonFlicker {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .card {
            padding: 1.5rem;
        }
    }
    
    /* Success Message Styling */
    .stSuccess {
        background: linear-gradient(135deg, #E8F5E8, #F0F8F0);
        border: 2px solid var(--primary-color);
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 1rem 0;
        animation: slideInUp 0.6s ease-out;
    }
    
    /* Sidebar Navigation */
    .css-1d391kg .css-1v0mbdj {
        font-weight: 600;
        color: var(--text-primary);
    }
    
    .css-1d391kg .css-1v0mbdj:hover {
        color: var(--primary-color);
        transition: var(--transition);
    }

    /* Treatment Step Styling */
    .treatment-step {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border-left: 4px solid var(--neon-green);
        border-radius: 0 var(--border-radius) var(--border-radius) 0;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
        transition: var(--transition);
        animation: slideInUp 0.5s ease-out;
    }

    .treatment-step:hover {
        transform: translateX(10px);
        box-shadow: var(--shadow-hover);
        border-left-color: var(--primary-color);
    }

    .step-number {
        font-family: 'Orbitron', monospace;
        color: var(--neon-green);
        font-size: 1.2rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        display: block;
    }

    .step-content {
        color: var(--text-primary);
        font-size: 1.05rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Theme toggle functionality
def toggle_theme():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    else:
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Add theme toggle button
st.markdown("""
<div class="theme-toggle" onclick="toggleTheme()">
    <span id="theme-icon">🌙</span>
</div>

<script>
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    
    if (body.getAttribute('data-theme') === 'dark') {
        body.setAttribute('data-theme', 'light');
        themeIcon.textContent = '🌙';
    } else {
        body.setAttribute('data-theme', 'dark');
        themeIcon.textContent = '☀️';
    }
}
</script>
""", unsafe_allow_html=True)

# Model loading with caching
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model("trained_plant_disease_model.keras")
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

@st.cache_resource
def load_classifier_model():
    try:
        # Load MobileNetV2 pre-trained on ImageNet for general object recognition
        model = MobileNetV2(weights='imagenet')
        return model
    except Exception as e:
        st.error(f"Error loading classifier model: {str(e)}")
        return None

def is_plant_image(test_image):
    classifier = load_classifier_model()
    if classifier is None:
        return True # Fail open if classifier fails
    
    try:
        # Preprocess for MobileNetV2
        img = Image.open(test_image).convert('RGB')
        img = img.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = mobile_preprocess(img_array)
        
        preds = classifier.predict(img_array)
        decoded_preds = decode_predictions(preds, top=5)[0]
        
        # Broad list of plant/agriculture related terms
        plant_keywords = [
            'leaf', 'plant', 'flower', 'fruit', 'vegetable', 'tree', 'grass', 
            'agriculture', 'crop', 'corn', 'maize', 'wheat', 'rice', 'soy', 
            'bean', 'berry', 'bush', 'shrub', 'forest', 'garden', 'pot',
            'broccoli', 'cabbage', 'cauliflower', 'cucumber', 'zucchini',
            'squash', 'pumpkin', 'melon', 'gourd', 'tomato', 'potato',
            'pepper', 'apple', 'orange', 'lemon', 'lime', 'banana',
            'grape', 'cherry', 'peach', 'pear', 'plum', 'strawberry',
            'daisy', 'rose', 'tulip', 'sunflower', 'orchid', 'lily',
            'fungus', 'mushroom', 'buckeye', 'ear', 'head_cabbage',
            'cardoon', 'artichoke', 'bell_pepper', 'pineapple', 'fig',
            'pomegranate', 'custard_apple', 'jackfruit', 'strawberry',
            'greenhouse', 'pot', 'vase', 'cauliflower', 
            # Textures often confused with leaves
            'velvet', 'wool', 'silk', 'handkerchief', 'tissue', 'towel', 
            'bath_towel', 'dishrag', 'doormat', 'swab', 'lint',
            # Shapes/Green things confused with leaves
            'chameleon', 'lizard', 'reptile', 'snake', 'slug', 'worm', 
            'nematode', 'conch', 'snail', 'shell', 'sea_slug', 
            'cucumber', 'zucchini', 'sea_anemone', 'coral', 'sponge',
            'lacewing', 'dragonfly', 'damselfly', 'mantis', 'grasshopper',
            'cricket', 'stick_insect', 'cockroach', 'ant', 'bee', 'fly'
        ]
        
        # Check if any top prediction contains a plant keyword
        is_plant = False
        detected_objects = []
        
        for _, label, score in decoded_preds:
            detected_objects.append(f"{label} ({score:.2f})")
            label_lower = label.lower()
            for keyword in plant_keywords:
                if keyword in label_lower:
                    is_plant = True
                    break
            if is_plant:
                break
                
        return is_plant, detected_objects
        
    except Exception as e:
        print(f"Error in classifier: {e}")
        return True, [] # Fail open

def model_prediction(test_image):
    model = load_model()
    if model is None:
        return None, 0
    
    try:
        image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128, 128))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])  # convert single image to batch
        predictions = model.predict(input_arr)
        confidence = np.max(predictions)
        result_index = np.argmax(predictions)
        return result_index, confidence
    except Exception as e:
        st.error(f"Error during prediction: {str(e)}")
        return None, 0

# KHASYAPIX Sidebar Branding
st.sidebar.markdown("""
<div style="text-align: center; padding: 1.5rem 0; border-bottom: 2px solid var(--primary-color); margin-bottom: 2rem; background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); border-radius: var(--border-radius); box-shadow: var(--shadow);">
    <h2 style="color: var(--primary-color); margin: 0; font-size: 1.8rem; font-family: 'Orbitron', monospace; font-weight: 700; text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);">🔬 KHASYAPIX</h2>
    <p style="color: var(--accent-color); margin: 0.5rem 0 0 0; font-size: 1rem; font-weight: 500; text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);">AI Plant Disease Detection</p>
    <p style="color: var(--text-secondary); margin: 0.3rem 0 0 0; font-size: 0.8rem;">Advanced Neural Network Technology</p>
</div>
""", unsafe_allow_html=True)

app_mode = st.sidebar.selectbox(
    "Select Page", 
    ["HOME", "DISEASE RECOGNITION"],
    key="page_selector"
)

# Add some spacing
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Add info section in sidebar
st.sidebar.markdown("""
<div style="background: var(--bg-secondary); padding: 1rem; border-radius: var(--border-radius); border: 1px solid var(--border-color);">
    <h4 style="color: var(--primary-color); margin: 0 0 0.5rem 0;">ℹ️ About</h4>
    <p style="color: var(--text-secondary); margin: 0; font-size: 0.9rem;">
        This system uses advanced AI to detect plant diseases from leaf images, helping farmers make informed decisions for sustainable agriculture.
    </p>
</div>
""", unsafe_allow_html=True)

# Load and display header image
try:
    img = Image.open("Diseases.png")
    st.image(img, use_container_width=True)
except Exception as e:
    st.warning("Could not load header image. Please ensure 'Diseases.png' is in the project directory.")

# Disease class names and descriptions
class_name = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
            'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
            'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
            'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
            'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
            'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
            'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
            'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
            'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
            'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
            'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
            'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
            'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
              'Tomato___healthy']

disease_descriptions = {
    'Apple___Apple_scab': 'Apple scab is a disease of apple and crabapple trees caused by the fungus Venturia inaequalis. It appears as olive-green to brown spots on leaves, fruit, and twigs. The spots can cause leaves to yellow and drop prematurely, and fruit to become deformed and scabby.',
    'Apple___Black_rot': 'Black rot is a fungal disease that affects apple trees. It can cause a variety of symptoms, including leaf spots, fruit rot, and cankers on branches. The fruit rot appears as a firm, black lesion that can eventually mummify the fruit.',
    'Apple___Cedar_apple_rust': 'Cedar-apple rust is a fungal disease that requires both an apple or crabapple tree and a juniper or cedar tree to complete its life cycle. On apple trees, it causes bright orange or yellow spots on the leaves and fruit. The spots on the fruit can make it inedible.',
    'Apple___healthy': 'The plant is healthy.',
    'Blueberry___healthy': 'The plant is healthy.',
    'Cherry_(including_sour)___Powdery_mildew': 'Powdery mildew of cherry is a fungal disease that affects sweet and sour cherries. It is caused by Podosphaera clandestina. The disease is characterized by a white powdery growth on the leaves and fruit of the tree.',
    'Cherry_(including_sour)___healthy': 'The plant is healthy.',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Gray leaf spot is a fungal disease that affects corn. It is caused by the fungus Cercospora zeae-maydis. The disease is characterized by small, rectangular, tan lesions on the leaves of the corn plant.',
    'Corn_(maize)___Common_rust_': 'Common rust is a fungal disease that affects corn. It is caused by the fungus Puccinia sorghi. The disease is characterized by small, circular, reddish-brown pustules on the leaves of the corn plant.',
    'Corn_(maize)___Northern_Leaf_Blight': 'Northern corn leaf blight is a fungal disease of corn caused by the fungus Exserohilum turcicum. The disease causes large, cigar-shaped lesions on the leaves of the corn plant, which can reduce the photosynthetic area of the leaf and lead to yield loss.',
    'Corn_(maize)___healthy': 'The plant is healthy.',
    'Grape___Black_rot': 'Black rot is a fungal disease of grapes caused by the fungus Guignardia bidwellii. The disease affects all green parts of the vine, but is most destructive to the fruit. The disease causes the fruit to turn black and shrivel, and can result in complete crop loss.',
    'Grape___Esca_(Black_Measles)': 'Esca, also known as black measles, is a complex fungal disease of grapevines that can cause a wide range of symptoms, including leaf striping, berry spotting, and sudden dieback of the vine. The disease is caused by a complex of fungi, and there is no cure.',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Isariopsis leaf spot is a fungal disease of grapes caused by the fungus Pseudocercospora vitis. The disease is characterized by dark brown to black, angular lesions on the leaves of the grapevine. The lesions can cause the leaves to turn yellow and drop prematurely, which can weaken the plant and reduce fruit production.',
    'Grape___healthy': 'The plant is healthy.',
    'Orange___Haunglongbing_(Citrus_greening)': 'Citrus greening, also known as Huanglongbing (HLB), is a devastating bacterial disease of citrus trees. The disease is caused by the bacterium Candidatus Liberibacter asiaticus, which is transmitted by the Asian citrus psyllid. There is no cure for citrus greening, and infected trees will eventually die.',
    'Peach___Bacterial_spot': 'Bacterial spot is a bacterial disease of peaches, nectarines, apricots, and plums caused by the bacterium Xanthomonas arboricola pv. pruni. The disease causes small, dark lesions on the leaves, fruit, and twigs of the tree. The lesions on the fruit can make it unmarketable.',
    'Peach___healthy': 'The plant is healthy.',
    'Pepper,_bell___Bacterial_spot': 'Bacterial spot of pepper is a common and destructive disease caused by several species of Xanthomonas bacteria. The disease causes lesions on the leaves, stems, and fruit of the pepper plant. The fruit lesions can make the peppers unmarketable.',
    'Pepper,_bell___healthy': 'The plant is healthy.',
    'Potato___Early_blight': 'Early blight of potato is a fungal disease caused by the fungus Alternaria solani. The disease causes dark, circular lesions on the leaves of the potato plant, which can reduce the photosynthetic area of the leaf and lead to yield loss.',
    'Potato___Late_blight': 'Late blight of potato is a devastating disease of potato caused by the oomycete Phytophthora infestans. The disease can cause rapid and complete defoliation of the potato plant, and can also infect the tubers, causing them to rot. Late blight was the cause of the Irish potato famine.',
    'Potato___healthy': 'The plant is healthy.',
    'Raspberry___healthy': 'The plant is healthy.',
    'Soybean___healthy': 'The plant is healthy.',
    'Squash___Powdery_mildew': 'Powdery mildew of squash is a fungal disease caused by the fungus Podosphaera xanthii. The disease is characterized by a white powdery growth on the leaves, stems, and fruit of the squash plant.',
    'Strawberry___Leaf_scorch': 'Leaf scorch of strawberry is a fungal disease caused by the fungus Diplocarpon earlianum. The disease is characterized by small, dark purple spots on the leaves of the strawberry plant. The spots can enlarge and merge, causing the leaves to turn brown and die.',
    'Strawberry___healthy': 'The plant is healthy.',
    'Tomato___Bacterial_spot': 'Bacterial spot of tomato is a bacterial disease caused by several species of Xanthomonas bacteria. The disease causes small, dark, water-soaked lesions on the leaves, stems, and fruit of the tomato plant. The fruit lesions can make the tomatoes unmarketable.',
    'Tomato___Early_blight': 'Early blight of tomato is a fungal disease caused by the fungus Alternaria solani. The disease causes dark, circular lesions on the leaves of the tomato plant, which can reduce the photosynthetic area of the leaf and lead to yield loss.',
    'Tomato___Late_blight': 'Late blight of tomato is a devastating disease of tomato caused by the oomycete Phytophthora infestans. The disease can cause rapid and complete defoliation of the tomato plant, and can also infect the fruit, causing them to rot.',
    'Tomato___Leaf_Mold': 'Leaf mold of tomato is a fungal disease caused by the fungus Passalora fulva. The disease is characterized by yellow spots on the upper surface of the leaves, and a velvety, olive-green mold on the underside of the leaves.',
    'Tomato___Septoria_leaf_spot': 'Septoria leaf spot of tomato is a fungal disease caused by the fungus Septoria lycopersici. The disease is characterized by small, circular spots with dark borders and tan or gray centers on the leaves of the tomato plant.',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'The two-spotted spider mite is a common pest of tomatoes and many other plants. The mites feed on the leaves of the plant, causing them to become stippled and yellow. In severe infestations, the mites can kill the plant.',
    'Tomato___Target_Spot': "Target spot of tomato is a fungal disease caused by the fungus Corynespora cassiicola. The disease is characterized by small, circular lesions with dark borders and tan or gray centers on the leaves of the tomato plant. The lesions can also have a 'target-like' appearance.",
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Tomato yellow leaf curl virus (TYLCV) is a DNA virus from the genus Begomovirus that is transmitted by the silverleaf whitefly, Bemisia tabaci. The virus causes severe stunting of tomato plants, with yellowing and upward curling of the leaves.',
    'Tomato___Tomato_mosaic_virus': 'Tomato mosaic virus (ToMV) is a plant pathogenic virus that can infect tomatoes and other plants. The virus causes a mosaic pattern of light and dark green on the leaves, as well as other symptoms such as stunting and leaf distortion.',
    'Tomato___healthy': 'The plant is healthy.'
}

# Treatment and cure information for each disease
disease_treatments = {
    'Apple___Apple_scab': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing myclobutanil, captan, or mancozeb starting at bud break and continuing every 7-14 days during wet weather.
2. **Pruning**: Remove infected leaves, fruit, and twigs. Prune to improve air circulation.
3. **Sanitation**: Rake and destroy fallen leaves in autumn to reduce overwintering spores.
4. **Resistant Varieties**: Plant scab-resistant apple varieties if possible.
5. **Cultural Practices**: Avoid overhead watering, maintain good tree nutrition, and ensure proper spacing for air flow.""",

    'Apple___Black_rot': """**Treatment Methods:**
1. **Pruning**: Remove all cankers, mummified fruits, and dead wood during dormant season.
2. **Fungicide Sprays**: Apply fungicides like captan or thiophanate-methyl during bloom and pre-harvest periods.
3. **Sanitation**: Collect and destroy all fallen leaves, fruit, and pruned material.
4. **Cultural Control**: Maintain tree vigor through proper fertilization and irrigation. Avoid wounding trees.
5. **Monitoring**: Regularly inspect trees and remove infected parts immediately.""",

    'Apple___Cedar_apple_rust': """**Treatment Methods:**
1. **Remove Alternative Host**: Eliminate nearby juniper/cedar trees within 300 meters if possible.
2. **Fungicide Treatment**: Apply fungicides containing myclobutanil, propiconazole, or mancozeb at bud break and continue every 7-10 days during spring.
3. **Resistant Varieties**: Plant rust-resistant apple varieties.
4. **Pruning**: Remove galled branches from juniper trees if present.
5. **Protective Sprays**: Apply protective fungicide before infections occur during wet spring weather.""",

    'Apple___healthy': """**Prevention Tips:**
- Continue regular monitoring and good cultural practices
- Maintain proper nutrition and watering
- Prune regularly for air circulation
- Remove any diseased plant material promptly""",

    'Blueberry___healthy': """**Prevention Tips:**
- Maintain proper soil pH (4.5-5.5)
- Provide adequate water and drainage
- Apply appropriate fertilizers
- Monitor for pests and diseases regularly""",

    'Cherry_(including_sour)___Powdery_mildew': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing myclobutanil, propiconazole, or sulfur-based products when symptoms first appear.
2. **Pruning**: Remove severely infected branches and improve air circulation through selective pruning.
3. **Water Management**: Avoid overhead irrigation. Water at the base of trees early in the day.
4. **Resistant Varieties**: Choose powdery mildew-resistant cherry varieties when planting.
5. **Cultural Practices**: Ensure adequate spacing between trees and maintain good tree vigor.""",

    'Cherry_(including_sour)___healthy': """**Prevention Tips:**
- Maintain proper pruning and air circulation
- Monitor for pests and diseases
- Provide adequate water and nutrients
- Remove any diseased material promptly""",

    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': """**Treatment Methods:**
1. **Fungicide Application**: Apply fungicides containing azoxystrobin, propiconazole, or pyraclostrobin when disease appears.
2. **Crop Rotation**: Rotate corn with non-host crops for at least 2-3 years.
3. **Tillage**: Plow under corn residue to reduce overwintering inoculum.
4. **Resistant Hybrids**: Plant resistant or tolerant corn hybrids.
5. **Proper Spacing**: Ensure proper plant spacing and avoid excessive nitrogen fertilization.""",

    'Corn_(maize)___Common_rust_': """**Treatment Methods:**
1. **Fungicide Treatment**: Apply fungicides like propiconazole, azoxystrobin, or pyraclostrobin when rust pustules first appear.
2. **Resistant Varieties**: Plant rust-resistant corn hybrids.
3. **Early Planting**: Plant early-maturing varieties to escape peak rust pressure.
4. **Crop Rotation**: Rotate with non-host crops.
5. **Field Sanitation**: Remove and destroy infected plant debris after harvest.""",

    'Corn_(maize)___Northern_Leaf_Blight': """**Treatment Methods:**
1. **Fungicide Application**: Apply fungicides containing propiconazole, azoxystrobin, or pyraclostrobin at tasseling stage.
2. **Resistant Hybrids**: Plant resistant corn varieties.
3. **Crop Rotation**: Rotate with non-host crops for 2-3 years.
4. **Tillage**: Plow under infected crop residue to reduce inoculum.
5. **Planting Density**: Avoid excessive plant populations that increase humidity.""",

    'Corn_(maize)___healthy': """**Prevention Tips:**
- Maintain proper crop rotation
- Use resistant varieties when available
- Monitor fields regularly for early disease detection
- Practice good field sanitation""",

    'Grape___Black_rot': """**Treatment Methods:**
1. **Fungicide Sprays**: Apply fungicides containing mancozeb, captan, or myclobutanil starting at bud break and continuing through fruit development.
2. **Pruning**: Remove and destroy all infected clusters, leaves, and canes.
3. **Sanitation**: Remove all mummified fruit and infected debris from vineyard floor.
4. **Canopy Management**: Improve air circulation through proper pruning and trellising.
5. **Timing**: Critical spray periods are pre-bloom, bloom, and 2-3 weeks after bloom.""",

    'Grape___Esca_(Black_Measles)': """**Treatment Methods:**
1. **Prevention Focus**: There is no cure once vines are infected. Focus on prevention.
2. **Pruning Wound Protection**: Protect pruning wounds with fungicidal paint or paste.
3. **Sanitation**: Remove and destroy severely infected vines.
4. **Proper Pruning**: Avoid large pruning wounds and prune during dry weather.
5. **Vineyard Management**: Maintain vine vigor through proper nutrition and irrigation.
6. **Note**: Infected vines should be removed and replaced with healthy stock.""",

    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing mancozeb, captan, or copper-based products when lesions first appear.
2. **Pruning**: Remove infected leaves and improve canopy air circulation.
3. **Sanitation**: Remove and destroy fallen leaves and infected plant material.
4. **Canopy Management**: Proper trellising and pruning to reduce humidity.
5. **Protective Sprays**: Begin fungicide applications before disease appears in wet seasons.""",

    'Grape___healthy': """**Prevention Tips:**
- Maintain proper canopy management and air circulation
- Monitor for pests and diseases regularly
- Apply preventive fungicides during critical growth stages
- Practice good vineyard sanitation""",

    'Orange___Haunglongbing_(Citrus_greening)': """**Treatment Methods:**
1. **No Cure Available**: There is currently no cure for citrus greening. Focus on management.
2. **Psyllid Control**: Control Asian citrus psyllid vectors with insecticides like imidacloprid or spinetoram.
3. **Remove Infected Trees**: Remove and destroy severely infected trees immediately.
4. **Nutritional Support**: Provide enhanced nutrition and irrigation to maintain tree vigor.
5. **Heat Therapy**: Experimental heat treatment may slow disease progression.
6. **Biological Control**: Use beneficial insects and integrated pest management.
7. **Prevention**: Source clean nursery stock and monitor psyllid populations regularly.
8. **Note**: Early detection and removal of infected trees is critical to prevent spread.""",

    'Peach___Bacterial_spot': """**Treatment Methods:**
1. **Copper-based Fungicides**: Apply copper hydroxide or copper sulfate during dormant season and at bud break.
2. **Antibiotic Sprays**: Use streptomycin or oxytetracycline during bloom (if legal in your area).
3. **Pruning**: Remove and destroy infected branches and twigs.
4. **Sanitation**: Remove fallen leaves and fruit debris.
5. **Resistant Varieties**: Plant bacterial spot-resistant peach varieties.
6. **Cultural Practices**: Avoid overhead irrigation, improve air circulation, and maintain tree vigor.""",

    'Peach___healthy': """**Prevention Tips:**
- Monitor for bacterial and fungal diseases regularly
- Maintain proper pruning and air circulation
- Apply preventive sprays during critical periods
- Remove any diseased material promptly""",

    'Pepper,_bell___Bacterial_spot': """**Treatment Methods:**
1. **Copper-based Bactericides**: Apply copper hydroxide or copper sulfate sprays weekly when conditions favor disease.
2. **Antibiotics**: Use streptomycin or oxytetracycline (if approved) during early disease stages.
3. **Seed Treatment**: Use disease-free seed or treat seeds with hot water or bleach.
4. **Sanitation**: Remove and destroy infected plants and debris.
5. **Resistant Varieties**: Plant resistant pepper varieties when available.
6. **Cultural Control**: Avoid overhead watering, use drip irrigation, and ensure proper spacing.
7. **Crop Rotation**: Rotate with non-host crops for 2-3 years.""",

    'Pepper,_bell___healthy': """**Prevention Tips:**
- Use disease-free seed and transplants
- Practice crop rotation
- Avoid overhead watering
- Monitor for early disease symptoms""",

    'Potato___Early_blight': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing chlorothalonil, mancozeb, or azoxystrobin when first lesions appear.
2. **Crop Rotation**: Rotate with non-host crops for at least 3 years.
3. **Sanitation**: Remove and destroy infected plant debris after harvest.
4. **Proper Spacing**: Ensure adequate plant spacing for air circulation.
5. **Fertilization**: Avoid excessive nitrogen fertilization which increases susceptibility.
6. **Resistant Varieties**: Plant early blight-resistant potato varieties.
7. **Water Management**: Use drip irrigation and avoid wetting foliage.""",

    'Potato___Late_blight': """**Treatment Methods:**
1. **Urgent Fungicide Treatment**: Apply fungicides containing mancozeb, chlorothalonil, or metalaxyl immediately upon detection.
2. **Protective Sprays**: Begin fungicide applications before disease appears in wet weather.
3. **Remove Infected Plants**: Immediately remove and destroy all infected plants and tubers.
4. **Crop Rotation**: Rotate with non-host crops for 3-4 years.
5. **Sanitation**: Destroy all infected plant material and cull tubers before storage.
6. **Resistant Varieties**: Plant late blight-resistant potato varieties.
7. **Monitoring**: Check fields daily during wet weather conditions.
8. **Storage**: Store only healthy tubers and maintain proper storage conditions.""",

    'Potato___healthy': """**Prevention Tips:**
- Practice crop rotation
- Use certified disease-free seed potatoes
- Monitor fields regularly
- Apply preventive fungicides during favorable weather conditions""",

    'Raspberry___healthy': """**Prevention Tips:**
- Maintain proper pruning and spacing
- Monitor for pests and diseases
- Provide adequate water and nutrients
- Remove any diseased canes promptly""",

    'Soybean___healthy': """**Prevention Tips:**
- Practice crop rotation
- Use resistant varieties when available
- Monitor fields regularly for early disease detection
- Maintain proper field sanitation""",

    'Squash___Powdery_mildew': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing myclobutanil, propiconazole, or sulfur when first signs appear.
2. **Organic Options**: Use baking soda solution (1 tbsp per gallon water) or neem oil.
3. **Milk Spray**: Apply milk solution (1 part milk to 9 parts water) as preventive measure.
4. **Pruning**: Remove severely infected leaves to improve air circulation.
5. **Water Management**: Water at soil level, avoid overhead irrigation.
6. **Resistant Varieties**: Plant powdery mildew-resistant squash varieties.
7. **Spacing**: Ensure adequate spacing between plants for air flow.""",

    'Strawberry___Leaf_scorch': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing captan, thiophanate-methyl, or myclobutanil starting in spring.
2. **Sanitation**: Remove and destroy all infected leaves and plant debris.
3. **Renovation**: Renovate beds after harvest by mowing and removing old foliage.
4. **Resistant Varieties**: Plant leaf scorch-resistant strawberry varieties.
5. **Water Management**: Use drip irrigation, avoid overhead watering.
6. **Cultural Practices**: Ensure proper plant spacing and good air circulation.
7. **Mulching**: Use clean straw mulch to prevent soil splash.""",

    'Strawberry___healthy': """**Prevention Tips:**
- Maintain proper bed renovation practices
- Monitor for diseases regularly
- Use drip irrigation
- Remove old leaves and debris after harvest""",

    'Tomato___Bacterial_spot': """**Treatment Methods:**
1. **Copper-based Bactericides**: Apply copper hydroxide or copper sulfate sprays every 7-10 days.
2. **Antibiotics**: Use streptomycin or oxytetracycline during early stages (if approved).
3. **Seed Treatment**: Use disease-free seed or treat with hot water (122°F for 25 minutes).
4. **Sanitation**: Remove and destroy infected plants immediately.
5. **Resistant Varieties**: Plant bacterial spot-resistant tomato varieties.
6. **Cultural Control**: Avoid overhead watering, use drip irrigation, space plants properly.
7. **Crop Rotation**: Rotate with non-host crops for 2-3 years.
8. **Staking**: Stake plants to keep foliage off the ground.""",

    'Tomato___Early_blight': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing chlorothalonil, mancozeb, or azoxystrobin when first lesions appear.
2. **Pruning**: Remove infected lower leaves as they appear.
3. **Sanitation**: Remove and destroy all plant debris after harvest.
4. **Mulching**: Use mulch to prevent soil splash onto leaves.
5. **Staking**: Stake or cage plants to improve air circulation.
6. **Water Management**: Water at soil level, avoid wetting foliage.
7. **Resistant Varieties**: Plant early blight-resistant tomato varieties.
8. **Crop Rotation**: Rotate with non-host crops for 2-3 years.""",

    'Tomato___Late_blight': """**Treatment Methods:**
1. **Immediate Action**: Apply fungicides containing mancozeb, chlorothalonil, or mefenoxam immediately upon detection.
2. **Protective Sprays**: Begin fungicide applications before disease appears in wet, cool weather.
3. **Remove Infected Plants**: Immediately remove and destroy all infected plants.
4. **Sanitation**: Destroy all infected plant material and fruit.
5. **Resistant Varieties**: Plant late blight-resistant tomato varieties.
6. **Water Management**: Use drip irrigation, avoid overhead watering.
7. **Monitoring**: Check plants daily during cool, wet weather.
8. **Prevention**: Apply preventive fungicides when conditions favor disease (cool, humid weather).""",

    'Tomato___Leaf_Mold': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing chlorothalonil, mancozeb, or copper-based products.
2. **Environmental Control**: Reduce humidity by improving ventilation and air circulation.
3. **Pruning**: Remove infected leaves and maintain proper plant spacing.
4. **Water Management**: Avoid overhead irrigation, water early in the day.
5. **Resistant Varieties**: Plant leaf mold-resistant tomato varieties.
6. **Staking**: Stake plants to improve air flow around foliage.
7. **Greenhouse Management**: In greenhouses, maintain humidity below 85% and ensure good ventilation.""",

    'Tomato___Septoria_leaf_spot': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing chlorothalonil, mancozeb, or copper-based products when first spots appear.
2. **Remove Infected Leaves**: Prune and remove infected lower leaves as they appear.
3. **Sanitation**: Remove and destroy all plant debris after harvest.
4. **Mulching**: Use mulch to prevent soil splash.
5. **Water Management**: Water at soil level, avoid overhead irrigation.
6. **Staking**: Stake plants to improve air circulation.
7. **Crop Rotation**: Rotate with non-host crops for 2-3 years.
8. **Spacing**: Ensure adequate spacing between plants.""",

    'Tomato___Spider_mites Two-spotted_spider_mite': """**Treatment Methods:**
1. **Miticide Applications**: Apply miticides containing abamectin, spiromesifen, or bifenazate.
2. **Natural Predators**: Introduce beneficial insects like Phytoseiulus persimilis or Neoseiulus californicus.
3. **Water Spray**: Use strong water sprays to dislodge mites from leaves.
4. **Neem Oil**: Apply neem oil or insecticidal soap weekly.
5. **Horticultural Oil**: Apply horticultural oils during dormant or early season.
6. **Remove Infected Leaves**: Prune and destroy severely infested leaves.
7. **Weed Control**: Remove weeds that can host spider mites.
8. **Monitoring**: Regularly check undersides of leaves for mites and webbing.
9. **Prevention**: Maintain adequate plant moisture and avoid water stress.""",

    'Tomato___Target_Spot': """**Treatment Methods:**
1. **Fungicide Applications**: Apply fungicides containing azoxystrobin, chlorothalonil, or mancozeb when first lesions appear.
2. **Pruning**: Remove infected leaves to reduce inoculum.
3. **Sanitation**: Remove and destroy all plant debris after harvest.
4. **Water Management**: Use drip irrigation, avoid overhead watering.
5. **Staking**: Stake plants to improve air circulation.
6. **Crop Rotation**: Rotate with non-host crops for 2-3 years.
7. **Resistant Varieties**: Plant target spot-resistant tomato varieties when available.
8. **Spacing**: Ensure adequate plant spacing for air flow.""",

    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': """**Treatment Methods:**
1. **No Direct Cure**: There is no cure for infected plants. Focus on prevention and management.
2. **Whitefly Control**: Control silverleaf whitefly vectors with insecticides like imidacloprid, thiamethoxam, or pyriproxyfen.
3. **Remove Infected Plants**: Immediately remove and destroy infected plants to prevent spread.
4. **Resistant Varieties**: Plant TYLCV-resistant tomato varieties.
5. **Physical Barriers**: Use fine mesh screens or row covers to exclude whiteflies.
6. **Yellow Sticky Traps**: Use yellow sticky traps to monitor and reduce whitefly populations.
7. **Reflective Mulch**: Use silver or aluminum reflective mulch to repel whiteflies.
8. **Biological Control**: Introduce beneficial insects that prey on whiteflies.
9. **Early Detection**: Monitor plants regularly and remove infected plants immediately.""",

    'Tomato___Tomato_mosaic_virus': """**Treatment Methods:**
1. **No Cure Available**: There is no cure for infected plants. Focus on prevention.
2. **Remove Infected Plants**: Immediately remove and destroy infected plants.
3. **Seed Treatment**: Use virus-free certified seed or treat seeds with 10% trisodium phosphate.
4. **Sanitation**: Disinfect tools, hands, and equipment between plants.
5. **Resistant Varieties**: Plant ToMV-resistant tomato varieties.
6. **Weed Control**: Remove weeds that may serve as virus reservoirs.
7. **Avoid Smoking**: Tobacco mosaic virus can spread through contact, avoid handling plants after smoking.
8. **Crop Rotation**: Rotate with non-host crops.
9. **Early Detection**: Monitor regularly and remove infected plants immediately to prevent spread.""",

    'Tomato___healthy': """**Prevention Tips:**
- Continue regular monitoring and good cultural practices
- Maintain proper nutrition and watering
- Apply preventive fungicides during critical periods
- Remove any diseased plant material promptly
- Practice crop rotation
- Use disease-resistant varieties when available"""
}

# KHASYAPIX Main Page
if app_mode == "HOME":
    st.markdown("""
    <div class="khasyapix-header">
        <h1 class="khasyapix-logo">KHASYAPIX</h1>
        <p class="khasyapix-tagline">🔬 AI-Powered Plant Disease Detection</p>
        <p class="khasyapix-subtitle">Advanced Neural Network Technology for Sustainable Agriculture</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="color: var(--primary-color); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(0, 255, 136, 0.3);">🔬 AI-Powered Detection</h3>
            <p style="color: var(--text-secondary); line-height: 1.6;">KHASYAPIX uses advanced neural networks to identify 38 different plant diseases with 95%+ accuracy, revolutionizing agricultural diagnostics.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="color: var(--accent-color); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(0, 212, 255, 0.3);">🌍 Sustainable Agriculture</h3>
            <p style="color: var(--text-secondary); line-height: 1.6;">Supporting eco-friendly farming practices through early disease detection, reducing crop losses by 40% and minimizing chemical usage.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3 style="color: var(--secondary-color); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(255, 0, 128, 0.3);">📱 Instant Analysis</h3>
            <p style="color: var(--text-secondary); line-height: 1.6;">Upload a plant leaf image and receive instant AI-powered disease diagnosis with detailed treatment recommendations and prevention strategies.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Supported plants section
    st.markdown("""
    <div class="card">
        <h3 style="color: var(--primary-color); margin-top: 0;">🌿 Supported Plants</h3>
        <p>Our system can detect diseases in the following plants:</p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div>🍎 Apple</div>
            <div>🫐 Blueberry</div>
            <div>🍒 Cherry</div>
            <div>🌽 Corn</div>
            <div>🍇 Grape</div>
            <div>🍊 Orange</div>
            <div>🍑 Peach</div>
            <div>🫑 Pepper</div>
            <div>🥔 Potato</div>
            <div>🍓 Raspberry</div>
            <div>🫘 Soybean</div>
            <div>🎃 Squash</div>
            <div>🍓 Strawberry</div>
            <div>🍅 Tomato</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# KHASYAPIX Prediction Page
elif app_mode == "DISEASE RECOGNITION":
    st.markdown("""
    <div class="khasyapix-header">
        <h1 class="khasyapix-logo" style="font-size: 3rem;">🔍 KHASYAPIX</h1>
        <p class="khasyapix-tagline">Neural Network Disease Recognition</p>
        <p class="khasyapix-subtitle">Upload a plant leaf image for instant AI-powered diagnosis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KHASYAPIX Disease Recognition - Organized Layout
    st.markdown("""
    <div class="card" style="margin-bottom: 2rem;">
        <h3 style="color: var(--primary-color); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(0, 255, 136, 0.3);">📸 Step 1: Upload Plant Image</h3>
        <p style="color: var(--text-secondary); line-height: 1.6;">Choose a high-quality image of a plant leaf for KHASYAPIX neural network analysis. Supported formats: JPG, PNG, JPEG</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input method selection
    input_method = st.radio(
        "Select Input Method:",
        ("Upload Image", "Take Photo"),
        horizontal=True
    )

    test_image = None

    if input_method == "Upload Image":
        # Image upload section
        test_image = st.file_uploader(
            "Choose an Image:",
            type=['jpg', 'jpeg', 'png'],
            help="Upload a clear image of a plant leaf for KHASYAPIX analysis"
        )
    else:
        # Camera input section
        test_image = st.camera_input("Take a photo")
    
    # Show uploaded image
    if test_image is not None:
        st.markdown("""
        <div class="card" style="margin: 1rem 0;">
            <h3 style="color: var(--accent-color); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(0, 212, 255, 0.3);">🖼️ Image Preview</h3>
        </div>
        """, unsafe_allow_html=True)
        st.image(test_image, use_container_width=True)
    
    # Analysis section
    st.markdown("""
    <div class="card" style="margin: 2rem 0;">
        <h3 style="color: var(--secondary-color); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(255, 0, 128, 0.3);">🔬 Step 2: KHASYAPIX Analysis</h3>
        <p style="color: var(--text-secondary); line-height: 1.6;">Click the analyze button to activate KHASYAPIX neural network and receive instant disease diagnosis with detailed analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Predict button with loading state
    if st.button("🔍 ANALYZE WITH KHASYAPIX", key="predict"):
        if test_image is not None:
            # Create a placeholder for loading animation
            loading_placeholder = st.empty()
            
            with loading_placeholder.container():
                # Add KHASYAPIX loading animation
                st.markdown("""
                <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); border: 2px solid var(--primary-color); border-radius: var(--border-radius); box-shadow: var(--shadow);">
                    <div class="loading-spinner" style="width: 40px; height: 40px; border: 4px solid rgba(0, 255, 136, 0.3); border-top-color: var(--primary-color); margin: 0 auto 1rem;"></div>
                    <h3 style="color: var(--primary-color); font-family: 'Exo 2', sans-serif; margin: 0;">🔬 KHASYAPIX Processing</h3>
                    <p style="color: var(--accent-color); margin: 0.5rem 0 0 0;">Neural network analyzing plant disease patterns...</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Check if it's a plant image first
            # Reset pointer
            test_image.seek(0)
            is_plant, detected = is_plant_image(test_image)
            
            if not is_plant:
                # Clear loading animation
                loading_placeholder.empty()
                
                st.markdown("""
                <div class="card" style="margin: 2rem 0;">
                    <h3 style="color: var(--neon-purple); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(139, 92, 246, 0.3);">📊 Step 3: KHASYAPIX Results</h3>
                    <p style="color: var(--text-secondary); line-height: 1.6;">Image Analysis Complete.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="prediction-result" style="background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); border: 3px solid var(--neon-orange); border-radius: var(--border-radius); padding: 2.5rem; margin: 2rem 0; box-shadow: var(--shadow-hover), 0 0 20px rgba(255, 107, 53, 0.3); animation: slideInUp 1s ease-out;">
                    <h3 style="color: var(--neon-orange); margin-bottom: 1.5rem; font-size: 2rem; font-family: 'Orbitron', monospace; text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);">⚠️ NON-PLANT DETECTED</h3>
                    <p style="color: var(--accent-color); font-size: 1.3rem; font-weight: 600; margin: 0 0 1rem 0;"><strong>Status:</strong> Invalid Image Type</p>
                    <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.8; margin: 0;">Our intelligent gatekeeper system has detected that this image is likely not a plant leaf.</p>
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                        <p style="color: var(--text-secondary); margin: 0;"><strong>Detected Objects:</strong> {', '.join(detected[:3])}</p>
                    </div>
                    <ul style="color: var(--text-secondary); font-size: 1rem; line-height: 2; margin: 1rem 0 0 2rem;">
                        <li>Please upload a clear image of a plant leaf</li>
                        <li>Avoid images of people, animals, buildings, or other objects</li>
                        <li>Ensure the plant is the main subject of the photo</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                # We stop here
            else:
                # Reset pointer again for the next prediction model
                test_image.seek(0)
                
                # Perform prediction
                result_index, confidence = model_prediction(test_image)
                
                # Clear loading animation immediately after prediction
                loading_placeholder.empty()
                
                if result_index is not None:
                    # Check confidence threshold
                    if confidence < 0.3:
                        # Low confidence - likely not in dataset
                        st.markdown("""
                        <div class="card" style="margin: 2rem 0;">
                            <h3 style="color: var(--neon-purple); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(139, 92, 246, 0.3);">📊 Step 3: KHASYAPIX Results</h3>
                            <p style="color: var(--text-secondary); line-height: 1.6;">Neural network analysis complete.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class="prediction-result" style="background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); border: 3px solid var(--neon-orange); border-radius: var(--border-radius); padding: 2.5rem; margin: 2rem 0; box-shadow: var(--shadow-hover), 0 0 20px rgba(255, 107, 53, 0.3); animation: slideInUp 1s ease-out;">
                            <h3 style="color: var(--neon-orange); margin-bottom: 1.5rem; font-size: 2rem; font-family: 'Orbitron', monospace; text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);">⚠️ UNRECOGNIZED DISEASE</h3>
                            <p style="color: var(--accent-color); font-size: 1.3rem; font-weight: 600; margin: 0 0 1rem 0;"><strong>Status:</strong> Disease Not Found in Database</p>
                            <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.8; margin: 0;">The uploaded image does not match any known disease in our database with high confidence.</p>
                            <ul style="color: var(--text-secondary); font-size: 1rem; line-height: 2; margin: 1rem 0 0 2rem;">
                                <li>The image may not be of a plant leaf</li>
                                <li>The disease is not currently in our detection system</li>
                                <li>The image quality may be insufficient for accurate detection</li>
                                <li>The plant species is not supported</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.warning("⚠️ The predicted disease does not exist in our database. Please ensure you upload a clear image of a plant leaf from a supported species.")

                # Validate that result_index is within valid range
                    # Validate that result_index is within valid range
                    elif result_index < 0 or result_index >= len(class_name):
                        # Invalid index - disease doesn't exist
                        st.markdown("""
                        <div class="card" style="margin: 2rem 0;">
                            <h3 style="color: var(--neon-purple); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(139, 92, 246, 0.3);">📊 Step 3: KHASYAPIX Results</h3>
                            <p style="color: var(--text-secondary); line-height: 1.6;">Neural network analysis complete.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("""
                        <div class="prediction-result" style="background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); border: 3px solid var(--neon-orange); border-radius: var(--border-radius); padding: 2.5rem; margin: 2rem 0; box-shadow: var(--shadow-hover), 0 0 20px rgba(255, 107, 53, 0.3); animation: slideInUp 1s ease-out;">
                            <h3 style="color: var(--neon-orange); margin-bottom: 1.5rem; font-size: 2rem; font-family: 'Orbitron', monospace; text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);">⚠️ UNRECOGNIZED DISEASE</h3>
                            <p style="color: var(--accent-color); font-size: 1.3rem; font-weight: 600; margin: 0 0 1rem 0;"><strong>Status:</strong> Disease Not Found in Database</p>
                            <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.8; margin: 0;">The uploaded image does not match any known disease in our database. This could mean:</p>
                            <ul style="color: var(--text-secondary); font-size: 1rem; line-height: 2; margin: 1rem 0 0 2rem;">
                                <li>The image may not be of a plant leaf</li>
                                <li>The disease is not currently in our detection system</li>
                                <li>The image quality may be insufficient for accurate detection</li>
                                <li>The plant species is not supported</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.warning("⚠️ The predicted disease does not exist in our database. Please ensure you upload a clear image of a plant leaf from a supported species.")
                        
                    else:
                        # Get disease name
                        disease_name = class_name[result_index]
                        
                        # Check if disease exists in our dictionaries
                        if disease_name not in disease_descriptions:
                            # Disease index is valid but not in our description database
                            st.markdown("""
                            <div class="card" style="margin: 2rem 0;">
                                <h3 style="color: var(--neon-purple); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(139, 92, 246, 0.3);">📊 Step 3: KHASYAPIX Results</h3>
                                <p style="color: var(--text-secondary); line-height: 1.6;">Neural network analysis complete.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                            <div class="prediction-result" style="background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); border: 3px solid var(--neon-orange); border-radius: var(--border-radius); padding: 2.5rem; margin: 2rem 0; box-shadow: var(--shadow-hover), 0 0 20px rgba(255, 107, 53, 0.3); animation: slideInUp 1s ease-out;">
                                <h3 style="color: var(--neon-orange); margin-bottom: 1.5rem; font-size: 2rem; font-family: 'Orbitron', monospace; text-shadow: 0 0 20px rgba(255, 107, 53, 0.5);">⚠️ UNRECOGNIZED DISEASE</h3>
                                <p style="color: var(--accent-color); font-size: 1.3rem; font-weight: 600; margin: 0 0 1rem 0;"><strong>Predicted:</strong> {disease_name.replace('___', ' - ')}</p>
                                <p style="color: var(--text-secondary); font-size: 1.1rem; line-height: 1.8; margin: 0;">This disease is not currently in our database. Detailed information and treatment recommendations are not available.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.warning(f"⚠️ The disease '{disease_name.replace('___', ' - ')}' does not exist in our database. Please contact support or try with a different image.")
                        else:
                            # Valid disease - display results
                            # Results section header
                            st.markdown("""
                            <div class="card" style="margin: 2rem 0;">
                                <h3 style="color: var(--neon-purple); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(139, 92, 246, 0.3);">📊 Step 3: KHASYAPIX Results</h3>
                                <p style="color: var(--text-secondary); line-height: 1.6;">Neural network analysis complete. Review the diagnosis and detailed information below.</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Display KHASYAPIX results
                            st.markdown(f"""
                            <div class="prediction-result" style="background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); border: 3px solid var(--primary-color); border-radius: var(--border-radius); padding: 2.5rem; margin: 2rem 0; box-shadow: var(--shadow-hover), var(--shadow-purple); animation: slideInUp 1s ease-out;">
                                <h3 style="color: var(--primary-color); margin-bottom: 1.5rem; font-size: 2rem; font-family: 'Orbitron', monospace; text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);">🎯 KHASYAPIX DIAGNOSIS</h3>
                                <p style="color: var(--accent-color); font-size: 1.3rem; font-weight: 600; margin: 0;"><strong>Disease Identified:</strong> {disease_name.replace('___', ' - ')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Disease description
                            st.markdown(f"""
                            <div class="card">
                                <h3 style="color: var(--accent-color); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(0, 212, 255, 0.3);">📋 Disease Analysis Report</h3>
                                <p style="color: var(--text-secondary); line-height: 1.8; font-size: 1.1rem;">{disease_descriptions[disease_name]}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Treatment and cure information
                            if disease_name in disease_treatments:
                                st.markdown("""
                                <div style="background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary)); border: 2px solid var(--neon-green); border-radius: var(--border-radius); padding: 2rem; margin: 2rem 0; box-shadow: var(--shadow), 0 0 20px rgba(57, 255, 20, 0.2);">
                                    <h3 style="color: var(--neon-green); margin-top: 0; margin-bottom: 1.5rem; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(57, 255, 20, 0.3); font-size: 1.5rem;">💊 Treatment & Cure Recommendations</h3>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Display treatment information with proper markdown formatting
                                treatment_text = disease_treatments[disease_name]
                                
                                # Parse and display treatments as styled steps
                                steps = []
                                lines = treatment_text.split('\n')
                                current_step = ""
                                
                                for line in lines:
                                    line = line.strip()
                                    if not line:
                                        continue
                                        
                                    # Check if line starts with a number (e.g., "1. ", "2. ")
                                    if len(line) > 2 and line[0].isdigit() and line[1] == '.':
                                        if current_step:
                                            steps.append(current_step)
                                        current_step = line
                                    elif len(line) > 3 and line[0].isdigit() and line[1].isdigit() and line[2] == '.': # Handle 10. etc
                                         if current_step:
                                            steps.append(current_step)
                                         current_step = line
                                    else:
                                        # Append to current step or keep as header/intro
                                        if current_step:
                                            current_step += " " + line
                                        elif "**Treatment Methods:**" in line:
                                            continue # Skip the header as we have our own
                                        else:
                                            # Likely prevention tips or unnumbered list
                                            if line.startswith('- '):
                                                 steps.append(line)
                                            else:
                                                 steps.append(line)
                                
                                if current_step:
                                    steps.append(current_step)
                                    
                                # Render steps
                                for i, step in enumerate(steps):
                                    # Extract number if present
                                    step_content = step
                                    step_num = ""
                                    
                                    if step[0].isdigit():
                                        parts = step.split('.', 1)
                                        if len(parts) > 1:
                                            step_num = parts[0]
                                            step_content = parts[1].strip()
                                            
                                            # Bold the title if it exists (e.g. **Fungicide Applications**:)
                                            if "**" in step_content:
                                                step_content = step_content.replace("**", "<span style='color: var(--accent-color); font-weight: 700;'>", 1).replace("**", "</span>", 1)
                                    
                                    if step_num:
                                        st.markdown(f"""
                                        <div class="treatment-step">
                                            <span class="step-number">STEP {step_num}</span>
                                            <div class="step-content">{step_content}</div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        # For bullet points or other text
                                        clean_content = step.replace('- ', '', 1) if step.startswith('- ') else step
                                        st.markdown(f"""
                                        <div class="treatment-step" style="border-left-color: var(--accent-color);">
                                            <div class="step-content">
                                                <span style="color: var(--accent-color); margin-right: 10px;">➤</span>
                                                {clean_content}
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            # Success message
                            st.success(f"🔬 KHASYAPIX Neural Network Prediction: {disease_name.replace('___', ' - ')}")
                else:
                    st.error("❌ KHASYAPIX failed to process the image. Please try again with a different image.")
        else:
            st.warning("⚠️ Please upload an image first for KHASYAPIX analysis!")
    
    # Add some spacing
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # KHASYAPIX Tips section
    st.markdown("""
    <div class="card">
        <h3 style="color: var(--primary-color); margin-top: 0; font-family: 'Exo 2', sans-serif; font-weight: 700; text-shadow: 0 0 15px rgba(0, 255, 136, 0.3);">💡 KHASYAPIX Optimization Tips</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem;">
            <div style="background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary)); padding: 1.5rem; border-radius: var(--border-radius); border: 1px solid var(--accent-color);">
                <h4 style="color: var(--accent-color); margin-top: 0; font-family: 'Exo 2', sans-serif;">📷 Image Quality</h4>
                <p style="color: var(--text-secondary); line-height: 1.6;">Use high-resolution, well-lit images with excellent contrast between the leaf and background for optimal KHASYAPIX analysis.</p>
            </div>
            <div style="background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary)); padding: 1.5rem; border-radius: var(--border-radius); border: 1px solid var(--secondary-color);">
                <h4 style="color: var(--secondary-color); margin-top: 0; font-family: 'Exo 2', sans-serif;">🍃 Leaf Focus</h4>
                <p style="color: var(--text-secondary); line-height: 1.6;">Ensure the leaf is the primary subject, covering 70%+ of the frame for maximum neural network accuracy.</p>
            </div>
            <div style="background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary)); padding: 1.5rem; border-radius: var(--border-radius); border: 1px solid var(--neon-purple);">
                <h4 style="color: var(--neon-purple); margin-top: 0; font-family: 'Exo 2', sans-serif;">🔍 Detail Level</h4>
                <p style="color: var(--text-secondary); line-height: 1.6;">Include visible disease symptoms, spots, or discoloration for KHASYAPIX to provide accurate diagnosis.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
