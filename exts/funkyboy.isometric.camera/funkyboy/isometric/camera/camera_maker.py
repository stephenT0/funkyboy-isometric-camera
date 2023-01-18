import omni.kit.commands
import omni.usd
import omni.kit.undo
from pxr import Gf, Sdf, Usd, UsdGeom


# this file creates the camera, binds it to an Xform of the same name and places it into default position

class CameraMaker:
    def __init__(self) -> None:
        # Get the current stage, which is a container for all the data in a USD file
        self._stage:Usd.Stage = omni.usd.get_context().get_stage()
        # Create the camera
        self.Create_Camera()

    def Create_Camera(self):
        #Create an undo action for every command in this function
        with omni.kit.undo.group():
            # Check if a prim named "/World" already exists in the stage
            world_prim = self._stage.GetPrimAtPath("/World")
            # Create an if/else condition to check for a /World prim because we need a place to put our camera.
            # Default Omniverse stage come with a /World but we cannot guarantee that every stage does 
            if world_prim:
                # If it exists, print a message and proceed with the rest of the code
                print("/World prim exists.")
                # Get the next available path under "/World" to create the isometric camera
                self.geom_xform_path = Sdf.Path(omni.usd.get_stage_next_free_path(self._stage, "/World/Isometric_Camera", False))
                # Create a new Xform prim under the previously obtained path
                omni.kit.commands.execute('CreatePrimWithDefaultXform', prim_type='Xform', prim_path=str(self.geom_xform_path))
                # Create a new 'Camera' prim with the path and set the projection to orthographic
                omni.kit.commands.execute('CreatePrimWithDefaultXform',
                        prim_type='Camera',
                        attributes={"projection": UsdGeom.Tokens.orthographic})
                # Move the camera prim to the newly created xform
                omni.kit.commands.execute('MovePrim',
                        path_from='/World/Camera',
                        path_to='/World/Isometric_Camera/Isometric_Camera')            
            else:
                # If the '/World' prim does not exist, create it
                print("/World prim does not exist.")
                world_path = Sdf.Path("/World")
                world_prim = self._stage.DefinePrim(world_path)
                print("/World prim created.")
                # Get the next available path for the camera
                self.geom_xform_path = Sdf.Path(omni.usd.get_stage_next_free_path(self._stage, "/World/Isometric_Camera", False))
                # Create a new 'Xform' prim with the path  
                omni.kit.commands.execute('CreatePrimWithDefaultXform', prim_type='Xform', prim_path=str(self.geom_xform_path))
                # Create a new 'Camera' prim with the path and set the projection to orthographic
                omni.kit.commands.execute('CreatePrimWithDefaultXform',
                        prim_type='Camera',
                        attributes={"projection": UsdGeom.Tokens.orthographic})
                # Move the camera prim to the specified path
                omni.kit.commands.execute('MovePrim',
                        path_from='/Camera',
                        path_to='/World/Isometric_Camera/Isometric_Camera')                          
            # Move Camera into default position 
            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Isometric_Camera/Isometric_Camera.xformOp:translate'),
                value=Gf.Vec3d(0.0, 0.0, 50000.0),
                prev=Gf.Vec3d(0.0, 0.0, 0.0))

            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Isometric_Camera/Isometric_Camera.horizontalAperture'),
                value=15000.0,
                prev=20.954999923706055)

            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Isometric_Camera/Isometric_Camera.verticalAperture'),
                value=5000.0,
                prev=15.290800094604492)

            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Isometric_Camera.xformOp:rotateXYZ'),
                value=Gf.Vec3d(-15.0, 25.600000381469727, 0.0),
                prev=Gf.Vec3d( 0.0, 0.0, 0.0))

            omni.kit.commands.execute('ChangeProperty',
                prop_path=Sdf.Path('/World/Isometric_Camera.xformOp:rotateXYZ'),
                value=Gf.Vec3d(-15.0, 45.0, 0.0),
                prev=Gf.Vec3d( 0.0, 25.600000381469727, 0.0))
