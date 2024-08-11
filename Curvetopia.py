import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import measure, morphology
from scipy.ndimage import binary_fill_holes

# Function to read CSV file and group polylines by their IDs
def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

# Function to calculate the discrete curvature
def calculate_curvature(XY):
    n = len(XY)
    curvatures = np.zeros(n)
    normals = np.zeros((n, 2))
    for i in range(1, n - 1):
        P1, P2, P3 = XY[i - 1], XY[i], XY[i + 1]
        v1, v2 = P2 - P1, P3 - P2
        curvature = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
        curvatures[i] = curvature / np.linalg.norm(v1)
        normals[i] = np.array([-v2[1], v2[0]]) / np.linalg.norm(v2)
    return curvatures, normals

# Function to detect open/closed and self-crossing curves
def detect_curve_properties(XY):
    is_closed = np.linalg.norm(XY[0] - XY[-1]) < 1e-5
    return is_closed

# Function to calculate the turning number for a closed curve
def calculate_turning_number(XY):
    if not detect_curve_properties(XY):
        return 0  # Turning number is only meaningful for closed curves

    angles = []
    n = len(XY)
    for i in range(n):
        P1, P2 = XY[i], XY[(i + 1) % n]
        angle = np.arctan2(P2[1] - P1[1], P2[0] - P1[0])
        angles.append(angle)

    # Calculate the total turning angle
    total_turning_angle = np.sum(np.diff(angles))

    # The turning number is the total turning angle divided by 2π
    turning_number = total_turning_angle / (2 * np.pi)
    return np.round(turning_number)

# Function to complete shapes based on curvature and normals
def complete_shape(XY, curvature, normals):
    if not detect_curve_properties(XY):
        last_point = XY[-1]
        last_direction = XY[-1] - XY[-2]
        last_direction = last_direction / np.linalg.norm(last_direction)
        new_points = [last_point + i * last_direction * 0.1 for i in range(1, 5)]
        XY = np.vstack((XY, new_points))
    return XY

# Function to regularize the shape by smoothing or adjusting based on curvature
def regularize_shape(XY, curvature):
    smoothed_XY = smooth_curve(XY)

    # Check for convexity
    if not check_convexity(curvature):
        print("Shape is not convex, further regularization might be needed.")

    return smoothed_XY

# Function to smooth a curve
def smooth_curve(XY, window_size=5):
    smoothed_XY = np.copy(XY)
    for i in range(1, len(XY) - 1):
        smoothed_XY[i] = np.mean(XY[max(i - window_size // 2, 0):min(i + window_size // 2 + 1, len(XY))], axis=0)
    return smoothed_XY

# Function to check convexity based on curvature
def check_convexity(curvature):
    return np.all(curvature >= 0) or np.all(curvature <= 0)

# Function to apply image segmentation for overlapping layer separation
def segment_image(image, threshold=127):
    ret, thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    segmented = measure.label(thresh, background=0)
    return segmented

# Function to detect and regularize shapes based on curvature
def detect_and_regularize_shapes(path_XYs):
    detected_shapes = []
    for XYs in path_XYs:
        for XY in XYs:
            curvature, normals = calculate_curvature(XY)
            turning_number = calculate_turning_number(XY)
            print(f"Turning number for the curve: {turning_number}")
            XY = complete_shape(XY, curvature, normals)
            XY = regularize_shape(XY, curvature)
            detected_shapes.append(XY)
    return detected_shapes

# Function to flip shapes vertically
def flip_shapes_vertically(detected_shapes):
    # Find the maximum y value
    max_y = max(np.max(XY[:, 1]) for XY in detected_shapes)
    # Flip y values
    flipped_shapes = [np.column_stack((XY[:, 0], max_y - XY[:, 1])) for XY in detected_shapes]
    return flipped_shapes

# Function to plot the detected and regularized shapes
def plot_shapes(detected_shapes):
    colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XY in enumerate(detected_shapes):
        c = colours[i % len(colours)]
        ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    plt.show()

# Function to detect symmetries in the shapes
def detect_symmetries(detected_shapes):
    for idx, XY in enumerate(detected_shapes):
        n = len(XY)
        # Check for central symmetry
        central_symmetry = True
        midpoints = []
        for i in range(n // 2):
            if not np.allclose(XY[i], XY[n - 1 - i]):
                central_symmetry = False
            midpoints.append((XY[i] + XY[n - 1 - i]) / 2)

        # Report only if central symmetry exists
        if central_symmetry:
            print(f"Shape {idx} exhibits central symmetry.")

        # Check for mirror symmetry
        mirror_symmetry = True
        if n % 2 == 0:
            axis = np.mean(midpoints, axis=0)
            for i in range(n // 2):
                if not np.isclose((XY[i] + XY[n - 1 - i]) / 2, axis).all():
                    mirror_symmetry = False

        # Report only if mirror symmetry exists
        if mirror_symmetry:
            print(f"Shape {idx} exhibits mirror symmetry.")

# Main function to execute the shape detection, completion, regularization, flipping, and symmetry detection
def main(csv_path):
    path_XYs = read_csv(csv_path)
    detected_shapes = detect_and_regularize_shapes(path_XYs)
    flipped_shapes = flip_shapes_vertically(detected_shapes)
    plot_shapes(flipped_shapes)
    detect_symmetries(flipped_shapes)

# Example usage
csv_path = '/content/occlusion1.csv'  # Replace with your actual CSV file path
main(csv_path)
