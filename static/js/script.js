feather.replace();

const controls = document.querySelector('.controls');
const cameraOptions = document.querySelector('.video-options>select');
const video = document.querySelector('video');
const canvas = document.querySelector('canvas');
const screenshotImage = document.querySelector('img');
const buttons = [...controls.querySelectorAll('button')];
let streamStarted = false;
let intervalId;

const [play, pause,stop,screenshot] = buttons;

const constraints = {
  video: {
    width: {
      min: 1280,
      ideal: 1920,
      max: 2560,
    },
    height: {
      min: 720,
      ideal: 1080,
      max: 1440
    },
  }
};

cameraOptions.onchange = () => {
  const updatedConstraints = {
    ...constraints,
    deviceId: {
      exact: cameraOptions.value
    }
  };

  startStream(updatedConstraints);
};
const doScreenshot = () => {
  // console.log(status)
  if (true){
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    screenshotImage.src = canvas.toDataURL('image/webp');
    screenshotImage.classList.remove('d-none');
  }
};
const recognize = () => {
  // console.log(status)
  if (true){
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    img = canvas.toDataURL('image/webp');
    recognizePeople(img)
    screenshotImage.classList.remove('d-none');
  }
};
play.onclick = () => {
  if (window.location.href.includes("scan")){
    intervalId = setInterval(recognize,1000)
  }
  if (streamStarted) {
    video.play();
    play.classList.add('d-none');
    pause.classList.remove('d-none');
    stop.classList.remove('d-none');
    screenshotImage.classList.remove('d-none');
    return;
  }
  if ('mediaDevices' in navigator && navigator.mediaDevices.getUserMedia) {
    const updatedConstraints = {
      ...constraints,
      deviceId: {
        exact: cameraOptions.value
      }
    };
    startStream(updatedConstraints);
  }
  
};
const stopStream = () => {
  stream = window.stream
  tracks = stream.getTracks()
  tracks.forEach(function(track) {
    track.stop();
  });
  clearInterval(intervalId)
  video.srcObject = null
  play.classList.remove('d-none');
  stop.classList.add('d-none');
  pause.classList.add('d-none');
  screenshot.classList.add('d-none');
};
const pauseStream = () => {
  video.pause();
  clearInterval(intervalId)
  play.classList.remove('d-none');
  pause.classList.add('d-none');
};
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
const recognizePeople = (img,error) => {
  var csrftoken = getCookie('csrftoken');
  $.ajax({
    type: "POST",
    url: "recognize/",
    data: {
        "csrfmiddlewaretoken" : csrftoken,
        "image": img,
    },
    success: function(data){
        data = JSON.parse(data)
        error = data[0].error
        if (error){
          console.log(data[0].status)
        }
        else{
        console.log(data[0].students[0].name);
        document.getElementById("person").innerHTML = data[0].students[0].name;
      }
    }
  });

};



pause.onclick = pauseStream;
stop.onclick = stopStream;
screenshot.onclick = doScreenshot;

const startStream = async (constraints) => {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  handleStream(stream);
};


const handleStream = (stream) => {
  window.stream = stream
  video.srcObject = stream;
  play.classList.add('d-none');
  pause.classList.remove('d-none');
  stop.classList.remove('d-none');
  screenshot.classList.remove('d-none');
};


const getCameraSelection = async () => {
  const devices = await navigator.mediaDevices.enumerateDevices();
  const videoDevices = devices.filter(device => device.kind === 'videoinput');
  const options = videoDevices.map(videoDevice => {
    return `<option value="${videoDevice.deviceId}">${videoDevice.label}</option>`;
  });
  cameraOptions.innerHTML = options.join('');
};

getCameraSelection();