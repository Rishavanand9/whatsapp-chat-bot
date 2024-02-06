from PIL import Image
import io
import base64

# Sample base64 encoded image data (replace with your actual data)
base64_data = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEABsbGxscGx4hIR4qLSgtKj04MzM4PV1CR0JHQl2NWGdYWGdYjX2Xe3N7l33gsJycsOD/2c7Z//////////////8BGxsbGxwbHiEhHiotKC0qPTgzMzg9XUJHQkdCXY1YZ1hYZ1iNfZd7c3uXfeCwnJyw4P/Zztn////////////////CABEIADwAHgMBIgACEQEDEQH/xAAuAAACAwEBAAAAAAAAAAAAAAAAAgEDBAUGAQEBAQAAAAAAAAAAAAAAAAAAAQL/2gAMAwEAAhADEAAAAPSVLjuei3M3pUml7cd1wSCZ1YAKjwMQH//EACMQAAICAgEEAgMAAAAAAAAAAAECABEDEjEQEyFBImEUUYH/2gAIAQEAAT8AjnJY0qLtqNqvpmvRqB/kd2rnJxxHDopvLkoATGbVT9R8yWQQ072P9NO7joCm8THlVzQBmR+2harmLZwCRQIjDIrj4jT2YCGFieODPyMCnXfzAQRYhhFqRYuDCiaj4/dwEeoYQDUZAxBuAKvAhPQgn3XX/8QAGBEAAgMAAAAAAAAAAAAAAAAAEWEAECD/2gAIAQIBAT8AFFQrP//EABoRAAICAwAAAAAAAAAAAAAAAAARAQISICH/2gAIAQMBAT8AZFuoxFr/AP/Z"

# Decode base64 data into bytes
image_data = base64.b64decode(base64_data)

# Open the image
image = Image.open(io.BytesIO(image_data))

# Check for compression
if image.format in ('JPEG', 'PNG'):
   print(f'The image is in {image.format} format, which is lossless.')
else:
   print(f'The image is in {image.format} format, which may have compression.')

# Display the image (optional)
image.show()