#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/objdetect.hpp"

#include <emscripten/bind.h>
#include <emscripten/val.h>

#include <stdio.h>
#include <vector>


/**
 * Class that stores RGBA image data and image dimensions.
 */
class Image {
private:
  int width;
  int height;
  int byteLength;
  unsigned char* data;
  cv::Mat image;
  emscripten::val uint8Array = emscripten::val::undefined();
  emscripten::val imageData = emscripten::val::undefined();

public:
  Image(int width, int height) {
    this->width = width;
    this->height = height;
    this->byteLength = width * height * 4; //RGBA
    this->data = new unsigned char[this->byteLength];

    //Init OpenCV Mat
    this->image = cv::Mat(height, width, CV_8UC4, (void*) this->data);

    //Init Uint8Array for JS
    this->uint8Array = emscripten::val(emscripten::typed_memory_view(this->byteLength, this->data));

    //Init ImageData for JS
    emscripten::val uint8ClampedArray = emscripten::val::global("Uint8ClampedArray")
      .new_(this->uint8Array["buffer"], this->uint8Array["byteOffset"], this->uint8Array["byteLength"]);
    this->imageData = emscripten::val::global("ImageData").new_(uint8ClampedArray, width, height);
  }

  ~Image() {
    delete[] this->data;
  }

  int getWidth() const {
    return this->width;
  }

  int getHeight() const {
    return this->height;
  }

  emscripten::val getUint8Array() const {
    return this->uint8Array;
  }

  emscripten::val getImageData() const {
    return this->imageData;
  }

  cv::Mat getOpenCVImage() {
    return this->image;
  }
};


/**
 * OpenCV classifier
 */
cv::CascadeClassifier face_cascade;
cv::CascadeClassifier eyes_cascade;

/**
 * Scaled image buffer. It is a global so we don't
 * need to reallocate data each time image is updated
 */
cv::Mat frame_scaled;

/**
 * Grayscale image buffer. It is a global so we don't
 * need to reallocate data each time image is updated
 */
cv::Mat frame_gray;

/**
 * Vectors for face and eyes coordinates.
 * Again, global so we avoid some allocations
 */
std::vector<cv::Rect> faces;
std::vector<cv::Rect> eyes;

/**
 * Takes Image and returns JavaScript object.
 * The returned object has keys 'faces' and 'eyes' which
 * are arrays with coordinates
 */
emscripten::val getFaces(Image& image) {
  float scaleFactor = 0.25;

  cv::Mat image_cv = image.getOpenCVImage();

  emscripten::val js_faces = emscripten::val::array();
  emscripten::val js_eyes = emscripten::val::array();

  //Reduce image size
  cv::resize(image_cv, frame_scaled, cv::Size(), scaleFactor, scaleFactor, cv::INTER_LINEAR);

  //Convert image to grayscale
  cv::cvtColor( frame_scaled, frame_gray, cv::COLOR_RGBA2GRAY );

  //Optimize image
  cv::equalizeHist( frame_gray, frame_gray );

  //Clear previously detected faces
  faces.clear();
  //Detect faces
  face_cascade.detectMultiScale( frame_gray, faces, 1.1, 2, 0|cv::CASCADE_SCALE_IMAGE, cv::Size(30, 30) );

  //Iterate over detected faces
  for( size_t i = 0; i < faces.size(); i++ )
  {
    //Create JavaScript object for each face and append it to js_faces
    emscripten::val face = emscripten::val::object();
    
     face.set("x", (faces[i].x + faces[i].width/2) / scaleFactor);
     face.set("y", (faces[i].y + faces[i].height/2) / scaleFactor);
     face.set("width", faces[i].width / scaleFactor);
     face.set("height", faces[i].height / scaleFactor);
     js_faces.call<void>("push", face);


     //Extract part of image with the face
     cv::Mat faceROI = frame_gray( faces[i] );
     //Detect eyes in the face
     eyes.clear(); //Clear previously detected eyes
     eyes_cascade.detectMultiScale( faceROI, eyes, 1.1, 2, 0 |cv::CASCADE_SCALE_IMAGE, cv::Size(10, 10) );

     //Iterate over eyes
     for( size_t j = 0; j < eyes.size(); j++ )
     {
       //Create a JavaScript object for each eye and append it to js_eyes
       emscripten::val eye = emscripten::val::object();
       eye.set("x", (faces[i].x + eyes[j].x + eyes[j].width/2) / scaleFactor);
       eye.set("y", (faces[i].y + eyes[j].y + eyes[j].height/2) / scaleFactor);
       eye.set("width", (eyes[i].width) / scaleFactor);
       eye.set("height", (eyes[i].height) / scaleFactor);
       js_eyes.call<void>("push", eye);
     }
   }

   //Create and return final output object
   emscripten::val output = emscripten::val::object();
   output.set("faces", js_faces);
   output.set("eyes", js_eyes);
   return output;
}

/**
 * Initialize classifier for finding faces and eyes in images
 * prelearned based on models described in .xml files
 */
void initClassifiers() {
    cv::String face_cascade_name = "/data/haarcascade_frontalface_default.xml";
    if( !face_cascade.load( face_cascade_name ) ){ printf("--(!)Error loading face cascade\n"); return; };

    cv::String eyes_cascade_name = "/data/haarcascade_eye.xml";
    if( !eyes_cascade.load( eyes_cascade_name ) ){ printf("--(!)Error loading eyes cascade\n"); return; };
}


/**
 * Entry point to our program
 */
int main(int argc, char** argv) {
    initClassifiers();
    printf("OpenCV %d.%d\n", CV_MAJOR_VERSION, CV_MINOR_VERSION);
    return 0;
}

/**
 * Expose the APIs to the JavaScript side
 */
EMSCRIPTEN_BINDINGS(my_module) {
  emscripten::class_<Image>("Image")
    .constructor<int, int>()
    .property("width", &Image::getWidth)
    .property("height", &Image::getHeight)
    .property("uint8Array", &Image::getUint8Array)
    .property("imageData", &Image::getImageData)
  ;
  emscripten::function("getFaces", &getFaces);
}
