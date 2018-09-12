# -*- coding: utf-8 -*-
"""
Stimulus presentation for pRF mapping.

Present retinotopic mapping stimuli with Psychopy.

This version: Non-square visual field coverage, i.e. bar stimuli all over the
              screen.
"""

# Part of pyprf library
# Copyright (C) 2016  Marian Schneider & Ingo Marquardt
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import argparse
import numpy as np
import datetime
from psychopy import visual, event, core,  monitors, logging, gui, data, misc
from psychopy.misc import pol2cart
from itertools import cycle
from PIL import Image

# Width of monitor [pixels]:
varPixX = 1920  # [1920.0] for 7T scanner
# Height of monitor [pixels]:
varPixY = 1200  # [1200.0] for 7T scanner
strPthNpz = '/home/john/PhD/GitHub/pyprf/pyprf/stimulus_presentation/design_matrices/Run_01.npz'

# Orientation convention is like a clock: 0 is vertical, and positive values rotate clockwise. Beyond 360 and below zero values wrap appropriately.
# NOTE: can/should be float
# lstOri = [0, 45, 90, 135, 180, 225, 270, 315]
# NOTE: WARNING! in the old version, the following list was hard coded at
# some point, perhaps the order of orientation is actually taken from this
# separate, hard-coded list; -- see line 176 of old script
# [90, 45, 180, 135, 270, 225, 0, 315]


def prf_stim(dicParam):
    """
    Present stimuli for population receptive field mapping.

    If in logging mode, this script creates a stimulus log of the stimuli used
    for the pRF mapping that can be used for the pRF finding analysis of the
    pyprf library. The stimuli are saved as png files, where each png
    represents the status of visual stimulation for one TR (the png files
    contain modified screenshots of the visual stimulus, and can be directly be
    loaded into the py_pRF_mapping pipepline.
    """
    # *****************************************************************************
    # *** Experimental parameters (from dictionary)

    # Path of design matrix (npz):
    strPthNpz = dicParam['Path of design matrix (npz)']

    # Output path & file name of log file:
    strPthLog = dicParam['Output path (log files)']

    # Target duration [s]:
    varTrgtDur = dicParam['Target duration [s]']

    # Logging mode (logging mode is for creating files for analysis, not to be
    # used during an experiment).
    lgcLogMde = dicParam['Logging mode']

    # Frequency of stimulus bar in Hz:
    varGrtFrq = dicParam['Temporal frequency [Hz]']

    # Sptial frequency of stimulus (cycles per degree):             ### WARNING CHECK UNITS###
    varSptlFrq = dicParam['Spatial frequency [cyc/deg]']

    # Distance between observer and monitor [cm]:
    varMonDist = dicParam['Distance between observer and monitor [cm]']

    # Width of monitor [cm]:
    varMonWdth = dicParam['Width of monitor [cm]']

    # Width of monitor [pixels]:
    varPixX = dicParam['Width of monitor [pixels]']

    # Height of monitor [pixels]:
    varPixY = dicParam['Height of monitor [pixels]']

    # Background colour:
    varBckgrd = dicParam['Background colour [-1 to 1]']

    # *************************************************************************
    # *** Retrieve design matrix

    #        np.savez(strPthNpz,
    #                 aryDsg=aryDsg,
    #                 vecTrgt=vecTrgt,
    #                 lgcFull=lgcFull,
    #                 varTr=varTr,
    #                 varNumVol=varNumVol,
    #                 varNumOri=varNumOri,
    #                 varNumPos=varNumPos,
    #                 varNumTrgt=varNumTrgt,
    #                 varIti=varIti)

    # Load stimulus parameters from npz file.
    objNpz = np.load(strPthNpz)

    # Get design matrix (for bar positions and orientation):
    aryDsg = objNpz['aryDsg']

    # Number of volumes:
    varNumVol = aryDsg.shape[0]

    # Vector with times of target events:
    vecTrgt = objNpz['vecTrgt']

    # Number of target events:
    varNumTrgt = vecTrgt.shape[0]

    # Full screen mode? If no, bar stimuli are restricted to a central square.
    # If yes, bars appear on the entire screen. This parameter is set when
    # creating the design matrix.
    lgcFull = bool(objNpz['lgcFull'])

    # Number of volumes:
    # varNumVol = int(objNpz['varNumVol'])

    # Number of bar positions:
    # varNumPos = int(objNpz['varNumPos'])

    # Number of orientation:
    # varNumOri = int(objNpz['varNumOri'])

    # Number of target events:
    # varNumTrgt = int(objNpz['varNumTrgt'])

    # Average inter-trial interval for target events:
    # varIti = float(objNpz['varIti'])

    # If in logging mode, only present stimuli very briefly:
    if lgcLogMde:
        # Note: If 'varTr' is set too low in logging mode, frames are
        # dropped and the stimuli do not get logged properly.
        varTr = 0.2
    # Otherwise, use actual volume TR:
    else:
        # Volume TR:
        varTr = float(objNpz['varTr'])

    # *************************************************************************
    # *** Logging

    # Set clock:
    objClck = core.Clock()

    # Set clock for logging:
    logging.setDefaultClock(objClck)

    # Create a log file and set logging verbosity:
    fleLog = logging.LogFile(strPthLog, level=logging.DATA)

    # Log stimulus parameters:
    fleLog.write('Log file path: ' + strPthLog + '\n')
    fleLog.write('Design matrix: ' + strPthNpz + '\n')
    fleLog.write('Full screen: ' + str(lgcFull) + '\n')
    fleLog.write('Volume TR [s]: ' + str(varTr) + '\n')
    fleLog.write('Frequency of stimulus bar in Hz: ' + str(varGrtFrq) + '\n')
    fleLog.write('Sptial frequency of stimulus (cycles per degree): '
                 + str(varSptlFrq) + '\n')
    fleLog.write('Distance between observer and monitor [cm]: '
                 + str(varMonDist) + '\n')
    fleLog.write('Width of monitor [cm]: ' + str(varMonWdth) + '\n')
    fleLog.write('Width of monitor [pixels]: ' + str(varPixX) + '\n')
    fleLog.write('Height of monitor [pixels]: ' + str(varPixY) + '\n')
    fleLog.write('Background colour [-1 to 1]: ' + str(varBckgrd) + '\n')
    fleLog.write('Target duration [s]: ' + str(varTrgtDur) + '\n')
    fleLog.write('Logging mode: ' + str(lgcLogMde) + '\n')

    # Set console logging verbosity:
    logging.console.setLevel(logging.WARNING)

    # *************************************************************************
    # *** Prepare behavioural response logging

    # Switch target (show target or not?):
    varSwtTrgt = 0

    # Switch that is used to control the logging of target events:
    varSwtTrgtLog = 1

    # Control the logging of participant responses:
    varSwtRspLog = 0

    # The key that the participant has to press after a target event:
    strTrgtKey = '1'

    # Counter for correct/incorrect responses:
    varCntHit = 0  # Counter for hits
    varCntMis = 0  # Counter for misses

    # Time (in seconds) that participants have to respond to a target event in
    # order for the event to be logged as a hit:
    varHitTme = 2.0

    # *************************************************************************
    # *** Setup

    # Create monitor object:
    objMon = monitors.Monitor('Screen_7T_NOVA_32_Channel_Coil',
                              width=varMonWdth,
                              distance=varMonDist)

    # Set size of monitor:
    objMon.setSizePix([varPixX, varPixY])

    # Set screen:
    objWin = visual.Window(
        size=(varPixX, varPixY),
        screen=0,
        winType='pyglet',  # winType : None, ‘pyglet’, ‘pygame’
        allowGUI=False,
        allowStencil=True,
        fullscr=True,
        monitor=objMon,
        color=varBckgrd,
        colorSpace='rgb',
        units='deg',
        blendMode='avg'
        )

    # *************************************************************************
    # *** Prepare stimulus properties

    # The area that will be covered by the bar stimulus depends on whether
    # presenting in full screen mode or not. If in full screen mode, the
    # entire width of the screen will be covered. If not, a central square
    # with a side length equal to the screen height will be covered.
    if lgcFull:
        varPixCov = varPixX
    else:
        varPixCov = varPixY

    # Convert size in pixels to size in degrees (given the monitor settings):
    varDegCover = misc.pix2deg(varPixCov, objMon)

    # The thickness of the bar stimulus depends on the size of the screen to
    # be covered, and on the number of positions at which to present the bar.
    # Bar thickness in pixels:
    varThckPix = float(varPixCov) / float(varNumPos)
    # Bar thickness in degree:
    varThckDgr = misc.pix2deg(varThckPix, objMon)

    # Offset of the bar stimuli. The bar stimuli should cover the screen area,
    # without extending beyond the screen. Because their position refers to
    # the centre of the bar, we need to limit the extend of positions at the
    # edge of the screen by an offset, Offset in pixels:
    varOffsetPix = varThckPix / 2.0

    # Maximum bar position in pixels, with respect to origin at centre of
    # screen:
    varPosMaxPix = float(varPixCov) / 2.0 - float(varOffsetPix)


    # Array of possible bar positions (displacement relative to origin at
    # centre of the screen) in pixels:
    vecPosPix = np.linspace((-varPosMaxPix), varPosMaxPix, varNumPos)



    # Vectors with as repititions of orientations and positions, so that there
    # is one unique combination of position & orientation for all positions
    # and orientations:
    # vecOriRep = np.repeat(lstOri, varNumPos)
    # vecPosPixRep = np.tile(vecPosPix, varNumOri)

    # Convert from polar to cartesian coordinates.
    # theta, radius = pol2cart(x, y, units=’deg’)
    # vecTheta, vecRadius = pol2cart(vecOriRep, vecPosPixRep, units='deg')

    # lstPosPix = []
    # for ori in lstOri:
    #     temp = zip(*pol2cart(np.tile(ori, varNumPos), vecPosPix))
    #     lstPosPix.append(temp)

    # Bar stimulus size (length & thickness), in pixels:
    tplBarSzePix = (int(varPixCov), int(varThckPix))

    # Bar stimulus spatial frequency (in x & y directions):
    tplBarSf = (float(varSptlFrq) / varThckPix,
                float(varSptlFrq) / varThckPix)

    # *************************************************************************
    # *** Stimuli

    # TODO: varPixCov = varPix

    # Bar stimulus:
    objBar = visual.GratingStim(
        objWin,
        tex='sqrXsqr',
        color=[1.0, 1.0, 1.0],
        colorSpace='rgb',
        opacity=1.0,
        size=tplBarSzePix,
        sf=tplBarSf,
        ori=0.0,
        autoLog=False,
        interpolate=False,
        units='pix'                           ##############CHECK###################
        )

    # Fixation dot:
    objFixDot = visual.Circle(
        objWin,
        radius=2.0,
        fillColor=[1.0, 0.0, 0.0],
        lineColor=[1.0, 0.0, 0.0],
        autoLog=False,
        units='pix')                           ##############CHECK###################

    # Fixation dot surround:
    objFixSrr = visual.Circle(
        objWin,
        radius=7.0,
        fillColor=[0.5, 0.5, 0.0],
        lineColor=[0.0, 0.0, 0.0],
        autoLog=False,
        units='pix')                           ##############CHECK###################

    # Fixation grid circle:
    objGrdCrcl = visual.Polygon(
        win=objWin,
        edges=90,
        ori=0.0,
        pos=[0, 0],
        lineWidth=2,
        lineColor=[1.0, 1.0, 1.0],
        lineColorSpace='rgb',
        fillColor=None,
        fillColorSpace='rgb',
        opacity=1.0,
        autoLog=False,
        interpolate=True,
        units='deg')

    # Fixation grid line:
    objGrdLne = visual.Line(
        win=objWin,
        autoLog=False,
        name='Line',
        start=(-varPixY, 0),
        end=(varPixY, 0),
        pos=[0, 0],
        lineWidth=2,
        lineColor=[1.0, 1.0, 1.0],
        lineColorSpace='rgb',
        fillColor=None,
        fillColorSpace='rgb',
        opacity=1,
        interpolate=True,)

    if not(lgcFull):
        # List with aperture coordinates (used to cover left and right side of
        # the screen when not in full-screen mode). List of tuples.
        lstAptrCor = [(varPixCov / 2, varPixCov / 2),
                      (-varPixCov / 2, varPixCov / 2),
                      (-varPixCov / 2, -varPixCov / 2),
                      (varPixCov / 2, -varPixCov / 2)]

        # Aperture for covering left and right side of screen if not
        # stimulating full screen.
        objAprtr = visual.Aperture(objWin,
                                   autoLog=False,
                                   shape=lstAptrCor)
        objAprtr.enabled = False

    # *************************************************************************
    # *** Logging mode preparations

    if lgcLogMde:

        print('Logging mode')

        # Calculate area to crop in y-dimension, at top and bottom (should be zero
        # is # full extend of screeen height is used):
        varCrpY = int(np.around((float(varPixY) - float(varPix)) * 0.5))

        print(('Stimulus log will be cropped by '
               + str(varCrpY)
               + ' in y-direction (screen height).'
               ))

        # Calculate area to crop in x-dimension, at left and right (would be zero
        # is full extend of screeen width was used):
        varCrpX = int(np.around((float(varPixX) - float(varPix)) * 0.5))

        print(('Stimulus log will be cropped by '
               + str(varCrpX)
               + ' in x-direction (screen width).'
               ))

        # Temporary array for screenshots, at full screen size and containing RGB
        # values (needed to obtain buffer content from psychopy):
        aryBuff = np.zeros((varPixY, varPixX, 3), dtype=np.int16)

        # Prepare array for screenshots. One value per pixel per volume; since the
        # stimuli are greyscale we discard 2nd and 3rd RGB dimension. Also, there
        # is no need to represent the entire screen, just the part of the screen
        # that is actually stimulated (this is typically a square at the centre of
        # the screen, flanked by unstimulated areas on the left and right side).
        aryFrames = np.zeros((varPixY, varPixX, varNumVol), dtype=np.int16)

        # Make sure that varPix is of interger type:
        varPix = int(np.around(varPix))

        # Counter for screenshots:
        idxFrame = 0

    # *************************************************************************
    # *** Timing & switches

    # Target counter:
    varCntTrgt = 0

    # Time of the first target event:
    varTmeTrgt = vecTrgt[varCntTrgt]

    # Switch for grating polarity flicker:
    varSwtGrt = 0

    # The input parameter 'varGrtFrq' gives the grating flicker frequency in
    # Hz. We need to convert to second:
    varGrtDur = 1.0 / float(varGrtFrq)

    # *************************************************************************
    # *** Presentation

    if not(lgcLogMde):

        # Draw fixation dot & surround:
        objFixDot.draw(win=objWin)
        objFixSrr.draw(win=objWin)

        # Draw fixation grid:
        objGrdCrcl.draw(win=objWin)
        objGrdLne.draw(win=objWin)

        objWin.flip()

        # Hide the mouse cursor:
        event.Mouse(visible=False)

        # Wait for scanner trigger pulse & set clock after receiving trigger
        # pulse (scanner trigger pulse is received as button press ('5')):
        strTrgr = ['0']
        while strTrgr[0][0] != '5':
            # Check for keypress:
            lstTmp = event.getKeys(keyList=['5'], timeStamped=False)
            # Whether the list has the correct length (if nothing has happened,
        # lstTmp # will have length zero):
            if len(lstTmp) == 1:
                strTrgr = lstTmp[0][0]

    # Trigger pulse received, reset clock:
    objClck.reset(newT=0.0)

    # Main timer which represents the starting point of the experiment:
    varTme01 = objClck.getTime()

    # Time that is updated continuously to track time:
    varTme02 = objClck.getTime()

    # Timer used to control the logging of stimulus events:
    varTme03 = objClck.getTime()

    # Timer for grating stimulus polarity flicker:
    varTme04 = objClck.getTime()

    # Start of the experiment:
    for idxVol in range(varNumVol):  #noqa

        # Show a grating during this volume?
        lgcOn = (aryDsg[idxVol, 0] == 1.0)

        # If a grating is shown, which orientation, position, and contrast?
        if lgcOn:

            # Timer for grating stimulus polarity flicker:
            varTme04 = objClck.getTime()

            # Get stimulus properties from design matrix:
            varTmpPos = aryDsg[idxVol, 1]
            varTmpOri = aryDsg[idxVol, 2]
            varTmpCon = aryDsg[idxVol, 3]

            # Set bar properties:
            objBar.setPos(varTmpPos)
            objBar.setOri(varTmpOri)
            # TODO : set bar contrast

        # Still on the same volume?
        while varTme02 < (varTme01 + (float(idxVol + 1) * varTr)):

            # Update timer:
            varTme02 = objClck.getTime()

            # *****************************************************************
            # *** Target control

            # Time for target?
            if ((varTmeTrgt <= varTme02)
                    and (varTme02 <= (varTmeTrgt + varTrgtDur))):

                varSwtTrgt = 1

            else:

                # Was the target just on?
                if varSwtTrgt == 1:

                        # Switch on the logging of the target event (so that
                        # the next target event will be logged):
                        varSwtTrgtLog = 1

                        # Only increase the counter if the last target has not
                        # been reached yet:
                        if (varCntTrgt + 1) < varNumTrgt:

                            # Increase the target counter:
                            varCntTrgt = varCntTrgt + 1

                            # Time of next target event:
                            varTmeTrgt = vecTrgt[varCntTrgt]

                # Switch the target off.
                varSwtTrgt = 0

            # Draw target?
            if varSwtTrgt == 1:

                    # Draw target:
                    objTarget.draw(win=objWin)
                    # objFixDot.fillColor = [0.0, 0.0, 1.0]

                    # Log target?
                    if varSwtTrgtLog == 1:

                        # Log target event:
                        strTmp = ('TARGET scheduled for: '
                                  + str(varTmeTrgt))
                        logging.data(strTmp)

                        # Switch off (so that the target event is only logged
                        # once):
                        varSwtTrgtLog = 0

                        # Once after target onset we set varSwtRspLog to
                        # one so that the participant's respond can be logged:
                        varSwtRspLog = 1

                        # Likewise, just after target onset we set the timer
                        # for response logging to the current time so that the
                        # response will only be counted as a hit in a specified
                        # time interval after target onset:
                        varTme03 = objClck.getTime()

            # Check for and log participant's response:
            lstRsps = event.getKeys(keyList=[strTrgtKey], timeStamped=False)

            # Has the response not been reported yet, and is it still within
            # the time window?
            if (varSwtRspLog == 1) and (varTme02 <= (varTme03 + varHitTme)):

                # Check whether the list has the correct length:
                if len(lstRsps) == 1:

                    # Does the list contain the response key?
                    if lstRsps[0] == strTrgtKey:

                        # Log hit:
                        logging.data('Hit')

                        # Count hit:
                        varCntHit += 1

                        # After logging the hit, we have to switch off the
                        # response logging, so that the same hit is nor logged
                        # over and over again:
                        varSwtRspLog = 0

            elif (varSwtRspLog == 1) and (varTme02 > (varTme03 + varHitTme)):

                # Log miss:
                logging.data('Miss')

                # Count miss:
                varCntMis += 1

                # If the subject does not respond to the target within time, we
                # log this as a miss and set varSwtRspLog to zero (so that the
                # response won't be logged as a hit anymore afterwards):
                varSwtRspLog = 0

            # *****************************************************************
            # *** Grating control

            # Set grating polarity:
            if varSwtGrt == 0:
                # TODO : set polarity

            else:
                # TODO : set reverse polarity

            # Change grating polarity:
            if (varTme04 + varGrtDur) <= varTme02:
                if varSwtGrt == 0:
                    varSwtGrt = 1
                else:
                    varSwtGrt = 0

            # Draw grating?
            if lgcOn:
                objBar.draw(win=objWin)

            if not(lgcLogMde):

                # Flip drawn objects to screen:
                objWin.flip()

            # Check whether exit keys have been pressed:
            if func_exit() == 1:
                break

            # Update current time:
            varTme02 = objClck.getTime()

    # *************************************************************************
    # *** Feedback

    logging.data('------End of the experiment.------')

    # Performance feedback only if there were any targets:
    if 0.0 < float(varCntHit + varCntMis):

        # Ratio of hits:
        varHitRatio = float(varCntHit) / float(varCntHit + varCntMis)

        # Present participant with feedback on her target detection
        # performance:
        if 0.99 < varHitRatio:
            # Perfect performance:
            strFeedback = ('You have detected '
                           + str(varCntHit)
                           + ' targets out of '
                           + str(varCntHit + varCntMis)
                           + '\n'
                           + 'Keep up the good work :)')
        elif 0.9 < varHitRatio:
            # OKish performance:
            strFeedback = ('You have detected '
                           + str(varCntHit)
                           + ' targets out of '
                           + str(varCntHit + varCntMis)
                           + '\n'
                           + 'There is still room for improvement.')
        else:
            # Low performance:
            strFeedback = ('You have detected '
                           + str(varCntHit)
                           + ' targets out of '
                           + str(varCntHit + varCntMis)
                           + '\n'
                           + 'Please try to focus more.')

        # Create text object:
        objTxtTmr = visual.TextStim(objWin,
                                    text=strFeedback,
                                    font="Courier New",
                                    pos=(0.0, 0.0),
                                    color=(1.0, 1.0, 1.0),
                                    colorSpace='rgb',
                                    opacity=1.0,
                                    contrast=1.0,
                                    ori=0.0,
                                    height=0.5,
                                    antialias=True,
                                    alignHoriz='center',
                                    alignVert='center',
                                    flipHoriz=False,
                                    flipVert=False,
                                    autoLog=False)

        # Show feedback text:
        varTme04 = objClck.getTime()
        while varTme02 < (varTme04 + 3.0):
            objTxtTmr.draw()
            objWin.flip()
            varTme02 = objClck.getTime()

        # Log total number of hits and misses:
        logging.data(('Number of hits: ' + str(varCntHit)))
        logging.data(('Number of misses: ' + str(varCntMis)))
        logging.data(('Percentage of hits: '
                      + str(np.around((varHitRatio * 100.0), decimals=1))))

    # *************************************************************************
    # *** End of the experiment

    # Make the mouse cursor visible again:
    event.Mouse(visible=True)

    # Close everyting:
    objWin.close()
    core.quit()
    monitors.quit()
    logging.quit()
    event.quit()

    # *************************************************************************
    # *** Logging mode

    # Save screenshots (logging mode):
    if lgcLogMde:

        print('Saving screenshots')

        # Target directory for frames (screenshots):
        strPthFrm = (dataFolderName + os.path.sep + 'Frames')

        # Check whether directory for frames exists, if not create it:
        lgcDir = os.path.isdir(strPthFrm)
        # If directory does not exist, create it:
        if not(lgcDir):
            # Create direcotry for segments:
            os.mkdir(strPthFrm)

        # Save stimulus frame array to npy file:
        aryFrames = aryFrames.astype(np.int16)
        np.savez_compressed((strPthFrm
                             + os.path.sep
                             + 'stimFramesRun'
                             + dicExp['run']),
                            aryFrames=aryFrames)

        # Maximum intensity of output PNG:
        varScle = 255

        # Rescale array:
        aryFrames = np.logical_or(np.equal(aryFrames, np.min(aryFrames)),
                                  np.equal(aryFrames, np.max(aryFrames))
                                  )
        aryFrames = np.multiply(aryFrames, varScle)
        aryFrames = aryFrames.astype(np.uint8)

        # Loop through volumes and save PNGs:
        for idxVol in range(varNumVol):

            print(('---Frame '
                  + str(idxVol)
                  + ' out of '
                  + str(int(varNumVol))))

            # Create image: TODO: compatibility with new Pillow version?
            im = Image.fromarray(aryFrames[:, :, idxVol])

            # File name (with leading zeros, e.g. '*_004' or '*_042'). For
            # consistency with earlier versions, the numbering of frames (PNG
            # files  corresponding to fMRI volumes) starts at '1' (not at '0').
            strTmpPth = (strPthFrm
                         + os.path.sep
                         + 'run_'
                         + dicExp['run']
                         + '_frame_'
                         + str(idxVol + 1).zfill(3)
                         + '.png')

            # Save image to disk:
            im.save(strTmpPth)

            # aryRgb = np.swapaxes(aryRgb, 0, 1)
            # aryRgb = np.swapaxes(aryRgb, 1, 2)

# *****************************************************************************
# *** Function definitions


def func_exit():
    """
    Check whether exit-keys have been pressed.

    The exit keys are 'e' and 'x'; they have to be pressed at the same time.
    This is supposed to make it less likely that the experiment is aborted
    by accident.
    """
    # Check keyboard, save output to temporary string:
    lstExit = event.getKeys(keyList=['e', 'x'], timeStamped=False)

    # Whether the list has the correct length (if nothing has happened lstExit
    # will have length zero):
    if len(lstExit) != 0:

        if ('e' in lstExit) and ('x' in lstExit):

            # Log end of experiment:
            logging.data('------Experiment aborted by user.------')

            # Make the mouse cursor visible again:
            event.Mouse(visible=True)

            # Close everyting:
            objWin.close()
            core.quit()
            monitors.quit()
            logging.quit()
            event.quit()

            return 1

        else:
            return 0

    else:
        return 0


# *****************************************************************************

if __name__ == "__main__":

    # *************************************************************************
    # *** GUI

    # Create parser object:
    objParser = argparse.ArgumentParser()

    # Add argument to namespace - open a GUI for user to specify design matrix
    # parameters?:
    objParser.add_argument('-gui',
                           # metavar='GUI',
                           choices=['True', 'False'],
                           default='True',
                           help='Open a GUI to set parameters for design \
                                 matrix?'
                           )

    # Add argument to namespace - open a GUI for user to specify design matrix
    # parameters?:
    objParser.add_argument('-filename',
                           # metavar='filename',
                           default=None,
                           help='Optional. Output file name for design \
                                 matrix. The  output file name can also be \
                                 set in the GUI.'
                           )

    # Namespace object containing arguments and values:
    objNspc = objParser.parse_args()

    # Get arguments from argument parser:
    strGui = objNspc.gui
    strFleNme = objNspc.filename

    # Dictionary with experiment parameters.
    dicParam = {'Run (name of design matrix file)': 'Run_01',
                'Target duration [s]': 0.3,
                'Logging mode': [False, True],
                'Temporal frequency [Hz]': 4.0,
                'Spatial frequency [cyc/deg]': 1.5,    ### WARNING CHECK UNITS###
                'Distance between observer and monitor [cm]': 99.0,
                'Width of monitor [cm]': 30.0,
                'Width of monitor [pixels]': 1920,
                'Height of monitor [pixels]': 1200,
                'Background colour [-1 to 1]': 0.7}

    if not(strFleNme is None):

        # If an input file name is provided, put it into the dictionary (as
        # default, can still be overwritten by user).
        dicParam['Output file name'] = strFleNme

    if strGui == 'True':

        # Pop-up GUI to let the user select parameters:
        objGui = gui.DlgFromDict(dictionary=dicParam,
                                 title='Design Matrix Parameters')

    # Start experiment if user presses 'ok':
    if objGui.OK is True:

        # Get date string as default session name:
        strDate = str(datetime.datetime.now())
        lstDate = strDate[0:10].split('-')
        lstTime = strDate[11:19].split(':')
        strDate = (lstDate[0] + lstDate[1] + lstDate[2] + '_' + lstTime[0]
                   + lstTime[1] + lstTime[2])

        # Path of parent directory:
        strPth = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        # Output path ('~/pyprf/pyprf/stimulus_presentation/design_matrices/'):
        strPthOut = os.path.join(strPth,
                                 'log',
                                 (dicParam['Output file name']
                                  + strDate
                                  + '.txt')
                                 )

        # Add output path to dictionary.
        dicParam['Output path (log files)'] = strPthOut

        # Path of design matrix file (npz):
        strPthNpz = os.path.join(strPth,
                                 'design_matrices',
                                 (dicParam['Run (name of design matrix file)']
                                  + '.npz')
                                 )

        # Add path of design matrix (npz file) to dictionary.
        dicParam['Path of design matrix (npz)'] = strPthNpz

        prf_stim(dicParam)

    else:

        # Close GUI if user presses 'cancel':
        core.quit()
