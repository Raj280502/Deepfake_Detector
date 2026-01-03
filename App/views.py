# views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from .inference import DeepFakeDetector
from .models import DetectionHistory
from PIL import Image
import cv2
import torch
import torchvision.transforms as transforms
import tempfile
import os
import time

# Load model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, "best_xception_model.pth")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
deepfake_detector = DeepFakeDetector(model_path, device)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


def home(request):
    """Home page view"""
    return render(request, 'home.html')


def detect(request):
    """Main detection view for both video and image"""
    if request.method == 'POST':
        start_time = time.time()
        media_type = request.POST.get('media_type', 'video')
        
        if media_type == 'video' and 'video' in request.FILES:
            return process_video(request, start_time)
        elif media_type == 'image' and 'image' in request.FILES:
            return process_image(request, start_time)
        else:
            return render(request, 'detect.html', {
                'error': 'No file uploaded. Please select a video or image.'
            })
    
    return render(request, 'detect.html')


def process_video(request, start_time):
    """Process uploaded video for deepfake detection"""
    video_file = request.FILES['video']
    file_name = video_file.name
    file_size = video_file.size
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        for chunk in video_file.chunks():
            temp_file.write(chunk)
        video_path = temp_file.name

    try:
        # Process video: extract 1 frame/second, predict
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        interval = int(fps)
        predictions = []
        frame_predictions = []
        count = 0
        frame_num = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if count % interval == 0:
                pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                img_tensor = transform(pil_image)
                prob = deepfake_detector.predict_frame(img_tensor)
                predictions.append(prob)
                frame_predictions.append({
                    'frame': frame_num,
                    'probability': round(prob * 100, 2)
                })
                frame_num += 1
            count += 1
        cap.release()
        
        avg_prob = sum(predictions) / len(predictions) if predictions else 0
        label = 'Fake' if avg_prob > 0.5 else 'Real'
        confidence = round(avg_prob * 100, 2) if label == 'Fake' else round((1 - avg_prob) * 100, 2)
        
        processing_time = time.time() - start_time
        
        # Save to history
        DetectionHistory.objects.create(
            file_name=file_name,
            media_type='video',
            result=label,
            confidence=confidence,
            frames_analyzed=len(predictions),
            processing_time=processing_time,
            file_size=file_size,
            frame_predictions=frame_predictions
        )

        return render(request, 'detect.html', {
            'result': label,
            'confidence': confidence,
            'frames_analyzed': len(predictions),
            'processing_time': f"{processing_time:.1f}s"
        })

    finally:
        os.unlink(video_path)


def process_image(request, start_time):
    """Process uploaded image for deepfake detection"""
    image_file = request.FILES['image']
    file_name = image_file.name
    file_size = image_file.size
    
    try:
        # Load and process image
        pil_image = Image.open(image_file).convert('RGB')
        img_tensor = transform(pil_image)
        prob = deepfake_detector.predict_frame(img_tensor)
        
        label = 'Fake' if prob > 0.5 else 'Real'
        confidence = round(prob * 100, 2) if label == 'Fake' else round((1 - prob) * 100, 2)
        
        processing_time = time.time() - start_time
        
        # Save to history
        DetectionHistory.objects.create(
            file_name=file_name,
            media_type='image',
            result=label,
            confidence=confidence,
            frames_analyzed=1,
            processing_time=processing_time,
            file_size=file_size
        )

        return render(request, 'detect.html', {
            'result': label,
            'confidence': confidence,
            'frames_analyzed': 1,
            'processing_time': f"{processing_time * 1000:.0f}ms"
        })

    except Exception as e:
        return render(request, 'detect.html', {
            'error': f'Error processing image: {str(e)}'
        })


def history(request):
    """View detection history with pagination and stats"""
    history_list = DetectionHistory.objects.all()
    
    # Calculate statistics
    stats = history_list.aggregate(
        total_scans=Count('id'),
        real_count=Count('id', filter=Q(result='Real')),
        fake_count=Count('id', filter=Q(result='Fake')),
        avg_confidence=Avg('confidence')
    )
    
    # Pagination
    paginator = Paginator(history_list, 10)
    page_number = request.GET.get('page')
    history = paginator.get_page(page_number)
    
    return render(request, 'history.html', {
        'history': history,
        'total_scans': stats['total_scans'],
        'real_count': stats['real_count'],
        'fake_count': stats['fake_count'],
        'avg_confidence': round(stats['avg_confidence'] or 0, 1)
    })


def delete_history(request, pk):
    """Delete a history record"""
    if request.method == 'POST':
        try:
            record = DetectionHistory.objects.get(pk=pk)
            record.delete()
            return JsonResponse({'success': True})
        except DetectionHistory.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Record not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def about(request):
    """About page view"""
    return render(request, 'about.html')


# Keep the old view for backward compatibility
def upload_video(request):
    """Legacy view - redirects to new detect view"""
    return redirect('detect')
