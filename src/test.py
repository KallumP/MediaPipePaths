import math


def GetDistance(start, end):

    xDistance2 = (start[0] - end[0]) ** 2
    yDistance2 = (start[1] - end[1]) ** 2

    distance = (xDistance2 + yDistance2) ** 0.5
    return distance


def GetAnglePoints(trackStart, trackMid, trackEnd):

    aLength = GetDistance(trackStart, trackMid)
    bLength = GetDistance(trackMid, trackEnd)
    cLength = GetDistance(trackEnd, trackStart)

    return GetAngleLengths(aLength, bLength, cLength)


def GetAngleLengths(a, b, c):

    # derivation
    # c^2 = a^2+b^2 - 2ab Cos(C)
    # 0 = a^2+b^2 - c^2 - 2ab Cos(C)
    # 2ab Cos(C) = a^2+b^2 - c^2
    # Cos(C) = (a^2+b^2 - c^2) / 2ab
    # C = Cos-1( (a^2+b^2 - c^2) / 2ab)

    C_rad = math.acos((a*a + b*b - c*c) / (2*a*b))
    C_deg = math.degrees(C_rad)
    return C_deg


print(GetAngleLengths(3, 4, 5))
