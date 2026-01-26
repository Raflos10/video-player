import math

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    dx = point1.x() - point2.x()
    dy = point1.y() - point2.y()
    return math.sqrt(dx ** 2 + dy ** 2)
