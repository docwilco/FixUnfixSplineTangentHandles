#Author: Rogier "DocWilco" Mulhuijzen
#Description: This script will fix or unfix the tangent handles on all of the
#splines in the current sketch. Fixing is needed for scaling splines.

import adsk.core, adsk.fusion, adsk.cam, traceback
from enum import Enum

class FixUnfix(Enum):
    FIX = 1
    UNFIX = 2

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Get the active product (should be a Fusion Design)
        design = adsk.fusion.Design.cast(app.activeProduct)
        if design is None:
            ui.messageBox('Please run this script in the Design workspace.')
            return
        
        # Check if the active edit object is a sketch
        active_sketch = adsk.fusion.Sketch.cast(design.activeEditObject)
        if active_sketch is None:
            ui.messageBox('No sketch is currently being edited.')
            return

        # Get all fitted splines in the active sketch. Only fitted splines have
        # tangent handles, fixed splines do not.
        fitted_splines = active_sketch.sketchCurves.sketchFittedSplines

        fixed_handles = 0
        unfixed_handles = 0

        for spline in fitted_splines:
            spline = adsk.fusion.SketchFittedSpline.cast(spline)
            for point in spline.fitPoints:
                # Get the point
                point = adsk.fusion.SketchPoint.cast(point)
                # Get the tangent SketchLine for the point
                handle = adsk.fusion.SketchLine.cast(spline.getTangentHandle(point))
                # Some points don't have a tangent handle, just skip them
                if handle is not None:
                    if handle.isFixed:
                        fixed_handles += 1
                    else:
                        unfixed_handles += 1

        # Build the message box
        title = 'Fix Splines'
        action = FixUnfix.FIX
        if fixed_handles != 0 and unfixed_handles != 0:
            text = 'There are {} fixed and {} unfixed tangent handles, do you want to make them all fixed?'.format(fixed_handles, unfixed_handles)
            icon = adsk.core.MessageBoxIconTypes.QuestionIconType
            buttons = adsk.core.MessageBoxButtonTypes.YesNoButtonType
        elif fixed_handles == 0 and unfixed_handles == 0:
            text = 'There are no tangent handles at all, nothing to do.'
            icon = adsk.core.MessageBoxIconTypes.InformationIconType
            buttons = adsk.core.MessageBoxButtonTypes.OKButtonType
            ui.messageBox(text, title, buttons, icon)
            return
        elif fixed_handles != 0: # All handles are fixed
            action = FixUnfix.UNFIX
            text = 'Unfixing {} tangent handles.'.format(fixed_handles)
            icon = adsk.core.MessageBoxIconTypes.InformationIconType
            buttons = adsk.core.MessageBoxButtonTypes.OKCancelButtonType
        else: # All handles are unfixed
            text = 'Fixing {} tangent handles.'.format(unfixed_handles)
            icon = adsk.core.MessageBoxIconTypes.InformationIconType
            buttons = adsk.core.MessageBoxButtonTypes.OKCancelButtonType
        
        # Show the message box
        button = ui.messageBox(text, title, buttons, icon)

        # Options are OK, Cancel, Yes, No, Error. So we only proceed if OK or
        # Yes is pressed
        if button != adsk.core.DialogResults.DialogYes and button != adsk.core.DialogResults.DialogOK:
            return
        
        # Fix or unfix the tangent handles
        count = 0
        for spline in fitted_splines:
            spline = adsk.fusion.SketchFittedSpline.cast(spline)
            for point in spline.fitPoints:
                point = adsk.fusion.SketchPoint.cast(point)
                handle = adsk.fusion.SketchLine.cast(spline.getTangentHandle(point))
                if handle is not None:
                    if handle.isFixed and action == FixUnfix.UNFIX:
                        handle.isFixed = False
                        count += 1
                    elif not handle.isFixed and action == FixUnfix.FIX:
                        handle.isFixed = True
                        count += 1

        # Report the results
        ui.messageBox('Done. {} tangent handles {}.'.format(count, 'fixed' if action == FixUnfix.FIX else 'unfixed'))

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
