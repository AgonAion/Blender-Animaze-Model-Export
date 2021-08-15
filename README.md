# Blender-Animaze-Model-Export
This is a Blender add-on that creates an export menu for easily exporting a model in the format used for Animaze.

This script was originally written by Agon Aion to be used in Blender 2.93.0 in order to help those developping models for Animaze.

Disclaimer: I personally would recommend not developing your model in Blender. The developers of Animaze use Maya, and Animaze itself is deveoped for Maya. While Blender is an incredibly powerful open source tool, it has shortcoming and nuances that make it quite frustrating to develop for Animaze in (I haven't tried creating in Maya as of this writing, so it may very well share all the same drawbacks).

Installation instructions:
1. Download the AnimazeExport.py script.
2. Start Blender 2.93.0 (May work with other versions as well)
3. Open the preferences menu by mousing over the top bar "Edit" tab and clicking "Preferences".
4. In the new menu, click on "Install" in the top right of the menu.
5. In the file selector, navigate to where the AnimazeExport.py file was downloaded, select it, and then click "Install Add-on" in the bottom right corner.
6. Now, back in the Preferences menu, make sure that the "Community" tab is highlighted and the "Enabled Add-ons only" check box is NOT checked.
7. Type "Animaze Export" into the search bar located in the top right corner. An element with the name "Import-Export: Animaze Export" should appear in the list.
8. Ensure that the check box beside this element is checked. If it is not, then do so by click on it.
9. Once the check box is highlighted, simply close the preferences menu and check to see if the ddd-on is working by hovering over the top bar menu "File" >> "Export" and seeing that "Export Model for Animaze" element is present in the dropdown menu.

Usage Instructions:
1. (Optional) Open the Blender System Console by mousing over the top drop down menu "Window" and clicking on "Toggle System Console". This will allow you to see the system console during the export operation, to see if Blender is still performing the export operations.
2. In the 3D Viewport of your loaded scene, make sure that the scene is in Object Mode. Any other mode will result in an error upon exporting.
3. CLick in the 3D Viewport and press the "A" key on your keyboard to select all objects in the scene.
4. Hover over the "File" drop down menu, hover over "Export", and then click "Export Model for Animaze".
5. In the file selector, navigate to the directory where you would like the folder containing the exported files to be created.
6. Write the name of your Avatar in the main field. The geometry file will inherit the name used here. (ex: Writing "AvatarAgon" will result in the folder being named "AvatarAgon" and the geometry file named "AvatarAgonGeometry.fbox".
7. Click "Export for Animaze Avatar".
8. Blender may freeze during the export process, as it does not like mass exporting of fbx files. However if you pulled the System Console up in step 1, you can monitor the process to ensure that it is still ongoing.
9. After some time, the export should be completed, indicated by "Export Complete." appearing in the console, or Blender unfreezing.
Note: I highly recommend performing some test exports with barebones animations and texturing. Depending on the number of animations, meshes, verteces, and textures, it may take much longer to complete the export procedure. See the "How it works" section below for further information of limitations

How it works:
This script is very simple. It utilizes the Blender API to retrieve the various elements needed for use in Animaze, and uses Python's "os" library to control naming and export destinations. Animations and Geometry are exported as .fbx files. Assets are explained in the "Export Assets:" section. 

Below is basic pseudocode of how the algorithm works immediately after the export process begins.

Make the directory at the chosen destination with the given name.
Record the file name.
Determine the filepath for the animations directory.
Determine the filepath for the assets directory.
Make both directories.
Record all active and selected objects pre-export.
Select all active objects in the scene.
Export .fbx with no animations into the main directory.
Export .fbx of all animations into Animations folder.
Copy textures into Assets folder.
Deselect all objectives.
Restore the selected objects from before export.



Below outlines some of the details regarding the exporting process of the geometry, animations, and assets:
Export Geometry:
  This just uses simple fbx export process of the scene with no baked animations.
  As of this writing, the export call is set to not support subdivision surfaces and to only use bone deformation.
  It is also set to use all space transform that Blender can apply. I'm not all that knowledgeable about what each of those does, but from the brief testing I've done, it seems to work well with Animaze.
  Additionally, the add leaf bones property is set to false.
  
Export Animations:
  This script only works with actions, which are accessed through bpy.data.actions.
  Blender doesn't actually let you export animations on their own, so what I ended up having to do was manually set each object's animation data to each action during each export.
  Some objects in the scene don't have animation data, so there is a check to make sure it has that attribute before assigning the animation data.
  Additionally, since I am only exporting each of the actions found in bpy.data.actions, I don't know if blendshape animaitons will export properly.
  The actual export call uses the same settings as geometry .fbx export, but with bake animations set to true and key all bones set to true.

Export Assets:
  This doesn't actually export the textures, so it might be broken for some models.
  All it actually does is find what is stored in bpy.data.images, finds there filepath if they have one, then copies them into the assets folder.
  This will definitely need to be tweaked and fixed.



Additional conext: 
I created this script mostly in order to aid the development of my own personal model, and given that my priority was not on developping a user-safe script, there are many caveats and issues with the way the script is as of this writing. I've done very little testing or usage checking. Additionally, because my model is extremely simple, I haven't used any of the more advanced features supported by Animaze like fur and complex texturing. The file selector menu is also extremely barebones, with no customization options given to the user. As of right now, I don't plan on improving this script, but once I've completed my debut and get into a good workflow, I will revisit this and make improvements. That being said, I have publicly uploaded this for anybody to make changes to. Feel free to improve it in any way you may want!
