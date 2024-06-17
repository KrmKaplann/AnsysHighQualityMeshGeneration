import math
import time

ListCircle = []
FaceAll = GetRootPart().Bodies

CenterCoordinateSystem = GetRootPart().CoordinateSystems[0]
CenterCoordinateSystemSelected = Selection.Create(CenterCoordinateSystem)
print(type(FaceAll))

CoordinateOfFaceDict = {}

FaceList = []

for index, OneFace in enumerate(FaceAll):
    FaceName = OneFace.GetName()
    selection = Selection.Create(CenterCoordinateSystem, OneFace.Faces[0])
    gap = MeasureHelper.DistanceBetweenObjects(selection)
    distance = gap.Distance
    distance = distance * 1000

    distance = "{:2f}".format(distance)
    selection.SetActive()
    CoordinateOfFaceDict[FaceName] = distance
    FaceList.append(FaceName)

Selection.Clear()
AllCordinateForRectangle = {}

for index, OneFace in enumerate(FaceAll):

    selection = Selection.Create(OneFace.Faces[0])
    result = ViewHelper.SetSketchPlane(selection, None)

    point = Point2D.Create(MM(0), MM(0))
    result = SketchPoint.Create(point)

    mode = InteractionMode.Solid
    result = ViewHelper.SetViewMode(mode, None)

    selectionCoordinate = Selection.Create(GetRootPart().CoordinateSystems[0])
    secondarySelection = Selection.Create(GetRootPart().Curves[0].GetChildren[ICurvePoint]()[0])

    gap = MeasureHelper.DistanceBetweenObjects(selectionCoordinate, secondarySelection)
    CenterX = gap.DeltaX * 1000
    CenterY = gap.DeltaY * 1000
    CenterZ = gap.DeltaZ * 1000

    FaceName = OneFace.GetName()

    origin = Point.Create(MM(CenterX), MM(CenterY), MM(CenterZ))
    x_Direction = Direction.DirX
    y_Direction = Direction.DirY
    z_Direction = Direction.DirZ

    result = DatumOriginCreator.Create(origin, x_Direction, y_Direction, None)

    CenterCoordinateSystem = GetRootPart().CoordinateSystems[0]
    CenterCoordinateSystemSelected = Selection.Create(CenterCoordinateSystem)

    for i in range(len(OneFace.Faces[0].Edges)):
        try:
            RadiusFinder = OneFace.Faces[0].Edges[i].Shape.Geometry.Radius * 2.0
            Object = OneFace.Faces[0].Edges[i].GetChildren[ICurvePoint]()[0]
            CircleCentrePoint = Selection.Create(Object)
            CircleCentrePoint.SetActive()

            gap = MeasureHelper.DistanceBetweenObjects(CenterCoordinateSystemSelected, CircleCentrePoint)
            CoordinateXYZ = [gap.DeltaX, gap.DeltaY, gap.DeltaZ]
            XYZ = ["X", "Y", "Z"]
            NetLocation = {}

            for index, OneCoordinate in enumerate(CoordinateXYZ):
                Delta = OneCoordinate * 1000
                NetLocation[XYZ[index]] = round(Delta, 4)

            selection = Selection.Create(OneFace.Faces[0])

            print(NetLocation)

            X = NetLocation["X"]
            Y = NetLocation["Y"]
            Z = NetLocation["Z"]

            AllCordinateForRectangle[i] = [NetLocation]
        except:
            pass
    result = ViewHelper.SetSketchPlane(selection, None)

    for No, Coordinate in AllCordinateForRectangle.items():
        X = Coordinate[0]["X"]
        Y = Coordinate[0]["Y"]
        Z = Coordinate[0]["Z"]

        Rectangle = 125
        Radius = RadiusFinder / 2 * 1000

        point1 = Point2D.Create(MM(X + Rectangle), MM(Y + Rectangle))
        point2 = Point2D.Create(MM(X - Rectangle), MM(Y + Rectangle))
        point3 = Point2D.Create(MM(X - Rectangle), MM(Y - Rectangle))
        result = SketchRectangle.Create(point1, point2, point3)

        origin = Point2D.Create(MM(X), MM(Y))
        result = SketchCircle.Create(origin, MM(Radius * 150 / 100))

        a = float(Radius * Radius / 2) ** 0.5

        start = Point2D.Create(MM(X + Rectangle), MM(Y + Rectangle))
        end = Point2D.Create(MM(X + a), MM(Y + a))
        result = SketchLine.Create(start, end)

        start = Point2D.Create(MM(X - Rectangle), MM(Y + Rectangle))
        end = Point2D.Create(MM(X - a), MM(Y + a))
        result = SketchLine.Create(start, end)

        start = Point2D.Create(MM(X - Rectangle), MM(Y - Rectangle))
        end = Point2D.Create(MM(X - a), MM(Y - a))
        result = SketchLine.Create(start, end)

        start = Point2D.Create(MM(X + Rectangle), MM(Y - Rectangle))
        end = Point2D.Create(MM(X + a), MM(Y - a))
        result = SketchLine.Create(start, end)

    mode = InteractionMode.Solid
    result = ViewHelper.SetViewMode(mode, None)

    try:
        selection = Selection.Create(GetRootPart().GetBodies("Surface"))
        result = Delete.Execute(selection)
    except:
        pass

    selection = Selection.Create(GetRootPart().CoordinateSystems[0])
    result = Delete.Execute(selection)

    AllCordinateForRectangle = {}

    selection = Selection.Create(GetRootPart().GetChildren[IDocObject]()[-1])
    result = Delete.Execute(selection)
