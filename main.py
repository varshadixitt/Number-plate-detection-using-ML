import cv2
import numpy as np
import easyocr
import imutils
import pandas as pd
from tkinter import Tk, Button, Label, filedialog, Text, END, Scrollbar, RIGHT, Y, messagebox
import os
import warnings

# Suppress the warning related to 'pin_memory'
warnings.filterwarnings("ignore", message=".*pin_memory.*")

# Initialize EasyOCR reader globally
reader = easyocr.Reader(['en'])

class PlateDetectorApp:
    def __init__(self, master):
        self.master = master
        master.title("License Plate Detector")

        self.label = Label(master, text="Select a folder with images to process:")
        self.label.pack(pady=10)

        self.select_button = Button(master, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=5)

        self.process_button = Button(master, text="Start Processing", command=self.process_images, state='disabled')
        self.process_button.pack(pady=5)

        self.log_text = Text(master, height=15, width=70)
        self.log_text.pack(pady=10)

        self.scrollbar = Scrollbar(master, command=self.log_text.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.log_text.config(yscrollcommand=self.scrollbar.set)

        self.folder_path = None

    def log(self, message):
        self.log_text.insert(END, message + "\n")
        self.log_text.see(END)
        self.master.update()

    def select_folder(self):
        self.folder_path = filedialog.askdirectory(title="Select folder with images")
        if self.folder_path:
            self.log(f"Selected folder: {self.folder_path}")
            self.process_button.config(state='normal')
        else:
            self.log("No folder selected.")

    def process_images(self):
        if not self.folder_path:
            self.log("No folder selected. Please select a folder first.")
            return

        output_dir = os.path.join(self.folder_path, 'output')
        cropped_dir = os.path.join(output_dir, 'cropped')
        annotated_dir = os.path.join(output_dir, 'annotated')
        os.makedirs(cropped_dir, exist_ok=True)
        os.makedirs(annotated_dir, exist_ok=True)

        results_list = []
        popup_results = ""

        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(self.folder_path, filename)
                self.log(f"Processing {filename}...")

                img = cv2.imread(file_path)
                if img is None:
                    self.log(f"Failed to read {filename}. Skipping.")
                    continue

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
                edged = cv2.Canny(bfilter, 30, 200)

                keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                contours = imutils.grab_contours(keypoints)
                contours = sorted(contours, key=cv2.contourArea, reverse=True)[:20]

                plate_count = 0
                found_texts = []

                for contour in contours:
                    approx = cv2.approxPolyDP(contour, 0.018 * cv2.arcLength(contour, True), True)
                    if len(approx) == 4:
                        mask = np.zeros(gray.shape, np.uint8)
                        new_image = cv2.drawContours(mask, [approx], 0, 255, -1)
                        new_image = cv2.bitwise_and(img, img, mask=mask)

                        (x, y) = np.where(mask == 255)
                        if len(x) == 0 or len(y) == 0:
                            continue
                        (x1, y1) = (np.min(x), np.min(y))
                        (x2, y2) = (np.max(x), np.max(y))
                        cropped_image = gray[x1:x2+1, y1:y2+1]

                        result = reader.readtext(cropped_image)

                        if result:
                            for detection in result:
                                detected_text = detection[1]
                                confidence = detection[2]
                                self.log(f"Detected: {detected_text} (Confidence: {confidence:.2f})")
                                found_texts.append((detected_text, confidence))

                                # Draw rectangle around plate
                                img = cv2.polylines(img, [approx], True, (0, 255, 0), 3)

                                # Save cropped image
                                crop_filename = f"{os.path.splitext(filename)[0]}_plate{plate_count}.png"
                                crop_save_path = os.path.join(cropped_dir, crop_filename)
                                cv2.imwrite(crop_save_path, cropped_image)

                                # Add to results
                                results_list.append({
                                    'Image': filename,
                                    'Plate_Number': detected_text,
                                    'Confidence': confidence,
                                    'Cropped_Image': crop_filename
                                })
                                popup_results += f"{filename}: {detected_text} (Confidence: {confidence:.2f})\n"
                                plate_count += 1

                if found_texts:
                    # Write the first detected plate at top-left corner with better visibility (white text with black outline)
                    main_text = f"{found_texts[0][0]} ({found_texts[0][1]*100:.1f}%)"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    # Outline (black)
                    cv2.putText(img, main_text, (20, 50), font, 1.2, (0, 0, 0), 4, cv2.LINE_AA)
                    # Text (white)
                    cv2.putText(img, main_text, (20, 50), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
                else:
                    results_list.append({
                        'Image': filename,
                        'Plate_Number': 'No detection',
                        'Confidence': 0.0,
                        'Cropped_Image': ''
                    })
                    popup_results += f"{filename}: No detection\n"
                    self.log("No license plate-like contour detected.")

                # Save annotated image
                annotated_save_path = os.path.join(annotated_dir, filename)
                cv2.imwrite(annotated_save_path, img)

        # Save CSV
        csv_save_path = os.path.join(output_dir, 'detection_results.csv')
        df = pd.DataFrame(results_list)
        df.to_csv(csv_save_path, index=False)
        self.log(f"\nAll done! Results saved to {csv_save_path}")

        # Show popup with all results
        messagebox.showinfo("Processing Complete", f"Results saved to:\n{csv_save_path}\n\nDetected plates:\n\n{popup_results.strip()}")

if __name__ == "__main__":
    root = Tk()
    app = PlateDetectorApp(root)
    root.mainloop()
