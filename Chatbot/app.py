import os
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import webbrowser
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'black', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'
        self.html_file_path = 'Chatbot\index.html'

        self.html_open = False

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self.label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        self.label.after(20, self.process_webcam)

    def login(self):
        unknown_log_path = './.tmp.jpg'
        cv2.imwrite(unknown_log_path, self.most_recent_capture_arr)

        # Load known faces and their encodings from the database
        known_face_encodings = []
        known_face_names = []

        for filename in os.listdir(self.db_dir):
            if filename.endswith(".jpg"):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.db_dir, filename)

                # Load the known face image
                known_image = face_recognition.load_image_file(image_path)

                # Encode the known face
                encoding = face_recognition.face_encodings(known_image)[0]

                known_face_encodings.append(encoding)
                known_face_names.append(name)

        print(f"Number of known faces: {len(known_face_encodings)}")

        # Load the unknown face image from unknown_log_path
        unknown_image = face_recognition.load_image_file(unknown_log_path)

        # Find all face locations in the unknown image
        face_locations = face_recognition.face_locations(unknown_image)

        # Encode the faces in the unknown image
        unknown_face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        print(f"Number of unknown faces: {len(unknown_face_encodings)}")

        # Compare the unknown face encodings with the known face encodings
        for unknown_face_encoding in unknown_face_encodings:
            results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding)

        for i, result in enumerate(results):
            if result:
                name = known_face_names[i]
                print(f"Recognized: {name}")
                # Perform actions for recognized faces here
                if not self.html_open:
                    webbrowser.open('file:///' + os.path.abspath(self.html_file_path))
                    self.html_open = True
                break

        os.remove(unknown_log_path)

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Please, \ninput username:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        util.msg_box('Success!', 'User successfully captured!')

        self.register_new_user_window.destroy()

if __name__ == "__main__":
    app = App()
    app.start()
