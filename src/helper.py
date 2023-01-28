import math
import time

# Returns the distance between two points
def GetDistance(start, end):
    xDistance2 = (start[0] - end[0]) ** 2
    yDistance2 = (start[1] - end[1]) ** 2

    distance = (xDistance2 + yDistance2) ** 0.5
    return distance


# gets the angle between three points (the angle of the middle parameter)
def GetAnglePoints(trackStart, trackMid, trackEnd):
    aLength = GetDistance(trackStart, trackMid)
    bLength = GetDistance(trackMid, trackEnd)
    cLength = GetDistance(trackEnd, trackStart)

    return GetAngleLengths(aLength, bLength, cLength)


# gets the angle of three lengths using cosine rule (angle opposite length C)
def GetAngleLengths(a, b, c):
    # derivation of cosine rule
    # c^2 = a^2+b^2 - 2ab Cos(C)
    # 0 = a^2+b^2 - c^2 - 2ab Cos(C)
    # 2ab Cos(C) = a^2+b^2 - c^2
    # Cos(C) = (a^2+b^2 - c^2) / 2ab
    # C = Cos-1( (a^2+b^2 - c^2) / 2ab)

    C_rad = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
    C_deg = math.degrees(C_rad)
    return C_deg


# returns if the user's points are within the target angle
def WithinAngle(index, point, results):
    if CheckWithinFrame(point, results):
        toTrack = point.get("toTrack")
        targetAngle = point.get("angle")
        leniency = point.get("leniency")

        # different points to track
        start = [results[toTrack[0]].x, results[toTrack[0]].y]
        mid = [results[toTrack[1]].x, results[toTrack[1]].y]
        end = [results[toTrack[2]].x, results[toTrack[2]].y]

        pointsAngle = GetAnglePoints(start, mid, end)

        # if the angle of the three points are that of the target
        if pointsAngle > targetAngle - leniency and pointsAngle < targetAngle + leniency:
            return True
    return False


# checks if a user's index is within a target position
def WithinTarget(index, point, results):
    if CheckWithinFrame(point, results):
        toTrack = point.get("toTrack")
        leniency = point.get("leniency")
        targetPosition = [point.get("target")[0], point.get("target")[1]]

        # gets the point of the index to be tracked
        indexPosition = [results[toTrack].x, results[toTrack].y]

        distance = GetDistance(indexPosition, targetPosition)

        if distance < leniency:
            return True
    return False

# checks if an index is above another index
def AboveTarget(index, point, results):
    if CheckWithinFrame(point, results):
        toTrack = point.get("toTrack")
        leniency = point.get("leniency")

        # different points to track
        index1y = results[toTrack[0]].y
        index2y = results[toTrack[1]].y
        
        if  index2y - leniency > index1y:
            return True
    return False

def CheckWithinFrame(point, results):
    toTrack = point.get("toTrack")
    withinFrame = True
    for target in toTrack:
        if results[target].x > 1 or results[target].x < 0 or results[target].y > 1 or results[target].y < 0:
            withinFrame = False  
            print("Index out of frame") 

    return withinFrame