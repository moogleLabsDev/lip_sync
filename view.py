from django.shortcuts import render
from django.http import HttpResponse
import tempfile
import torch
from diffusers import AutoPipelineForImage2Image, AutoPipelineForText2Image, DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import load_image, make_image_grid, export_to_video
from elevenlabs import generate, play, VoiceDesign, Gender, Age, Accent, set_api_key
from pydub.utils import mediainfo
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import subprocess
from django.http import JsonResponse ,StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from inference import main
import gc
from django.http import FileResponse
from sldl.video import VideoSR
import mimetypes
from wsgiref.util import FileWrapper 
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:2048"
set_api_key('sample api key that will be load from .env')


def gen_audio(script):
    audio = generate(
        text=script,
        voice="Clyde",
        model='eleven_monolingual_v1'
    ) #Rachel
    return audio
     
@csrf_exempt
def Main(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        audio = request.FILES.get("audio")
        script = request.POST.get("script")
        result_path = 'Wav2Lip/results/result_video.mp4'
        try:
            if image:
                print("image uploaded")
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    for chunk in image.chunks():
                        temp_file.write(chunk)
                    temp_file.close()
                init_image = load_image(temp_file.name)
                temp_image_path =temp_file.name
                # image.save(temp_image_path)
                image = cv2.imread(temp_image_path)
                torch.cuda.empty_cache()
                if audio == None and script !='':
                    audio = gen_audio(script)
                    specific_path = 'Wav2Lip/media/audio.wav'
                    with open(specific_path, 'wb') as f:
                        f.write(audio)
                    audio_info = mediainfo(specific_path)
                    duration_str = audio_info['duration']
                    duration_ms = float(duration_str) * 1000  # Convert seconds to milliseconds
                    duration_seconds = duration_ms / 1000  # Convert milliseconds to seconds
                    rounded_duration = round(duration_seconds)
                    image = cv2.imread(temp_image_path)
                    video_duration = rounded_duration
                    fps = 30
                    output_folder_name = 'Wav2Lip/media'
                    output_folder = os.path.join(os.getcwd(), output_folder_name)
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    output_video_path = os.path.join(output_folder, 'output.mp4')
                    video_writer = cv2.VideoWriter(output_video_path,
                                            cv2.VideoWriter_fourcc(*'mp4v'),
                                            fps,
                                            (image.shape[1], image.shape[0]))
                    for i in range(video_duration * fps):
                        video_writer.write(image)
                    video_writer.release()
                    main()
                    if os.path.exists(result_path):
                        try:
                            mime_type, _ = mimetypes.guess_type(result_path)
                            response = StreamingHttpResponse(FileWrapper(open(result_path, 'rb')), content_type=mime_type)
                            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(result_path)}"'
                            return response
                        except Exception as e:
                            return JsonResponse({'error': str(e)}, status=500)
                    else:
                        return JsonResponse({'error': 'File not found'}, status=404)
                   
                elif script == '' and audio != None:
                    audiofilename = 'audio.wav'
                    file_path = 'Wav2Lip/media/' + audiofilename
                    with open(file_path, 'wb+') as destination:
                        for chunk in audio.chunks():
                            destination.write(chunk)
                    audio_info = mediainfo(file_path)
                    duration_str = audio_info['duration']
                    duration_ms = float(duration_str) * 1000  # Convert seconds to milliseconds
                    duration_seconds = duration_ms / 1000  # Convert milliseconds to seconds
                    rounded_duration = round(duration_seconds)
                    image = cv2.imread(temp_image_path)
                    video_duration = rounded_duration
                    fps = 30
                    output_folder_name = 'Wav2Lip/media'
                    output_folder = os.path.join(os.getcwd(), output_folder_name)
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    output_video_path = os.path.join(output_folder, 'output.mp4')
                    video_writer = cv2.VideoWriter(output_video_path,
                                                cv2.VideoWriter_fourcc(*'mp4v'),
                                                fps,
                                                (image.shape[1], image.shape[0]))
                    for i in range(video_duration * fps):
                        video_writer.write(image)
                    video_writer.release()
                    cv2.destroyAllWindows()
                    main()
                    if os.path.exists(result_path):
                        try:
                            mime_type, _ = mimetypes.guess_type(result_path)
                            response = StreamingHttpResponse(FileWrapper(open(result_path, 'rb')), content_type=mime_type)
                            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(result_path)}"'
                            return response
                        except Exception as e:
                            return JsonResponse({'error': str(e)}, status=500)
                    else:
                        return JsonResponse({'error': 'File not found'}, status=404)
                    
                elif audio != None and script !='':
                    return JsonResponse({'message': 'Please upload only one (Audio or Script). failed'}, status=400)
                else:
                    script = "Hello there! I'm Cookie, your friendly neighborhood AI. I like to think of myself as a digital companion here to sprinkle a bit of sweetness into your day. My recipe? Well, it's a dash of intelligence, a pinch of humor, and a whole lot of curiosity!"
                    audio = gen_audio(script)
                    specific_path = 'Wav2Lip/media/audio.wav'
                    with open(specific_path, 'wb') as f:
                        f.write(audio)
                    # Calculate the length of the audio file in seconds
                    audio_info = mediainfo(specific_path)
                    duration_str = audio_info['duration']
                    duration_ms = float(duration_str) * 1000  # Convert seconds to milliseconds
                    duration_seconds = duration_ms / 1000  # Convert milliseconds to seconds
                    rounded_duration = round(duration_seconds)
                    image = cv2.imread(temp_image_path)
                    video_duration = rounded_duration 
                    fps = 30
                    output_folder_name = 'Wav2Lip/media'
                    output_folder = os.path.join(os.getcwd(), output_folder_name)
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    output_video_path = os.path.join(output_folder, 'output.mp4')
                    video_writer = cv2.VideoWriter(output_video_path,
                                                cv2.VideoWriter_fourcc(*'mp4v'),
                                                fps,
                                                (image.shape[1], image.shape[0]))
                    for i in range(video_duration * fps):
                        video_writer.write(image)
                    video_writer.release()
                    cv2.destroyAllWindows()
                    main()
                    if os.path.exists(result_path):
                        try:
                            mime_type, _ = mimetypes.guess_type(result_path)
                            response = StreamingHttpResponse(FileWrapper(open(result_path, 'rb')), content_type=mime_type)
                            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(result_path)}"'
                            return response
                        except Exception as e:
                            return JsonResponse({'error': str(e)}, status=500)
                    else:
                        return JsonResponse({'error': 'File not found'}, status=404)
            else:
                print("image was not uplaoded ")
                return JsonResponse({'message': 'File upload failed'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    return render(request, "index.html")
    

def upscale(request):
    # Assuming `sr` is an instance of SuperResolution
    sr = VideoSR('RealESRGAN')

    # Perform the super resolution on the video
    result_path = 'upscaled_video.mp4'
    try:
        sr('Main/Wav2Lip/results/result_video.mp4', result_path)
    except ValueError as e:
        return HttpResponse(str(e), status=500)

    # Return the upscaled video as a response
    with open(result_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Disposition'] = 'inline; filename="upscaled_video.mp4"'
        return response
    
