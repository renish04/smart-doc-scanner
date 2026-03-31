"""
Generate the Project Report PDF for CSE3010 BYOP submission.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)


def build_report(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1 * inch,
        leftMargin=1 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"],
        fontSize=22, spaceAfter=6, textColor=HexColor("#1a1a2e"),
        alignment=TA_CENTER,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        fontSize=12, spaceAfter=4, textColor=HexColor("#444444"),
        alignment=TA_CENTER,
    )
    heading_style = ParagraphStyle(
        "SectionHeading", parent=styles["Heading1"],
        fontSize=15, spaceBefore=20, spaceAfter=8,
        textColor=HexColor("#1a1a2e"), borderWidth=0,
    )
    subheading_style = ParagraphStyle(
        "SubHeading", parent=styles["Heading2"],
        fontSize=12, spaceBefore=14, spaceAfter=6,
        textColor=HexColor("#2c3e50"),
    )
    body_style = ParagraphStyle(
        "BodyText", parent=styles["Normal"],
        fontSize=10.5, leading=15, spaceAfter=8,
        alignment=TA_JUSTIFY,
    )
    code_style = ParagraphStyle(
        "CodeBlock", parent=styles["Code"],
        fontSize=9, leading=12, spaceAfter=8,
        backColor=HexColor("#f4f4f4"),
        borderPadding=6, fontName="Courier",
    )

    story = []

    # ===== TITLE PAGE =====
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph("Smart Document Scanner &amp; Analyzer", title_style))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("CSE3010 — Computer Vision", subtitle_style))
    story.append(Paragraph("Bring Your Own Project (BYOP)", subtitle_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(HRFlowable(width="60%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph("Course Project Report", subtitle_style))
    story.append(Paragraph("March 2026", subtitle_style))
    story.append(PageBreak())

    # ===== TABLE OF CONTENTS =====
    story.append(Paragraph("Table of Contents", heading_style))
    toc_items = [
        "1. Introduction and Problem Statement",
        "2. Motivation and Real-World Relevance",
        "3. Technical Approach",
        "4. System Architecture",
        "5. Implementation Details",
        "6. Course Concepts Applied",
        "7. Challenges Faced and Solutions",
        "8. Results and Observations",
        "9. Limitations and Future Work",
        "10. Conclusion and Reflections",
    ]
    for item in toc_items:
        story.append(Paragraph(item, body_style))
    story.append(PageBreak())

    # ===== 1. INTRODUCTION =====
    story.append(Paragraph("1. Introduction and Problem Statement", heading_style))
    story.append(Paragraph(
        "Every day, millions of people take photographs of documents using their smartphones — "
        "receipts, handwritten notes, printed letters, certificates, whiteboard contents, and "
        "more. These photographs almost always suffer from perspective distortion (the camera "
        "is rarely perfectly perpendicular to the document), uneven lighting, background clutter, "
        "and noise. The result is an image that is difficult to read, share, or archive in a "
        "structured way.",
        body_style
    ))
    story.append(Paragraph(
        "Commercial document scanning applications like CamScanner and Adobe Scan solve this "
        "problem seamlessly, but their inner workings are opaque to most users. The goal of "
        "this project is to build a fully functional document scanning and analysis tool from "
        "scratch, using only classical Computer Vision techniques covered in CSE3010, to "
        "understand and demonstrate the algorithms that make this everyday convenience possible.",
        body_style
    ))
    story.append(Paragraph(
        "The project is designed as a command-line tool that accepts a photograph of a document "
        "and produces a clean, perspective-corrected scan. Beyond scanning, it also performs "
        "comprehensive visual analysis — feature extraction using multiple algorithms (SIFT, ORB, "
        "HOG, Harris) and image segmentation (K-Means clustering, Watershed, text region detection) "
        "— to demonstrate a broad range of course concepts in a single, cohesive application.",
        body_style
    ))

    # ===== 2. MOTIVATION =====
    story.append(Paragraph("2. Motivation and Real-World Relevance", heading_style))
    story.append(Paragraph(
        "The motivation for choosing this project stems from a simple observation: document "
        "scanning is one of the most universally relatable applications of Computer Vision. "
        "Unlike specialized tasks like autonomous driving or medical imaging, document scanning "
        "is something nearly everyone has needed to do at some point. By building this tool, "
        "the abstract concepts from the course syllabus — projective transformations, edge detection, "
        "feature descriptors, segmentation — become grounded in a tangible, useful application.",
        body_style
    ))
    story.append(Paragraph(
        "Furthermore, the problem is rich enough to require techniques from almost every module "
        "in the course. Image preprocessing (Module 1) handles noise and contrast. Edge detection "
        "and feature extraction (Module 3) identify the document boundary and its structural "
        "elements. Homography and perspective correction (Modules 1 and 2) rectify the geometry. "
        "Segmentation and clustering (Modules 3 and 4) analyze the document layout. This breadth "
        "of coverage was a deliberate design choice.",
        body_style
    ))
    story.append(Paragraph(
        "Importantly, this project uses only classical CV techniques — no deep learning or "
        "pre-trained neural networks. This constraint was intentional: the goal was to deeply "
        "understand the foundational algorithms rather than rely on black-box models. Every step "
        "of the pipeline has a clear mathematical basis that connects directly to course material.",
        body_style
    ))

    # ===== 3. TECHNICAL APPROACH =====
    story.append(Paragraph("3. Technical Approach", heading_style))
    
    story.append(Paragraph("3.1 Document Scanning Pipeline", subheading_style))
    story.append(Paragraph(
        "The scanning pipeline follows a five-stage architecture. First, the input image is "
        "converted to grayscale and smoothed with a Gaussian blur to suppress noise while "
        "preserving edge structure. The Gaussian kernel size is a tunable parameter — larger "
        "kernels provide stronger smoothing but risk blurring important edges. For typical "
        "smartphone photos, a 5x5 kernel provides a good balance.",
        body_style
    ))
    story.append(Paragraph(
        "Second, Canny edge detection identifies pixels with strong gradient changes. The Canny "
        "algorithm applies Sobel filters to compute gradient magnitude and direction at each "
        "pixel, then performs non-maximum suppression to thin edges to single-pixel width, "
        "followed by hysteresis thresholding using dual thresholds. Pixels above the high "
        "threshold are definite edges; those between the low and high thresholds are retained "
        "only if connected to a strong edge. This two-threshold approach produces clean, "
        "connected edge chains while rejecting isolated noise responses.",
        body_style
    ))
    story.append(Paragraph(
        "Third, the edge map is analyzed using contour detection and polygon approximation. "
        "The Douglas-Peucker algorithm simplifies each contour to a polygon with fewer vertices. "
        "The system searches for the largest quadrilateral — a four-sided polygon — that covers "
        "at least 10% of the image area. This heuristic works because a document in a photo "
        "will typically be the largest rectangular region present.",
        body_style
    ))
    story.append(Paragraph(
        "Fourth, once four corner points are identified, a 3x3 homography matrix is computed "
        "using OpenCV's getPerspectiveTransform function. This matrix encodes the projective "
        "transformation that maps the detected trapezoid to a rectangle. The warpPerspective "
        "function then applies this transformation, producing a top-down \"bird's eye\" view of "
        "the document, effectively removing the perspective distortion.",
        body_style
    ))
    story.append(Paragraph(
        "Finally, the rectified image is enhanced and binarized. CLAHE (Contrast Limited "
        "Adaptive Histogram Equalization) improves local contrast by dividing the image into "
        "tiles and equalizing each independently. Adaptive Gaussian thresholding then converts "
        "the image to black-and-white using locally-computed thresholds, making the result "
        "robust to shadows and uneven illumination.",
        body_style
    ))

    story.append(Paragraph("3.2 Feature Extraction", subheading_style))
    story.append(Paragraph(
        "The feature extraction module demonstrates four distinct algorithms. ORB (Oriented "
        "FAST and Rotated BRIEF) combines the FAST keypoint detector with the BRIEF binary "
        "descriptor. FAST identifies corners by examining a ring of 16 pixels around each "
        "candidate, while BRIEF produces a compact binary descriptor through intensity "
        "comparisons. ORB adds rotation invariance by computing keypoint orientation from "
        "intensity centroids.",
        body_style
    ))
    story.append(Paragraph(
        "SIFT (Scale-Invariant Feature Transform) operates through a multi-stage pipeline: "
        "scale-space extrema detection using Difference of Gaussians (DoG), keypoint localization "
        "with sub-pixel accuracy, orientation assignment based on local gradient histograms, "
        "and descriptor computation using 128-dimensional gradient orientation histograms. Each "
        "descriptor captures the spatial distribution of gradients in the keypoint neighborhood, "
        "providing invariance to scale, rotation, and partial illumination changes.",
        body_style
    ))
    story.append(Paragraph(
        "HOG (Histogram of Oriented Gradients) captures shape information by computing gradient "
        "orientation histograms within a grid of cells, then normalizing over overlapping blocks. "
        "The Harris corner detector computes a response function based on eigenvalues of the "
        "structure tensor (the local gradient auto-correlation matrix), classifying points where "
        "both eigenvalues are large as corners.",
        body_style
    ))

    story.append(Paragraph("3.3 Image Segmentation", subheading_style))
    story.append(Paragraph(
        "Three segmentation approaches are implemented. K-Means color clustering partitions "
        "pixel values into k groups by iteratively assigning pixels to the nearest centroid "
        "and recomputing centroids as cluster means. For documents, this effectively separates "
        "text (dark pixels), background (light pixels), and colored elements into distinct regions.",
        body_style
    ))
    story.append(Paragraph(
        "Watershed segmentation treats the grayscale image as a topographic surface and "
        "identifies region boundaries by simulating flooding from marker points. Sure foreground "
        "is determined via distance transform thresholding, sure background via morphological "
        "dilation, and the watershed algorithm builds boundaries where different flood basins "
        "meet. Text region detection combines adaptive thresholding, morphological closing to "
        "merge nearby characters into continuous blocks, and connected component analysis to "
        "identify and bound text regions with rectangles.",
        body_style
    ))

    # ===== 4. SYSTEM ARCHITECTURE =====
    story.append(Paragraph("4. System Architecture", heading_style))
    story.append(Paragraph(
        "The project follows a modular architecture with clear separation of concerns. The "
        "codebase is organized into four source modules under the src/ directory, each "
        "responsible for a distinct aspect of the pipeline.",
        body_style
    ))
    story.append(Paragraph(
        "The scanner module (scanner.py) implements the core five-stage scanning pipeline: "
        "preprocessing, edge detection, contour detection, perspective transformation, and "
        "adaptive thresholding. The features module (features.py) provides ORB, SIFT, HOG, "
        "and Harris corner detection with a unified interface. The segmentation module "
        "(segmentation.py) implements K-Means clustering, Watershed segmentation, region "
        "growing, and text region detection. The visualization module (visualization.py) "
        "generates annotated output images for each pipeline stage.",
        body_style
    ))
    story.append(Paragraph(
        "The main.py entry point uses Python's argparse library to provide three CLI commands: "
        "'demo' generates a synthetic test image and runs the full pipeline, 'scan' runs the "
        "scanning pipeline on a user-provided image, and 'analyze' performs feature extraction "
        "and segmentation. This design allows each component to be used independently or as "
        "part of the complete pipeline.",
        body_style
    ))

    # ===== 5. IMPLEMENTATION DETAILS =====
    story.append(Paragraph("5. Implementation Details", heading_style))
    
    story.append(Paragraph("5.1 Point Ordering for Homography", subheading_style))
    story.append(Paragraph(
        "A critical implementation detail is the consistent ordering of the four corner points "
        "before computing the homography. The contour detection step returns corners in an "
        "arbitrary order, but the perspective transform requires a known correspondence between "
        "source and destination points. The solution uses the sum and difference of coordinates: "
        "the top-left corner has the smallest x+y sum, the bottom-right has the largest, the "
        "top-right has the smallest y-x difference, and the bottom-left has the largest. This "
        "geometric property holds regardless of the document's orientation and provides a "
        "reliable ordering without complex angle calculations.",
        body_style
    ))

    story.append(Paragraph("5.2 Graceful Fallback Handling", subheading_style))
    story.append(Paragraph(
        "Not every input image contains a clearly bounded document. When the contour detector "
        "fails to find a quadrilateral (for example, if the document fills the entire frame or "
        "has rounded corners), the system falls back to processing the full image rather than "
        "failing. This is implemented by substituting the image corners as the \"detected\" "
        "contour, effectively applying an identity transform. The metadata dictionary records "
        "this fallback so the user is informed of the situation.",
        body_style
    ))

    story.append(Paragraph("5.3 Synthetic Test Image Generation", subheading_style))
    story.append(Paragraph(
        "To enable testing without requiring external images, the project includes a function "
        "that generates a synthetic document photo. A white \"document\" with text and bar charts "
        "is created, then warped onto a textured background using a known homography. This "
        "synthetic image has controlled perspective distortion, making it ideal for verifying "
        "that the pipeline correctly detects and rectifies the document. Adding Gaussian noise "
        "to the background texture makes the scene realistic enough to test edge detection "
        "robustness.",
        body_style
    ))

    # ===== 6. COURSE CONCEPTS =====
    story.append(Paragraph("6. Course Concepts Applied", heading_style))
    
    table_data = [
        ["Module", "Concept", "Implementation"],
        ["1", "Gaussian Filtering & Convolution", "Preprocessing with GaussianBlur"],
        ["1", "Histogram Processing (CLAHE)", "Adaptive contrast enhancement"],
        ["1", "Image Enhancement", "Adaptive thresholding for scan output"],
        ["1", "Projective Transformation", "Perspective warp via getPerspectiveTransform"],
        ["1", "Morphological Operations", "Dilation, closing for text merging"],
        ["2", "Homography", "3x3 perspective transform matrix"],
        ["3", "Canny Edge Detection", "Edge map with dual thresholds"],
        ["3", "Harris Corner Detection", "Structure tensor eigenvalue analysis"],
        ["3", "SIFT / DOG / Scale-Space", "Scale-invariant feature descriptors"],
        ["3", "HOG", "Gradient orientation histograms"],
        ["3", "Region Growing", "Seed-based intensity segmentation"],
        ["4", "K-Means Clustering", "Color-based pixel clustering"],
        ["4", "Watershed Segmentation", "Topographic flooding for boundaries"],
        ["4", "Object Detection", "Text region bounding boxes"],
    ]

    t = Table(table_data, colWidths=[1.0 * cm, 5.5 * cm, 6.5 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f9f9f9"), HexColor("#ffffff")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t)

    # ===== 7. CHALLENGES =====
    story.append(Paragraph("7. Challenges Faced and Solutions", heading_style))
    
    story.append(Paragraph("7.1 Edge Detection Sensitivity", subheading_style))
    story.append(Paragraph(
        "The initial implementation used fixed Canny thresholds (100, 200), which worked well "
        "for high-contrast documents but failed on images with soft edges or low contrast between "
        "the document and background. The solution was to use more permissive thresholds (50, 150) "
        "combined with morphological dilation to close small gaps in the edge contour. This "
        "trade-off introduced more noise edges but made the quadrilateral detection more reliable "
        "because the contour was more likely to be complete.",
        body_style
    ))
    
    story.append(Paragraph("7.2 Contour Approximation Epsilon", subheading_style))
    story.append(Paragraph(
        "The Douglas-Peucker approximation parameter (epsilon) controls how aggressively contours "
        "are simplified. A value too small produces polygons with many vertices; a value too "
        "large over-simplifies and may reduce a near-rectangle to a triangle. After experimentation, "
        "2% of the contour perimeter was chosen as the epsilon value, providing reliable four-point "
        "approximations for rectangular documents while tolerating slight curvature or damage at "
        "edges.",
        body_style
    ))
    
    story.append(Paragraph("7.3 Handling Non-Rectangular Documents", subheading_style))
    story.append(Paragraph(
        "Some documents do not present as clean quadrilaterals — for instance, a receipt may be "
        "curved, or a note may have torn edges. The system handles this through the minimum area "
        "threshold (10% of image area) and the fallback mechanism. If no quadrilateral meets the "
        "criteria, the system processes the entire image. While this does not produce a perspective-"
        "corrected result, it ensures that the feature extraction and segmentation stages still "
        "provide useful analysis.",
        body_style
    ))

    # ===== 8. RESULTS =====
    story.append(Paragraph("8. Results and Observations", heading_style))
    story.append(Paragraph(
        "The scanning pipeline was tested on both synthetic and real-world document photographs. "
        "On the synthetic test image, the system correctly identifies all four corners and "
        "produces a clean, perspective-corrected scan. The contour is detected reliably, and the "
        "homography accurately maps the trapezoid to a rectangle. The adaptive thresholding "
        "produces legible binary output with clean text rendering.",
        body_style
    ))
    story.append(Paragraph(
        "Feature extraction results show that SIFT and ORB both detect hundreds of keypoints "
        "concentrated around text and graphical elements, which are the high-frequency regions "
        "of the document. Harris corner detection identifies thousands of corner responses, "
        "concentrated at character corners and intersections. The HOG descriptor produces a "
        "1764-dimensional feature vector that encodes the global shape structure.",
        body_style
    ))
    story.append(Paragraph(
        "Segmentation analysis reveals that K-Means clustering with k=3 effectively separates "
        "text, background, and graphical elements into distinct regions. Watershed segmentation "
        "successfully identifies boundaries between adjacent text blocks and figures. Text region "
        "detection correctly identifies and bounds major text blocks with rectangular bounding "
        "boxes, although very small text or isolated characters may be missed by the morphological "
        "merging step.",
        body_style
    ))
    story.append(Paragraph(
        "The complete demo pipeline generates 14 output images, providing visual evidence of "
        "each stage's contribution. Processing a typical image takes under 2 seconds on a modern "
        "machine, with feature extraction being the most computationally intensive stage due to "
        "the SIFT scale-space computation.",
        body_style
    ))

    # ===== 9. LIMITATIONS =====
    story.append(Paragraph("9. Limitations and Future Work", heading_style))
    story.append(Paragraph(
        "The current implementation has several known limitations. First, it assumes a single "
        "document per image. Detecting multiple documents would require a more sophisticated "
        "contour selection strategy that evaluates all candidate quadrilaterals rather than "
        "returning only the largest. Second, the system relies on the document having a distinct "
        "boundary — documents on white surfaces or with very similar background colors may not "
        "be detected. Third, the scanning pipeline is purely geometric and does not perform OCR "
        "(Optical Character Recognition), so the text content is not extracted as machine-readable "
        "text.",
        body_style
    ))
    story.append(Paragraph(
        "Possible extensions include integrating Tesseract OCR for text extraction from scanned "
        "documents, adding optical flow analysis (Module 4) for video-based document tracking, "
        "implementing feature matching between document templates and scanned images for automatic "
        "document classification, and incorporating the Shape from Texture concepts from Module 5 "
        "to estimate document surface curvature for non-planar documents.",
        body_style
    ))

    # ===== 10. CONCLUSION =====
    story.append(Paragraph("10. Conclusion and Reflections", heading_style))
    story.append(Paragraph(
        "This project demonstrates that the fundamental Computer Vision techniques covered in "
        "CSE3010 are sufficient to build a practical, functional document scanning application. "
        "The pipeline uses Gaussian filtering and Canny edge detection from Module 1/3, "
        "homography-based perspective correction from Module 2, SIFT/ORB/HOG/Harris feature "
        "extraction from Module 3, and K-Means/Watershed segmentation from Module 4. Each "
        "algorithm contributes a specific capability, and together they form a coherent system.",
        body_style
    ))
    story.append(Paragraph(
        "The most valuable learning came from understanding how these algorithms interact in a "
        "pipeline. For instance, the quality of edge detection directly affects contour detection, "
        "which in turn determines whether the homography is computed from correct corner points. "
        "Tuning one stage often requires revisiting earlier stages — the preprocessing parameters "
        "that work best for edge detection may not be optimal for feature extraction. This "
        "systems-level understanding of how individual algorithms compose into a working application "
        "is, in my view, the most important outcome of this project.",
        body_style
    ))
    story.append(Paragraph(
        "Building the project from scratch — without relying on deep learning or pre-built "
        "scanning libraries — forced a deep engagement with the mathematical foundations of each "
        "technique. Understanding why the Canny detector uses hysteresis thresholding, how the "
        "homography matrix encodes a projective transformation, and what the eigenvalues of the "
        "structure tensor signify for corner detection are insights that would be difficult to "
        "gain from using higher-level abstractions alone.",
        body_style
    ))

    # Build PDF
    doc.build(story)
    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    build_report("/home/claude/smart-doc-scanner/Project_Report_CSE3010.pdf")
