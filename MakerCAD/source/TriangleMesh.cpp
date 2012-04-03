#include "TriangleMesh.h"


TriangleMesh::TriangleMesh(Body& b) 
{
	TopoDS_Shape shape = b.get_shape_reference();
	BRepMesh::Mesh(shape, 0.01f);
	
	// <stolen>
    TopExp_Explorer Ex; 
    int index_offset = 0;
    for (Ex.Init(shape,TopAbs_FACE); Ex.More(); Ex.Next()) { 

        TopoDS_Face Face = TopoDS::Face(Ex.Current());
        TopLoc_Location Location = TopLoc_Location();
        Handle(Poly_Triangulation) facing = BRep_Tool::Triangulation(Face,Location);
 
        if (!facing.IsNull()) {
            TColgp_Array1OfDir normals(facing->Nodes().Lower(), facing->Nodes().Upper());
            Poly_Connect connect(facing);
            StdPrs_ToolShadedShape::Normal(Face, connect, normals);
            
            for (int i = 1; i <= facing->NbNodes(); ++i) {
                gp_Pnt vertex = facing->Nodes().Value(i);
                gp_Pnt transformedVtx = vertex.Transformed(Face.Location().Transformation());
                
                vertexbuffer.push_back(transformedVtx.X());
                vertexbuffer.push_back(transformedVtx.Y());
                vertexbuffer.push_back(transformedVtx.Z());
                
                vertexbuffer.push_back(normals(i).X());
                vertexbuffer.push_back(normals(i).Y());
                vertexbuffer.push_back(normals(i).Z());
            }
            
            for (int i = 1; i <= facing->NbTriangles(); ++i) {
                Poly_Triangle triangle = facing->Triangles().Value(i);
                Standard_Integer index1, index2, index3;
                
                if (Face.Orientation() == TopAbs_REVERSED) {
                    triangle.Get(index1, index3, index2);
                } else {
                    triangle.Get(index1, index2, index3);
                }
                
                elementbuffer.push_back(index_offset + index1 - 1);
                elementbuffer.push_back(index_offset + index2 - 1);
                elementbuffer.push_back(index_offset + index3 - 1);

            }
            
            index_offset += facing->NbNodes();    
        }
    }
	// </stolen>
}
