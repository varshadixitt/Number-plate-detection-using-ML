
# Number Plate Detector

This Python application is designed to process a folder of images and detect license plates. Using **EasyOCR** for optical character recognition (OCR) and **OpenCV** for image processing, the tool helps you extract text from vehicle plates and save the results in an easy-to-read format.

---

## 🛠️ **Features**
- **Select Folder**: Choose a folder containing your images (JPEG, PNG, etc.).
- **License Plate Detection**: Automatically detects license plates in the images.
- **Text Extraction**: Uses OCR to extract text (plate numbers) from the detected regions.
- **Annotations**: Annotates the image with the detected plate number.
- **Cropped Images**: Saves cropped images of the detected plates for reference.
- **CSV Export**: Saves all the detected plate numbers, along with their confidence scores, in a CSV file.
- **Results Pop-up**: After processing, you'll see a pop-up with a summary of all detections.

---

## 📦 **Requirements**
To get started with this project, you’ll need to install the following Python libraries:
- **easyocr**: For optical character recognition.
- **opencv-python**: For image processing and manipulation.
- **imutils**: A helper library for OpenCV functions.
- **pandas**: For saving results into a CSV file.
- **tkinter**: A simple GUI for user interaction.

Install them via `pip`:

```bash
pip install easyocr opencv-python imutils pandas tk
```

---

## 🚀 **How to Use**

1. **Clone the repository** or download the Python script.

2. **Run the application**:
   - Simply execute the script in Python.
   - A GUI will appear asking you to select a folder containing the images you want to process.

3. **Select a folder**:
   - Choose the folder with images (JPEG, PNG, etc.) containing vehicle plates.
   
4. **Start Processing**:
   - Click the **Start Processing** button to begin detection.
   - The program will:
     - Detect plates in each image.
     - Extract the text using OCR.
     - Annotate the image with detected text.
     - Save the annotated and cropped images to output directories.

5. **Results**:
   - A pop-up will show after processing is complete, summarizing all detected plates and their confidence scores.
   - A **CSV file** will be saved with the details of the detected plates (image name, plate number, confidence score).

---

## 💾 **Output Files**

- **Annotated Images**: Saved in the `annotated` folder.
- **Cropped Images**: Saved in the `cropped` folder.
- **CSV File**: Results stored in `detection_results.csv` inside the `output` folder, with:
  - **Image Name**: The name of the image processed.
  - **Plate Number**: The detected text from the plate.
  - **Confidence**: The confidence score of the OCR detection.
  - **Cropped Image Filename**: Name of the cropped image file saved.

---

## ⚙️ **Technical Notes**

- **Pin Memory Warning**: You might see a warning regarding `pin_memory`. This is related to GPU optimization. If you're using a CPU, you can safely ignore it. The program still works perfectly fine on a CPU!

---

## 🐛 **Troubleshooting**

- If your images are not being processed or you see strange behavior, try the following:
  1. Make sure your images are in a supported format (e.g., `.jpg`, `.png`).
  2. Ensure all necessary libraries are installed (you can check with `pip list`).
  3. For large images, processing might take a little longer. If the program seems stuck, give it some time.

---

## 🤝 **Contributing**

Feel free to fork this project and contribute improvements, bug fixes, or features. You can open issues and pull requests on the GitHub repository. 

---

## 📧 **Contact**  
If you have any questions or need support, feel free to contact me. You can reach out via email or open an issue on GitHub.

---