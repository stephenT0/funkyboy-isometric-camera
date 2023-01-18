import omni.ext
import omni.ui as ui
import omni.kit.commands
import omni.usd
from .camera_maker import CameraMaker
from omni.kit.widget.viewport import ViewportWidget
from pxr import Gf, Sdf

# this file controls all ui elements and

WINDOW_TITLE = "Isometric Camera"

SPACING = 4

class IsometricCameraWindow(ui.Window):
    def __init__(self, title, menu_path):
        # call the super class init method and set the window's title and size
        super().__init__(title, width=450, height=200)
        # dock the extension besides the enviornments tab
        super().dock_in_window("Environments", ui.DockPosition.SAME) 
        # store the menu path passed as an argument
        self._menu_path = menu_path
        # set a function that will be called when the window's visibility changes
        self.set_visibility_changed_fn(self._on_visibility_changed)
        # set a function that will be called to build the window
        self.frame.set_build_fn(self._build_window)
        # flag to keep track if a camera has been created
        self.camera_created = False
        # flag to keep track of the camera's current projection
        self.is_isometric = False

    def _build_window(self):
        # Create a scrolling frame
        with ui.ScrollingFrame():
            # Create a vertical stack layout
            with ui.VStack(height=0):
                # Define a function for creating a camera 
                def on_create_camera():
                    #calling on the CamerMaker function from .camera_maker
                    CameraMaker()
                    # Set the camera created flag to True
                    self.camera_created = True
                    # Set the build function to the one for when a camera has been created
                    self.frame.set_build_fn(self._build_window_camera_created)
                # Create a horizontal stack layout
                with ui.HStack(height=0, spacing=SPACING):
                    # Create a label "Start Here: "
                    ui.Label("Start Here: ", height=40, width=0)
                    # Create a button with the text "Create Camera" and call the on_create_camera function when clicked
                    ui.Button("Create Camera", clicked_fn=on_create_camera)

    def _build_window_camera_created(self):
        with ui.ScrollingFrame():
            with ui.VStack(height=0):
                def on_switch_camera():
                    # Get the active viewport
                    from omni.kit.viewport.utility import get_active_viewport
                    viewport = get_active_viewport()
                    # Check if there is no active viewport and raise an error if there isn't
                    if not viewport:
                        raise RuntimeError("No active Viewport")
                    # make button switch to isometric camera
                    if not self.is_isometric:
                        viewport.camera_path = ("/World/Isometric_Camera/Isometric_Camera")
                        self.is_isometric = True
                    # make button switch to Omniverse default perspective view 
                    else:
                        viewport.camera_path = ('/OmniverseKit_Persp')
                        self.is_isometric = False
                # Create UI Buttons to switch perspective
                with ui.HStack(height=0, spacing=SPACING):
                    ui.Label("Camera Created: ", height=40, width=0)
                    ui.Button("Switch Perspective", clicked_fn=on_switch_camera, label=self.get_button_label())
                # with ui.HStack(height=0, spacing=SPACING):
                #     ui.Label("Current camera: ", height=40, width=0)
                #     ui.Label("Isometric Camera" if self.is_isometric else "Perspective Camera", id="current_camera")
            
             
                #create a simple float value that can be bound to a UI
                self._slider_model_x = ui.SimpleFloatModel()
                self._slider_model_y = ui.SimpleFloatModel()
                self._slider_model_zoom = ui.SimpleFloatModel()
                self._source_prim_model = ui.SimpleStringModel()

                #variable that holds the current rotation value on the x-axis
                current_rotation_x = -15.0
                #variable that holds the current rotation value on the y-axis
                current_rotation_y = 45.0
                #variable that holds the current zoom value of the camera
                current_zoom = 15000


                ui.Spacer(width=0,height=0)
                # Create Ui elements to control the camera
                with ui.CollapsableFrame("Camera Controls", name="group", height=100,):
                    with ui.VStack(height=0, spacing=SPACING):
                        with ui.HStack():
                            ui.Spacer(width=5)
                            ui.Label(" Rotate Up-Down: ", height=0, width=0)
                            ui.FloatSlider(self._slider_model_x,  min=0, max=-90, step=0.5,
                            style={
                        "draw_mode": ui.SliderDrawMode.HANDLE,
                        })   

                        # This function updates the rotation of the camera on the x-axis    
                        def update_rotate_x(prim_name, value, current_rotation_x):
                            # Update the current rotation value
                            current_rotation_x = value
                            # Get the current USD context
                            usd_context = omni.usd.get_context()
                            # Get the stage from the context
                            stage = usd_context.get_stage()
                            # Get the xform prim at the path "/World/Isometric_Camera"
                            xform_prim = stage.GetPrimAtPath("/World/Isometric_Camera")
                            # Get the "xformOp:rotateXYZ" attribute from the xform prim
                            rotate_attr = xform_prim.GetAttribute("xformOp:rotateXYZ")
                            # Get the current rotation values
                            rotate = rotate_attr.Get()
                            # Set the rotation values to the new x rotation, the current y rotation, and the current z rotation
                            rotate_attr.Set(Gf.Vec3d(current_rotation_x, rotate[1], rotate[2]))
                        # Set Slider to the new value
                        if self._slider_model_x:
                            # Set the self._slider_subscription_x to None
                            self._slider_subscription_x = None
                            # Set the value of the self._slider_model_x to the current rotation value
                            self._slider_model_x.as_float = current_rotation_x
                            # Subscribe to the value changed function of self._slider_model_x and pass in the update_rotate_x function
                            self._slider_subscription_x = self._slider_model_x.subscribe_value_changed_fn(lambda m, p=self._source_prim_model, c=current_rotation_x: update_rotate_x(p, m.as_float, c))
                        # UI Elements for rotate Y
                        
                        with ui.HStack():
                            ui.Spacer(width=10)
                            ui.Label("Rotate Side-to-Side", height=0, width=0)
                            ui.Spacer(width=5)
                            ui.FloatSlider(self._slider_model_y, min=-180, max=180)
                            ui.Spacer(width=10)
                        # This function updates the rotation of the camera on the Y-axis     
                        def update_rotate_y(prim_name, value, current_rotation_y):
                            current_rotation_y = value
                            # Get the current USD context
                            usd_context = omni.usd.get_context()
                            # Get the stage from the context
                            stage = usd_context.get_stage()
                            # Get the xform prim at the path "/World/Isometric_Camera"
                            xform_prim = stage.GetPrimAtPath("/World/Isometric_Camera")
                            # Get the "xformOp:rotateXYZ" attribute from the xform prim                           
                            rotate_attr = xform_prim.GetAttribute("xformOp:rotateXYZ")
                            # Get the current rotation values
                            rotate = rotate_attr.Get()
                            # Set the rotation values to the new y rotation, the current x rotation, and the current z rotation
                            rotate_attr.Set(Gf.Vec3d(rotate[0], current_rotation_y, rotate[2]))
                        # Set Slider to the new value
                        if self._slider_model_y:
                            # Set the self._slider_subscription_y to None
                            self._slider_subscription_y = None
                            # Set the value of the self._slider_model_x to the current rotation value
                            self._slider_model_y.as_float = current_rotation_y
                            # Subscribe to the value changed function of self._slider_model_x and pass in the update_rotate_y function
                            self._slider_subscription_y = self._slider_model_y.subscribe_value_changed_fn(lambda m, p=self._source_prim_model, c=current_rotation_y: update_rotate_y(p, m.as_float, c))
                        # UI elements for Zoom slider        
                        with ui.HStack():
                            ui.Spacer(width=10)
                            ui.Label(" Zoom in and Out", height=0, width=0)
                            ui.Spacer(width=5)
                            ui.FloatSlider(self._slider_model_zoom, min=1000, max=50000)
                            ui.Spacer(width=10)
                        # Function updates the value of the zoom attribute of the camera.
                        def update_zoom(prim_name, value, current_zoom):
                            current_zoom = value
                            # Get the context of the USD stage
                            usd_context = omni.usd.get_context()
                            # Get the stage
                            stage = usd_context.get_stage()
                            # Get the camera primitive at the specified path
                            camera_prim = stage.GetPrimAtPath("/World/Isometric_Camera/Isometric_Camera")
                            # Get the zoom attribute of the camera primitive
                            zoom_attr = camera_prim.GetAttribute("horizontalAperture")
                            # Set the value of the zoom attribute to the new value
                            zoom_attr.Set(float(current_zoom))

                        if self._slider_model_zoom:
                            self._slider_subscription_zoom = None
                            self._slider_model_zoom.as_float = current_zoom
                            self._slider_subscription_zoom = self._slider_model_zoom.subscribe_value_changed_fn(lambda m, p=self._source_prim_model, c=current_zoom: update_zoom(p, m.as_float, c))

                def on_reset():
                    # Delete the isometric camera and resets extension to default state 
                    omni.kit.commands.execute('DeletePrims', paths=["/World/Isometric_Camera", "/World/Isometric_Camera/Isometric_Camera" ])
                    self.camera_created = False
                    self.frame.set_build_fn(self._build_window)  
                with ui.HStack(height=0, spacing=SPACING):
                    ui.Label("Reset Extension: ", height=0, width=0)
                    ui.Button("Reset (Camera will be deleted)", clicked_fn=on_reset)        

    def get_button_label(self):
        return "Switch to Perspective Camera" if self.is_isometric else "Switch to Isometric Camera"

    def _on_visibility_changed(self, visible):
        omni.kit.ui.get_editor_menu().set_value(self._menu_path, visible)


    def destroy(self) -> None:
        self._change_info_path_subscription = None
        self._color_changed_subs = None
        return super().destroy()

    def on_shutdown(self):
        self._win = None

    def show(self):
        self.visible = True
        self.focus()    
    
    def hide(self):
        self.visible = False
   