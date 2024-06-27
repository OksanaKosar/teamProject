import math

from django.shortcuts import render, redirect, get_object_or_404
from .models import BMPImage
from .forms import BMPImageForm, ExtendedBMPImageForm
from PIL import Image
import struct
import os
import io
from django.contrib.auth.decorators import login_required
from django.core.files import File


def about_authors_view(request):
    return render(request, 'bmp/about_authors.html')


def about_program_view(request):
    return render(request, 'bmp/about_program.html')


def user_manual_view(request):
    return render(request, 'bmp/user_manual.html')


@login_required
def user_bmp_images(request):
    user = request.user
    bmp_images = BMPImage.objects.filter(user=user).order_by('-id')[:3]
    return render(request, 'bmp/user_bmp_images.html', {'bmp_images': bmp_images})


@login_required
def embed_message(request):
    if request.method == 'POST':
        form = BMPImageForm(request.POST, request.FILES)
        if form.is_valid():
            bmp_image = form.save(commit=False)
            bmp_image.user = request.user
            message = request.POST.get('message')
            bmp_image.text = "The message that was attached: " + message
            bmp_image.save()

            buffer = io.BytesIO()
            hide_message(bmp_image.image.path, buffer, message)
            buffer.seek(0)
            bmp_image.res_image.save('res_' + os.path.basename(bmp_image.image.path), File(buffer), save=False)
            bmp_image.save()

            return render(request, 'bmp/success_hiding.html', {'bmp_image': bmp_image})
    else:
        form = BMPImageForm()
    return render(request, 'bmp/embed_message.html', {'form': form})


@login_required
def extract_message(request):
    if request.method == 'POST':
        form = BMPImageForm(request.POST, request.FILES)
        if form.is_valid():
            bmp_image = form.save(commit=False)
            bmp_image.user = request.user
            bmp_image.save()
            message = extract_message_from_image(bmp_image.image.path)
            bmp_image.text = "The message that was received: " + message
            bmp_image.save()
            return render(request, 'bmp/extract_message.html', {'message': message, 'bmp_image': bmp_image})
    else:
        form = BMPImageForm()
    return render(request, 'bmp/extract_message.html', {'form': form})


def hide_message(input_image, output_buffer, message):
    with open(input_image, 'rb') as file:
        bmp_data = file.read()

    pixel_array_offset = struct.unpack_from('<I', bmp_data, 10)[0]

    message_bits = ''.join(format(ord(char), '08b') for char in message) + '0' * 8

    encoded_data = bytearray(bmp_data)
    for i in range(len(message_bits)):
        byte_index = pixel_array_offset + i
        encoded_data[byte_index] = (encoded_data[byte_index] & 0xFE) | int(message_bits[i])

    output_buffer.write(encoded_data)


def extract_message_from_image(input_image):
    with open(input_image, 'rb') as file:
        bmp_data = file.read()

    pixel_array_offset = struct.unpack_from('<I', bmp_data, 10)[0]

    message_bits = ''
    for i in range(pixel_array_offset, len(bmp_data)):
        message_bits += str(bmp_data[i] & 0x01)
        if len(message_bits) % 8 == 0:
            if message_bits[-8:] == '00000000':
                break

    message = ''.join(chr(int(message_bits[i:i + 8], 2)) for i in range(0, len(message_bits) - 8, 8))
    return message


@login_required
def image_detail(request, image_id):
    image = get_object_or_404(BMPImage, id=image_id)
    return render(request, 'bmp/image_detail.html', {'image': image})


@login_required
def create_bmp(request):
    if request.method == 'POST':
        form = ExtendedBMPImageForm(request.POST, request.FILES)
        if form.is_valid():
            bmp_image = form.save(commit=False)
            bmp_image.user = request.user

            build_type = request.POST.get('build_type')
            color_combination = request.POST.get('color_combination')
            bmp_image.text = f"Build Type: {build_type}, Color Combination: {color_combination}"
            bmp_image.save()

            new_image_path = generate_bmp(bmp_image.image.path, build_type, color_combination)
            with open(new_image_path, 'rb') as f:
                bmp_image.res_image.save('new_' + os.path.basename(new_image_path), File(f), save=False)
            bmp_image.save()

            return render(request, 'bmp/success_creating.html', {'bmp_image': bmp_image})
    else:
        form = ExtendedBMPImageForm()
    return render(request, 'bmp/create_bmp.html', {'form': form})


def generate_bmp(input_image_path, build_type, color_combination):
    with open(input_image_path, 'rb') as f:
        bmp_data = f.read()

    header_size = struct.unpack_from('<I', bmp_data, 14)[0]
    width, height = struct.unpack_from('<ii', bmp_data, 18)
    pixel_array_offset = struct.unpack_from('<I', bmp_data, 10)[0]

    new_image_path = 'images/new_image.bmp'
    with open(new_image_path, 'wb') as f:
        f.write(bmp_data[:pixel_array_offset])

        for y in range(height):
            for x in range(width):
                color = calculate_color(x, y, width, height, build_type, color_combination)
                f.write(struct.pack('BBB', *color))

    return new_image_path


def calculate_color(x, y, width, height, build_type, color_combination):
    if build_type == 'type1':
        return draw_spiral(x, y, color_combination)
    elif build_type == 'type2':
        return draw_diamond(x, y, width, height, color_combination)
    elif build_type == 'type3':
        return draw_rose(x, y, width, height, color_combination)


def draw_spiral(x, y, color_combination):
    distance = math.sqrt(x ** 2 + y ** 2)
    angle = math.atan2(y, x)

    normalized_distance = int(distance) % 256
    normalized_angle = int(angle * (256 / (2 * math.pi))) % 256

    if color_combination == 'combination1':
        return normalized_distance, normalized_angle, (normalized_distance + normalized_angle) % 256
    elif color_combination == 'combination2':
        return normalized_angle, (normalized_distance + normalized_angle) % 256, normalized_distance
    else:
        return (normalized_distance + normalized_angle) % 256, normalized_distance, normalized_angle


def draw_diamond(x, y, width, height, color_combination):
    cx, cy = width // 2, height // 2
    a, b = width // 3, height // 3

    dx = x - cx
    dy = y - cy

    nx = dx / a
    ny = dy / b

    asteroid_value = abs(nx) ** (2 / 3) + abs(ny) ** (2 / 3)

    if asteroid_value <= 1:
        if color_combination == 'combination1':
            return 255, 0, 0
        elif color_combination == 'combination2':
            return 0, 255, 0
        else:
            return 0, 0, 255
    else:
        return 255, 255, 255


def draw_rose(x, y, width, height, color_combination):
    cx, cy = width // 2, height // 2

    dx = x - cx
    dy = y - cy
    distance = math.sqrt(dx ** 2 + dy ** 2)
    angle = math.atan2(dy, dx)
    k = 4

    rose_value = math.sin(k * angle) * distance

    normalized_value = int((rose_value + 256) % 256)

    if color_combination == 'combination1':
        return normalized_value, normalized_value // 2, normalized_value // 3
    elif color_combination == 'combination2':
        return normalized_value // 2, normalized_value, normalized_value // 3
    else:
        return normalized_value // 3, normalized_value // 2, normalized_value
