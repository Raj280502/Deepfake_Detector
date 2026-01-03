# detection/inference.py

import torch
import timm

class DeepFakeDetector:
    def __init__(self, model_path, device='cpu'):
        self.device = torch.device(device)
        self.model = timm.create_model('xception', pretrained=False, num_classes=1)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        
    def predict_frame(self, frame_tensor):
        """Infer probability that a frame is a deepfake."""
        with torch.no_grad():
            frame_tensor = frame_tensor.unsqueeze(0).to(self.device)
            output = self.model(frame_tensor)
            prob = torch.sigmoid(output).item()
        return prob
