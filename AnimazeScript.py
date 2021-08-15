bl_info = {
    "name": "Animaze Export",
    "blender": (2, 93, 0),
    "category": "Import-Export",
}


# This script was written by Agon Aion in order to expedite the process of exporting
# a model and its animations in the format supported by Animaze. This is the first
# script I've written using the blender API, so there may very well be some mistakes
# and issues with the formatting and logic. Additionally, I've really just been
# focusing on creating this to aid my model development, so I haven't really 
# implemented any safety/smart checks.

#   TO DO LIST:
#       Test and verify if the script works for blendshapes
#       Test and verify if the script works for non-scuffed textures
#       Test and verify if the script works for fur and other complex texture/mesh properties
#       Improve comments
#       Add properties to the file select window to allow user customization
#       Add various safety checks and dialogue boxes
#       Add keymapping

import bpy
import os

class AnimazeExportMenu(bpy.types.Operator):
    
    # Label and ID name of the top bar menu element
    bl_label = "Export for Animaze Avatar"
    bl_idname = "export.animaze"
    
    # Variable for containing the file path
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    
    # This checks to see if execute can be run
    @classmethod
    def poll(cls, context):
        return context.object is not None
    
    # Method to invoke the file select window
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
    # Method to export all animations in bulk
    def export_animations(self, filepath, objects):
        
        # Retrieve a list containing all actions/animations
        actions = bpy.data.actions
        
        # For every action/animation
        for act in actions:
            
            # For every object
            for obj in objects:
                
                # Set the animation data of the current object to the current action/animation
                if (obj.animation_data != None):
                    obj.animation_data.action = act
                
                
            # Export the animation fbx file
            bpy.ops.export_scene.fbx(
                filepath=os.path.join(filepath, act.name + ".fbx"),
                check_existing=True,
                use_selection=True,
                apply_unit_scale=True,
                use_space_transform=True,
                bake_space_transform=True,
                add_leaf_bones=False,
                use_armature_deform_only=True,
                bake_anim_use_nla_strips=False,
                bake_anim_use_all_actions=False,
                bake_anim_force_startend_keying=False,
                )
                
    # Function to export all textures of the model
    def export_textures(self, filepath):
        
        # Retrieve a list containing all images
        textures = bpy.data.images
        
        # Import copyfile function
        from shutil import copyfile
        
        # For every image in the image list
        for text in textures:
            
            # Determine the filepath to the image
            text_path = bpy.path.abspath(text.filepath, library=text.library)
            
            # Check to see if the file path is valid before copying the file into the Assets folder
            if os.path.isfile(text_path):
                copyfile(text_path, os.path.join(filepath, text.name + ".png"))
    
    
    # The main function of the script, called when the export animaze file selector window is executed
    def execute(self, context):
        
        # Create a directory with the filepath determined from the file selector window
        os.mkdir(self.filepath)
        
        # Record the name of the directory for use later
        base_file_name = os.path.basename(os.path.normpath(self.filepath))
        
        # Determine the filepath of the Animations and Assets folders
        animations_filepath = os.path.join(self.filepath, "Animations")
        assets_filepath = os.path.join(self.filepath, "Assets")
        
        # Create the Animation and Assets folder
        os.mkdir(animations_filepath)
        os.mkdir(assets_filepath)
        
        
        
        # Retrieve the view layer
        view_layer = bpy.context.view_layer

        # Retrieve current selected objects to restore once the exporting process is completed
        obj_active = view_layer.objects.active
        selection = bpy.context.selected_objects
        
        # Select all objects in the scene and record a list containing the selected objects
        bpy.ops.object.select_all(action='SELECT')
        objs = bpy.context.selected_objects
        
        # Export the main geometry file without any baked animations
        bpy.ops.export_scene.fbx(
                filepath=os.path.join(self.filepath, base_file_name + "Geometry.fbx"),
                check_existing=True,
                use_selection=True,
                apply_unit_scale=True,
                use_space_transform=True,
                bake_space_transform=True,
                add_leaf_bones=False,
                use_armature_deform_only=True,
                bake_anim=False,
                )
        
        # Export the Animations and Assets
        self.export_animations(animations_filepath, objs)
        self.export_textures(assets_filepath)
        
        
        
        # Deselect all objects in the scene
        bpy.ops.object.select_all(action='DESELECT')
        
        # Restore active objects to how they were before the export process
        view_layer.objects.active = obj_active

        # Restore selected objects
        for obj in selection:
            obj.select_set(True)
        
        # Return that the process is finished
        return {'FINISHED'}



# Function to call the AnimazeExportMenu operator    
def menu_func(self, context):
    self.layout.operator(AnimazeExportMenu.bl_idname)

# Function for registering the AnimazeExportMenu class
def register():
    bpy.utils.register_class(AnimazeExportMenu)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

# Function for unregistering the AnimazeExportMenu class    
def unregister():
    bpy.utils.unregister_class(AnimazeExportMenu)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

# This line allows for execution of the script in the editor    
if __name__ == "__main__":
    register()