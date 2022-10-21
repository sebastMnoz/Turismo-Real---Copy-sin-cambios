const {} =   Swal.fire({
         title: "Wenawena",
         text:"Esto es un texto"
        // html:
        // icon:
        // confirmButtonText:
        // footer:
        // width:
        // padding:
        // background:
        // grow:
        // backdrop:
        // timer:
        // timerProgressBar:
        // toast:
        // position:
        // allowOutsideClick:
        // allowEscapeKey:
        // allowEnterKey:
        // stopKeydownPropagation:
    
        // input:
        // inputPlaceholder:
        // inputValue:
        // inputOptions:
        
        //  customClass:
        // 	container:
        // 	popup:
        // 	header:
        // 	title:
        // 	closeButton:
        // 	icon:
        // 	image:
        // 	content:
        // 	input:
        // 	actions:
        // 	confirmButton:
        // 	cancelButton:
        // 	footer:	
    
        // showConfirmButton:
        // confirmButtonColor:
        // confirmButtonAriaLabel:
    
        // showCancelButton:
        // cancelButtonText:
        // cancelButtonColor:
        // cancelButtonAriaLabel:
        
        // buttonsStyling:
        // showCloseButton:
        // closeButtonAriaLabel:
    
    
        // imageUrl:
        // imageWidth:
        // imageHeight:
        // imageAlt:
    });

$("#btn1").click(function(){
    alert("hola");

});





$(document).ready(function() {    
  $('#calendar').fullCalendar({                header: {       
     left: 'prev,next today',
     center: 'title',
     right: 'month,basicWeek,basicDay',       
   },
   locale: 'es',
    monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
   monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'],
   dayNames: ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'],
   dayNamesShort: ['Dom','Lun','Mar','Mié','Jue','Vie','Sáb'],     
                               
   //Evento Click
 dayClick: function(date, jsEvent, view) {
 alert('Clicked on: ' + date.format());
 alert('Coordinates: ' + jsEvent.pageX + ',' + jsEvent.pageY);
 alert('Current view: ' + view.name);
 // change the day's background color just for fun
 $(this).css('background-color', 'red');   
  }
//Fin Evento Click
                               
                              
   });    // full calendar   
 });  // function

  

// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: -25.344, lng: 131.031 };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 4,
      center: uluru,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
    });
  }

  window.initMap = initMap;