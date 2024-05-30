# Description: This script creates a dataset of 512x512x3 images of a random triangle. it also saves the position of the triangle in a json file.

from argparse import ArgumentParser
import os
import numpy as np
import cv2
import json
import tqdm

IMAGE_SIZE = 512

def calculate_angles(p1, p2, p3):
    # Convert points to numpy arrays
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    
    # Calculate vectors
    v1 = p1 - p2
    v2 = p3 - p2
    v3 = p3 - p1
    v4 = p1 - p3
    
    # Calculate the norms of the vectors
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)
    v3_norm = np.linalg.norm(v3)
    v4_norm = np.linalg.norm(v4)
    
    # Calculate the dot products
    dot1 = np.dot(v1, v2)
    dot2 = np.dot(-v1, v3)
    dot3 = np.dot(v4, -v2)
    
    # Calculate the angles in radians
    angle1 = np.arccos(dot1 / (v1_norm * v2_norm))
    angle2 = np.arccos(dot2 / (v1_norm * v3_norm))
    angle3 = np.arccos(dot3 / (v2_norm * v4_norm))
    
    # Convert angles to degrees if needed
    angle1_deg = np.degrees(angle1)
    angle2_deg = np.degrees(angle2)
    angle3_deg = np.degrees(angle3)
    
    return angle1_deg, angle2_deg, angle3_deg

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-n', '--num-images', type=int, help='Number of images to generate')
    parser.add_argument('-o', '--output', help='Dataset file name')
    parser.add_argument('-a', '--min-angle', type=int, default=30, help='Minimum angle of the triangles in degrees')
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    positions = []
    min_angle = args.min_angle
    for i in tqdm.tqdm(range(args.num_images)):
        img = np.ones((IMAGE_SIZE, IMAGE_SIZE, 3), dtype=np.uint8)
        img *= 240

        file_name = f'{i:0>4}.png'

        # positions of the vertices of the triangle (shouldn't be too close to the edges of the image)
        buffer = 50

        p1 = (np.random.randint(buffer, IMAGE_SIZE-buffer), np.random.randint(buffer, IMAGE_SIZE-buffer))
        p2 = (np.random.randint(buffer, IMAGE_SIZE-buffer), np.random.randint(buffer, IMAGE_SIZE-buffer))
        p3 = (np.random.randint(buffer, IMAGE_SIZE-buffer), np.random.randint(buffer, IMAGE_SIZE-buffer))
        
        alpha1, alpha2, alpha3 = calculate_angles(p1, p2, p3)
        min_of_angles = min(alpha1, alpha2, alpha3)

        while min_of_angles < min_angle:
            p1 = (np.random.randint(buffer, IMAGE_SIZE-buffer), np.random.randint(buffer, IMAGE_SIZE-buffer))
            p2 = (np.random.randint(buffer, IMAGE_SIZE-buffer), np.random.randint(buffer, IMAGE_SIZE-buffer))
            p3 = (np.random.randint(buffer, IMAGE_SIZE-buffer), np.random.randint(buffer, IMAGE_SIZE-buffer))

            alpha1, alpha2, alpha3 = calculate_angles(p1, p2, p3)
            min_of_angles = min(alpha1, alpha2, alpha3)
        
        # print(f"angles: {int(alpha1)}, {int(alpha2)}, {int(alpha3)}, {alpha1+alpha2+alpha3}")
        
        # random color (not too close to the background)
        color = (np.random.randint(0, 220), np.random.randint(0, 220), np.random.randint(0, 220)) 

        # draw the triangle
        triangle = np.array([p1, p2, p3], np.int32)
        cv2.fillPoly(img, [triangle], color)

        # normalize the points
        p1 = (p1[0] / IMAGE_SIZE, p1[1] / IMAGE_SIZE)
        p2 = (p2[0] / IMAGE_SIZE, p2[1] / IMAGE_SIZE)
        p3 = (p3[0] / IMAGE_SIZE, p3[1] / IMAGE_SIZE)

        positions.append({'image':f"{args.output}/file_name", 'points':[p1, p2, p3]})

        # save the image
        cv2.imwrite(os.path.join(args.output, file_name), img)

    with open('train.json', 'w') as f:
        json.dump(positions, f)
    
    print(f'Dataset \"{args.output}\" created successfully!')