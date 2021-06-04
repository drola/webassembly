var workingBuffer = null;

onmessage = function(e) {
  switch(e.data.type) {
    case "image_data":
      if(!workingBuffer || workingBuffer.width != e.data.imageData.width || workingBuffer.height != e.data.imageData.height) {
          if(workingBuffer) {
              workingBuffer.delete();
          }
          //Initialize a new Image instance for passing image data from JS to C++
          workingBuffer = new cv.Image(e.data.imageData.width, e.data.imageData.height);
      }

      //Copy image data to C++ side
      workingBuffer.imageData.data.set(e.data.imageData.data, 0);

      //Detect faces and eyes in the image
      var faces = cv.getFaces(workingBuffer);

      //Send list of faces from this worker to the page
      postMessage({
          "type": "got_faces",
          "faces": faces.faces,
          "eyes": faces.eyes
      });
      //Indicate that the worker is ready to process another frame
      postMessage({
          "type": "worker_ready"
      });
  }
}


importScripts("cv.js");
cv().then(function(cv_) {
    cv = cv_;
    postMessage({
        "type": "worker_ready"
    });
});
