# Smart Document Scanner & Analyzer

A command-line Computer Vision application that detects documents in photographs, extracts them using perspective correction, and performs comprehensive visual analysis including feature extraction and image segmentation.

This project demonstrates real-world application of core Computer Vision concepts covered in CSE3010, including image preprocessing, edge detection, projective transformations, feature extraction (SIFT, ORB, HOG, Harris), and segmentation (K-Means, Watershed, Region Growing).

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Project Architecture](#project-architecture)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [Pipeline Description](#pipeline-description)
- [Course Concepts Applied](#course-concepts-applied)
- [Output Examples](#output-examples)
- [Project Structure](#project-structure)

---

## Problem Statement

Millions of people photograph documents daily — receipts, notes, certificates, whiteboards — using smartphones. These photos typically suffer from perspective distortion, uneven lighting, and noisy backgrounds. Existing scanner apps solve this problem, but understanding *how* they work requires implementing the underlying Computer Vision pipeline from scratch.

This project builds a complete document scanning and analysis tool from the ground up using classical CV techniques (no deep learning), demonstrating that fundamental algorithms from this course can solve a practical, everyday problem.

---

## Project Architecture

```
Input Image → Preprocessing → Edge Detection → Contour Detection → Perspective Transform → Clean Scan
                                                                          ↓
                                                              Feature Extraction (SIFT, ORB, HOG, Harris)
                                                                          ↓
                                                              Segmentation (K-Means, Watershed, Text Detection)
```

---

## Setup Instructions

### Prerequisites

You need Python 3.8 or higher and pip installed on your system. This project runs entirely from the command line and does not require a GUI.

### Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/smart-doc-scanner.git
cd smart-doc-scanner
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate        # On Linux/macOS
venv\Scripts\activate           # On Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs NumPy and OpenCV (including the contrib modules for SIFT).

### Verify Installation

```bash
python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"
```

You should see the OpenCV version printed without errors.

---

## How to Run

The application has three commands: `demo`, `scan`, and `analyze`.

### Run the Full Demo (No Input Image Needed)

This generates a synthetic document image and runs the complete pipeline on it. This is the best way to verify everything works.

```bash
python main.py demo
```

Outputs will be saved to the `output/` directory.

### Scan a Document from a Photo

```bash
python main.py scan path/to/your/photo.jpg
```

To specify a custom output directory:

```bash
python main.py scan photo.jpg -o my_results/
```

### Analyze Features and Segments

```bash
python main.py analyze path/to/image.jpg
```

This runs feature extraction (ORB, SIFT, HOG, Harris corners) and segmentation (K-Means, Watershed, text region detection) on the input image.

### Quick Test with Built-in Sample

```bash
python main.py scan demo
python main.py analyze demo
```

Both commands accept `demo` as the image argument to use the built-in synthetic sample.

---

## Pipeline Description

### Phase 1: Document Scanning

**Step 1 — Preprocessing (Module 1):** The input image is converted to grayscale and smoothed with a Gaussian blur. This removes high-frequency noise that would otherwise produce spurious edges in the next step. The Gaussian kernel size controls the trade-off between noise reduction and detail preservation.

**Step 2 — Edge Detection (Module 3):** Canny edge detection identifies pixels with strong gradient changes. The algorithm applies Sobel filters to compute gradient magnitude and direction, then uses non-maximum suppression to thin edges to single-pixel width, followed by hysteresis thresholding with dual thresholds to trace continuous edge chains.

**Step 3 — Contour Detection (Module 3):** The edge map is searched for contours. Each contour is approximated as a polygon using the Douglas-Peucker algorithm. The system looks for the largest quadrilateral (4-sided polygon) that covers a significant portion of the image, which corresponds to the document boundary.

**Step 4 — Perspective Transformation (Modules 1 & 2):** Once four corners are identified, a 3×3 homography matrix is computed that maps these corners to a rectangle. This projective transformation corrects for the perspective distortion inherent in photographing a flat document from an angle, producing a top-down "scanned" view.

**Step 5 — Adaptive Thresholding (Module 1):** The rectified image is converted to a clean binary (black-on-white) scan. CLAHE (Contrast Limited Adaptive Histogram Equalization) improves contrast locally, then adaptive Gaussian thresholding binarizes the image using locally-computed thresholds, making the output robust to shadows and uneven illumination.

### Phase 2: Feature Extraction (Module 3)

**ORB Features:** Detects corner-like keypoints using FAST and describes them with rotation-invariant BRIEF descriptors. The output shows keypoint locations with their scale and orientation.

**SIFT Features:** Detects scale-invariant keypoints via Difference of Gaussians in scale space, then computes 128-dimensional gradient histogram descriptors. These are invariant to scale, rotation, and partially to illumination.

**HOG Descriptor:** Computes the distribution of gradient orientations over a grid of cells, then normalizes over overlapping blocks. The resulting feature vector captures the overall shape structure of the document.

**Harris Corners:** Computes a corner response function based on eigenvalues of the local structure tensor (gradient auto-correlation matrix). Points where both eigenvalues are large indicate corners.

### Phase 3: Segmentation (Modules 3 & 4)

**K-Means Clustering:** Partitions pixels into k color clusters by iteratively assigning pixels to nearest centroids and recomputing centroids. For documents, this typically separates text, background, and graphical elements.

**Watershed Segmentation:** Treats the image as a topographic surface and "floods" from foreground markers, building boundaries where different flood basins meet. This separates touching or overlapping regions.

**Text Region Detection:** Uses adaptive thresholding, morphological closing (to merge individual characters into text blocks), and connected component analysis to locate and bound text regions with rectangles.

---

## Course Concepts Applied

| Module | Concept | Where Applied |
|--------|---------|---------------|
| Module 1 | Gaussian Filtering, Convolution | Preprocessing stage |
| Module 1 | Histogram Processing (CLAHE) | Contrast enhancement |
| Module 1 | Image Enhancement, Restoration | Adaptive thresholding |
| Module 1 | Projective Transformation | Perspective warp |
| Module 1 | Morphological Operations | Text block merging |
| Module 2 | Homography | getPerspectiveTransform |
| Module 3 | Canny Edge Detection | Edge map computation |
| Module 3 | Harris Corner Detection | Feature extraction |
| Module 3 | SIFT, DOG, Scale-Space | Feature extraction |
| Module 3 | HOG | Shape descriptor |
| Module 3 | Region Growing | Segmentation |
| Module 4 | K-Means Clustering | Color segmentation |
| Module 4 | Watershed Segmentation | Region segmentation |
| Module 4 | Object Detection | Text region detection |

---

## Output Examples

After running `python main.py demo`, the `output/` directory will contain:

```
output/
├── sample_input.jpg           # Generated synthetic document photo
├── scan/
│   ├── 01_detected_contour.jpg   # Original with green boundary overlay
│   ├── 02_edges.jpg              # Canny edge map
│   ├── 03_preprocessed.jpg       # Grayscale + Gaussian blur
│   ├── 04_warped_color.jpg       # Perspective-corrected color image
│   ├── 05_final_scan.jpg         # Clean binary scan output
│   ├── scanned_color.jpg         # Final color scan
│   └── scanned_binary.jpg        # Final binary scan
└── analysis/
    ├── features_orb.jpg          # ORB keypoints visualization
    ├── features_sift.jpg         # SIFT keypoints visualization
    ├── features_harris.jpg       # Harris corners visualization
    ├── seg_kmeans.jpg            # K-Means color segmentation
    ├── seg_watershed.jpg         # Watershed boundaries
    └── seg_text_regions.jpg      # Detected text regions with bounding boxes
```

---

## Project Structure

```
smart-doc-scanner/
├── main.py                    # CLI entry point with argparse commands
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── src/
│   ├── __init__.py
│   ├── scanner.py             # Core scanning pipeline (Modules 1, 2)
│   ├── features.py            # Feature extraction (Module 3)
│   ├── segmentation.py        # Segmentation algorithms (Modules 3, 4)
│   └── visualization.py       # Output generation and visualization
├── samples/                   # Place your test images here
└── output/                    # Generated outputs (created at runtime)
```

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'cv2'"** — Run `pip install opencv-contrib-python` to install OpenCV with the contrib modules (needed for SIFT).

**"No document found" warning** — The contour detector could not find a clear quadrilateral boundary. This can happen if the document blends into the background or has rounded corners. The system falls back to processing the full image.

**Low keypoint count** — Very small or low-contrast images may yield few keypoints. Try providing a higher-resolution input image.

---

## License

This project is developed as a course project for CSE3010 — Computer Vision. It is intended for educational purposes.
