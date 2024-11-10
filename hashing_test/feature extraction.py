from PIL import Image
import torch
import torchvision.models as models
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights
from scipy.spatial.distance import cosine
import os



# Load ResNet-50 with pre-trained weights
resnet50 = models.resnet50(weights=ResNet50_Weights.DEFAULT)

# a list of all the layers in the model except the final layer that is 
# responsible for classification
layers = list(resnet50.children())[:-1]

resnet50 = torch.nn.Sequential(*layers)

# Switch to evaluation mode
resnet50.eval()

# images must be transformed into certain format for the model to use
# code taken from documentation and stackoverflow
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def transform_image(path):
    image = Image.open(path).convert('RGB')

    # return the tensor, unqueeze(0) indicates that there is one image being returned
    return transform(image).unsqueeze(0)
# tensor is like vector but allows machine learning models to efficiently represent and use data

def extract_features(image_tensor):
    # turn off gradient tracking, a computationally intense resnet50 feature that is not necessary for our task
    # torch.set_grad_enabled(False)
    # returns a tensor containing the singular feature vector in the last convolutional layer of the model
    features = resnet50(image_tensor)
    # turn gradient tracking back on
    # torch.set_grad_enabled(True)
    # returns a tensor containing the singular feature vector in the last convolutional layer of the model
    return features.squeeze()  # Remove the indication that you are returning a single vector from the tensor

# we are storing our feature vectors in a list, for future larger implementation, a numpy or pandas
# database would prevent bottlenecks from iterating through the list

def load_vectors(vector_list, folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)  # Get full file path
        
        vector_list.append(extract_features(transform_image(file_path)))

def find_closest_match(query_image_path, feature_list):
    # Extract features from the query image
    query_features = extract_features(query_image_path).numpy()

    # Compute cosine similarity with each feature vector in the list
    similarities = [1 - cosine(query_features, features) for features in feature_list]

    # Sort by similarity (highest similarity first)
    sorted_similarities = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
    
    return sorted_similarities  # Return the list of similarities and their positions



test_list = []

load_vectors(test_list, "C:/Users/preme/OneDrive/Documents/vscode/hacked/hashing_test/test_cat_images")

matches = find_closest_match("C:/Users/preme/OneDrive/Documents/vscode/hacked/hashing_test/test_cat_images/cat - Copy.jpg", test_list)

print(matches)

