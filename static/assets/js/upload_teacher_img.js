UploadImage = (e) => {
    var image = document.getElementById('output');
    image.src = URL.createObjectURL(e.target.files[0]);
    var imageFile = e.target.files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
      payload = JSON.stringify({
          image_enc_data : reader.result,
      })
      fetch("/teacher-profile-pic-upload", {method: 'POST', body: payload, headers: {
        'Content-Type': 'application/json'
      },})
        .then(res => res.json()).then(data => {
          if (data.status){
            console.log("image uploaded")
          }
          else console.log("image not uploaded")
        })
    }
    reader.readAsDataURL(imageFile);
  }