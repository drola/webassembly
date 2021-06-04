#!/usr/bin/python
import os, sys, re, json, shutil
from subprocess import Popen, PIPE, STDOUT

# Startup
exec(open(os.path.expanduser('~/.emscripten'), 'r').read())

try:
    EMSCRIPTEN_ROOT
except:
    print "ERROR: Missing EMSCRIPTEN_ROOT (which should be equal to emscripten's root dir) in ~/.emscripten"
    sys.exit(1)

#Popen('source ' + emenv)
sys.path.append(EMSCRIPTEN_ROOT)
import tools.shared as emscripten

# Settings
'''
          Settings.INLINING_LIMIT = 0
          Settings.DOUBLE_MODE = 0
          Settings.PRECISE_I64_MATH = 0
          Settings.CORRECT_SIGNS = 0
          Settings.CORRECT_OVERFLOWS = 0
          Settings.CORRECT_ROUNDINGS = 0
	  Settings.BINAREN_TRAP_MODE = 'allow'
'''
#Debug
#emcc_args = '-O0 -g4 --llvm-lto 0 -s ASSERTIONS=1 -s DISABLE_EXCEPTION_CATCHING=0 -s NO_EXIT_RUNTIME=1 -s AGGRESSIVE_VARIABLE_ELIMINATION=0 -s NO_DYNAMIC_EXECUTION=0 -s WASM=1 -s BINARYEN=1 --memory-init-file 0 -s NO_FILESYSTEM=0'.split(' ')

#Optimized
emcc_args = '-O3 --llvm-lto 3 -s INVOKE_RUN=1 -s ASSERTIONS=0 -s DISABLE_EXCEPTION_CATCHING=1 -s NO_EXIT_RUNTIME=1 -s AGGRESSIVE_VARIABLE_ELIMINATION=1 -s NO_DYNAMIC_EXECUTION=0 -s WASM=1 -s BINARYEN=1 --memory-init-file 0 -s NO_FILESYSTEM=0'.split(' ')

#ASM.js
#emcc_args = '-O3 --llvm-lto 1 -s USE_PTHREADS=1 -s PTHREAD_HINT_NUM_CORES=4 -s ASSERTIONS=0 -s DISABLE_EXCEPTION_CATCHING=1 -s NO_EXIT_RUNTIME=1 -s AGGRESSIVE_VARIABLE_ELIMINATION=1 -s NO_DYNAMIC_EXECUTION=0 --memory-init-file 0 -s NO_FILESYSTEM=0'.split(' ')

print
print '--------------------------------------------------'
print 'Building opencv.js, build type:', emcc_args
print '--------------------------------------------------'
print


stage_counter = 0
def stage(text):
    global stage_counter
    stage_counter += 1
    text = 'Stage %d: %s' % (stage_counter, text)
    print
    print '=' * len(text)
    print text
    print '=' * len(text)
    print

# Main
try:
    this_dir = os.getcwd()
    os.chdir('opencv')
    if not os.path.exists('build'):
        os.makedirs('build')
    os.chdir('build')

    stage('OpenCV Configuration')
    configuration = ['cmake',
                     '-DCMAKE_BUILD_TYPE=RELEASE',
                     '-DBUILD_DOCS=OFF',
                     '-DBUILD_EXAMPLES=OFF',
                     '-DBUILD_PACKAGE=OFF',
                     '-DBUILD_WITH_DEBUG_INFO=OFF',
                     '-DBUILD_opencv_bioinspired=OFF',
                     '-DBUILD_opencv_calib3d=OFF',
                     '-DBUILD_opencv_cuda=OFF',
                     '-DBUILD_opencv_cudaarithm=OFF',
                     '-DBUILD_opencv_cudabgsegm=OFF',
                     '-DBUILD_opencv_cudacodec=OFF',
                     '-DBUILD_opencv_cudafeatures2d=OFF',
                     '-DBUILD_opencv_cudafilters=OFF',
                     '-DBUILD_opencv_cudaimgproc=OFF',
                     '-DBUILD_opencv_cudaoptflow=OFF',
                     '-DBUILD_opencv_cudastereo=OFF',
                     '-DBUILD_opencv_cudawarping=OFF',
                     '-DBUILD_opencv_gpu=OFF',
                     '-DBUILD_opencv_gpuarithm=OFF',
                     '-DBUILD_opencv_gpubgsegm=OFF',
                     '-DBUILD_opencv_gpucodec=OFF',
                     '-DBUILD_opencv_gpufeatures2d=OFF',
                     '-DBUILD_opencv_gpufilters=OFF',
                     '-DBUILD_opencv_gpuimgproc=OFF',
                     '-DBUILD_opencv_gpuoptflow=OFF',
                     '-DBUILD_opencv_gpustereo=OFF',
                     '-DBUILD_opencv_gpuwarping=OFF',
                     '-BUILD_opencv_hal=OFF',
                     '-DBUILD_opencv_highgui=OFF',
                     '-DBUILD_opencv_java=OFF',
                     '-DBUILD_opencv_legacy=OFF',
                     '-DBUILD_opencv_ml=ON',
                     '-DBUILD_opencv_nonfree=OFF',
                     '-DBUILD_opencv_optim=ON',
                     '-DBUILD_opencv_photo=ON',
                     '-DBUILD_opencv_shape=ON',
                     '-DBUILD_opencv_objdetect=ON',
                     '-DBUILD_opencv_softcascade=OFF',
                     '-DBUILD_opencv_stitching=OFF',
                     '-DBUILD_opencv_superres=OFF',
                     '-DBUILD_opencv_ts=OFF',
                     '-DBUILD_opencv_videostab=OFF',
                     '-DENABLE_PRECOMPILED_HEADERS=OFF',
                     '-DWITH_1394=OFF',
                     '-DWITH_CUDA=OFF',
                     '-DWITH_CUFFT=OFF',
                     '-DWITH_EIGEN=OFF',
                     '-DWITH_FFMPEG=OFF',
                     '-DWITH_GIGEAPI=OFF',
                     '-DWITH_GSTREAMER=OFF',
                     '-DWITH_GTK=OFF',
                     '-DWITH_JASPER=OFF',
                     '-DWITH_JPEG=OFF',
                     '-DWITH_OPENCL=OFF',
                     '-DWITH_OPENCLAMDBLAS=OFF',
                     '-DWITH_OPENCLAMDFFT=OFF',
                     '-DWITH_OPENEXR=OFF',
                     '-DWITH_PNG=OFF',
                     '-DWITH_PVAPI=OFF',
                     '-DWITH_TIFF=OFF',
                     '-DWITH_LIBV4L=OFF',
                     '-DWITH_WEBP=OFF',
                     '-DWITH_PTHREADS_PF=OFF',
                     '-DBUILD_opencv_apps=OFF',
                     '-DBUILD_PERF_TESTS=OFF',
                     '-DBUILD_TESTS=OFF',
                     '-DBUILD_SHARED_LIBS=OFF',
                     '-DWITH_IPP=OFF',
                     '-DENABLE_SSE=OFF',
                     '-DENABLE_SSE2=OFF',
                     '-DENABLE_SSE3=OFF',
                     '-DENABLE_SSE41=OFF',
                     '-DENABLE_SSE42=OFF',
                     '-DENABLE_AVX=OFF',
                     '-DENABLE_AVX2=OFF',
                     '-DCMAKE_CXX_FLAGS=%s' % ' '.join(emcc_args),
                     '-DCMAKE_EXE_LINKER_FLAGS=%s' % ' '.join(emcc_args),
                     '-DCMAKE_CXX_FLAGS_DEBUG=%s' % ' '.join(emcc_args),
                     '-DCMAKE_CXX_FLAGS_RELWITHDEBINFO=%s' % ' '.join(emcc_args),
                     '-DCMAKE_C_FLAGS_RELWITHDEBINFO=%s' % ' '.join(emcc_args),
                     '-DCMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO=%s' % ' '.join(emcc_args),
                     '-DCMAKE_MODULE_LINKER_FLAGS_RELEASE=%s' % ' '.join(emcc_args),
                     '-DCMAKE_MODULE_LINKER_FLAGS_DEBUG=%s' % ' '.join(emcc_args),
                     '-DCMAKE_MODULE_LINKER_FLAGS_RELWITHDEBINFO=%s' % ' '.join(emcc_args),
                     '-DCMAKE_SHARED_LINKER_FLAGS_RELEASE=%s' % ' '.join(emcc_args),
                     '-DCMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO=%s' % ' '.join(emcc_args),
                     '-DCMAKE_SHARED_LINKER_FLAGS_DEBUG=%s' % ' '.join(emcc_args),
                     '..']
    emscripten.Building.configure(configuration)


    stage('Making OpenCV')

    emcc_args += ('-s TOTAL_MEMORY=%d' % (128*1024*1024)).split(' ') # default 128MB.
    emcc_args += '-s ALLOW_MEMORY_GROWTH=0'.split(' ')  # resizable heap
    emcc_args += '-s EXPORT_NAME="cv" -s MODULARIZE=1'.split(' ')


    emscripten.Building.make(['make', '-j8'])

    stage('Compiling findFaces.cpp')
    INCLUDE_DIRS = [
             os.path.join('..', 'modules', 'core', 'include'),
             os.path.join('..', 'modules', 'flann', 'include'),
             os.path.join('..', 'modules', 'ml', 'include'),
             os.path.join('..', 'modules', 'photo', 'include'),
             os.path.join('..', 'modules', 'shape', 'include'),
             os.path.join('..', 'modules', 'imgproc', 'include'),
             os.path.join('..', 'modules', 'features2d', 'include'),
             os.path.join('..', 'modules', 'objdetect', 'include'),
             os.path.join('..', 'modules', 'hal', 'include'),
             os.path.join('.')
    ]
    include_dir_args = ['-I'+item for item in INCLUDE_DIRS]
    emcc_binding_args = ['--bind']
    emcc_binding_args += include_dir_args

    emscripten.Building.emcc('../../findFaces.cpp', emcc_binding_args, 'findFaces.bc')
    assert os.path.exists('findFaces.bc')

    stage('Linking')
    opencv = os.path.join('..', '..', 'cv.js')
    data = os.path.join('..', '..', 'cv.data')

    input_files = [
        'findFaces.bc',

         os.path.join('lib','libopencv_ml.a'),
         os.path.join('lib','libopencv_flann.a'),
         os.path.join('lib','libopencv_objdetect.a'),
         os.path.join('lib','libopencv_features2d.a') ,
         os.path.join('lib','libopencv_shape.a'),
         os.path.join('lib','libopencv_photo.a'),
         os.path.join('lib','libopencv_imgproc.a'),
         os.path.join('lib','libopencv_core.a')
  ]

    emscripten.Building.link(input_files, 'libOpenCV.bc')
    emcc_args += ['--bind']
    emcc_args += '--preload-file ../../data/'.split(' ')

    emscripten.Building.emcc('libOpenCV.bc', emcc_args, opencv)

finally:
    os.chdir(this_dir)
