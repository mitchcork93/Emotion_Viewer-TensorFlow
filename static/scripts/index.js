var trackFace = document.getElementById("face").checked;
var trackEmotion = document.getElementById("emotion").checked;
var pollingMark = 3;
var currentPoll = 0;
var currentEmotion = "";
var votedEmotion = "";

(function () {

	var canvas = document.getElementById('canvas');

	var emotion_button = document.getElementById('emotion');
	var text = document.getElementById('display_emotion');
	
	var width = 640;
	var height = 480;
	var ws = new WebSocket("ws://" + location.host + "/live");

	var canvasFace = document.getElementById('canvas-face');
	var context = canvasFace.getContext('2d');

	var slider = document.getElementById("voteSlider");
	var output = document.getElementById("val");
	output.innerHTML = slider.value; // Display the default slider value

	// show loading notice
	context.fillStyle = '#333';
	context.fillText('Loading...', canvasFace.width / 2 - 30, canvasFace.height / 3);


	ws.onmessage = function (event) {

		var data = JSON.parse(event.data);

	  	if ((trackEmotion) && (data.emotion !== null) && (typeof data.emotion != 'undefined')){
	  		
	  		if (currentPoll == 0) 	// Should only be the case on first run
	  		{
	  			text.innerHTML = data.emotion;
	  			currentEmotion = data.emotion;
	  			votedEmotion = data.emotion;
	  			currentPoll = 1;
	  		}

	  		else
	  		{	
	  			vote(data.emotion);
	  		}
	  	}

		var img = new Image();
		img.onload = function () {
			context.drawImage(this, 0, 0, canvasFace.width, canvasFace.height);
		};

		if ((trackEmotion == false) && (trackFace == false)){
			img.src = data.img;
		}
		else{
			img.src = 'data:image/jpeg;base64,' + data.img;
		}
	};

	function takepicture(video) {
		return function () {

			var context = canvas.getContext('2d');
			if (width && height) {
				canvas.width = width;
				canvas.height = height;
				context.drawImage(video, 0, 0, width, height);
				var jpgQuality = 0.6;
				var theDataURL = canvas.toDataURL('image/jpeg', jpgQuality);
				
				var msg = { img: theDataURL, face: trackFace, emotion: trackEmotion };
				ws.send(JSON.stringify(msg));
			}
		}
	}

	function vote(result){

		// Result is the output from classification

		if (result.localeCompare(votedEmotion) == 0)
		{
			currentPoll++;						// Increase vote for emotion

			if(currentPoll >= pollingMark)		// Voting requirement met, change displayed emotion
			{
				text.innerHTML = result;
				currentPoll = 1;				// Reset polling
			}
		}

		else
		{
			votedEmotion = result;				// Voting for new emotion
			currentPoll = 1;					// Reset polling
		}

	}

	slider.oninput = function() {
    	output.innerHTML = this.value;
    	pollingMark = this.value
	}

	navigator.mediaDevices.getUserMedia({video: true, audio: false}).then(function(stream) {

	    var videoTracks = stream.getVideoTracks();
	    
	    stream.onended = function() {
	      console.log('Stream ended');
	    };
	    window.stream = stream; // make variable available to console
	    const video = document.getElementsByTagName('video')[0];
	    video.srcObject = stream;
	    video.play();
		setInterval(takepicture(video), 200);
	  })
	
})();

function toggleFace(){
	trackFace = document.getElementById("face").checked;
}

function toggleEmotion(){
	trackEmotion = document.getElementById("emotion").checked;
}