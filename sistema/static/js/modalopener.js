function prueba() {
    var ele = document.getElementsByName('seleccionado');
    var id = 0;
    var f = false;
    for (var i = 0; i < ele.length; i++) {
        if (ele[i].checked) {
            console.log(ele[i].value);
            id = ele[i].value;
            f = true;
            ele[i].checked = false;
            break;
        }
    }
    if (!f) {
        alert("Seleccione un curso a consultar");
    } else {
        f = false;
        //aqui se escribe todo el modal
        var html =
            '{% for cursos in Curso %}' +
            '{% if cursos.id == '+id+' %}'+
            '<div class="form-row">' +
            '<h5>Nombre del curso</h5>' +
            '<input type="text" readonly class="form-control-plaintext" value={{cursos.nombre}}>' +
            '</div>' +
            '{% endif %}'+
            '{% endfor %}';
        $("#modal-body").html(html);
        $('#ModalConsultar').modal('show');
    }
}