function update_booking_status(id, stat){
    fetch("/update_booking", {
        method:"POST",
        body: JSON.stringify({booking_id: id, status:stat}),
    }).then(response => response.json()).then(json => { 
        console.log(json)
        $("#modalUpdateBooking").addClass('fade d-none');
        window.location.href = "/";
        /*if(json['count'] != 0)
            document.getElementById("react_"+id).innerHTML = "("+json['count']+")";
        else
             document.getElementById("react_"+id).innerHTML = "";*/

    });
}