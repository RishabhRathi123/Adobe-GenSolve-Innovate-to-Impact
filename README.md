# Adobe-GenSolve-Innovate-to-Impact
# Curvetopia
# Shape Detection, Completion, Regularization, and Symmetry Detection

This repository provides a Python implementation to analyze, complete, regularize, and detect symmetries in shapes described by polylines. The code processes polylines stored in a CSV file and performs several geometric operations to manipulate and analyze the shapes.

## Overview

### Key Features

- **Polyline Reading**: Parses a CSV file containing polylines and groups them by their IDs.
- **Curvature Calculation**: Computes the discrete curvature of each polyline, which is essential for understanding the shape's properties.
- **Shape Completion**: Extends open polylines to form closed shapes when necessary.
- **Shape Regularization**: Applies smoothing techniques to regularize the shape based on its curvature.
- **Symmetry Detection**: Detects central and mirror symmetries within the shapes.
- **Shape Plotting**: Visualizes the detected and regularized shapes using Matplotlib.
- **Vertical Flipping**: Includes a utility to flip shapes vertically.

### Applications

This tool can be useful in various applications, including:

- **Computer Vision**: Analyzing and refining detected shapes in images.
- **Geometric Processing**: Regularizing and analyzing shapes in vector graphics.
- **Pattern Recognition**: Detecting symmetrical patterns in geometric data.

## Prerequisites

Ensure that you have the following Python packages installed:

- `numpy`
- `matplotlib`
- `opencv-python`
- `scikit-image`
- `scipy`

You can install these dependencies using pip:

```bash
pip install numpy matplotlib opencv-python scikit-image scipy
```

## CSV File Format

The CSV file should have the following structure:

- **First Column**: Polyline ID
- **Second Column**: Point ID within the polyline
- **Third Column**: X-coordinate
- **Fourth Column**: Y-coordinate

Example:
```
1,1,10.5,25.3
1,2,15.2,30.1
1,3,20.0,35.7
2,1,5.0,15.0
2,2,10.0,20.0
```

## Code Explanation

### Functions

- **`read_csv(csv_path)`**: Reads and groups polylines by their IDs from the specified CSV file.
- **`calculate_curvature(XY)`**: Calculates the discrete curvature and normals for a given polyline.
- **`detect_curve_properties(XY)`**: Checks whether a polyline is closed.
- **`calculate_turning_number(XY)`**: Computes the turning number, a key topological invariant, for closed curves.
- **`complete_shape(XY, curvature, normals)`**: Completes open shapes by extending the polyline based on curvature and normals.
- **`regularize_shape(XY, curvature)`**: Regularizes the shape by smoothing it and checking for convexity.
- **`smooth_curve(XY, window_size=5)`**: Applies a smoothing filter to the polyline.
- **`check_convexity(curvature)`**: Determines whether the shape is convex based on its curvature.
- **`segment_image(image, threshold=127)`**: Segments an image for layer separation, typically used for handling overlapping shapes.
- **`detect_and_regularize_shapes(path_XYs)`**: Performs detection, completion, and regularization on all polylines.
- **`flip_shapes_vertically(detected_shapes)`**: Flips the detected shapes vertically.
- **`plot_shapes(detected_shapes)`**: Plots the detected and regularized shapes.
- **`detect_symmetries(detected_shapes)`**: Detects central and mirror symmetries in the shapes.

### Main Function

The `main` function orchestrates the entire process:
1. Reads the polyline data from the CSV file.
2. Detects and regularizes the shapes.
3. Flips the shapes vertically.
4. Plots the shapes.
5. Detects and reports symmetries.

```python
def main(csv_path):
    path_XYs = read_csv(csv_path)
    detected_shapes = detect_and_regularize_shapes(path_XYs)
    flipped_shapes = flip_shapes_vertically(detected_shapes)
    plot_shapes(flipped_shapes)
    detect_symmetries(flipped_shapes)
```

### Example Usage

```python
csv_path = '/path/to/your/csvfile.csv'
main(csv_path)
```

## Output

- **Plots**: The script generates plots of the detected and regularized shapes.
- **Symmetry Detection**: Outputs details about the symmetries (if any) detected in the shapes.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue if you encounter bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

This `README.md` file provides an overview of your code, instructions for setting it up, and details on how to use it. You can further customize it to match any specific nuances of your project.
