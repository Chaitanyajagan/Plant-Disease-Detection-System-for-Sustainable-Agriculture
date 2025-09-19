import streamlit as st
import tensorflow as tf
import numpy as np
def model_prediction(test_image):
    model = tf.keras.models.load_model("trained_plant_disease_model.keras")
    image = tf.keras.preprocessing.image.load_img(test_image,target_size=(128,128))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr]) #convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions) #return index of max element

#Sidebar
st.sidebar.title("Plant Disease Detection System for Sustainable Agriculture")
app_mode = st.sidebar.selectbox("Select Page",["HOME","DISEASE RECOGNITION"])
#app_mode = st.sidebar.selectbox("Select Page",["Home"," ","Disease Recognition"])

# import Image from pillow to open images
from PIL import Image
img = Image.open("Diseases.png")

# display image using streamlit
# width is used to set the width of an image
st.image(img)

#Main Page
if(app_mode=="HOME"):
    st.markdown("<h1 style='text-align: center;'>Plant Disease Detection System for Sustainable Agriculture", unsafe_allow_html=True)
    
#Prediction Page
elif(app_mode=="DISEASE RECOGNITION"):
    st.header("Plant Disease Detection System for Sustainable Agriculture")
    test_image = st.file_uploader("Choose an Image:")
    if(st.button("Show Image")):
        st.image(test_image,width=4,use_column_width=True)
    #Predict button
    if(st.button("Predict")):
        st.write("Our Prediction")
        result_index = model_prediction(test_image)
        #Reading Labels
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
        st.success("Model is Predicting it's a {}".format(class_name[result_index]))
        st.write(disease_descriptions[class_name[result_index]])
