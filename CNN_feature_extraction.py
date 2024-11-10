from PIL import Image
import torch
import torchvision.models as models
from torchvision import transforms
from torchvision.models import resnet50, ResNet50_Weights

def create_img_vector(img_path):
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

    image = Image.open(img_path).convert('RGB')
    
    # return the tensor, unqueeze(0) indicates that there is one image being returned
    img_tensor = transform(image).unsqueeze(0)
    # tensor is like vector but allows machine learning models to efficiently represent and use data
    
    
    # turn off gradient tracking, a computationally intense resnet50 feature that is not necessary for our task
    torch.set_grad_enabled(False)
    # returns a tensor containing the singular feature vector in the last convolutional layer of the model
    features = resnet50(img_tensor)
    # turn gradient tracking back on
    torch.set_grad_enabled(True)
    # returns a tensor containing the singular feature vector in the last convolutional layer of the model
    return features.squeeze()  # Remove the indication that you are returning a single vector from the tensor
    