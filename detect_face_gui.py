import os
import sys
import time
import logging
from pprint import pprint
from collections import defaultdict
import qdarkstyle

from Qt import QtWidgets, QtGui, QtCore, QtCompat

from mtcnn import MTCNN

from point import Point
import loader
import nuke_node_builder as nnb

class MyApp():
    def __init__(self) -> None:
        TITLE = os.path.splitext(os.path.basename(__file__))[0]
        print(TITLE)
        #BUILD local ui path
        path_ui = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])
        path_img = os.path.dirname(__file__) + "/img/{}.jpg"

        self.execute_folder = os.path.dirname(__file__)
        self.sequence_directory = ''
        self.animated_crop = ''

        self.app = QtCompat.loadUi(path_ui)

        self.my_app = QtWidgets.QApplication.instance()
        self.clipboard = self.my_app.clipboard()

        self.my_app.setStyleSheet(qdarkstyle.load_stylesheet())        
        
        # set default values      
        self.app.lbl_folder_directory.setText(self.sequence_directory)
        self.app.lbl_face.setPixmap(QtGui.QPixmap(path_img.format('lbl_face')))

        # create connections
        self.app.btn_select_folder.clicked.connect(self.press_btnSelectFolder)
        self.app.btn_findFaces.clicked.connect(self.findFaces)
        self.app.btn_copy_to_clipboard.clicked.connect(self.press_btn_copy_to_clipboard)

        self.app.show()

    def press_btnSelectFolder(self):
        self.sequence_directory = QtWidgets.QFileDialog.getExistingDirectory(
            None, 
            "Select Folder To find Sequences", 
            self.execute_folder,)  

        self.app.lbl_folder_directory.setText(self.sequence_directory)
        log_msg = 'Sequence Folder is \n{}'.format(self.sequence_directory)
        self.app.txt_statusLog.appendPlainText(log_msg)

        ## update the sequences_list part now
        face = loader.FrameHandler(self.sequence_directory) 
        sequences = face.print_sequences()

        self.list = self.app.sequences_list
        for sequence in sequences:
                self.list.addItem(str(sequence))  

    def press_btn_copy_to_clipboard(self): 
        self.clipboard.setText(str(self.animated_crop))
    
    def findFaces(self):
        face = loader.FrameHandler(self.sequence_directory) 
        id_of_sequence = (self.app.sequences_list.currentRow())
        face.select_sequence(id_of_sequence)

        # create the detector, using default weights
        detector = MTCNN()

        start_time      = time.time()
        first_frame     = face.first_frame()
        last_frame      = face.last_frame()

        # dict used for animation later on.  
        nuke_animation = defaultdict(lambda: defaultdict(dict))
        for frame in range(first_frame, last_frame+1,):
            log_msg = 'Processing frame {:>3} of {:<3}'.format(frame, last_frame, )
            self.app.txt_statusLog.appendPlainText(log_msg)

            face.load_frame(frame, 100, 100)

            # detect faces in the image
            log_msg = face.add_mtcnn_data(frame, detector.detect_faces(face.image(frame)))
            self.app.txt_statusLog.appendPlainText(str(log_msg))
            
            img_width, img_height = face.image_dimensions(frame)

            try:
                for face_detection in face.get_mtcnn_data(frame):
                    # compute the (x, y)-coordinates of the bounding box for the
                    startX, startY, width, height = face_detection['box']
                    p1 = Point(startX, startY, img_width, img_height)
                    p2 = Point(startX + width, startY + height, img_width, img_height) 

                    top_left_x, top_left_y         = p1.point_in_nuke()
                    bottom_right_x, bottom_right_y = p2.point_in_nuke()

                    nuke_animation[frame]['x1'] = top_left_x
                    nuke_animation[frame]['y1'] = top_left_y
                    nuke_animation[frame]['x2'] = bottom_right_x
                    nuke_animation[frame]['y2'] = bottom_right_y
            except :
                print('no mtcnn data')   

            self.my_app.processEvents()
            
            face.remove_image(frame)    
        # create animated curve

        x1 = y1 = x2 = y2 = ''
        for frame in range(first_frame, last_frame+1,):
            x1 += nnb.create_frame_value(frame, nuke_animation[frame]['x1'])
            y1 += nnb.create_frame_value(frame, nuke_animation[frame]['y1'])
            x2 += nnb.create_frame_value(frame, nuke_animation[frame]['x2'])
            y2 += nnb.create_frame_value(frame, nuke_animation[frame]['y2'])

        x1_anim = nnb.create_animation_curve(x1)
        y1_anim = nnb.create_animation_curve(y1)
        x2_anim = nnb.create_animation_curve(x2)
        y2_anim = nnb.create_animation_curve(y2)

        animation_curve_list = [x1_anim, y1_anim, x2_anim, y2_anim]
        self.animated_crop =nnb.create_crop(animation_curve_list)
        log_msg = 'Total time to process was {} '.format(time.time() - start_time)
        self.app.txt_statusLog.appendPlainText(str(log_msg))
        self.app.lbl_crop.setPlainText(str(self.animated_crop))

def main():  
    os.environ['QT_API'] = 'pyside2'
    app = QtWidgets.QApplication(sys.argv)
    myApp = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()