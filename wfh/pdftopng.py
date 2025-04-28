from pdf2image import convert_from_path
import os

def pdf_to_png(pdf_path, output_folder='output_images'):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Convert PDF to list of images
    images = convert_from_path(pdf_path)

    # Save each page as a separate PNG file
    for i, image in enumerate(images, start=1):
        image_path = os.path.join(output_folder, f'EXHIBIT page{i}.png')
        image.save(image_path, 'PNG')
        print(f"Saved {image_path}")

# Example usage
pdf_to_png('aspex.pdf')

